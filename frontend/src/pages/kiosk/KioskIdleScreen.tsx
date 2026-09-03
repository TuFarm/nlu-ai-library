export default function KioskIdleScreen({ onStart, busy = false }: { onStart: () => void; busy?: boolean }) {
  return <div className="kiosk-center idle-screen">
    <div className="orb"><span>✦</span><i/><i/><i/></div>
    <span className="kiosk-kicker">TRỢ LÝ THƯ VIỆN LUÔN SẴN SÀNG</span>
    <h1>Vui lòng đứng trước kiosk<br/>để bắt đầu</h1>
    <p>Camera chỉ được mở sau khi bạn bắt đầu phiên.</p>
    <button className="kiosk-primary" onClick={onStart} disabled={busy}>◎ {busy ? "Đang bắt đầu…" : "Bắt đầu phiên thử nghiệm"}</button>
    <small>Bạn có thể tiếp tục với tư cách khách nếu không muốn dùng FaceID.</small>
  </div>;
}
