import { useCallback, useEffect, useRef, useState } from "react";
import type { CameraStatus } from "../types/kiosk";

export function useCamera() {
  const videoElementRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [cameraStatus, setCameraStatus] = useState<CameraStatus>("IDLE");
  const [error, setError] = useState<string | null>(null);

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    if (videoElementRef.current) videoElementRef.current.srcObject = null;
    setCameraStatus("STOPPED");
  }, []);

  const requestCamera = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setError("Trình duyệt này không hỗ trợ truy cập camera.");
      setCameraStatus("ERROR");
      return false;
    }
    setCameraStatus("REQUESTING"); setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = stream;
      if (videoElementRef.current) {
        videoElementRef.current.srcObject = stream;
        await videoElementRef.current.play();
      }
      setCameraStatus("READY");
      return true;
    } catch (reason) {
      const denied = reason instanceof DOMException && (reason.name === "NotAllowedError" || reason.name === "SecurityError");
      setCameraStatus(denied ? "DENIED" : "ERROR");
      setError(denied
        ? "Camera chưa được cấp quyền. Vui lòng cho phép truy cập camera trong trình duyệt."
        : "Không thể mở camera. Vui lòng kiểm tra thiết bị và thử lại.");
      return false;
    }
  }, []);

  const captureFrame = useCallback(async () => {
    const video = videoElementRef.current;
    if (!video || cameraStatus !== "READY" || !video.videoWidth || !video.videoHeight) throw new Error("Camera chưa sẵn sàng để chụp ảnh.");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth; canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    if (!context) throw new Error("Không thể tạo khung ảnh từ camera.");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return new Promise<Blob>((resolve, reject) => canvas.toBlob(
      (blob) => blob ? resolve(blob) : reject(new Error("Không thể mã hóa ảnh camera.")), "image/jpeg", 0.88,
    ));
  }, [cameraStatus]);

  const videoRef = useCallback((video: HTMLVideoElement | null) => {
    videoElementRef.current = video;
    if (video && streamRef.current) {
      video.srcObject = streamRef.current;
      void video.play();
    }
  }, []);
  useEffect(() => stopCamera, [stopCamera]);
  return { videoRef, requestCamera, stopCamera, captureFrame, cameraStatus, error };
}
