import type { KioskUser } from "../../types/kiosk";
export default function WelcomeScreen({ user, onContinue }: { user: KioskUser | null; onContinue: () => void }) {
  return <div className="kiosk-center"><div className="state-symbol success">✓</div>
    <span className="kiosk-kicker">{user ? "NHẬN DIỆN THÀNH CÔNG" : "CHẾ ĐỘ KHÁCH"}</span>
    <h1>Xin chào, {user?.full_name ?? "bạn"}!</h1>
    <p>{user ? "Rất vui được gặp lại bạn tại Thư viện Đại học Nông Lâm." : "Tôi là trợ lý AI thư viện. Bạn cần hỗ trợ gì hôm nay?"}</p>
    {user && <div className="student-card"><div className="student-avatar">{user.full_name.split(" ").at(-1)?.[0]}</div>
      <div><strong>{user.full_name}</strong><span>Mã số sinh viên: {user.student_code}</span></div><dl>
        <div><dt>Khoa</dt><dd>{user.faculty || "Chưa cập nhật"}</dd></div>
        <div><dt>Ngành</dt><dd>{user.major || "Chưa cập nhật"}</dd></div>
        <div><dt>Khóa tuyển sinh</dt><dd>{user.admission_year ?? "Chưa cập nhật"}</dd></div>
        <div><dt>Sinh viên năm</dt><dd>{user.student_year ?? "Chưa cập nhật"}</dd></div>
      </dl></div>}
    <button className="kiosk-primary" onClick={onContinue}>Tiếp tục →</button>
    <small>Tự động chuyển sang trò chuyện sau vài giây</small>
  </div>;
}
