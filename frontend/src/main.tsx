import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, MemoryRouter } from "react-router-dom";

import App from "./App";
import "./styles/global.css";

const isElectron = "kiosk" in window;
const Router = isElectron ? MemoryRouter : BrowserRouter;

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router {...(isElectron ? { initialEntries: ["/kiosk/fullscreen"] } : {})}>
      <App />
    </Router>
  </StrictMode>,
);
