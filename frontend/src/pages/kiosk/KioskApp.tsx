import { useCallback, useEffect } from "react";
import { CameraPreview } from "../../components/kiosk/CameraPreview";
import { KioskChrome } from "../../components/kiosk/KioskChrome";
import { useCamera } from "../../hooks/useCamera";
import { useKioskFlow } from "../../hooks/useKioskFlow";
import FaceScanningScreen from "./FaceScanningScreen";
import FaceUnknownScreen from "./FaceUnknownScreen";
import KioskBookSuggestionScreen from "./KioskBookSuggestionScreen";
import KioskChatScreen from "./KioskChatScreen";
import KioskErrorScreen from "./KioskErrorScreen";
import KioskIdleScreen from "./KioskIdleScreen";
import KioskSurveyScreen from "./KioskSurveyScreen";
import KioskThankYouScreen from "./KioskThankYouScreen";
import WelcomeScreen from "./WelcomeScreen";

export default function KioskApp() {
  const flow = useKioskFlow();
  const camera = useCamera();

  const start = useCallback(async () => {
    if (!await flow.startSession()) return;
    const granted = await camera.requestCamera();
    if (granted) flow.cameraGranted();
    else flow.cameraDenied(camera.error ?? undefined);
  }, [flow.startSession, flow.cameraGranted, flow.cameraDenied, camera.requestCamera, camera.error]);

  const scan = useCallback(async () => {
    try { await flow.verifyFace(await camera.captureFrame()); }
    catch (reason) { flow.dispatch({ type: "FACE_VERIFY_FAILED", error: reason instanceof Error ? reason.message : "Không thể chụp ảnh camera." }); }
  }, [camera.captureFrame, flow.verifyFace, flow.dispatch]);

  useEffect(() => {
    if (flow.currentState === "IDLE" || flow.currentState === "WELCOME" || flow.currentState === "AI_CHAT") camera.stopCamera();
  }, [flow.currentState, camera.stopCamera]);

  const permission = <div className="kiosk-center permission-screen">
    <CameraPreview videoRef={camera.videoRef} status={camera.cameraStatus} error={camera.error} showFrameOverlay={false}/>
    <span className="kiosk-kicker">QUYỀN TRUY CẬP CAMERA</span>
    <h1>{camera.cameraStatus === "REQUESTING" ? "Đang kết nối camera…" : "Camera cần được cấp quyền"}</h1>
    <p>Vui lòng cho phép truy cập camera để sử dụng tính năng nhận diện khuôn mặt.</p>
    <div className="kiosk-actions">
      <button onClick={async () => { const ok = await camera.requestCamera(); ok ? flow.cameraGranted() : flow.cameraDenied(camera.error ?? undefined); }}>Thử cấp quyền camera</button>
      <button className="kiosk-secondary" onClick={flow.continueAsGuest}>Tiếp tục với tư cách khách</button>
    </div>
  </div>;

  const content = (() => {
    switch (flow.currentState) {
      case "IDLE": return <KioskIdleScreen onStart={start} busy={flow.isProcessing}/>;
      case "CAMERA_PERMISSION": return permission;
      case "CAMERA_READY": return <div className="kiosk-center"><CameraPreview videoRef={camera.videoRef} status={camera.cameraStatus} error={camera.error} showFrameOverlay/><h1>Camera đã sẵn sàng</h1><p>Vui lòng nhìn thẳng vào màn hình. Hệ thống sẽ bắt đầu quét ngay.</p></div>;
      case "FACE_SCANNING": return <FaceScanningScreen videoRef={camera.videoRef} cameraStatus={camera.cameraStatus} cameraError={camera.error} busy={flow.isProcessing} onScan={scan}/>;
      case "FACE_RECOGNIZED": return <div className="kiosk-center"><div className="state-symbol success">✓</div><h1>Đã nhận diện thành công</h1></div>;
      case "WELCOME": return <WelcomeScreen user={flow.user} onContinue={() => { void flow.startConversation(); }}/>;
      case "FACE_UNKNOWN": return <FaceUnknownScreen
        error={flow.error} onRetry={() => camera.cameraStatus === "READY" ? flow.startFaceScan() : void start()}
        onGuest={flow.continueAsGuest} onSimulateSuccess={import.meta.env.DEV ? () => flow.simulateFace(true) : undefined}/>;
      case "AI_CHAT": return <KioskChatScreen flow={flow}/>;
      case "BOOK_SUGGESTION": return <KioskBookSuggestionScreen onBack={() => flow.transitionTo("AI_CHAT")} onSurvey={flow.openSurvey}/>;
      case "SURVEY": return <KioskSurveyScreen sessionId={flow.session?.session_id} userId={flow.user?.id} onComplete={flow.completeSurvey}/>;
      case "THANK_YOU": return <KioskThankYouScreen onHome={() => { void flow.resetToIdle("COMPLETED"); }}/>;
      default: return <KioskErrorScreen message={flow.error ?? undefined} onRetry={() => { void flow.resetToIdle("RETRY"); }} onHome={() => { void flow.resetToIdle("USER_EXIT"); }}/>;
    }
  })();

  return <KioskChrome state={flow.currentState} onExit={flow.currentState !== "IDLE" ? () => { void flow.resetToIdle("USER_EXIT"); } : undefined}>
    {content}
    {import.meta.env.DEV && flow.currentState !== "IDLE" && <div className="kiosk-dev-panel">
      <b>DEV</b>
      <button onClick={() => flow.simulateFace(true)}>Nhận diện thành công</button>
      <button onClick={() => flow.simulateFace(false)}>Khuôn mặt lạ</button>
      <button onClick={flow.continueAsGuest}>Bỏ qua FaceID</button>
      <button onClick={() => { void flow.resetToIdle("DEV_RESET"); }}>Reset kiosk</button>
    </div>}
  </KioskChrome>;
}
