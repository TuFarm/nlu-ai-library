export type KioskState = "IDLE" | "PRESENCE_DETECTED" | "FACE_SCANNING" | "FACE_RECOGNIZED" | "FACE_UNKNOWN" | "WELCOME" | "AI_CHAT" | "BOOK_SUGGESTION" | "SURVEY" | "THANK_YOU" | "ERROR";
export type KioskUser = { id: string; student_code: string; full_name: string; faculty: string; major: string; admission_year: number; student_year: number };
export type KioskSession = { session_id: string; status: string };
export type KioskConversation = { conversation_id: string; status: string };
