import { useCallback, useEffect, useReducer, useRef } from "react";
import { aiApi, conversationApi, faceApi, kioskApi, MOCK_FALLBACK_ENABLED, voiceApi } from "../services/apiClient";
import type { CameraStatus, FaceVerifyResult, KioskAction, KioskConversation, KioskFlowState, KioskMessage, KioskState, MessageInputMethod, MicStatus } from "../types/kiosk";

const DEVICE_CODE = String(import.meta.env.VITE_KIOSK_DEVICE_CODE ?? "KIOSK_DEV_01");
const FALLBACK_ANSWER = "Máy chủ đang tạm thời không phản hồi. Đây là chế độ thử nghiệm ngoại tuyến; vui lòng khởi động backend để nhận câu trả lời từ hệ thống.";
const MOCK_USER = {
  id: "00000000-0000-4000-8000-000000000001", student_code: "ITCSIU24092", full_name: "Phạm Hoàng Tuấn Tú",
  faculty: "Khoa Công nghệ Thông tin", major: "Công nghệ thông tin", admission_year: 2024, student_year: 3,
};

function initialState(): KioskFlowState {
  return {
    currentState: "IDLE", session: null, device: { code: DEVICE_CODE }, user: null, conversation: null,
    cameraStatus: "IDLE", micStatus: "IDLE", lastFaceResult: null, messages: [], currentTranscript: "",
    lastAiResponse: null, selectedBookCategory: null, suggestedBooks: [], survey: null, error: null,
    lastActivityAt: Date.now(), isProcessing: false, mockFallbackActive: false,
  };
}

function reducer(state: KioskFlowState, action: KioskAction): KioskFlowState {
  const active = { lastActivityAt: Date.now() };
  switch (action.type) {
    case "START_SESSION": return { ...initialState(), session: action.session, device: { code: DEVICE_CODE, id: action.session.device_id }, currentState: "CAMERA_PERMISSION", ...active };
    case "CAMERA_PERMISSION_GRANTED": return { ...state, cameraStatus: "READY", currentState: "CAMERA_READY", error: null, ...active };
    case "CAMERA_PERMISSION_DENIED": return { ...state, cameraStatus: "DENIED", currentState: "CAMERA_PERMISSION", error: action.error ?? null, ...active };
    case "START_FACE_SCAN": return { ...state, currentState: "FACE_SCANNING", error: null, ...active };
    case "FACE_VERIFY_SUCCESS": return { ...state, lastFaceResult: action.result, user: action.result.user, currentState: "FACE_RECOGNIZED", isProcessing: false, ...active };
    case "FACE_VERIFY_UNKNOWN": return { ...state, lastFaceResult: action.result, user: null, currentState: "FACE_UNKNOWN", isProcessing: false, ...active };
    case "FACE_VERIFY_FAILED": return { ...state, error: action.error, currentState: "FACE_UNKNOWN", isProcessing: false, ...active };
    case "CONTINUE_AS_GUEST": return { ...state, user: null, currentState: "WELCOME", error: null, ...active };
    case "START_CONVERSATION": {
      const greeting: KioskMessage = { id: crypto.randomUUID(), role: "assistant", text: state.user
        ? `Xin chào ${state.user.full_name}! Hôm nay tôi có thể giúp gì cho bạn?`
        : "Xin chào bạn, tôi là trợ lý AI thư viện. Bạn cần hỗ trợ gì hôm nay?" };
      return { ...state, conversation: action.conversation, currentState: "AI_CHAT", messages: state.messages.length ? state.messages : [greeting], isProcessing: false, ...active };
    }
    case "USER_MESSAGE_SUBMITTED": return { ...state, messages: [...state.messages, action.message], currentTranscript: action.message.text, isProcessing: true, ...active };
    case "AI_RESPONSE_RECEIVED": return { ...state, messages: [...state.messages, action.message], lastAiResponse: action.message.text, isProcessing: false, mockFallbackActive: state.mockFallbackActive || Boolean(action.mockFallback), ...active };
    case "OPEN_BOOK_SUGGESTIONS": return { ...state, currentState: "BOOK_SUGGESTION", ...active };
    case "OPEN_SURVEY": return { ...state, currentState: "SURVEY", ...active };
    case "SURVEY_SUBMITTED": return { ...state, currentState: "THANK_YOU", ...active };
    case "END_SESSION": return { ...state, isProcessing: false };
    case "RESET_TO_IDLE": return initialState();
    case "SET_ERROR": return { ...state, error: action.error, currentState: "ERROR", isProcessing: false, ...active };
    case "SET_CAMERA_STATUS": return { ...state, cameraStatus: action.status, ...active };
    case "SET_MIC_STATUS": return { ...state, micStatus: action.status, ...active };
    case "SET_TRANSCRIPT": return { ...state, currentTranscript: action.transcript, ...active };
    case "SET_BOOK_DATA": return { ...state, selectedBookCategory: action.categoryId, suggestedBooks: action.books, ...active };
    case "SET_SURVEY": return { ...state, survey: action.survey, ...active };
    case "SET_PROCESSING": return { ...state, isProcessing: action.value, ...active };
    case "TOUCH": return { ...state, ...active };
    case "TRANSITION": return { ...state, currentState: action.state, error: null, ...active };
  }
}

export function useKioskFlow(timeoutSeconds = Number(import.meta.env.VITE_KIOSK_IDLE_TIMEOUT_SECONDS ?? 60)) {
  const [state, dispatch] = useReducer(reducer, undefined, initialState);
  const stateRef = useRef(state);
  const endedSessionRef = useRef<string | null>(null);
  stateRef.current = state;

  const endCurrentSession = useCallback(async (exitReason: string) => {
    const sessionId = stateRef.current.session?.session_id;
    if (!sessionId || endedSessionRef.current === sessionId) return;
    endedSessionRef.current = sessionId;
    try { await kioskApi.endSession(sessionId, exitReason); } catch { /* reset locally even if the backend is unavailable */ }
    dispatch({ type: "END_SESSION" });
  }, []);

  const resetToIdle = useCallback(async (exitReason = "USER_EXIT") => {
    await endCurrentSession(exitReason);
    dispatch({ type: "RESET_TO_IDLE" });
  }, [endCurrentSession]);

  const startSession = useCallback(async () => {
    endedSessionRef.current = null;
    dispatch({ type: "SET_PROCESSING", value: true });
    try {
      const session = await kioskApi.startSession(DEVICE_CODE);
      dispatch({ type: "START_SESSION", session });
    } catch (reason) {
      if (!MOCK_FALLBACK_ENABLED) {
        dispatch({ type: "SET_ERROR", error: reason instanceof Error ? reason.message : "Không thể bắt đầu phiên kiosk." });
        return false;
      }
      dispatch({ type: "START_SESSION", session: { session_id: crypto.randomUUID(), device_id: "mock-device", status: "active" } });
    }
    return true;
  }, []);

  const cameraGranted = useCallback(() => dispatch({ type: "CAMERA_PERMISSION_GRANTED" }), []);
  const cameraDenied = useCallback((error?: string) => dispatch({ type: "CAMERA_PERMISSION_DENIED", error }), []);
  const setCameraStatus = useCallback((status: CameraStatus) => dispatch({ type: "SET_CAMERA_STATUS", status }), []);
  const startFaceScan = useCallback(() => dispatch({ type: "START_FACE_SCAN" }), []);

  const verifyFace = useCallback(async (imageBlob: Blob) => {
    dispatch({ type: "SET_PROCESSING", value: true });
    try {
      const current = stateRef.current;
      const result = await faceApi.verifyFace({ sessionId: current.session?.session_id, deviceCode: current.device.code, imageBlob });
      dispatch({ type: result.next_state === "WELCOME" && result.user ? "FACE_VERIFY_SUCCESS" : "FACE_VERIFY_UNKNOWN", result });
    } catch (reason) {
      dispatch({ type: "FACE_VERIFY_FAILED", error: reason instanceof Error ? reason.message : "Không thể xác minh khuôn mặt." });
    }
  }, []);

  const simulateFace = useCallback((recognized: boolean) => {
    const result: FaceVerifyResult = recognized
      ? { result: "SUCCESS", user: MOCK_USER, confidence_score: 0.94, next_state: "WELCOME" }
      : { result: "UNKNOWN_FACE", user: null, confidence_score: 0.2, next_state: "FACE_UNKNOWN" };
    dispatch({ type: recognized ? "FACE_VERIFY_SUCCESS" : "FACE_VERIFY_UNKNOWN", result });
  }, []);

  const logEvent = useCallback((event_type: string, content_summary?: string) => {
    const sessionId = stateRef.current.session?.session_id;
    if (sessionId) void kioskApi.logEvent(sessionId, { event_type, content_summary }).catch(() => undefined);
  }, []);
  const continueAsGuest = useCallback(() => {
    logEvent("GUEST_CONTINUED");
    dispatch({ type: "CONTINUE_AS_GUEST" });
  }, [logEvent]);
  const startConversation = useCallback(async (): Promise<KioskConversation | null> => {
    if (stateRef.current.conversation) {
      dispatch({ type: "TRANSITION", state: "AI_CHAT" });
      return stateRef.current.conversation;
    }
    dispatch({ type: "SET_PROCESSING", value: true });
    try {
      const current = stateRef.current;
      const conversation = await conversationApi.startConversation({
        session_id: current.session?.session_id, user_id: current.user?.id,
      });
      dispatch({ type: "START_CONVERSATION", conversation });
      return conversation;
    } catch (reason) {
      if (MOCK_FALLBACK_ENABLED) {
        const conversation = { conversation_id: crypto.randomUUID(), status: "active" };
        dispatch({ type: "START_CONVERSATION", conversation });
        return conversation;
      }
      dispatch({ type: "SET_ERROR", error: reason instanceof Error ? reason.message : "Không thể bắt đầu hội thoại." });
      return null;
    }
  }, []);

  const submitMessage = useCallback(async (text: string, inputMethod: MessageInputMethod = "TEXT", confidence?: number) => {
    const clean = text.trim();
    if (!clean || stateRef.current.isProcessing) return;
    const conversation = stateRef.current.conversation ?? await startConversation();
    if (!conversation) return;
    dispatch({ type: "USER_MESSAGE_SUBMITTED", message: { id: crypto.randomUUID(), role: "user", text: clean, inputMethod } });
    try {
      const current = stateRef.current;
      if (inputMethod === "VOICE") {
        await voiceApi.sendBrowserTranscript({
          session_id: current.session?.session_id, conversation_id: conversation.conversation_id,
          transcript: clean, confidence_score: confidence,
        });
      }
      const result = await aiApi.answer({
        conversation_id: conversation.conversation_id, session_id: current.session?.session_id,
        message_text: clean, save_user_message: inputMethod !== "VOICE",
      });
      dispatch({ type: "AI_RESPONSE_RECEIVED", message: { id: crypto.randomUUID(), role: "assistant", text: result.answer } });
    } catch (reason) {
      if (MOCK_FALLBACK_ENABLED) {
        dispatch({ type: "AI_RESPONSE_RECEIVED", message: { id: crypto.randomUUID(), role: "assistant", text: FALLBACK_ANSWER }, mockFallback: true });
      } else dispatch({ type: "SET_ERROR", error: reason instanceof Error ? reason.message : "Không thể nhận câu trả lời từ AI." });
    }
  }, [startConversation]);

  const setMicStatus = useCallback((status: MicStatus) => dispatch({ type: "SET_MIC_STATUS", status }), []);
  const openBooks = useCallback(() => { logEvent("BOOK_SUGGESTIONS_OPENED"); dispatch({ type: "OPEN_BOOK_SUGGESTIONS" }); }, [logEvent]);
  const openSurvey = useCallback(() => { logEvent("SURVEY_OPENED"); dispatch({ type: "OPEN_SURVEY" }); }, [logEvent]);
  const completeSurvey = useCallback(() => dispatch({ type: "SURVEY_SUBMITTED" }), []);
  const transitionTo = useCallback((next: KioskState) => dispatch({ type: "TRANSITION", state: next }), []);
  const touch = useCallback(() => dispatch({ type: "TOUCH" }), []);

  useEffect(() => {
    if (state.currentState === "CAMERA_READY") {
      const id = window.setTimeout(() => dispatch({ type: "START_FACE_SCAN" }), 650);
      return () => window.clearTimeout(id);
    }
    if (state.currentState === "FACE_RECOGNIZED") {
      const id = window.setTimeout(() => dispatch({ type: "TRANSITION", state: "WELCOME" }), 900);
      return () => window.clearTimeout(id);
    }
    if (state.currentState === "WELCOME") {
      const id = window.setTimeout(() => { void startConversation(); }, 2600);
      return () => window.clearTimeout(id);
    }
    if (state.currentState === "THANK_YOU") {
      const id = window.setTimeout(() => { void resetToIdle("COMPLETED"); }, 5000);
      return () => window.clearTimeout(id);
    }
  }, [state.currentState, resetToIdle, startConversation]);

  useEffect(() => {
    if (state.currentState === "IDLE" || state.isProcessing || state.micStatus === "LISTENING") return;
    const elapsed = Date.now() - state.lastActivityAt;
    const id = window.setTimeout(() => { void resetToIdle("TIMEOUT"); }, Math.max(0, timeoutSeconds * 1000 - elapsed));
    return () => window.clearTimeout(id);
  }, [state.currentState, state.isProcessing, state.lastActivityAt, state.micStatus, timeoutSeconds, resetToIdle]);

  useEffect(() => {
    const onActivity = () => dispatch({ type: "TOUCH" });
    window.addEventListener("pointerdown", onActivity); window.addEventListener("keydown", onActivity);
    return () => { window.removeEventListener("pointerdown", onActivity); window.removeEventListener("keydown", onActivity); };
  }, []);

  return { ...state, dispatch, startSession, cameraGranted, cameraDenied, setCameraStatus, startFaceScan, verifyFace,
    simulateFace, continueAsGuest, startConversation, submitMessage, setMicStatus, openBooks, openSurvey,
    completeSurvey, transitionTo, touch, resetToIdle };
}
