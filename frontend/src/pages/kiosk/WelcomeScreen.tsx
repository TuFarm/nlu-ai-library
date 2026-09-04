import { useEffect, useRef } from "react";
import { useTextToSpeech } from "../../hooks/useTextToSpeech";
import type { KioskUser } from "../../types/kiosk";
export default function WelcomeScreen({ user, onContinue }: { user: KioskUser | null; onContinue: () => void }) {
  const tts = useTextToSpeech();
  const started = useRef(false);
  const speakRef = useRef(tts.speak);
  speakRef.current = tts.speak;
  useEffect(() => {
    if (started.current) return;
    started.current = true;
    void speakRef.current(user ? `Xin chào ${user.full_name}. Rất vui được gặp lại bạn.` : "Xin chào bạn. Rất vui được gặp bạn.");
    return () => { started.current = false; tts.stop(); };
  }, []);
  return <div className="kiosk-center welcome-smile"><div className="welcome-avatar">☺<span>✓</span></div>
    <span className="kiosk-kicker">{user ? "NHẬN DIỆN THÀNH CÔNG" : "CHẾ ĐỘ KHÁCH"}</span>
    <h1>Xin chào, {user?.full_name ?? "bạn"}!</h1>
    <p>{user ? "Rất vui được gặp lại bạn tại Thư viện Đại học Nông Lâm." : "Tôi là trợ lý AI thư viện. Bạn cần hỗ trợ gì hôm nay?"}</p>
    {user && <div className="student-card"><div className="student-avatar">{user.full_name.split(" ").at(-1)?.[0]}</div>
      <div><strong>{user.full_name}</strong><span>Mã số sinh viên: {user.student_code || "Chưa cập nhật"}</span></div><dl>
        <div><dt>Khoa</dt><dd>{user.faculty || "Chưa cập nhật"}</dd></div>
        <div><dt>Ngành</dt><dd>{user.major || "Chưa cập nhật"}</dd></div>
        <div><dt>Khóa tuyển sinh</dt><dd>{user.admission_year ?? "Chưa cập nhật"}</dd></div>
        <div><dt>Sinh viên năm</dt><dd>{user.student_year ?? "Chưa cập nhật"}</dd></div>
      </dl></div>}
    <button className="kiosk-primary" onClick={onContinue}>Tiếp tục →</button>
    <small>{tts.notice ?? "Tự động chuyển sang trò chuyện giọng nói sau vài giây"}</small>
  </div>;
}
