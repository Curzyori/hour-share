# DESIGN.md — Hour Share

## Palette

| Token | Light | Dark | Penggunaan |
|---|---|---|---|
| `--primary` | `#5645D4` | `#8B7CFF` | Brand accent, tombol utama, active tab, focus ring |
| `--primary-soft` | `#ECE9FB` | `#2A2745` | Background link/pill, drag-over state |
| `--primary-ink` | `#3A2E96` | `#C4BBFF` | Teks di atas primary-soft |
| `--canvas` | `#FFFFFF` | `#16161B` | Background halaman, card |
| `--surface` | `#F7F6F4` | `#1E1E25` | File row, dropzone, textarea, pill bg |
| `--surface-2` | `#EDEBE8` | `#28282F` | Hover state surface |
| `--ink` | `#1A1A1A` | `#F5F5F5` | Heading, nama file |
| `--ink-2` | `#4A4A4A` | `#C4C4C4` | Body text, meta |
| `--ink-3` | `#6B6B6B` | `#A1A1A1` | Hint, sub label, brand subtitle |
| `--line` | `#E5E3DF` | `#33333D` | Border card, file row, separator |
| `--danger` | `#D44A4A` | `#E66A6A` | Tombol hapus / error toast |
| `--danger-bg` | `#FBE9E9` | `#3A1F1F` | Hover danger |
| `--ok` | `#2BA66B` | `#4ADE80` | Status "LIVE" pill, success toast |
| `--ok-bg` | `#E5F5EC` | `#14321F` | Empty success bg |
| `--warn` | `#8A5A00` | `#FBBF24` | Expire timer pill |
| `--warn-bg` | `#FFF1D6` | `#3A2B0F` | Expire timer bg |

## Typografi

- **Body**: `DM Sans` (Google Fonts), 15px / 1.6 line-height, system fallback.
- **Heading / brand / btn / pill / tab**: `Space Grotesk` (Google Fonts).
- **Code / IP / port**: `ui-monospace` 13px.
- **Heading section (card h2)**: 14px uppercase, letter-spacing .06em, `--primary`.

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:...&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Spacing & Radius

- Card padding: 20px (16px di mobile)
- Grid gap (home): 20px
- Card radius: 14px (`--radius`)
- Inner radius: 10px (`--radius-sm`)
- Pill radius: 999px (full)
- Toast: bottom-center pill, ink bg

## Shadow

```
--shadow:     0 1px 2px rgba(0,0,0,.04), 0 4px 14px rgba(86,69,212,.08)
--shadow-lg:  0 2px 4px rgba(0,0,0,.05), 0 10px 28px rgba(86,69,212,.12)
```
Subtle, tinted ke primary. Dark mode shadow lebih gelap (.2–.4 alpha).

## Motion (design-taste layer)

- `hs-rise`: card/file naik fade-in (.55s cubic-bezier(.16,1,.3,1)).
- `hs-breathe`: live-dot scale pulse (2.4s infinite).
- Hover lift: card/file translateY(-2px) + shadow-lg.
- `prefers-reduced-motion`: semua animasi → 0.01ms.

## Layout

### Header (sticky, blur backdrop)
- **Kiri**: logo SVG 34×34 (`#5645D4` rounded rect + white "H" stroke) + title "Hour**Share** v1.0.0" + subtitle "Local Web Share via QR".
- **Kanan** (`header-actions`):
  1. Donate button → `https://donate.curzy.dev` (pink heart SVG)
  2. Theme toggle (sun/moon SVG) → `data-theme` dark/light
  3. Language dropdown (inline SVG flag) → en/id/cn/jp
  4. Options dropdown (⋮) → Website / GitHub / Docs links

### Main — Nav Panel: HOME (`#panel-home`)
2-column grid `.home-grid` (320px QR + 1fr content), collapse ke 1 kolom <920px.

#### Left — QR card (`.qr-card`)
- Section label "QR CONNECT" (uppercase, primary)
- QR image 220×220 px (`/api/qr`), toggle hide/show (blur)
- URL pill (monospace, click-to-copy)
- Meta row: IP · Port · LIVE pill (breathing dot)

#### Right — Tabbed Actions card (`.card` + `.tab-pills`)
3 pill tabs (role=tablist), default active = **Send**:

| Tab | Panel | Isi |
|---|---|---|
| **Send** | `#panel-send` | Dropzone (drag/click, max 100MB) + send preview list + textarea + password (required) + SEND BUNDLE btn |
| **Receive** | `#panel-receive` | Password input → Buka Bundle → show text/files + expire timer + copy/lock |
| **Group** | `#panel-group` | Join/create group (name+pass) → active section: messages log + sender name + text + file upload + Kirim ke Group |

- Tab pill: `flex:1`, active = primary bg white text. Mobile <480px: padding menyusut.
- Panel switch: JS toggle `.active` class (no animation).

### Toast
Fixed bottom-center pill, ink bg. Variants: `.error` (danger), `.success` (ok). Auto-hide ~1.8s.

## Logo Motif

Inline SVG 34×34:
1. Rounded rect `#5645D4` base
2. White stroke "H" path (M11 9h12 M11 9l4.2 8-4.2 8 M23 9l-4.2 8 4.2 8)

Favicon: sama, data-URI di `<link rel="icon">`.

## i18n

- **4 locale**: `en` (default), `id`, `cn`, `jp`. Object `I18N.{locale}` di `<script>`.
- Apply: query `[data-i18n]` + `[data-i18n-placeholder]`.
- Selector: language dropdown, **inline SVG flag** (`.flag` 22×22, box-shadow inset), gak pakai emoji bendera.
- Pilihan disimpan di `localStorage.lang`.
- Flag render: `.lang-toggle .flag` (20px), `.lang-select-btn .flag` (22px).

## Accessibility

- Skip link (`#main`) → `Skip to content` (i18n).
- `*:focus-visible` → 2px primary outline.
- ARIA: `role="tab"`/`tabpanel`, `aria-selected`, `aria-controls`, `aria-live` di group log + toast.
- Touch target ≥40px di `@media (pointer: coarse)`.
- `prefers-reduced-motion` respected.

## Responsive

- **≥ 920px**: 2-col grid (QR 320px + content fluid)
- **< 920px**: stack 1 kolom, QR di atas
- **< 480px**: card padding 16px, brand title block, donate text hidden (icon only), tab-pill shrinks
- **< 360px**: tab-pill extra compact

## Component Inventory (reffrontend index.html)

`header.top` · `brand` · `header-actions` · `donate` · `theme-toggle` · `lang-toggle` + `lang-menu` · `option-btn` + `option-menu` · `nav-panel` · `home-grid` · `qr-card` + `qr-toggle` · `url-pill` · `meta-row` + `pill.ok` · `tab-pills` + `tab-pill` · `tab-panel` · `drop` · `send-preview` + `send-file-item` · `form-input` · `btn` (`.ghost`/`.danger`/`.success`/`.full`) · `files` + `file` + `file-icon` · `text-display` · `group-messages` + `message-item` · `empty` (+`.success`) · `toast` · `flag` · `live-dot`
