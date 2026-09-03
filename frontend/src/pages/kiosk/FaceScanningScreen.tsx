import { useEffect, useRef, type Ref } from "react";
import { CameraPreview } from "../../components/kiosk/CameraPreview";
import type { CameraStatus } from "../../types/kiosk";

export default function FaceScanningScreen({ videoRef, cameraStatus, cameraError, busy, onScan }: {
  videoRef: Ref<HTMLVideoElement>; cameraStatus: CameraStatus; cameraError?: string | null; busy: boolean; onScan: () => void;
}) {
  const started = useRef(false);
  useEffect(() => {
    if (cameraStatus !== "READY" || started.current) return;
    started.current = true;
    const id = window.setTimeout(onScan, 1200);
    return () => window.clearTimeout(id);
  }, [cameraStatus, onScan]);
  return <div className="kiosk-center scanning-screen">
    <CameraPreview videoRef={videoRef} status={cameraStatus} error={cameraError} showFrameOverlay/>
    <span className="kiosk-kicker pulse-text">● {busy ? "ĐANG XÁC MINH" : "ĐANG QUÉT"}</span>
    <h1>{busy ? "Đang gửi ảnh để nhận diện…" : "Đang nhận diện khuôn mặt…"}</h1>
    <p>Vui lòng nhìn thẳng vào màn hình và giữ yên trong giây lát.</p>
    {!busy && <button onClick={onScan}>Quét lại ngay</button>}
  </div>;
}
