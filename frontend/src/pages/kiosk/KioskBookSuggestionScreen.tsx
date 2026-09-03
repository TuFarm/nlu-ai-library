import { useEffect, useState } from "react";
import { bookSuggestionApi, MOCK_FALLBACK_ENABLED } from "../../services/apiClient";
import type { BookCategory, SuggestedBook } from "../../types/kiosk";

const fallbackCategories: BookCategory[] = [
  { id: "it", category_name: "Công nghệ thông tin" }, { id: "agriculture", category_name: "Nông nghiệp" },
  { id: "economics", category_name: "Kinh tế" }, { id: "language", category_name: "Ngoại ngữ" },
];
const fallbackBooks: Record<string, SuggestedBook[]> = {
  it: [{ id: "mock-it", category_id: "it", external_book_id: "NLU-IT-001", title: "Nhập môn trí tuệ nhân tạo", author_name: "Nguyễn Văn A", short_description: "Tài liệu nhập môn về các khái niệm AI." }],
  agriculture: [{ id: "mock-ag", category_id: "agriculture", external_book_id: "NLU-AG-014", title: "Nông nghiệp thông minh", author_name: "Trần Thị B", short_description: "Ứng dụng công nghệ trong nông nghiệp." }],
};

export default function KioskBookSuggestionScreen({ onBack, onSurvey }: { onBack: () => void; onSurvey: () => void }) {
  const [categories, setCategories] = useState<BookCategory[]>([]);
  const [categoryId, setCategoryId] = useState<string>();
  const [books, setBooks] = useState<SuggestedBook[]>([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    let active = true;
    bookSuggestionApi.getCategories().then((rows) => {
      if (!active) return;
      setCategories(rows); setCategoryId(rows[0]?.id);
      if (!rows.length) setNotice("Hiện chưa có chủ đề sách trong hệ thống.");
    }).catch(() => {
      if (!active) return;
      if (MOCK_FALLBACK_ENABLED) { setCategories(fallbackCategories); setCategoryId(fallbackCategories[0].id); setNotice("Đang hiển thị dữ liệu gợi ý thử nghiệm."); }
      else setNotice("Không thể tải chủ đề sách từ máy chủ.");
    }).finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!categoryId) { setBooks([]); return; }
    setLoading(true);
    bookSuggestionApi.getSuggestedBooks(categoryId).then(setBooks).catch(() => {
      if (MOCK_FALLBACK_ENABLED) setBooks(fallbackBooks[categoryId] ?? []);
      else setNotice("Không thể tải sách gợi ý từ máy chủ.");
    }).finally(() => setLoading(false));
  }, [categoryId]);

  return <div className="kiosk-books">
    <div className="kiosk-section-heading"><div><span className="kiosk-kicker">GỢI Ý ĐƠN GIẢN THEO CHỦ ĐỀ</span><h1>Khám phá cuốn sách tiếp theo</h1></div>
      <button className="kiosk-ghost" onClick={onBack}>← Quay lại trò chuyện</button></div>
    <div className="kiosk-category-list">{categories.map((category) =>
      <button className={category.id === categoryId ? "active" : ""} onClick={() => setCategoryId(category.id)} key={category.id}>{category.category_name}</button>)}</div>
    {loading ? <div className="kiosk-empty">Đang tải gợi ý sách…</div> : books.length ? <div className="kiosk-book-grid">{books.map((book) =>
      <article key={book.id}><div className="kiosk-book-cover">NLU<small>LIBRARY</small></div>
        <span>Sách gợi ý</span><h2>{book.title}</h2><p>{book.author_name}</p>
        {book.short_description && <p>{book.short_description}</p>}
        {book.external_book_id && <small>Mã nguồn: {book.external_book_id}</small>}</article>)}</div>
      : <div className="kiosk-empty">Chưa có sách gợi ý cho chủ đề này.</div>}
    <div className="kiosk-bottom-actions"><p>{notice || "Gợi ý theo chủ đề, không hiển thị mượn/trả hay tình trạng bản sách."}</p>
      <button onClick={onSurvey}>Tiếp tục khảo sát →</button></div>
  </div>;
}
