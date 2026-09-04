export default function FaceUnknownScreen({ onRegister, onRetry, onGuest, onSimulateSuccess, error }: {
  onRegister: () => void; onRetry: () => void; onGuest: () => void; onSimulateSuccess?: () => void; error?: string | null;
}) {
  return <div className="kiosk-center">
    <div className="state-symbol amber friendly-face">?</div><span className="kiosk-kicker">CHƯA CÓ HỒ SƠ NHẬN DIỆN</span>
    <h1>Bạn chưa có dữ liệu khuôn mặt.</h1>
    <p>{error ?? "Bạn muốn đăng ký khuôn mặt ngay không?"}</p>
    <div className="kiosk-actions vertical">
      <button onClick={onRegister}>Đăng ký ngay</button>
      <button className="kiosk-secondary" onClick={onRetry}>↻ Thử lại</button>
      <button className="kiosk-ghost" onClick={onGuest}>Tiếp tục với tư cách khách →</button>
      {onSimulateSuccess && <button className="kiosk-dev-action" onClick={onSimulateSuccess}>DEV · Mô phỏng nhận diện</button>}
    </div>
  </div>;
}
