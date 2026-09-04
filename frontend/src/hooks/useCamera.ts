import { useCallback, useEffect, useRef, useState } from "react";
import { hasLiveVideoTrack, waitForVideoFrame } from "../config/cameraRuntime";
import type { CameraStatus } from "../types/kiosk";

async function attachStream(video: HTMLVideoElement, stream: MediaStream) {
  if (video.srcObject !== stream) video.srcObject = stream;
  video.muted = true;
  video.playsInline = true;
  try { await video.play(); } catch { /* capture readiness reports a useful error later */ }
}

export function useCamera() {
  const previewElementRef = useRef<HTMLVideoElement | null>(null);
  const captureElementRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const requestRef = useRef<Promise<boolean> | null>(null);
  const [videoElement, setVideoElement] = useState<HTMLVideoElement | null>(null);
  const [cameraStatus, setCameraStatus] = useState<CameraStatus>("IDLE");
  const [error, setError] = useState<string | null>(null);

  const getCaptureElement = useCallback(() => {
    if (!captureElementRef.current) {
      const video = document.createElement("video");
      video.autoplay = true; video.muted = true; video.playsInline = true;
      captureElementRef.current = video;
    }
    return captureElementRef.current;
  }, []);

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    if (previewElementRef.current) previewElementRef.current.srcObject = null;
    if (captureElementRef.current) captureElementRef.current.srcObject = null;
    setCameraStatus("STOPPED");
  }, []);

  const requestCamera = useCallback(async () => {
    if (requestRef.current) return requestRef.current;
    const request = (async () => {
      if (!navigator.mediaDevices?.getUserMedia) {
        setError("Thiết bị này không hỗ trợ truy cập camera.");
        setCameraStatus("ERROR");
        return false;
      }
      if (hasLiveVideoTrack(streamRef.current)) {
        const captureVideo = getCaptureElement();
        await attachStream(captureVideo, streamRef.current!);
        if (previewElementRef.current) await attachStream(previewElementRef.current, streamRef.current!);
        setError(null); setCameraStatus("READY");
        return true;
      }
      setCameraStatus("REQUESTING"); setError(null);
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 }, frameRate: { ideal: 24, max: 30 } },
          audio: false,
        });
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = stream;
        await attachStream(getCaptureElement(), stream);
        if (previewElementRef.current) await attachStream(previewElementRef.current, stream);
        setCameraStatus("READY");
        return true;
      } catch (reason) {
        const denied = reason instanceof DOMException && (reason.name === "NotAllowedError" || reason.name === "SecurityError");
        setCameraStatus(denied ? "DENIED" : "ERROR");
        setError(denied
          ? "Camera chưa được cấp quyền. Vui lòng cho phép camera để tiếp tục."
          : "Không thể mở camera. Vui lòng kiểm tra thiết bị và thử lại.");
        return false;
      }
    })();
    requestRef.current = request;
    try { return await request; }
    finally { requestRef.current = null; }
  }, [getCaptureElement]);

  const captureFrame = useCallback(async () => {
    if (!hasLiveVideoTrack(streamRef.current)) throw new Error("Camera đã ngắt kết nối. Vui lòng kết nối lại camera.");
    const video = getCaptureElement();
    await attachStream(video, streamRef.current!);
    if (!await waitForVideoFrame(video)) throw new Error("Camera đang khởi động. Vui lòng giữ nguyên vị trí và thử lại.");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth; canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    if (!context) throw new Error("Không thể tạo khung ảnh từ camera.");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return new Promise<Blob>((resolve, reject) => canvas.toBlob(
      (blob) => blob ? resolve(blob) : reject(new Error("Không thể mã hóa ảnh camera.")), "image/jpeg", 0.88,
    ));
  }, [getCaptureElement]);

  const videoRef = useCallback((video: HTMLVideoElement | null) => {
    previewElementRef.current = video;
    setVideoElement(video);
    if (video && streamRef.current && hasLiveVideoTrack(streamRef.current)) void attachStream(video, streamRef.current);
  }, []);

  useEffect(() => stopCamera, [stopCamera]);
  return { videoRef, videoElement, requestCamera, stopCamera, captureFrame, cameraStatus, error };
}
