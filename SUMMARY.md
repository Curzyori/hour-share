<!-- gsd-meta: date=2026-07-20 02:45 | model=dip | by=hermes-agent | session=hourshare-audit-v2 -->

# Summary — Audit hourshare v1.0.2 (backend-curzy / api-curzy)

## Goal
Audit ulang peringatan npm/Socket.dev pada hourshare v1.0.2 (latest) — verifikasi
keamanan kode + dependency, dan jelaskan asal alert yang muncul di npm.

## Findings
- 🔴 **Pillow 12.2.0 = 8 CVE** (PYSEC-2026-2253/2255/2257/2256/2254/3453/3451/3452).
  Diperbaiki: `requirements.txt` `pillow==12.2.0` → `pillow==12.3.0`. pip-audit clean setelahnya.
- 🟢 **NPM package integrity**: `npm pack hourshare@1.0.2` vs git repo 100% identik
  (kecuali requirements.txt yang baru dipatch). Tidak ada supply-chain injection/
  obfuscation di artifact publik.
- 🟢 **child_process/execSync** (bin/hourshare.js): semua argumen trusted/static
  (PORT divalidasi 1–65535, path dari __dirname/os.homedir). Tidak ada command injection.
- 🟢 **server.py**: path traversal aman (`secure_filename` + `send_from_directory` +
  regex `^[a-z0-9_-]{1,40}$` untuk group name, runtime-tested 404 pada traversal).
  Session pakai `os.urandom(24)` per-startup. Rate limit 30/60s per IP aktif.
  Bundle ID `uuid4().hex[:12]` (tak ter-enumerasi). No debug endpoint.
- 🟡 **CSRF**: POST endpoint tanpa token, tapi SameSite=Lax cookie + CORS tidak
  dikonfigurasi (same-origin only) → cross-origin POST gagal baca respons. Low risk.
- ✅ **/health** endpoint ditambah (returns `{"status":"ok"}`) untuk api-curzy checklist.

## Penjelasan alert npm
Socket alert (eval 99 pkg, native 240 pkg, shell 95 pkg, obfuscated 2 pkg) adalah
**false positive untuk hourshare** — hourshare punya 0 npm dependency. Angka tsb
berasal dari audit workspace/dependency tree luas (parent `50-Projects-Challenges/`
atau project lain), bukan dari hourshare sendiri.

## Files changed
- `requirements.txt` — pillow 12.2.0 → 12.3.0
- `server.py` — tambah `GET /health`
- `TASK.md`, `SUMMARY.md` — GSD tracking

## Status
Aman untuk publish. Rekomendasi: bump version → `npm publish` ulang agar tarball
baru ikut `requirements.txt` yang sudah dipatch.
