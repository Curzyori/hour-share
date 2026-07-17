#!/usr/bin/env node
"use strict";

const { spawn, execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const os = require("os");

// ---- paths ----
const DATA_DIR = path.join(os.homedir(), ".hourshare");
const PID_FILE = path.join(DATA_DIR, "pid");
const INIT_DONE = path.join(DATA_DIR, ".init_done");
const LOCAL_VERSION = "1.0.0";
const SERVER_SCRIPT = path.join(__dirname, "..", "server.py");
const REQ_FILE = path.join(__dirname, "..", "requirements.txt");
const DEFAULT_PORT = 10101;

// ---- ANSI colours ----
const R = "\x1b[0m";
const P = "\x1b[35m";
const G = "\x1b[32m";
const D = "\x1b[31m";
const GY = "\x1b[90m";
const BD = "\x1b[1m";

// ---- CLI flags ----
let PORT = DEFAULT_PORT;
let daemonMode = false;

function parseArgs() {
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--port":
        const v = parseInt(args[++i], 10);
        if (isNaN(v) || v < 1 || v > 65535) {
          console.error(D + "  Invalid port. Use 1-65535." + R);
          process.exit(1);
        }
        PORT = v;
        break;
      case "--daemon":
        daemonMode = true;
        break;
      case "--help":
      case "-h":
        console.log("");
        console.log(P + "  Hour Share" + R + " — Local Web Share via QR");
        console.log("");
        console.log("  " + BD + "Usage:" + R);
        console.log("    hourshare                  Start interactive menu");
        console.log("    hourshare --port 8080       Custom port");
        console.log("    hourshare --help            Show this help");
        console.log("");
        console.log("  " + BD + "Options:" + R);
        console.log("    --port <number>        Server port " + GY + "(default: " + DEFAULT_PORT + ")" + R);
        console.log("    --help, -h             Show this help");
        console.log("");
        process.exit(0);
      default:
        console.error(D + "  Unknown option: " + args[i] + R);
        console.error("  See hourshare --help");
        process.exit(1);
    }
  }
}

// ---- helpers ----
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function isRunning() {
  if (!fs.existsSync(PID_FILE)) return false;
  const pid = parseInt(fs.readFileSync(PID_FILE, "utf-8").trim(), 10);
  try {
    return process.kill(pid, 0);
  } catch {
    return false;
  }
}

function pyExe() {
  const venvPip = path.join(__dirname, "..", ".venv", "bin", "pip");
  return fs.existsSync(venvPip)
    ? path.join(__dirname, "..", ".venv", "bin", "python3")
    : "python3";
}

function startServer() {
  if (isRunning()) return;
  ensureDataDir();
  const child = spawn(pyExe(), [SERVER_SCRIPT], {
    stdio: "ignore",
    detached: true,
    cwd: path.join(__dirname, ".."),
    env: { ...process.env, HOURSHARE_PORT: String(PORT) },
  });
  fs.writeFileSync(PID_FILE, String(child.pid));
  child.unref();
}

function stopServer() {
  if (!fs.existsSync(PID_FILE)) return;
  const pid = parseInt(fs.readFileSync(PID_FILE, "utf-8").trim(), 10);
  try {
    process.kill(pid, "SIGTERM");
  } catch {}
  try {
    fs.unlinkSync(PID_FILE);
  } catch {}
}

function openBrowser(url) {
  try {
    const p = process.platform;
    if (p === "darwin") execSync(`open "${url}"`);
    else if (p === "win32") execSync(`start "" "${url}"`);
    else execSync(`xdg-open "${url}" 2>/dev/null || true`);
  } catch {}
}

function waitKey() {
  return new Promise((resolve) => {
    const stdin = process.stdin;
    if (stdin.isTTY) stdin.setRawMode(true);
    stdin.resume();
    stdin.once("data", () => {
      if (stdin.isTTY) stdin.setRawMode(false);
      stdin.pause();
      resolve();
    });
  });
}

function detectOS() {
  const p = process.platform;
  if (p === "darwin") return "macOS";
  if (p === "win32") return "Windows";
  return "Linux";
}

function installDeps() {
  return new Promise((resolve, reject) => {
    console.log(GY + "  Detected OS: " + detectOS() + R);
    console.log(GY + "  Installing Python dependencies…" + R);

    const venvPip = path.join(__dirname, "..", ".venv", "bin", "pip");
    const pipExe = fs.existsSync(venvPip) ? venvPip : "pip3";
    const args = ["install", "-r", REQ_FILE];
    if (!fs.existsSync(venvPip)) args.push("--break-system-packages");

    const pip = spawn(pipExe, args, {
      stdio: "inherit",
      cwd: path.join(__dirname, ".."),
    });
    pip.on("close", (code) => {
      if (code === 0) {
        fs.writeFileSync(INIT_DONE, "1");
        resolve();
      } else {
        reject(new Error("pip install failed"));
      }
    });
  });
}

function checkDeps() {
  try {
    execSync("python3 --version", { stdio: "ignore" });
  } catch {
    console.error(D + "  python3 not found. Install Python 3.10+ first." + R);
    process.exit(1);
  }
  try {
    execSync(pyExe() + " -c 'import bcrypt, flask, qrcode' 2>/dev/null", { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

async function init() {
  if (fs.existsSync(INIT_DONE)) return;
  ensureDataDir();
  console.clear();
  console.log(P + "=".repeat(40) + R);
  console.log(`  ${BD}Hour Share${R} ${GY}(v${LOCAL_VERSION})${R}`);
  console.log(P + "=".repeat(40) + R);
  try {
    await installDeps();
    console.log(G + "  Dependencies installed." + R);
  } catch {
    console.error(D + "  Failed to install dependencies." + R);
    console.error(D + "  Run: pip3 install -r requirements.txt" + R);
    process.exit(1);
  }
}

// ---- auto-start (run at login/boot) ----
function autoStartEnabled() {
  const p = process.platform;
  try {
    if (p === "linux") {
      return execSync("systemctl --user is-enabled hourshare 2>/dev/null")
        .toString()
        .trim() === "enabled";
    } else if (p === "darwin") {
      return fs.existsSync(
        path.join(os.homedir(), "Library", "LaunchAgents", "com.curzy.hourshare.plist")
      );
    } else if (p === "win32") {
      execSync('schtasks /Query /TN "HourShare" 2>nul');
      return true;
    }
  } catch {}
  return false;
}

function autoStartContent() {
  const node = process.execPath;
  const script = __filename;
  const portArgs = ["--daemon", "--port", String(PORT)];
  if (process.platform === "linux") {
    return `[Unit]
Description=HourShare background server
After=network.target

[Service]
Type=simple
ExecStart=${node} ${script} ${portArgs.join(" ")}
Restart=on-failure

[Install]
WantedBy=default.target
`;
  }
  if (process.platform === "darwin") {
    const arr = [node, script, ...portArgs].map((a) => `    <string>${a}</string>`).join("\n");
    return `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.curzy.hourshare</string>
  <key>ProgramArguments</key>
  <array>
${arr}
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
`;
  }
  return "";
}

function enableAutoStart() {
  const p = process.platform;
  if (p === "linux") {
    const dir = path.join(os.homedir(), ".config", "systemd", "user");
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "hourshare.service"), autoStartContent());
    execSync("systemctl --user daemon-reload");
    execSync("systemctl --user enable --now hourshare");
  } else if (p === "darwin") {
    const plist = path.join(
      os.homedir(),
      "Library",
      "LaunchAgents",
      "com.curzy.hourshare.plist"
    );
    fs.writeFileSync(plist, autoStartContent());
    try {
      execSync(`launchctl load -w "${plist}"`);
    } catch {}
  } else if (p === "win32") {
    const inner = `"${process.execPath}" "${__filename}" --daemon --port ${PORT}`;
    execSync(`schtasks /Create /TN "HourShare" /SC ONLOGON /TR "${inner}" /F`);
  } else {
    throw new Error("Platform ini belum didukung untuk Auto Start");
  }
}

function disableAutoStart() {
  const p = process.platform;
  if (p === "linux") {
    try {
      execSync("systemctl --user disable --now hourshare 2>/dev/null");
    } catch {}
    try {
      fs.unlinkSync(
        path.join(os.homedir(), ".config", "systemd", "user", "hourshare.service")
      );
    } catch {}
  } else if (p === "darwin") {
    const plist = path.join(
      os.homedir(),
      "Library",
      "LaunchAgents",
      "com.curzy.hourshare.plist"
    );
    try {
      execSync(`launchctl unload "${plist}" 2>/dev/null`);
    } catch {}
    try {
      fs.unlinkSync(plist);
    } catch {}
  } else if (p === "win32") {
    try {
      execSync('schtasks /Delete /TN "HourShare" /F 2>nul');
    } catch {}
  }
}

function applyAutoStart() {
  try {
    if (autoStartEnabled()) {
      disableAutoStart();
      console.log("  " + G + "Auto Start: DISABLED" + R);
    } else {
      enableAutoStart();
      console.log("  " + G + "Auto Start: ENABLED" + R);
    }
  } catch (e) {
    console.error(D + "  Gagal set Auto Start: " + e.message + R);
  }
  console.log("  " + GY + "Press any key to continue…" + R);
}

// ---- check update ----
function checkUpdate() {
  try {
    const out = String(
      execSync("npm view hourshare version", { timeout: 10000, encoding: "utf-8" })
    ).trim();
    return out;
  } catch {
    return null;
  }
}

function showUpdateScreen(remoteVersion) {
  let selected = 0;
  const updateMenu = [
    { label: "Stop", action() { stopServer(); showMenu(); } },
    { label: "Exit", action() { process.exit(0); } },
  ];

  const stdin = process.stdin;

  function render() {
    console.clear();
    const B = "\u2500".repeat(34);
    console.log("  \u250c" + B + "\u2510");
    console.log("  \u2502 " + BD + "New version available: v" + remoteVersion + R);
    console.log("  \u2502 " + GY + "(current: v" + LOCAL_VERSION + ")" + R);
    console.log("  \u251c" + B + "\u2524");
    console.log("  \u2502 " + GY + "To update:" + R);
    console.log("  \u2502 " + GY + "1. Stop this server" + R);
    console.log("  \u2502 " + GY + "2. npm install -g hourshare@latest" + R);
    console.log("  \u2502 " + GY + "3. hourshare" + R);
    console.log("  \u2514" + B + "\u2518");
    console.log("");

    const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, "");
    const labels = updateMenu.map((m) => (typeof m.label === "function" ? m.label() : m.label));
    const labelW = Math.max(...labels.map((l) => strip(l).length));

    updateMenu.forEach((item, i) => {
      const star = i === selected ? P + "\u2605" + R : GY + "\u2606" + R;
      const plain = strip(labels[i]);
      console.log(" " + star + " " + labels[i] + " ".repeat(Math.max(0, labelW - plain.length)));
    });
    console.log(GY + "  \u2191\u2193 navigate \u00b7 Enter select \u00b7 Esc/Ctrl+C exit" + R);
  }

  readline.emitKeypressEvents(stdin);
  if (stdin.isTTY) stdin.setRawMode(true);
  stdin.resume();
  render();

  const onKey = (str, key) => {
    if (key.name === "up") { selected = (selected - 1 + updateMenu.length) % updateMenu.length; render(); }
    else if (key.name === "down") { selected = (selected + 1) % updateMenu.length; render(); }
    else if (key.name === "return") {
      stdin.removeListener("keypress", onKey);
      if (stdin.isTTY) stdin.setRawMode(false);
      stdin.pause();
      updateMenu[selected].action();
    } else if (key.name === "escape" || (key.name === "c" && key.ctrl)) {
      stdin.removeListener("keypress", onKey);
      if (stdin.isTTY) stdin.setRawMode(false);
      stdin.pause();
      process.exit(0);
    }
  };
  stdin.on("keypress", onKey);
}

// ---- keyboard menu ----
const MENU = [
  {
    label: "Start (Open in Browser)",
    action() {
      startServer();
      openBrowser(`http://localhost:${PORT}`);
    },
  },
  {
    label: () => "Auto Start (" + (autoStartEnabled() ? D + "Disable" + R : G + "Enable" + R) + ")",
    action() {
      applyAutoStart();
      return waitKey().then(() => showMenu());
    },
  },
  {
    label: () => "Check Update (" + GY + "Internet Require" + R + ")",
    action() {
      const remote = checkUpdate();
      if (remote === null) {
        console.log(D + "  Couldn't check (offline or npm error)." + R);
        console.log(GY + "  Press any key…" + R);
        return waitKey().then(() => showMenu());
      }
      if (remote === LOCAL_VERSION) {
        console.log(G + "  You're on the latest version (v" + LOCAL_VERSION + ")." + R);
        console.log(GY + "  Press any key…" + R);
        return waitKey().then(() => showMenu());
      }
      showUpdateScreen(remote);
    },
  },
  {
    label: "Stop",
    action() {
      stopServer();
    },
  },
  {
    label: "Exit",
    action() {
      process.exit(0);
    },
  },
];

function render(selected) {
  console.clear();
  const status = isRunning()
    ? G + "● Running" + R
    : D + "○ Stopped" + R;

  console.log(P + "=".repeat(40) + R);
  console.log(`  ${BD}Hour Share${R} ${GY}(v${LOCAL_VERSION})${R}`);
  console.log(`  ${P}🚀${R} Server: ${BD}http://localhost:${PORT}${R}`);
  console.log(P + "=".repeat(40) + R);

  const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, "");
  const labels = MENU.map((m) => (typeof m.label === "function" ? m.label() : m.label));
  const labelW = Math.max(...labels.map((l) => strip(l).length));

  MENU.forEach((item, i) => {
    const star = i === selected ? P + "★" + R : GY + "☆" + R;
    const plain = strip(labels[i]);
    const line = ` ${star} ${labels[i]}${" ".repeat(Math.max(0, labelW - plain.length))}`;
    if (i === 0) {
      console.log(line + "   " + status);
    } else {
      console.log(line);
    }
  });
  console.log(GY + "  ↑↓ navigate · Enter select · Esc/Ctrl+C exit" + R);
}

function showMenu() {
  let selected = 0;
  const stdin = process.stdin;

  readline.emitKeypressEvents(stdin);
  if (stdin.isTTY) stdin.setRawMode(true);
  stdin.resume();

  render(selected);

  const onKey = (str, key) => {
    if (key.name === "up") {
      selected = (selected - 1 + MENU.length) % MENU.length;
      render(selected);
    } else if (key.name === "down") {
      selected = (selected + 1) % MENU.length;
      render(selected);
    } else if (key.name === "return") {
      stdin.removeListener("keypress", onKey);
      if (stdin.isTTY) stdin.setRawMode(false);
      stdin.pause();
      const result = MENU[selected].action();
      if (result && typeof result.then === "function") {
        result.catch(() => process.exit(1));
      }
    } else if (key.name === "escape" || (key.name === "c" && key.ctrl)) {
      stdin.removeListener("keypress", onKey);
      if (stdin.isTTY) stdin.setRawMode(false);
      stdin.pause();
      process.exit(0);
    }
  };

  stdin.on("keypress", onKey);
}

// ---- main ----
async function main() {
  parseArgs();
  ensureDataDir();
  if (checkDeps()) {
    fs.writeFileSync(INIT_DONE, "1");
  }
  if (daemonMode) {
    await init();
    startServer();
    process.exit(0);
  }
  await init();
  showMenu();
}

main();
