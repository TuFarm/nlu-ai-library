import { useCallback, useEffect, useRef, useState } from "react";
import { AnimatedTransition, AssistantAvatar, CountdownAnimation, ScanningAnimation, SuccessAnimation } from "../../components/kiosk/KioskAnimations";
import { CameraPreview } from "../../components/kiosk/CameraPreview";
import { KioskChrome } from "../../components/kiosk/KioskChrome";
import { KIOSK_TIMING, wait } from "../../config/kioskRuntime";
import { useCamera } from "../../hooks/useCamera";
import { useKioskFlow } from "../../hooks/useKioskFlow";
import { useVisualDetection } from "../../hooks/useVisualDetection";
import type { KioskState } from "../../types/kiosk";
import FaceRegistrationScreen from "./FaceRegistrationScreen";
import FaceUnknownScreen from "./FaceUnknownScreen";
import KioskBookSuggestionScreen from "./KioskBookSuggestionScreen";
import KioskErrorScreen from "./KioskErrorScreen";
import KioskIdleScreen from "./KioskIdleScreen";
import KioskSurveyScreen from "./KioskSurveyScreen";
import KioskThankYouScreen from "./KioskThankYouScreen";
import KioskVoiceChatScreen from "./KioskVoiceChatScreen";
import WelcomeScreen from "./WelcomeScreen";

const VOICE_STATES: KioskState[] = ["VOICE_GREETING", "VOICE_LISTENING", "USER_SPEAKING", "PROCESSING", "AI_SPEAKING", "LISTENING"];

function CountdownSequence({ onComplete }: { onComplete: () => void }) {
  const [value, setValue] = useState(3);
  const completeRef = useRef(onComplete);
  completeRef.current = onComplete;
  useEffect(() => {
    const id = window.setInterval(() => setValue((current) => {
      if (current <= 1) {
        window.clearInterval(id);
        window.setTimeout(() => completeRef.current(), 120);
        return 1;
      }
      return current - 1;
    }), KIOSK_TIMING.countdownStepMs);
    return () => window.clearInterval(id);
  }, []);
  return <div className="kiosk-center countdown-screen"><CountdownAnimation value={value}/><h1>Giữ nguyên vị trí</h1><p>Hệ thống sẽ chụp một khung hình duy nhất.</p></div>;
}

export default function KioskApp() {
  const flow = useKioskFlow();
  const camera = useCamera();
  const presenceStartRef = useRef(false);
  const captureInFlightRef = useRef(false);
  const detectionMode = flow.currentState === "IDLE" ? "idle" : flow.currentState === "FACE_STABILIZING" ? "stability" : "off";
  const visual = useVisualDetection(camera.videoElement, detectionMode);

  const ensureCamera = useCallback(async () => {
    const granted = await camera.requestCamera();
    if (granted) flow.cameraGranted();
    else flow.cameraDenied(camera.error ?? "Camera cần được cấp quyền để kiosk tự động nhận diện.");
    return granted;
  }, [camera.requestCamera, camera.error, flow.cameraGranted, flow.cameraDenied]);

  useEffect(() => {
    if (flow.currentState === "IDLE") {
      presenceStartRef.current = false;
      captureInFlightRef.current = false;
      void ensureCamera();
    }
  }, [flow.currentState, ensureCamera]);

  useEffect(() => {
    if (flow.currentState !== "IDLE" || !visual.present || presenceStartRef.current) return;
    presenceStartRef.current = true;
    void flow.startSession();
  }, [flow.currentState, visual.present, flow.startSession]);

  useEffect(() => {
    if (flow.currentState === "FACE_STABILIZING" && visual.mode === "stability" && visual.stable) flow.transitionTo("COUNTDOWN");
  }, [flow.currentState, visual.mode, visual.stable, flow.transitionTo]);

  useEffect(() => {
    if (flow.currentState !== "CAMERA_PREPARING") return;
    let active = true;
    void (async () => {
      if (!await ensureCamera()) return;
      await wait(KIOSK_TIMING.cameraPreparationMs);
      if (active) flow.transitionTo("FACE_STABILIZING");
    })();
    return () => { active = false; };
  }, [flow.currentState, flow.transitionTo, ensureCamera]);

  const captureAndVerify = useCallback(async () => {
    if (captureInFlightRef.current) return;
    captureInFlightRef.current = true;
    try {
      if (!await ensureCamera()) return;
      await flow.verifyFace(await camera.captureFrame());
    }
    catch (reason) {
      flow.cameraDenied(reason instanceof Error ? reason.message : "Không thể kết nối với camera.");
    } finally { captureInFlightRef.current = false; }
  }, [camera.captureFrame, flow.verifyFace, flow.cameraDenied, ensureCamera]);

  const retryRecognition = useCallback(async () => {
    if (await ensureCamera()) flow.transitionTo("CAMERA_PREPARING");
  }, [ensureCamera, flow.transitionTo]);

  const openRegistration = useCallback(async () => {
    if (await ensureCamera()) flow.transitionTo("REGISTER");
  }, [ensureCamera, flow.transitionTo]);

  useEffect(() => {
    if (flow.currentState === "FACE_CAPTURE") void captureAndVerify();
  }, [flow.currentState, captureAndVerify]);

  useEffect(() => {
    if (flow.currentState === "GREETING" || VOICE_STATES.includes(flow.currentState)) camera.stopCamera();
  }, [flow.currentState, camera.stopCamera]);

  const permission = <div className="kiosk-center permission-screen">
    <CameraPreview videoRef={camera.videoRef} status={camera.cameraStatus} error={camera.error} showFrameOverlay={false}/>
    <span className="kiosk-kicker">CẦN QUYỀN CAMERA</span><h1>Cho phép camera để tiếp tục</h1>
    <p>Trên kiosk Electron, quyền này được cấu hình một lần khi cài đặt. Trong bản phát triển, hãy cho phép camera trong cửa sổ hiện tại.</p>
    <div className="kiosk-actions"><button onClick={() => void ensureCamera()}>Cho phép camera</button><button className="kiosk-ghost" onClick={flow.continueAsGuest}>Tiếp tục với tư cách khách</button></div>
  </div>;

  const content = (() => {
    if (VOICE_STATES.includes(flow.currentState)) return <KioskVoiceChatScreen flow={flow}/>;
    switch (flow.currentState) {
      case "IDLE": return <KioskIdleScreen videoRef={camera.videoRef} cameraStatus={camera.cameraStatus} cameraError={camera.error}/>;
      case "CAMERA_PERMISSION": return permission;
      case "PRESENCE_DETECTED": return <div className="kiosk-center presence-screen"><AssistantAvatar mood="greeting"/><span className="kiosk-kicker">ĐÃ NHẬN THẤY BẠN</span><h1>Xin chào!</h1><p>Đang chuẩn bị nhận diện...</p></div>;
      case "CAMERA_PREPARING": return <div className="kiosk-center preparation-screen"><CameraPreview videoRef={camera.videoRef} status={camera.cameraStatus} error={camera.error}/><h1>Vui lòng nhìn thẳng vào màn hình</h1><p>Camera đang điều chỉnh ánh sáng và khung hình.</p></div>;
      case "FACE_STABILIZING": return <div className="kiosk-center stabilizing-screen"><CameraPreview videoRef={camera.videoRef} status={camera.cameraStatus} error={camera.error}/><span className="kiosk-kicker pulse-text">● ĐANG CĂN CHỈNH</span><h1>{visual.guidance}</h1><p>Đưa khuôn mặt vào giữa khung và giữ yên trong giây lát.</p></div>;
      case "COUNTDOWN": return <CountdownSequence onComplete={() => flow.transitionTo("FACE_CAPTURE")}/>;
      case "FACE_CAPTURE": return <div className="kiosk-center"><div className="capture-flash"/><h1>Đã chụp ảnh</h1><p>Đang chuyển sang bước xác minh.</p></div>;
      case "VERIFYING": return <div className="kiosk-center verifying-screen"><ScanningAnimation/><span className="kiosk-kicker pulse-text">ĐANG XÁC MINH</span><h1>Đang xác minh danh tính...</h1><p>Quá trình này chỉ mất một chút thời gian.</p></div>;
      case "FACE_SUCCESS": return <div className="kiosk-center"><SuccessAnimation/><h1>Nhận diện thành công</h1><p>Đang chuẩn bị lời chào dành cho bạn.</p></div>;
      case "GREETING": return <WelcomeScreen user={flow.user} onContinue={() => void flow.startConversation()}/>;
      case "UNKNOWN_FACE": return <FaceUnknownScreen onRegister={() => void openRegistration()} error={flow.error}
        onRetry={() => void retryRecognition()} onGuest={flow.continueAsGuest}
        onSimulateSuccess={import.meta.env.DEV ? () => flow.simulateFace(true) : undefined}/>;
      case "REGISTER":
      case "REGISTER_PROCESSING": return <FaceRegistrationScreen videoRef={camera.videoRef} cameraStatus={camera.cameraStatus}
        cameraError={camera.error} busy={flow.isProcessing} captureFrame={camera.captureFrame} onEnroll={flow.enrollFace}
        onRetry={() => void retryRecognition()} onGuest={flow.continueAsGuest}/>;
      case "REGISTER_SUCCESS": return <div className="kiosk-center"><SuccessAnimation/><span className="kiosk-kicker">ĐĂNG KÝ HOÀN TẤT</span><h1>Hồ sơ khuôn mặt đã sẵn sàng</h1><p>Từ lần sau, kiosk có thể nhận ra bạn nhanh hơn.</p></div>;
      case "BOOK_SUGGESTION": return <KioskBookSuggestionScreen onBack={() => flow.transitionTo("VOICE_LISTENING")} onSurvey={flow.openSurvey}/>;
      case "SURVEY": return <KioskSurveyScreen sessionId={flow.session?.session_id} userId={flow.user?.id} onComplete={flow.completeSurvey}/>;
      case "THANK_YOU": return <KioskThankYouScreen onHome={() => flow.transitionTo("RETURN_IDLE")}/>;
      case "RETURN_IDLE": return <div className="kiosk-center return-idle"><AssistantAvatar mood="goodbye"/><h1>Hẹn gặp lại</h1></div>;
      default: return <KioskErrorScreen message={flow.error ?? undefined} onRetry={() => void flow.resetToIdle("RETRY")} onHome={() => void flow.resetToIdle("USER_EXIT")}/>;
    }
  })();

  return <KioskChrome state={flow.currentState} onExit={flow.currentState !== "IDLE" ? () => flow.transitionTo("THANK_YOU") : undefined}>
    <AnimatedTransition state={flow.currentState}>{content}</AnimatedTransition>
    {import.meta.env.DEV && String(import.meta.env.VITE_ENABLE_DEV_CONTROLS ?? "true") === "true" && <div className="kiosk-dev-panel">
      <b>DEV</b><button onClick={() => void flow.startSession()}>Hiện diện</button><button onClick={() => flow.simulateFace(true)}>Thành công</button>
      <button onClick={() => flow.simulateFace(false)}>Khuôn mặt lạ</button><button onClick={() => void flow.resetToIdle("DEV_RESET")}>Reset</button>
    </div>}
  </KioskChrome>;
}
