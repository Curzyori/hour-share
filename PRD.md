# PRD — Hour Share (v1.0.0)

## 1. Overview

**Type:** Local Web Tool (CLI wrapper + Flask server + web dashboard)
**Stack:** Node.js (CLI, vanilla) + Python 3.10/Flask (server) + vanilla HTML/CSS/JS (frontend)
**Core:** Share file & text antar device dalam 1 Wi-Fi via QR — no internet, no login.

- **Tagline**: Share Files & Text Across Devices via QR Code — No Internet, No Login
- **Status**: v1.0.0 — shipped (auto-start + CLI menu + Check Update)
- **Repo**: `github.com/curzyori/hour-share`
- **Website**: `hour-share.curzy.dev`
- **License**: MIT

## 2. Problem Statement

Transfer file antar device di jaringan lokal ribet:
- Cari IP + ketik manual di browser HP (sering salah).
- Upload ke cloud/WhatsApp = butuh internet + akun.
- USB cable = repot buat file kecil sekali pakai.

Hour Share: `hourshare` → scan QR → buka dashboard → upload/download/text lewat password. Auto-expire 60m biar gak nyisain sampah di disk.

## 3. Target Users

- Dev / power user yang sering pindahin file kecil antar laptop ↔ HP dalam 1 jaringan lokal.
- User yang gak mau cloud/WA/USB buat transfer cepat.
- Cross-platform: Linux, macOS, Windows (CLI node jalan di semua OS).

## 4. Goals

**Primary**
- [x] Share file/text antar device via QR tanpa internet/login.
- [x] Password protection + auto-expire 60m.
- [x] Auto-start di login session (OS service).

**Secondary**
- [x] Group chat lokal (file/text real-time dalam 1 group).
- [x] i18n ID/EN + dark/light toggle di web.
- [x] CLI Check Update (npm) buat notif versi baru.
- [ ] npm publish → Check Update verifiable end-to-end.

## 5. Features (shipped v1.0.0)

| Fitur | Status | Catatan |
|---|---|---|
| QR Connect | ✅ | Scan → buka dashboard di HP |
| File Upload | ✅ | Drag-drop / pilih, max 100 MB/file |
| File Download | ✅ | 1 klik, password-gated |
| Text Share | ✅ | Paste text/snippet/link |
| Password Protection | ✅ | bcrypt per bundle/group |
| Auto-Expire | ✅ | Bundle + group + item grup dihapus <60m |
| Group Chat | ✅ | Real-time file/text share dalam group |
| i18n ID/EN | ✅ | Toggle header, localStorage |
| Dark/Light | ✅ | Toggle header, `data-theme` |
| Auto Start (OS service) | ✅ | Linux/macOS/Windows, toggle di CLI |
| Check Update (npm) | ✅ | Baris ke-3 CLI, cek `npm view hourshare version` |

## 6. Architecture

```
hourshare (CLI, Node.js)
  ├─ TUI menu (arrow keys) → Start / Auto Start / Check Update / Stop / Exit
  ├─ --daemon → spawn server.py (background, detached)
  ├─ --version → print version
  └─ Auto Start: systemd --user (Linux) / LaunchAgent (macOS) / schtasks (Windows)

server.py (Flask, Python 3.10+)
  ├─ Storage: file-based JSON (shared/metadata.json) + folder bundles/ groups/
  ├─ Auth: bcrypt password per bundle/group
  ├─ QR: qrcode[pil] → /api/qr
  ├─ Sweeper: hapus expired tiap 10s (EXPIRE_MINUTES=60)
  └─ Rate limit: 30 req/IP/60s di endpoint auth/send

templates/index.html (frontend)
  ├─ 2-col grid: QR card (kiri) + tabbed panel (kanan)
  ├─ Tabs: Send / Receive / Group (desktop row, mobile column)
  ├─ Dark/Light toggle + i18n ID/EN
  └─ Toast feedback, skip-link, focus-visible, reduced-motion
```

## 7. Check Update — Design (fitur terbaru)

- **Trigger**: user pilih `☆ Check Update (Internet Require)` di TUI.
- **Action**: `execSync("npm view hourshare version", {timeout:10000})` → banding `LOCAL_VERSION` (`bin/hourshare.js:14`).
- **Branch**:
  - npm call gagal/offline → teks merah "Couldn't check (offline or npm error)." + wait key → balik menu.
  - versi sama → teks hijau "You're on the latest version (vX)." + wait key → balik menu.
  - versi beda → layar box:
    ```
    ╭─ New version available: v<remote> ─╮
    │ (current: v<local>)               │
    │ To update:                        │
    │ 1. Stop this server               │
    │ 2. npm install -g hourshare@latest│
    │ 3. hourshare                      │
    ╰───────────────────────────────────╯
    ☆ Stop
    ☆ Exit
    ```
- **Non-goal**: gak auto-install. User update manual. GitHub releases API menyusul (belum dipakai).
- **Blocker**: `hourshare` belum dipublish ke npm → cek sekarang return E404. Perlu `npm publish` dulu biar fitur testable live.

## 8. Non-Functional Requirements

| Aspek | Target |
|-------|--------|
| Performance | Flask threaded, sweeper 10s, bundle <100MB, latency = LAN |
| Security | bcrypt hash, path-traversal guard, rate limit per-IP, session auth download |
| Privacy | Gak ada data keluar jaringan (kecuali Check Update sengaja hubungi npm) |
| Compat | Node >=18, Python 3.10+, venv (bcrypt/qrcode/Flask) |
| Reliability | Auto-start OS-level (Restart=on-failure / KeepAlive) survive logout |

## 9. Tech Stack

- CLI: Node.js (vanilla, no deps) — `bin/hourshare.js`
- Backend: Python 3.10+, Flask 3, bcrypt, qrcode[pil], Pillow
- Frontend: vanilla HTML/CSS/JS (no build step), inline SVG icons
- Storage: file-based JSON (no DB)
- Distribusi: npm global (`npm i -g hourshare`), repo GitHub

## 10. Distribution & Update Plan

1. Publish ke npm (`hourshare`) — source of truth versi buat Check Update.
2. Nanti mirror ke GitHub releases + website.
3. Cross-platform: 1 npm package覆盖 Linux/macOS/Windows (node CLI). Auto-start beda per OS (systemd/LaunchAgent/schtasks) — sudah di-handle di CLI.

| Link | Pattern |
|------|---------|
| GitHub | `github.com/curzyori/hour-share` |
| Website | `hour-share.curzy.dev` |
| Donate | `donate.curzy.dev` |

## 11. Error Handling

| Scenario | Handling |
|----------|----------|
| Port 10101 sudah dipakai | Flask raise; CLI catch → pesan "port in use", exit 1 |
| Password salah / bundle expired | `/api/receive` → 403 "Password salah atau bundle tidak ditemukan" |
| Upload tanpa password | 400 "Password wajib diisi!" |
| File melebihi 100MB | Flask 413 (MAX_CONTENT_LENGTH) |
| Rate limit terlampaui (30/IP/60s) | 429 abort |
| Path traversal di nama file | `secure_filename` + validasi group regex `^[a-z0-9_-]{1,40}$` |
| Check Update offline / npm error | Teks merah, balik menu (gak crash) |
| Download tanpa auth session | 403 (harus input password dulu) |

## 12. Non-Goals / Out of Scope

- Auto-install update (user update manual via npm).
- Cloud sync / akses dari luar Wi-Fi.
- WebSocket real-time push (group pakai polling `/api/group/<name>/info`).
- Settings screen di web buat toggle auto-start (butuh IPC browser→CLI).
- macOS/Windows live-test auto-start (logic setara Linux).

## 13. Open Issues

1. README shields "Platform: Python | Flask" — padahal ada Node CLI juga. Perlu update label.
2. `hourshare` npm package belum publish → Check Update gak testable live (E404).
3. macOS/Windows auto-start belum di-test live (gak ada env), logic setara Linux.
4. Setting screen di web app buat toggle auto-start — butuh IPC browser→CLI (out of scope).

## 14. Decision Log

| # | Keputusan | Alternatif | Alasan |
|---|-----------|------------|--------|
| 1 | License = **MIT** | Apache-2.0 | User pilih MIT; package.json disinkron ke MIT (sebelumnya Apache-2.0) |
| 2 | Distribusi = npm dulu → GitHub | GitHub dulu, GitHub saja | npm = source of truth versi buat Check Update; mirror ke GitHub nanti |
| 3 | Check Update pakai npm registry | GitHub releases API, auto-install | Manual update lebih aman; npm view simpel, gak perlu token |
| 4 | Storage file-based JSON | SQLite, Redis | YAGNI — volume kecil, expiry 60m, no concurrency heavy |
| 5 | Auto-start = OS service (systemd/LaunchAgent/schtasks) | cron, in-app loop | OS manage lifetime (restart on failure), survive logout |
| 6 | Group chat pakai polling | WebSocket | YAGNI — polling cukup untuk low-frequency local share |

## 15. Success Criteria

- [x] Share file/text antar device via QR tanpa internet.
- [x] Password + auto-expire jalan.
- [x] Auto-start di login (Linux verified).
- [x] CLI Check Update ngecek npm (pending publish buat live test).
- [ ] npm publish done → Check Update verifiable end-to-end.
