import type { Ref } from "react";
import { AssistantAvatar } from "../../components/kiosk/KioskAnimations";
import { CameraPreview } from "../../components/kiosk/CameraPreview";
import type { CameraStatus } from "../../types/kiosk";

export default function KioskIdleScreen({ videoRef, cameraStatus, cameraError }: {
  videoRef: Ref<HTMLVideoElement>; cameraStatus: CameraStatus; cameraError?: string | null;
}) {
  return <div className="kiosk-center idle-screen production-idle">
    <div className="idle-camera" aria-hidden="true"><CameraPreview videoRef={videoRef} status={cameraStatus} error={cameraError} showFrameOverlay={false}/></div>
    <AssistantAvatar mood="idle"/>
    <span className="kiosk-kicker">TRỢ LÝ THƯ VIỆN ĐANG SẴN SÀNG</span>
    <h1>Xin chào</h1>
    <p className="idle-primary-copy">Vui lòng đứng trước kiosk.</p>
    <p className="idle-secondary-copy">Hệ thống sẽ tự động nhận diện.</p>
    <div className="presence-pulse" aria-label="Đang chờ người dùng"><i/><span>Đang chờ bạn</span></div>
  </div>;
}
