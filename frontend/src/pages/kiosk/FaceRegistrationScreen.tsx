import { useState, type FormEvent, type Ref } from "react";
import { CameraPreview } from "../../components/kiosk/CameraPreview";
import type { CameraStatus, FaceRegistrationFields } from "../../types/kiosk";

export default function FaceRegistrationScreen({ videoRef, cameraStatus, cameraError, busy, captureFrame, onEnroll, onRetry, onGuest }: {
  videoRef: Ref<HTMLVideoElement>; cameraStatus: CameraStatus; cameraError?: string | null; busy: boolean;
  captureFrame: () => Promise<Blob>; onEnroll: (fields: FaceRegistrationFields, image: Blob) => Promise<unknown>;
  onRetry: () => void; onGuest: () => void;
}) {
  const [fields, setFields] = useState<FaceRegistrationFields>({ full_name: "" });
  const [error, setError] = useState("");
  const update = (name: keyof FaceRegistrationFields, value: string) => setFields((current) => ({
    ...current, [name]: name === "admission_year" ? (value ? Number(value) : undefined) : value,
  }));
  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const image = await captureFrame();
      await onEnroll(fields, image);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể đăng ký khuôn mặt.");
    }
  }
  return <div className="face-registration">
    <div className="registration-camera"><CameraPreview videoRef={videoRef} status={cameraStatus} error={cameraError} showFrameOverlay/></div>
    <form onSubmit={submit}>
      <span className="kiosk-kicker">ĐĂNG KÝ KHUÔN MẶT</span><h1>Tạo hồ sơ nhận diện</h1>
      <p>Ảnh chỉ được dùng để tạo mẫu khuôn mặt phát triển. Vui lòng đứng một mình trong khung hình.</p>
      <div className="registration-grid">
        <label>Họ và tên *<input required value={fields.full_name} onChange={(event) => update("full_name", event.target.value)}/></label>
        <label>Mã số sinh viên<input value={fields.student_code ?? ""} onChange={(event) => update("student_code", event.target.value)}/></label>
        <label>Email<input type="email" value={fields.email ?? ""} onChange={(event) => update("email", event.target.value)}/></label>
        <label>Số điện thoại<input value={fields.phone ?? ""} onChange={(event) => update("phone", event.target.value)}/></label>
        <label>Khoa<input value={fields.faculty ?? ""} onChange={(event) => update("faculty", event.target.value)}/></label>
        <label>Ngành<input value={fields.major ?? ""} onChange={(event) => update("major", event.target.value)}/></label>
        <label>Khóa tuyển sinh<input type="number" min="1990" max="2100" value={fields.admission_year ?? ""} onChange={(event) => update("admission_year", event.target.value)}/></label>
      </div>
      {error && <div className="registration-error">{error}</div>}
      <div className="registration-actions">
        <button disabled={busy || cameraStatus !== "READY"}>{busy ? "Đang đăng ký…" : "Chụp và đăng ký"}</button>
        <button type="button" className="kiosk-ghost" onClick={onRetry}>Quay lại quét lại</button>
        <button type="button" className="kiosk-ghost" onClick={onGuest}>Tiếp tục với tư cách khách</button>
      </div>
    </form>
  </div>;
}
