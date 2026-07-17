<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="Hour Share Desktop Dashboard" width="800"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/logo.png" alt="Hour Share Logo" width="120"/>
</p>

<h1 align="center">Hour Share</h1>
<p align="center">
  <strong>Share Files & Text Across Devices via QR Code - No Internet, No Login</strong>
</p>

<p align="center">
  <a href="https://hour-share.curzy.dev"><strong>🌐 Live Website</strong></a>
</p>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share)
[![Forks](https://img.shields.io/github/forks/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share/network/members)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Python%20%7C%20Node.js%20%7C%20Cross--platform-black?style=for-the-badge)](#)

</div>

<p align="center">
  <a href="#why-hour-share">Why This</a> ·
  <a href="#key-features">Features</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#cli-flags">CLI Flags</a> ·
  <a href="#api-endpoints">API</a> ·
  <a href="#preview">Preview</a> ·
  <a href="#support">Support</a>
</p>

<p align="center">🌐 In 4 languages -
  <a href="README.md"><b>🇺🇸 EN</b></a> ·
  <a href="README_ID.md">🇮🇩 ID</a> ·
  <a href="README_CN.md">🇨🇳 CN</a> ·
  <a href="README_JP.md">🇯🇵 JP</a>
</p>

---

## Why Hour Share?

Transferring files between devices on the same local network is unnecessarily difficult:
- Finding IP addresses and typing them manually on a phone is error-prone.
- Cloud storage or WhatsApp requires internet and an account.
- USB cables are overkill for quick, one-time file transfers.

Hour Share solves this: launch the CLI, scan the QR code, and share files or text instantly - password-protected and auto-expiring after 60 minutes.

| | |
|---|---|
| ⚡ **Instant Connect** | Scan QR, opens directly on your phone. No more typing IP addresses. |
| 🔒 **Password Protected** | Every bundle is secured with bcrypt password hashing. |
| 📱 **No Internet Required** | Works entirely over local Wi-Fi. Zero data leaves your network. |
| ⏰ **Auto-Expire** | Files and text delete automatically after 60 minutes. |

---

## Key Features

| Feature | Status | Description |
| :--- | :---: | :--- |
| **QR Connect** | ✅ | Scan from phone, opens directly in browser |
| **File Upload** | ✅ | Drag & drop or select files. 100 MB limit per file |
| **File Download** | ✅ | One-click download, password-gated |
| **Text Share** | ✅ | Paste text, code snippets, or links |
| **Password Protection** | ✅ | bcrypt per bundle and per group |
| **Auto-Expire** | ✅ | Background sweeper removes expired items every 60 minutes |
| **Group Chat** | ✅ | Real-time file and text sharing within a group |
| **i18n (EN/ID/CN/JP)** | ✅ | 4 languages toggle in the header |
| **Dark/Light Mode** | ✅ | Theme toggle in header, persistent preference |
| **Auto Start** | ✅ | OS-level auto-start (systemd / LaunchAgent / schtasks) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **CLI** | Node.js (vanilla, zero dependencies) |
| **Backend** | Python 3.10+, Flask 3, bcrypt, qrcode[pil], Pillow |
| **Frontend** | Vanilla HTML/CSS/JS (no build step), inline SVG icons |
| **Storage** | File-based JSON (no database) |
| **Distribution** | npm global package + GitHub repository |
| **License** | MIT |

---

## Quick Start

Install the CLI globally (recommended):

```bash
npm install -g hourshare
hourshare
```

1. Run `hourshare` in your terminal.
2. Select **Start** from the menu.
3. Open the displayed URL in your browser on the same device, or scan the QR code from your phone.
4. Enter a password and share files or text. To receive, enter the same password.

**Auto Start:** Select **Auto Start** from the menu to launch the server at login.

---

## Installation

<a href="https://github.com/Curzyori/hour-share/releases">Download from GitHub Releases</a> or build from source:

```bash
git clone https://github.com/Curzyori/hour-share.git
cd hour-share
pip install flask bcrypt qrcode[pil] pillow
```

**Requirements:**
- Node.js >= 18
- Python 3.10+ (Linux, macOS, Windows)
- pip packages: `flask`, `bcrypt`, `qrcode[pil]`, `pillow`

---

## CLI Flags

```bash
hourshare                     # Interactive menu
hourshare --port 8080          # Custom port
hourshare --daemon             # Headless mode (no menu)
hourshare --help               # Show help
```

---

## API Endpoints

| Method | Path | Function |
|--------|------|----------|
| `GET` | `/` | Web dashboard |
| `GET` | `/api/qr` | QR Code PNG |
| `POST` | `/api/send` | Upload bundle (files + text + password) |
| `POST` | `/api/receive` | Access bundle with password |
| `POST` | `/api/group/join` | Join or create a group |
| `GET` | `/api/group/{name}/info` | Group info |
| `POST` | `/api/group/{name}/send` | Send to group |
| `GET` | `/download/bundle/{id}/{filename}` | Download file (requires auth session) |

---

## Preview

<table align="center">
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="Desktop Dashboard" width="250"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/mobile-preview.jpg" alt="Mobile Dashboard" width="250"/></td>
  </tr>
  <tr>
    <td align="center"><em>Desktop: Send / Receive / Group tabs</em></td>
    <td align="center"><em>Mobile: QR scan + tabbed panel</em></td>
  </tr>
</table>

---

## Support

<a href="https://donate.curzy.dev/">Support this project by buying me a coffee!</a>

<a href="https://donate.curzy.dev/">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200">
</a>

---

## License

This project is released under the **MIT** license - see <a href="LICENSE">LICENSE</a> for full text.

<sub>Built with passion as the 21st Project of the 50 Projects Challenge by **@Curzyori**</sub>
