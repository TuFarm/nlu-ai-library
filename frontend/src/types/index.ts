export type FaceResult = { result: string; user: { full_name: string; student_code: string } | null; confidence_score: number; message: string };
export type Book = { external_book_id: string | null; title: string; author_name: string; category: string };
export type DocumentItem = { id: string; title: string; source_type: string; status: "processed" | "processing" | "failed" };
export type Metric = { label: string; value: string; detail: string; icon: string };
export type ChatMessage = { role: "user" | "assistant"; text: string };
