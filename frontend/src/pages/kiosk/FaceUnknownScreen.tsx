export default function FaceUnknownScreen({ onRetry, onGuest, onSimulateSuccess, error }: {
  onRetry: () => void; onGuest: () => void; onSimulateSuccess?: () => void; error?: string | null;
}) {
  return <div className="kiosk-center">
    <div className="state-symbol amber">?</div><span className="kiosk-kicker">CHƯA XÁC ĐỊNH DANH TÍNH</span>
    <h1>Không nhận diện được người dùng.</h1>
    <p>{error ?? "Bạn có thể thử lại hoặc tiếp tục với tư cách khách. Tất cả tính năng hỏi đáp vẫn sẵn sàng."}</p>
    <div className="kiosk-actions vertical">
      <button onClick={onRetry}>↻ Thử lại</button>
      <button className="kiosk-secondary" onClick={onGuest}>Tiếp tục với tư cách khách →</button>
      <button className="kiosk-ghost" disabled>Đăng ký khuôn mặt · Đang phát triển</button>
      {onSimulateSuccess && <button className="kiosk-dev-action" onClick={onSimulateSuccess}>DEV · Mô phỏng nhận diện</button>}
    </div>
  </div>;
}
