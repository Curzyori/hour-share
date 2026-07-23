<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="Dashboard Desktop Hour Share" width="800"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/logo.png" alt="Logo Hour Share" width="120"/>
</p>

<h1 align="center">Hour Share</h1>
<p align="center">
  <strong>Berbagi File & Teks Antar Perangkat via QR Code - Tanpa Internet, Tanpa Login</strong>
</p>

<p align="center">
  <a href="https://hour-share.curzy.dev"><strong>🌐 Website Live</strong></a>
</p>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share)
[![Forks](https://img.shields.io/github/forks/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share/network/members)
[![Downloads](https://img.shields.io/npm/dw/hourshare?style=for-the-badge&color=374151)](https://www.npmjs.com/package/hourshare)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Python%20%7C%20Node.js%20%7C%20Cross--platform-black?style=for-the-badge)](#)

</div>

<p align="center">
  <a href="#kenapa-hour-share">Kenapa Ini</a> ·
  <a href="#fitur-utama">Fitur</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#tech-stack">Tech Stack</a> ·
  <a href="#cara-pakai">Cara Pakai</a> ·
  <a href="#instalasi">Instalasi</a> ·
  <a href="#cli-flags">CLI Flags</a> ·
  <a href="#api-endpoints">API</a> ·
  <a href="#preview">Preview</a> ·
  <a href="#support">Support</a> ·
  <a href="#license">License</a>
</p>

<p align="center">🌐 Dalam 4 bahasa -
  <a href="README.md">🇺🇸 EN</a> ·
  <a href="README_ID.md"><b>🇮🇩 ID</b></a> ·
  <a href="README_CN.md">🇨🇳 CN</a> ·
  <a href="README_JP.md">🇯🇵 JP</a>
</p>

---

## Kenapa Hour Share?

Mentransfer file antar perangkat dalam satu jaringan lokal sering ribet:
- Cari IP dan ketik manual di HP rawan salah.
- Cloud storage atau WhatsApp butuh internet dan akun.
- Kabel USB berlebihan untuk transfer cepat sekali pakai.

Hour Share menyelesaikannya: jalankan CLI, scan QR, bagikan file atau teks instan - terproteksi password dan otomatis kedaluwarsa 60 menit.

| | |
|---|---|
| ⚡ **Konek Instan** | Scan QR, langsung terbuka di HP. Tak perlu ketik IP. |
| 🔒 **Terproteksi Password** | Setiap bundle aman dengan hashing password bcrypt. |
| 📱 **Tanpa Internet** | Jalan sepenuhnya via Wi-Fi lokal. Tak ada data keluar jaringan. |
| ⏰ **Auto-Kedaluwarsa** | File dan teks terhapus otomatis setelah 60 menit. |

---

## ✨ Fitur Utama

| Fitur | Status | Deskripsi |
| :--- | :---: | :--- |
| **QR Connect** | ✅ | Scan dari HP, langsung terbuka di browser |
| **Upload File** | ✅ | Drag & drop atau pilih file. Maks 100 MB per file |
| **Download File** | ✅ | Satu klik, berpassword |
| **Bagikan Teks** | ✅ | Tempel teks, snippet kode, atau link |
| **Proteksi Password** | ✅ | bcrypt per bundle dan per grup |
| **Auto-Kedaluwarsa** | ✅ | Sweeper hapus item kedaluwarsa tiap 60 menit |
| **Check Update** | ✅ | CLI cek npm registry untuk versi terbaru |
| **Group Chat** | ✅ | Berbagi file dan teks real-time dalam grup |
| **i18n (EN/ID/CN/JP)** | ✅ | 4 bahasa toggle di header |
| **Mode Gelap/Terang** | ✅ | Toggle tema di header, preferensi tersimpan |
| **Auto Start** | ✅ | Auto-start level OS (systemd / LaunchAgent / schtasks) |

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **CLI** | Node.js (vanilla, tanpa dependency) |
| **Backend** | Python 3.10+, Flask 3, bcrypt, qrcode[pil], Pillow |
| **Frontend** | Vanilla HTML/CSS/JS (tanpa build), ikon SVG inline |
| **Storage** | File-based JSON (tanpa database) |
| **Distribusi** | Paket npm global + repo GitHub |
| **License** | MIT |

---

## 🏗️ Architecture

```
hour-share/
├── bin/hourshare.js        # CLI: TUI menu, daemon spawn, auto-start
├── server.py               # Flask backend (file/text share, QR, auth, sweeper)
├── requirements.txt        # Python dependencies
├── templates/index.html    # Web dashboard (2-col grid, tabs, i18n, theme)
├── static/                 # Static assets (CSS/JS)
├── shared/                 # File storage + metadata JSON
│   ├── bundles/            # Uploaded file bundles (auto-expired)
│   └── groups/             # Group chat data
└── Auto-Start/             # OS service configs (systemd / LaunchAgent / schtasks)
```

---

## 🚀 Cara Pakai

Install CLI global (disarankan):

```bash
npm install -g hourshare
hourshare
```

1. Jalankan `hourshare` di terminal.
2. Pilih **Start** dari menu:

```text
========================================
  Hour Share (v1.0.3)
  🚀 Server: http://localhost:10101
========================================
 ★ Start (Open in Browser)           ○ Stopped
 ☆ Auto Start (Disable)           
 ☆ Check Update (Internet Require)
 ☆ Stop                           
 ☆ Exit                           
  ↑↓ navigate · Enter select · Esc/Ctrl+C exit
```

3. Buka URL lokal yang tampil (seperti `http://localhost:10101` atau IP lokal Anda) di browser perangkat yang sama, atau scan QR dari HP.
4. Masukkan password dan bagikan file atau teks. Untuk menerima, masukkan password yang sama.

**Auto Start:** Pilih **Auto Start** dari menu untuk menjalankan server saat login.

---

## 📦 Instalasi

<a href="https://github.com/Curzyori/hour-share/releases">Unduh dari GitHub Releases</a> atau build from source:

```bash
git clone https://github.com/Curzyori/hour-share.git
cd hour-share
pip install flask bcrypt qrcode[pil] pillow
```

**Syarat:**
- Node.js >= 18
- Python 3.10+ (Linux, macOS, Windows)
- pip packages: `flask`, `bcrypt`, `qrcode[pil]`, `pillow`

---

## 🎮 CLI Flags

```bash
hourshare                     # Menu interaktif
hourshare --port 8080          # Port kustom
hourshare --daemon             # Mode headless (tanpa menu)
hourshare --help               # Tampilkan bantuan
```

---

## 📡 API Endpoints

| Method | Path | Fungsi |
|--------|------|--------|
| `GET` | `/` | Dashboard web |
| `GET` | `/api/qr` | QR Code PNG |
| `POST` | `/api/send` | Upload bundle (file + teks + password) |
| `POST` | `/api/receive` | Akses bundle dengan password |
| `POST` | `/api/group/join` | Gabung atau buat grup |
| `GET` | `/api/group/{name}/info` | Info grup |
| `POST` | `/api/group/{name}/send` | Kirim ke grup |
| `GET` | `/download/bundle/{id}/{filename}` | Download file (perlu session auth) |

---

## 🖼️ Preview

<table align="center">
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="Dashboard Desktop" width="250"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/mobile-preview.jpg" alt="Dashboard Mobile" width="250"/></td>
  </tr>
  <tr>
    <td align="center"><em>Desktop: Tab Send / Receive / Group</em></td>
    <td align="center"><em>Mobile: Scan QR + panel tab</em></td>
  </tr>
</table>

---

## ☕ Support

Jika Anda merasa project ini bermanfaat, mohon pertimbangkan untuk memberikan ⭐ Star atau melakukan 🍴 Fork untuk menunjukkan dukungan dan membuat saya lebih semangat lagi membuat project open-source yang menarik ke depannya! Setiap star dan fork sangat berharga bagi developer.

Donasi Anda menjaga proyek ini tetap gratis dan open-source. Setiap kontribusi sangat berarti, dan dukungan Anda membantu saya untuk terus membuat proyek open-source menarik ke depannya.

<a href="https://donate.curzy.dev/">Dukung project ini dengan membelikan saya kopi! 💝</a>

<a href="https://donate.curzy.dev/">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200" />
</a>

---

## ⚖️ License

Project ini dirilis under lisensi **MIT** - lihat <a href="LICENSE">LICENSE</a> untuk teks lengkap.

<p align="center"><sub>Dibangun dengan passion sebagai Project ke-21 dari 50 Projects Challenge by **@Curzyori**</sub></p>
