<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="Hour Share 桌面仪表盘" width="800"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/logo.png" alt="Hour Share Logo" width="120"/>
</p>

<h1 align="center">Hour Share</h1>
<p align="center">
  <strong>通过二维码跨设备共享文件与文本 - 无需联网，无需登录</strong>
</p>

<p align="center">
  <a href="https://hour-share.curzy.dev"><strong>🌐 在线网站</strong></a>
</p>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share)
[![Forks](https://img.shields.io/github/forks/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share/network/members)
[![Downloads](https://img.shields.io/npm/dw/hourshare?style=for-the-badge&color=374151)](https://www.npmjs.com/package/hourshare)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Python%20%7C%20Node.js%20%7C%20Cross--platform-black?style=for-the-badge)](#)

</div>

<p align="center">
  <a href="#why-hour-share">背景</a> ·
  <a href="#key-features">功能</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#tech-stack">技术栈</a> ·
  <a href="#quick-start">快速开始</a> ·
  <a href="#installation">安装</a> ·
  <a href="#cli-flags">CLI参数</a> ·
  <a href="#api-endpoints">API</a> ·
  <a href="#preview">预览</a> ·
  <a href="#support">支持</a> ·
  <a href="#license">许可证</a>
</p>

<p align="center">🌐 支持 4 种语言 -
  <a href="README.md">🇺🇸 EN</a> ·
  <a href="README_ID.md">🇮🇩 ID</a> ·
  <a href="README_CN.md"><b>🇨🇳 CN</b></a> ·
  <a href="README_JP.md">🇯🇵 JP</a>
</p>

---

## <a id="why-hour-share"></a>背景

在同一局域网内跨设备传输文件往往很麻烦：
- 在手机上查找并手动输入 IP 地址容易出错。
- 云存储或微信需要联网和账号。
- USB 数据线对于一次性快速传输来说过于繁琐。

Hour Share 解决了这个问题：启动 CLI，扫描二维码，即可即时共享文件或文本 - 密码保护且 60 分钟后自动过期。

| | |
|---|---|
| ⚡ **即时连接** | 扫描二维码，直接在手机上打开。无需手动输入 IP。 |
| 🔒 **密码保护** | 每个数据包均使用 bcrypt 密码哈希加密。 |
| 📱 **无需联网** | 完全通过本地 Wi-Fi 运行。数据不会离开您的网络。 |
| ⏰ **自动过期** | 文件和文本在 60 分钟后自动删除。 |

---

## ✨ <a id="key-features"></a>主要功能

| 功能 | 状态 | 描述 |
| :--- | :---: | :--- |
| **二维码连接** | ✅ | 手机扫描，直接在浏览器中打开 |
| **文件上传** | ✅ | 拖放或选择文件。单文件上限 100 MB |
| **文件下载** | ✅ | 一键下载，密码保护 |
| **文本共享** | ✅ | 粘贴文本、代码片段或链接 |
| **密码保护** | ✅ | 每个数据包和群组使用 bcrypt |
| **自动过期** | ✅ | 后台清理程序每 60 分钟删除过期项目 |
| **检查更新** | ✅ | CLI 检查 npm 注册表以获取更新版本 |
| **群聊** | ✅ | 群组内实时共享文件与文本 |
| **i18n (EN/ID/CN/JP)** | ✅ | 页头切换 4 种语言 |
| **深色/浅色模式** | ✅ | 页头主题切换，偏好持久保存 |
| **自动启动** | ✅ | 操作系统级自动启动（systemd / LaunchAgent / schtasks） |

---

## 🛠️ 技术栈

| 层 | 技术 |
|-------|-----------|
| **CLI** | Node.js（纯原生，零依赖） |
| **后端** | Python 3.10+、Flask 3、bcrypt、qrcode[pil]、Pillow |
| **前端** | 纯原生 HTML/CSS/JS（无构建步骤），SVG 内联图标 |
| **存储** | 基于文件的 JSON（无数据库） |
| **分发** | npm 全局包 + GitHub 仓库 |
| **许可证** | MIT |

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

---

## 🚀 <a id="quick-start"></a>快速开始

全局安装 CLI（推荐）：

```bash
npm install -g hourshare
hourshare
```

1. 在终端运行 `hourshare`。
2. 从菜单中选择 **Start**：

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

3. 在同一设备的浏览器中打开显示的本地 URL（如 `http://localhost:10101` 或本地 IP），或用手机扫描二维码。
4. 输入密码并共享文件或文本。要接收，请输入相同密码。

**自动启动：** 从菜单中选择 **Auto Start** 可在登录时启动服务器。

---

## 📦 <a id="installation"></a>安装

<a href="https://github.com/Curzyori/hour-share/releases">从 GitHub Releases 下载</a> 或从源码构建：

```bash
git clone https://github.com/Curzyori/hour-share.git
cd hour-share
pip install flask bcrypt qrcode[pil] pillow
```

**要求：**
- Node.js >= 18
- Python 3.10+（Linux、macOS、Windows）
- pip 包：`flask`、`bcrypt`、`qrcode[pil]`、`pillow`

---

## 🎮 <a id="cli-flags"></a>CLI 参数

```bash
hourshare                     # 交互式菜单
hourshare --port 8080          # 自定义端口
hourshare --daemon             # 无界面模式（无菜单）
hourshare --help               # 显示帮助
```

---

## 📡 <a id="api-endpoints"></a>API 接口

| 方法 | 路径 | 功能 |
|--------|------|----------|
| `GET` | `/` | Web 仪表盘 |
| `GET` | `/api/qr` | 二维码 PNG |
| `POST` | `/api/send` | 上传数据包（文件 + 文本 + 密码） |
| `POST` | `/api/receive` | 使用密码访问数据包 |
| `POST` | `/api/group/join` | 加入或创建群组 |
| `GET` | `/api/group/{name}/info` | 群组信息 |
| `POST` | `/api/group/{name}/send` | 发送至群组 |
| `GET` | `/download/bundle/{id}/{filename}` | 下载文件（需要会话授权） |

---

## 🖼️ <a id="preview"></a>预览

<table align="center">
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="桌面仪表盘" width="250"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/mobile-preview.jpg" alt="移动仪表盘" width="250"/></td>
  </tr>
  <tr>
    <td align="center"><em>桌面：发送 / 接收 / 群组 标签</em></td>
    <td align="center"><em>移动：扫描二维码 + 标签面板</em></td>
  </tr>
</table>

---

## ☕ <a id="support"></a>支持

如果你觉得这个项目对你有帮助，请考虑给一个 ⭐ Star 或 🍴 Fork 以示支持，这能让我更有动力继续开发更多有趣的开源项目！每一个 Star 和 Fork 对开发者来说都无比珍贵。

您的捐赠能让这个项目保持免费与开源。每一份贡献都至关重要，您的支持也将激励我未来继续开发更多有趣的开源项目。

<a href="https://donate.curzy.dev/">请我喝杯咖啡吧！ 💝</a>

<a href="https://donate.curzy.dev/">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200" />
</a>

---

## ⚖️ 许可证

本项目基于 **MIT** 许可证发布 - 完整文本见 <a href="LICENSE">LICENSE</a>。

<sub>作为 50 Projects Challenge 的第 21 个项目，由 **@Curzyori** 倾情打造</sub>
