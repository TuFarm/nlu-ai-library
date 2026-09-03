import { useCallback, useEffect, useRef, useState } from "react";
import { apiClient } from "../services/apiClient";
import type { KioskConversation, KioskSession, KioskState, KioskUser } from "../types/kiosk";

const MOCK_USER: KioskUser = { id: "mock-user", student_code: "ITCSIU24092", full_name: "Phạm Hoàng Tuấn Tú", faculty: "Khoa Công nghệ Thông tin", major: "Công nghệ thông tin", admission_year: 2024, student_year: 3 };

export function useKioskFlow(timeoutSeconds = Number(import.meta.env.VITE_KIOSK_TIMEOUT_SECONDS ?? 120)) {
  const [currentState, setCurrentState] = useState<KioskState>("IDLE");
  const [currentUser, setCurrentUser] = useState<KioskUser | null>(null);
  const [currentSession, setCurrentSession] = useState<KioskSession | null>(null);
  const [currentConversation, setCurrentConversation] = useState<KioskConversation | null>(null);
  const timer = useRef<number | undefined>(undefined);

  const resetToIdle = useCallback(async () => {
    if (currentSession) { try { await apiClient.post(`/kiosk/sessions/${currentSession.session_id}/end`, {}); } catch { /* Offline mock cleanup. */ } }
    setCurrentState("IDLE"); setCurrentUser(null); setCurrentSession(null); setCurrentConversation(null);
  }, [currentSession]);
  const transitionTo = useCallback((next: KioskState) => setCurrentState(next), []);
  const refreshTimeout = useCallback(() => { window.clearTimeout(timer.current); if (currentState !== "IDLE") timer.current = window.setTimeout(resetToIdle, timeoutSeconds * 1000); }, [currentState, resetToIdle, timeoutSeconds]);

  useEffect(() => { refreshTimeout(); const events = ["pointerdown", "keydown"] as const; events.forEach(e => window.addEventListener(e, refreshTimeout)); return () => { window.clearTimeout(timer.current); events.forEach(e => window.removeEventListener(e, refreshTimeout)); }; }, [refreshTimeout]);
  useEffect(() => { if (currentState === "PRESENCE_DETECTED") { const id = window.setTimeout(() => setCurrentState("FACE_SCANNING"), 850); return () => window.clearTimeout(id); } if (currentState === "FACE_RECOGNIZED") { const id = window.setTimeout(() => setCurrentState("WELCOME"), 650); return () => window.clearTimeout(id); } if (currentState === "THANK_YOU") { const id = window.setTimeout(resetToIdle, 7000); return () => window.clearTimeout(id); } }, [currentState, resetToIdle]);

  async function startMockPresence() { setCurrentState("PRESENCE_DETECTED"); try { setCurrentSession(await apiClient.post<KioskSession>("/kiosk/sessions/start", {})); } catch { setCurrentSession({ session_id: crypto.randomUUID(), status: "active" }); } }
  async function handleMockFaceSuccess() { try { const r = await apiClient.post<{ user: KioskUser }>("/face/verify/mock", { scenario: "SUCCESS" }); setCurrentUser(r.user); } catch { setCurrentUser(MOCK_USER); } setCurrentState("FACE_RECOGNIZED"); }
  function handleMockFaceUnknown() { setCurrentUser(null); setCurrentState("FACE_UNKNOWN"); }
  async function startChat() { if (!currentConversation) { try { setCurrentConversation(await apiClient.post<KioskConversation>("/conversations/start", { session_id: currentSession?.session_id })); } catch { setCurrentConversation({ conversation_id: crypto.randomUUID(), status: "active" }); } } setCurrentState("AI_CHAT"); }
  const startSurvey = () => setCurrentState("SURVEY");
  const completeSurvey = () => setCurrentState("THANK_YOU");
  return { currentState, currentUser, currentSession, currentConversation, transitionTo, resetToIdle, startMockPresence, handleMockFaceSuccess, handleMockFaceUnknown, startChat, startSurvey, completeSurvey };
}
