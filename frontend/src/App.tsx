import { Navigate, Route, Routes } from "react-router-dom";

import { appRoutes } from "./routes";

export default function App() {
  return (
    <Routes>
      {appRoutes.map(({ path, element }) => (
        <Route key={path} path={path} element={element} />
      ))}
      <Route path="*" element={<Navigate to="/kiosk" replace />} />
    </Routes>
  );
}

