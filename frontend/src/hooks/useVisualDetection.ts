import { useCallback, useEffect, useRef, useState } from "react";
import { KIOSK_MOTION, KIOSK_TIMING } from "../config/kioskRuntime";

type DetectorMode = "idle" | "stability" | "off";
type DetectionState = { mode: DetectorMode; present: boolean; stable: boolean; guidance: string };

type NativeFaceDetector = { detect: (source: HTMLVideoElement) => Promise<Array<{ boundingBox: DOMRectReadOnly }>> };
type FaceDetectorConstructor = new (options?: { fastMode?: boolean; maxDetectedFaces?: number }) => NativeFaceDetector;

function frameMetrics(video: HTMLVideoElement, canvas: HTMLCanvasElement, previous?: Uint8ClampedArray) {
  const width = 96; const height = 54;
  canvas.width = width; canvas.height = height;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) return null;
  context.drawImage(video, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height).data;
  const luminance = new Uint8ClampedArray(width * height);
  let total = 0; let squares = 0; let difference = 0;
  for (let source = 0, target = 0; source < pixels.length; source += 4, target += 1) {
    const value = (pixels[source] * 3 + pixels[source + 1] * 6 + pixels[source + 2]) / 10;
    luminance[target] = value; total += value; squares += value * value;
    if (previous) difference += Math.abs(value - previous[target]);
  }
  const mean = total / luminance.length;
  return { luminance, contrast: Math.sqrt(Math.max(0, squares / luminance.length - mean * mean)), difference: previous ? difference / luminance.length : 0 };
}

export function useVisualDetection(video: HTMLVideoElement | null, mode: DetectorMode): DetectionState {
  const [state, setState] = useState<DetectionState>({ mode: "off", present: false, stable: false, guidance: "Đang quan sát khu vực phía trước kiosk" });
  const previousRef = useRef<Uint8ClampedArray | undefined>(undefined);
  const detectedSinceRef = useRef<number | undefined>(undefined);
  const lastPresenceAtRef = useRef<number | undefined>(undefined);
  const stableSinceRef = useRef<number | undefined>(undefined);
  const previousFaceCenterRef = useRef<{ x: number; y: number } | null>(null);
  const baselineReadyRef = useRef(false);
  const detectorRef = useRef<NativeFaceDetector | null>(null);

  const sample = useCallback(async () => {
    if (!video || video.readyState < 2 || !video.videoWidth) return;
    const FaceDetector = (window as Window & { FaceDetector?: FaceDetectorConstructor }).FaceDetector;
    if (FaceDetector && !detectorRef.current) detectorRef.current = new FaceDetector({ fastMode: true, maxDetectedFaces: 1 });
    let faceCenter: { x: number; y: number } | null = null;
    if (detectorRef.current) {
      try {
        const faces = await detectorRef.current.detect(video);
        if (faces.length === 1) {
          const box = faces[0].boundingBox;
          faceCenter = { x: box.x + box.width / 2, y: box.y + box.height / 2 };
        }
      } catch { detectorRef.current = null; }
    }
    const metrics = frameMetrics(video, document.createElement("canvas"), previousRef.current);
    if (!metrics) return;
    const now = performance.now();
    const hasVisualSubject = metrics.contrast >= KIOSK_MOTION.minimumContrast;
    const movementPresence = baselineReadyRef.current && metrics.difference >= KIOSK_MOTION.presenceDifference;
    let faceStable = false;
    if (faceCenter && previousFaceCenterRef.current) {
      const movement = Math.hypot(faceCenter.x - previousFaceCenterRef.current.x, faceCenter.y - previousFaceCenterRef.current.y);
      faceStable = movement / Math.hypot(video.videoWidth, video.videoHeight) < 0.025;
    }
    previousFaceCenterRef.current = faceCenter;
    if (faceCenter || (hasVisualSubject && movementPresence)) lastPresenceAtRef.current = now;
    const presentNow = Boolean(faceCenter) || Boolean(lastPresenceAtRef.current && now - lastPresenceAtRef.current < 900);
    previousRef.current = metrics.luminance;
    baselineReadyRef.current = true;

    if (mode === "idle") {
      detectedSinceRef.current = presentNow ? (detectedSinceRef.current ?? now) : undefined;
      const present = Boolean(detectedSinceRef.current && now - detectedSinceRef.current >= KIOSK_TIMING.presenceConfirmationMs);
      setState({ mode, present, stable: false, guidance: presentNow ? "Đã phát hiện người dùng" : "Vui lòng đứng trước kiosk" });
      return;
    }

    const stableNow = faceCenter ? faceStable : (hasVisualSubject && metrics.difference <= KIOSK_MOTION.stableDifference);
    stableSinceRef.current = stableNow ? (stableSinceRef.current ?? now) : undefined;
    const stable = Boolean(stableSinceRef.current && now - stableSinceRef.current >= KIOSK_TIMING.faceStableMs);
    setState({ mode, present: presentNow || hasVisualSubject, stable, guidance: stableNow ? "Tốt rồi, hãy giữ nguyên" : "Giữ yên khuôn mặt" });
  }, [mode, video]);

  useEffect(() => {
    previousRef.current = undefined; detectedSinceRef.current = undefined; lastPresenceAtRef.current = undefined; stableSinceRef.current = undefined; previousFaceCenterRef.current = null; baselineReadyRef.current = false;
    setState({ mode, present: false, stable: false, guidance: mode === "stability" ? "Vui lòng nhìn thẳng vào màn hình" : "Vui lòng đứng trước kiosk" });
    if (mode === "off") return;
    const id = window.setInterval(() => { void sample(); }, mode === "idle" ? KIOSK_TIMING.presenceSampleMs : KIOSK_TIMING.faceSampleMs);
    return () => window.clearInterval(id);
  }, [mode, sample]);

  return state;
}
