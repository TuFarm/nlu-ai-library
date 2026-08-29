import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("kiosk", {
  getAppVersion: () => ipcRenderer.invoke("kiosk:get-app-version"),
});

