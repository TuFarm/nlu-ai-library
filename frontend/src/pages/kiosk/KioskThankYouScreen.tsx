import { AssistantAvatar } from "../../components/kiosk/KioskAnimations";

export default function KioskThankYouScreen({ onHome }: { onHome: () => void }) {
  return <div className="kiosk-center thank-you-runtime" onDoubleClick={onHome}>
    <AssistantAvatar mood="goodbye" label="Trợ lý vẫy tay tạm biệt"/>
    <span className="kiosk-kicker">PHIÊN ĐÃ HOÀN TẤT</span>
    <h1>Cảm ơn bạn.</h1>
    <p>Chúc bạn một ngày học tập thật hiệu quả!</p>
    <small>Tự động trở về màn hình chờ</small>
  </div>;
}
