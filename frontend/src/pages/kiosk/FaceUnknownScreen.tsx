export default function FaceUnknownScreen({ onRegister, onRetry, onGuest, onSimulateSuccess, error }: {
  onRegister: () => void; onRetry: () => void; onGuest: () => void; onSimulateSuccess?: () => void; error?: string | null;
}) {
  return <div className="kiosk-center unknown-face-screen">
    <AssistantAvatar mood="greeting" label="Trợ lý chào khách mới"/><span className="kiosk-kicker">RẤT VUI ĐƯỢC GẶP BẠN</span>
    <h1>Xin chào!</h1>
    <p>{error ?? "Chúng tôi chưa tìm thấy dữ liệu khuôn mặt của bạn."}</p>
    <div className="kiosk-actions vertical">
      <button onClick={onRegister}>Đăng ký khuôn mặt</button>
      <button className="kiosk-secondary" onClick={onRetry}>Thử lại</button>
      <button className="kiosk-ghost" onClick={onGuest}>Tiếp tục với tư cách khách</button>
      {onSimulateSuccess && <button className="kiosk-dev-action" onClick={onSimulateSuccess}>DEV · Mô phỏng nhận diện</button>}
    </div>
  </div>;
}
import { AssistantAvatar } from "../../components/kiosk/KioskAnimations";
