"""HourShare-21 — Local Web Share via QR & Password Protection.
"""

import io
import json
import os
import socket
import threading
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import re
import bcrypt
import qrcode
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
    url_for,
    session,
)

# ---------------------------------------------------------------------------
# Konfigurasi dasar
# ---------------------------------------------------------------------------

APP_ROOT = Path(__file__).resolve().parent
SHARED_DIR = APP_ROOT / "shared"
BUNDLES_DIR = SHARED_DIR / "bundles"
GROUPS_DIR = SHARED_DIR / "groups"
METADATA_FILE = SHARED_DIR / "metadata.json"

SHARED_DIR.mkdir(parents=True, exist_ok=True)
BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
GROUPS_DIR.mkdir(parents=True, exist_ok=True)

PORT = int(os.environ.get("HOURSHARE_PORT", "10101"))
HOST = "0.0.0.0"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
EXPIRE_MINUTES = 60
SWEEP_INTERVAL = 10  # Sweep lebih cepat biar responsive

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("HOURSHARE_SECRET") or os.urandom(24).hex()
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Lock untuk thread-safe access ke metadata
db_lock = threading.Lock()

# Simple in-memory rate limiter (per-IP) untuk endpoint auth/send
_rate_limit: dict[str, list[float]] = {}
_RATE_WINDOW = 60.0
_RATE_MAX = 30

def rate_limited(remote_addr: str | None, max_req: int = _RATE_MAX, window: float = _RATE_WINDOW) -> bool:
    """Return True jika IP melebihi batas (block)."""
    ip = remote_addr or "127.0.0.1"
    now = time.time()
    hits = _rate_limit.get(ip)
    if hits is None:
        _rate_limit[ip] = [now]
        return False
    # buang hit di luar window
    hits = [t for t in hits if now - t < window]
    if len(hits) >= max_req:
        _rate_limit[ip] = hits
        return True
    hits.append(now)
    _rate_limit[ip] = hits
    return False

# Validasi nama group: hanya huruf/angka/-/_, max 40 char
_VALID_GROUP = re.compile(r"^[a-z0-9_-]{1,40}$")

def clean_filename(filename: str) -> str:
    """Sanitasi nama file upload biar aman dari path traversal."""
    name = secure_filename(filename)
    if not name:
        name = f"file_{uuid.uuid4().hex[:8]}"
    return name

# ---------------------------------------------------------------------------
# Database Helper (JSON based)
# ---------------------------------------------------------------------------

def load_db():
    if not METADATA_FILE.exists():
        return {"bundles": {}, "groups": {}}
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"bundles": {}, "groups": {}}

def save_db(db):
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[db] error saving db: {e}")

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()

def human_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def sweep_expired():
    """Hapus bundle & group yang sudah lewat dari 60 menit."""
    now = time.time()
    with db_lock:
        db = load_db()
        
        # 1. Sweep Bundles
        expired_bundles = []
        for bundle_id, data in list(db.get("bundles", {}).items()):
            if data.get("expires_at", 0) < now:
                expired_bundles.append(bundle_id)
        
        for bundle_id in expired_bundles:
            db["bundles"].pop(bundle_id, None)
            # Hapus folder fisiknya
            b_path = BUNDLES_DIR / bundle_id
            if b_path.exists():
                import shutil
                try:
                    shutil.rmtree(b_path)
                except OSError:
                    pass
        
        # 2. Sweep Groups
        expired_groups = []
        for group_id, data in list(db.get("groups", {}).items()):
            if data.get("expires_at", 0) < now:
                expired_groups.append(group_id)
        
        for group_id in expired_groups:
            db["groups"].pop(group_id, None)
            g_path = GROUPS_DIR / group_id
            if g_path.exists():
                import shutil
                try:
                    shutil.rmtree(g_path)
                except OSError:
                    pass
                    
        # 3. Sweep file di dalam Group yang umurnya > 60 menit secara individual
        for group_id, gdata in db.get("groups", {}).items():
            valid_items = []
            for item in gdata.get("items", []):
                # Jika item berumur lebih dari 60 menit
                if item.get("created_at", 0) + (EXPIRE_MINUTES * 60) < now:
                    # Hapus file fisik jika bertipe file
                    if item.get("type") == "file":
                        fpath = GROUPS_DIR / group_id / item.get("safe_name")
                        if fpath.exists():
                            try:
                                fpath.unlink()
                            except OSError:
                                pass
                else:
                    valid_items.append(item)
            gdata["items"] = valid_items

        if expired_bundles or expired_groups:
            save_db(db)
            print(f"[sweep] Cleaned up expired bundles/groups.")

def sweeper_loop():
    while True:
        try:
            sweep_expired()
        except Exception as e:
            print(f"[sweep] error: {e}")
        time.sleep(SWEEP_INTERVAL)

# ---------------------------------------------------------------------------
# Flask API Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    local_ip = get_local_ip()
    base_url = f"http://{local_ip}:{PORT}"
    max_mb = MAX_FILE_SIZE // (1024 * 1024)
    return render_template(
        "index.html",
        base_url=base_url,
        local_ip=local_ip,
        port=PORT,
        expire_minutes=EXPIRE_MINUTES,
        max_file_mb=max_mb,
    )

@app.route("/api/qr")
def api_qr():
    local_ip = get_local_ip()
    base_url = f"http://{local_ip}:{PORT}"
    img = qrcode.make(base_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    from flask import Response
    return Response(buf.getvalue(), mimetype="image/png")

@app.route("/api/send", methods=["POST"])
def api_send():
    """Membuat bundle baru (SEND)."""
    if rate_limited(request.remote_addr):
        abort(429)
    password = request.form.get("password", "").strip()
    text_content = request.form.get("text", "").strip()

    if not password:
        return jsonify({"error": "Password wajib diisi!"}), 400
    if len(password) > 128:
        return jsonify({"error": "Password terlalu panjang!"}), 400

    files = request.files.getlist("files")

    bundle_id = uuid.uuid4().hex[:12]
    bundle_dir = BUNDLES_DIR / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for f in files:
        if f.filename:
            safe_name = clean_filename(f.filename)
            # Hindari tabrakan nama file dalam satu bundle
            dest = bundle_dir / safe_name
            f.save(dest)
            saved_files.append({
                "name": safe_name,
                "size": human_size(dest.stat().st_size),
                "safe_name": safe_name
            })

    now = time.time()
    bundle_data = {
        "password_hash": hash_password(password),
        "text": text_content,
        "files": saved_files,
        "created_at": now,
        "expires_at": now + (EXPIRE_MINUTES * 60)
    }
    
    with db_lock:
        db = load_db()
        db["bundles"][bundle_id] = bundle_data
        save_db(db)
        
    return jsonify({"ok": True, "bundle_id": bundle_id})

@app.route("/api/receive", methods=["POST"])
def api_receive():
    """Mengakses bundle menggunakan password."""
    if rate_limited(request.remote_addr):
        abort(429)
    data = request.get_json(silent=True) or {}
    password = data.get("password", "").strip()
    
    if not password:
        return jsonify({"error": "Password wajib diisi!"}), 400
    if len(password) > 128:
        return jsonify({"error": "Password terlalu panjang!"}), 400
        
    with db_lock:
        db = load_db()
        
    # Cari bundle yang password-nya cocok
    target_bundle = None
    target_id = None
    now = time.time()
    
    for b_id, b_data in db.get("bundles", {}).items():
        if b_data.get("expires_at", 0) > now:
            if check_password(password, b_data.get("password_hash", "")):
                target_bundle = b_data
                target_id = b_id
                break
                
    if not target_bundle:
        return jsonify({"error": "Password salah atau bundle tidak ditemukan!"}), 403
        
    # Simpan status otentikasi di session
    if "auth_bundles" not in session:
        session["auth_bundles"] = []
    
    auth_list = list(session["auth_bundles"])
    if target_id not in auth_list:
        auth_list.append(target_id)
        session["auth_bundles"] = auth_list
        
    sisa_detik = int(target_bundle["expires_at"] - now)
    
    return jsonify({
        "ok": True,
        "bundle_id": target_id,
        "text": target_bundle["text"],
        "files": [
            {
                "name": f["name"],
                "size": f["size"],
                "url": f"/download/bundle/{target_id}/{f['safe_name']}"
            }
            for f in target_bundle["files"]
        ],
        "expires_in_sec": sisa_detik
    })

@app.route("/download/bundle/<bundle_id>/<filename>")
def download_bundle_file(bundle_id, filename):
    """Download file dari bundle terproteksi."""
    # Pastikan user sudah memasukkan password yang valid untuk bundle ini
    auth_list = session.get("auth_bundles", [])
    if bundle_id not in auth_list:
        abort(403)
        
    with db_lock:
        db = load_db()
        
    bundle = db.get("bundles", {}).get(bundle_id)
    if not bundle or bundle.get("expires_at", 0) < time.time():
        abort(404)
        
    # Verifikasi nama file ada di dalam bundle
    file_exists = False
    for f in bundle.get("files", []):
        if f["safe_name"] == filename:
            file_exists = True
            break
            
    if not file_exists:
        abort(404)
        
    target_dir = BUNDLES_DIR / bundle_id
    return send_from_directory(str(target_dir), filename, as_attachment=True)

# ---------------------------------------------------------------------------
# Group API Routes
# ---------------------------------------------------------------------------

@app.route("/api/group/join", methods=["POST"])
def api_group_join():
    """Masuk atau membuat group."""
    if rate_limited(request.remote_addr):
        abort(429)
    data = request.get_json(silent=True) or {}
    group_name = data.get("name", "").strip().lower()
    password = data.get("password", "").strip()
    
    if not group_name or not password:
        return jsonify({"error": "Nama group dan Password wajib diisi!"}), 400
    if len(password) > 128:
        return jsonify({"error": "Password terlalu panjang!"}), 400
    if not _VALID_GROUP.match(group_name):
        return jsonify({"error": "Nama group tidak valid (hanya huruf, angka, -, _, max 40 karakter)!"}), 400
        
    with db_lock:
        db = load_db()
        groups = db.get("groups", {})
        
        now = time.time()
        # Jika group sudah ada
        if group_name in groups:
            group = groups[group_name]
            if not check_password(password, group.get("password_hash", "")):
                return jsonify({"error": "Password Group salah!"}), 403
            # Perpanjang waktu kadaluwarsa grup saat aktif digunakan
            group["expires_at"] = now + (EXPIRE_MINUTES * 60)
        else:
            # Buat group baru
            groups[group_name] = {
                "password_hash": hash_password(password),
                "created_at": now,
                "expires_at": now + (EXPIRE_MINUTES * 60),
                "items": []
            }
            
        save_db(db)
        
    # Simpan di session
    if "auth_groups" not in session:
        session["auth_groups"] = []
    
    auth_list = list(session["auth_groups"])
    if group_name not in auth_list:
        auth_list.append(group_name)
        session["auth_groups"] = auth_list
        
    return jsonify({"ok": True, "group_name": group_name})

@app.route("/api/group/<group_name>/info", methods=["GET"])
def api_group_info(group_name):
    """Mendapatkan data real-time isi group."""
    group_name = group_name.strip().lower()
    if not _VALID_GROUP.match(group_name):
        return jsonify({"error": "Nama group tidak valid"}), 400
    auth_list = session.get("auth_groups", [])
    if group_name not in auth_list:
        return jsonify({"error": "Unauthorized"}), 403
        
    with db_lock:
        db = load_db()
        
    group = db.get("groups", {}).get(group_name)
    if not group or group.get("expires_at", 0) < time.time():
        return jsonify({"error": "Group expired or not found"}), 404
        
    now = time.time()
    items = []
    for item in group.get("items", []):
        age = int(now - item["created_at"])
        sisa_time = max(0, (EXPIRE_MINUTES * 60) - age)
        
        # Buat download URL jika file
        download_url = ""
        if item["type"] == "file":
            download_url = f"/download/group/{group_name}/{item['safe_name']}"
            
        items.append({
            "id": item["id"],
            "type": item["type"],
            "sender": item["sender"],
            "name": item["name"],
            "content": item["content"],
            "size": item["size"],
            "expires_in_sec": sisa_time,
            "url": download_url
        })
        
    return jsonify({
        "ok": True,
        "name": group_name,
        "items": items
    })

@app.route("/api/group/<group_name>/send", methods=["POST"])
def api_group_send(group_name):
    """Kirim teks/file ke dalam Group."""
    if rate_limited(request.remote_addr):
        abort(429)
    group_name = group_name.strip().lower()
    if not _VALID_GROUP.match(group_name):
        abort(400)
    auth_list = session.get("auth_groups", [])
    if group_name not in auth_list:
        return jsonify({"error": "Unauthorized"}), 403
        
    sender_name = request.form.get("sender", "Anonim").strip() or "Anonim"
    text_content = request.form.get("text", "").strip()
    uploaded_files = request.files.getlist("files")
    
    with db_lock:
        db = load_db()
        groups = db.get("groups", {})
        if group_name not in groups:
            return jsonify({"error": "Group not found"}), 404
            
        group = groups[group_name]
        now = time.time()
        
        # Update expires_at group biar gak mati selagi dipakai aktif
        group["expires_at"] = now + (EXPIRE_MINUTES * 60)
        
        # Simpan teks jika ada
        if text_content:
            item_id = uuid.uuid4().hex[:12]
            group["items"].append({
                "id": item_id,
                "type": "text",
                "sender": sender_name,
                "name": "",
                "content": text_content,
                "size": "",
                "created_at": now
            })
            
        # Simpan files
        group_dir = GROUPS_DIR / group_name
        group_dir.mkdir(parents=True, exist_ok=True)
        
        for f in uploaded_files:
            if f.filename:
                safe_name = clean_filename(f.filename)
                
                # Biar gak tabrakan dengan file lama bernama sama
                stem = Path(safe_name).stem
                suffix = Path(safe_name).suffix
                dest = group_dir / safe_name
                i = 1
                while dest.exists():
                    safe_name = f"{stem}_{i}{suffix}"
                    dest = group_dir / safe_name
                    i += 1
                    
                f.save(dest)
                item_id = uuid.uuid4().hex[:12]
                group["items"].append({
                    "id": item_id,
                    "type": "file",
                    "sender": sender_name,
                    "name": f.filename,
                    "safe_name": safe_name,
                    "content": "",
                    "size": human_size(dest.stat().st_size),
                    "created_at": now
                })
                
        save_db(db)
        
    return jsonify({"ok": True})

@app.route("/download/group/<group_name>/<filename>")
def download_group_file(group_name, filename):
    """Download file dari Group terproteksi."""
    group_name = group_name.strip().lower()
    if not _VALID_GROUP.match(group_name):
        abort(400)
    filename = clean_filename(filename)
    auth_list = session.get("auth_groups", [])
    if group_name not in auth_list:
        abort(403)
        
    with db_lock:
        db = load_db()
        
    group = db.get("groups", {}).get(group_name)
    if not group or group.get("expires_at", 0) < time.time():
        abort(404)
        
    # Cari safe_name file
    file_exists = False
    for item in group.get("items", []):
        if item.get("type") == "file" and item.get("safe_name") == filename:
            file_exists = True
            break
            
    if not file_exists:
        abort(404)
        
    target_dir = GROUPS_DIR / group_name
    return send_from_directory(str(target_dir), filename, as_attachment=True)

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

def print_banner(local_ip: str, port: int, shared_dir: Path):
    """Print startup banner with ASCII QR for terminal scanning."""
    base_url = f"http://{local_ip}:{port}"

    # ASCII QR
    import io as _io
    qr = qrcode.QRCode(border=1, box_size=2)
    qr.add_data(base_url)
    qr.make()
    buf = _io.StringIO()
    qr.print_ascii(out=buf)
    buf.seek(0)
    qr_ascii = buf.read()

    # ANSI colors
    C = "\033[0m"
    B = "\033[1m"
    D = "\033[2m"
    P = "\033[38;2;86;69;212m"  # #5645D4 primary
    V = "1.0.2"

    print()
    print(P + "=" * 56 + C)
    print(f"  {B}Hour Share{C} {D}v{V}{C}")
    print(P + "=" * 56 + C)
    print()
    print(qr_ascii)
    print(f"  {B}URL{C}       : {P}{base_url}{C}")
    print()
    print(f"  {B}Local IP{C}  : {local_ip}")
    print(f"  {B}Port{C}      : {port}")
    print(f"  {B}Shared dir{C}: {shared_dir}")
    print(f"  {B}Expire{C}    : {EXPIRE_MINUTES} min")
    print(f"  {B}Max file{C}  : {MAX_FILE_SIZE // (1024*1024)} MB")
    print(P + "=" * 56 + C)
    print(f"  {B}Browser{C}: {P}{base_url}/api/qr{C}")
    print(P + "=" * 56 + C)
    print()


def main():
    sweep_expired()
    t = threading.Thread(target=sweeper_loop, daemon=True, name="sweeper")
    t.start()

    local_ip = get_local_ip()
    print_banner(local_ip, PORT, SHARED_DIR)

    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.WARNING)

    app.run(host=HOST, port=PORT, debug=False, use_reloader=False, threaded=True)

if __name__ == "__main__":
    main()
