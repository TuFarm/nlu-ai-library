import type { Book, DocumentItem, FaceResult } from "../types";

export const categories = ["Công nghệ thông tin", "Nông nghiệp", "Kinh tế", "Ngoại ngữ", "Kỹ năng mềm"];
export const books: Book[] = [
  { external_book_id: "NLU-IT-001", title: "Nhập môn trí tuệ nhân tạo", author_name: "Nguyễn Văn A", category: categories[0] },
  { external_book_id: "NLU-AG-014", title: "Nông nghiệp thông minh", author_name: "Trần Thị B", category: categories[1] },
  { external_book_id: "NLU-EC-009", title: "Kinh tế học căn bản", author_name: "Lê Văn C", category: categories[2] },
  { external_book_id: "NLU-LA-021", title: "English for University", author_name: "Jane Smith", category: categories[3] },
  { external_book_id: "NLU-SK-003", title: "Kỹ năng học đại học", author_name: "Phạm Minh D", category: categories[4] },
];
export const documents: DocumentItem[] = [
  { id: "1", title: "Nội quy thư viện", source_type: "PDF", status: "processed" },
  { id: "2", title: "Giờ mở cửa thư viện", source_type: "Text", status: "processed" },
  { id: "3", title: "Quy định mượn tài liệu", source_type: "Word", status: "processing" },
  { id: "4", title: "Câu hỏi thường gặp", source_type: "Web Link", status: "failed" },
];
export const mockFace = (success: boolean): FaceResult => success
  ? { result: "SUCCESS", user: { full_name: "Phạm Hoàng Tuấn Tú", student_code: "ITCSIU24092" }, confidence_score: .94, message: "Xin chào, Phạm Hoàng Tuấn Tú!" }
  : { result: "UNKNOWN_FACE", user: null, confidence_score: .32, message: "Không nhận diện được người dùng. Bạn có thể thử lại hoặc tiếp tục ẩn danh." };
export const mockAnswer = "Thư viện thường mở cửa theo khung giờ được quy định trong tài liệu nội bộ. Đây là câu trả lời mô phỏng; khi tích hợp RAG, hệ thống sẽ truy xuất tài liệu để trả lời chính xác hơn.";
