import type { ReactElement } from "react";

import AIChatPanel from "../components/AIChatPanel/AIChatPanel";
import BasicDashboardPage from "../components/BasicDashboardPage/BasicDashboardPage";
import BookSuggestionPanel from "../components/BookSuggestionPanel/BookSuggestionPanel";
import FaceRecognitionPanel from "../components/FaceRecognitionPanel/FaceRecognitionPanel";
import KioskHome from "../components/KioskHome/KioskHome";
import KnowledgeUploadPage from "../components/KnowledgeUploadPage/KnowledgeUploadPage";
import SurveyForm from "../components/SurveyForm/SurveyForm";

type AppRoute = { path: string; element: ReactElement };

export const appRoutes: AppRoute[] = [
  { path: "/kiosk", element: <KioskHome /> },
  { path: "/kiosk/face", element: <FaceRecognitionPanel /> },
  { path: "/kiosk/chat", element: <AIChatPanel /> },
  { path: "/kiosk/books", element: <BookSuggestionPanel /> },
  { path: "/kiosk/survey", element: <SurveyForm /> },
  { path: "/admin/knowledge", element: <KnowledgeUploadPage /> },
  { path: "/admin/dashboard", element: <BasicDashboardPage /> },
];
