<p align="center">
  <img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/logo.png" alt="Hour Share Logo" width="120"/>
</p>

<h1 align="center">Hour Share</h1>
<p align="center">
  <strong>QRコードでデバイス間にファイルとテキストを共有 - インターネット不要、ログイン不要</strong>
</p>

<p align="center">
  <a href="https://hour-share.curzy.dev"><strong>🌐 ウェブサイト</strong></a>
</p>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share)
[![Forks](https://img.shields.io/github/forks/Curzyori/hour-share?style=for-the-badge&color=374151)](https://github.com/Curzyori/hour-share/network/members)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Python%20%7C%20Node.js%20%7C%20Cross--platform-black?style=for-the-badge)](#)

</div>

<p align="center">
  <a href="#why-hour-share">概要</a> ·
  <a href="#key-features">機能</a> ·
  <a href="#quick-start">クイックスタート</a> ·
  <a href="#installation">インストール</a> ·
  <a href="#cli-flags">CLIオプション</a> ·
  <a href="#api-endpoints">API</a> ·
  <a href="#preview">プレビュー</a> ·
  <a href="#support">サポート</a>
</p>

<p align="center">🌐 4か国語対応 -
  <a href="README.md">🇺🇸 EN</a> ·
  <a href="README_ID.md">🇮🇩 ID</a> ·
  <a href="README_CN.md">🇨🇳 CN</a> ·
  <a href="README_JP.md"><b>🇯🇵 JP</b></a>
</p>

---

## 概要

同じローカルネットワーク内でデバイス間にファイルを転送するのは面倒です：
- IPアドレスを探してスマホで手入力するのはミスが起きやすい。
- クラウドストレージやLINEにはインターネットとアカウントが必要。
- USBケーブルは一度きりのクイック転送には過剰。

Hour Share が解決します。CLIを起動し、QRコードをスキャンするだけでファイルやテキストを即座に共有 - パスワード保護され、60分で自動期限切れ。

| | |
|---|---|
| ⚡ **即時接続** | QRをスキャンするだけでスマホで直接開く。IP入力は不要。 |
| 🔒 **パスワード保護** | 各バンドルはbcryptハッシュで保護。 |
| 📱 **インターネット不要** | ローカルWi-Fiのみで動作。データはネットワークから出ない。 |
| ⏰ **自動期限切れ** | ファイルとテキストは60分後に自動削除。 |

---

## 主な機能

| 機能 | 状態 | 説明 |
| :--- | :---: | :--- |
| **QR接続** | ✅ | スマホでスキャン、ブラウザで直接開く |
| **ファイル送信** | ✅ | ドラッグ＆ドロップまたは選択。1ファイル最大100MB |
| **ファイル受信** | ✅ | ワンクリックでダウンロード、パスワード保護 |
| **テキスト共有** | ✅ | テキスト、コードスニペット、リンクを貼り付け |
| **パスワード保護** | ✅ | バンドルおよびグループごとにbcrypt |
| **自動期限切れ** | ✅ | バックグラウンドスイーパーが60分ごとに削除 |
| **グループチャット** | ✅ | グループ内でリアルタイムにファイルとテキスト共有 |
| **i18n (EN/ID/CN/JP)** | ✅ | ヘッダーで4言語切替 |
| **ダーク/ライトモード** | ✅ | ヘッダーでテーマ切替、設定を保存 |
| **自動起動** | ✅ | OSレベルの自動起動（systemd / LaunchAgent / schtasks） |

---

## 技術スタック

| 層 | 技術 |
|-------|-----------|
| **CLI** | Node.js（純正、依存なし） |
| **バックエンド** | Python 3.10+、Flask 3、bcrypt、qrcode[pil]、Pillow |
| **フロントエンド** | 純HTML/CSS/JS（ビルド不要）、SVGインラインアイコン |
| **ストレージ** | ファイルベースJSON（データベースなし） |
| **配布** | npmグローバルパッケージ + GitHubリポジトリ |
| **ライセンス** | MIT |

---

## クイックスタート

```bash
npm install -g hourshare
hourshare
```

1. ターミナルで `hourshare` を実行。
2. メニューから **Start** を選択。
3. 同じデバイスのブラウザで表示されたURLを開くか、スマホでQRコードをスキャン。
4. パスワードを入力してファイルやテキストを共有。受信するには同じパスワードを入力。

**自動起動：** メニューから **Auto Start** を選択するとログイン時にサーバーが起動。

---

## インストール

<a href="https://github.com/Curzyori/hour-share/releases">GitHub Releasesからダウンロード</a> またはソースからビルド：

```bash
git clone https://github.com/Curzyori/hour-share.git
cd hour-share
```

**要件：**
- Node.js >= 18
- Python 3.10+
- pipパッケージ：`flask`、`bcrypt`、`qrcode[pil]`、`pillow`（初回起動時に自動インストール）

---

## CLIオプション

```bash
hourshare                     # 対話メニュー
hourshare --port 8080          # ポート指定
hourshare --daemon             # ヘッドレスモード（メニューなし）
hourshare --help               # ヘルプ表示
```

---

## APIエンドポイント

| メソッド | パス | 機能 |
|--------|------|----------|
| `GET` | `/` | Webダッシュボード |
| `GET` | `/api/qr` | QRコードPNG |
| `POST` | `/api/send` | バンドル送信（ファイル＋テキスト＋パスワード） |
| `POST` | `/api/receive` | パスワードでバンドルにアクセス |
| `POST` | `/api/group/join` | グループ参加または作成 |
| `GET` | `/api/group/{name}/info` | グループ情報 |
| `POST` | `/api/group/{name}/send` | グループへ送信 |
| `GET` | `/download/bundle/{id}/{filename}` | ファイルダウンロード（セッション認証要） |

---

## プレビュー

<table align="center">
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/desktop-preview.png" alt="デスクトップダッシュボード" width="250"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/Curzyori/hour-share/main/images/mobile-preview.jpg" alt="モバイルダッシュボード" width="250"/></td>
  </tr>
  <tr>
    <td align="center"><em>デスクトップ：送信 / 受信 / グループ タブ</em></td>
    <td align="center"><em>モバイル：QRスキャン + タブパネル</em></td>
  </tr>
</table>

---

## サポート

<a href="https://donate.curzy.dev/">コーヒーをおごってプロジェクトを支援！</a>

<a href="https://donate.curzy.dev/">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200">
</a>

---

## ライセンス

本プロジェクトは **MIT** ライセンスで公開されています - 全文は <a href="LICENSE">LICENSE</a> を参照。

<sub>50 Projects Challenge の第21弾として **@Curzyori** が情熱を込めて開発</sub>
