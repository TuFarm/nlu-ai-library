import type { ReactElement } from "react";

import AIInteractionHub from "../components/AIInteractionHub/AIInteractionHub";
import FaceIDScanner from "../components/FaceIDScanner/FaceIDScanner";
import KioskHome from "../components/KioskHome/KioskHome";
import RemoteRegistrationForm from "../components/RemoteRegistrationForm/RemoteRegistrationForm";

type AppRoute = { path: string; element: ReactElement };

export const appRoutes: AppRoute[] = [
  { path: "/register", element: <RemoteRegistrationForm /> },
  { path: "/kiosk", element: <KioskHome /> },
  { path: "/kiosk/face-id", element: <FaceIDScanner /> },
  { path: "/kiosk/hub", element: <AIInteractionHub /> },
];

