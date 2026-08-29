import { app, BrowserWindow, ipcMain, session } from "electron";
import isDev from "electron-is-dev";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const devServerUrl = process.env.ELECTRON_RENDERER_URL ?? "http://localhost:5173";

// Electron currently reports camera/microphone requests as "media". The
// additional names retain compatibility with platform and Electron variations.
const kioskPermissions = new Set([
  "media",
  "camera",
  "microphone",
  "audioCapture",
  "videoCapture",
]);

function configureKioskPermissions() {
  session.defaultSession.setPermissionRequestHandler(
    (_webContents, permission, callback) => callback(kioskPermissions.has(permission)),
  );
}

async function createWindow() {
  const window = new BrowserWindow({
    kiosk: true,
    fullscreen: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  if (isDev) {
    await window.loadURL(devServerUrl);
  } else {
    await window.loadFile(path.join(__dirname, "../dist/index.html"));
  }
}

app.whenReady().then(async () => {
  configureKioskPermissions();
  ipcMain.handle("kiosk:get-app-version", () => app.getVersion());
  await createWindow();

  app.on("activate", async () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      await createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

