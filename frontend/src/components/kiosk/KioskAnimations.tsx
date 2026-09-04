import type { ReactNode } from "react";

export function AnimatedTransition({ state, children }: { state: string; children: ReactNode }) {
  return <div className="kiosk-transition" data-kiosk-state={state}>{children}</div>;
}

export function AssistantAvatar({ mood = "idle", label = "Trợ lý AI" }: {
  mood?: "idle" | "greeting" | "listening" | "thinking" | "speaking" | "goodbye";
  label?: string;
}) {
  return <div className={`assistant-avatar-runtime ${mood}`} role="img" aria-label={label}>
    <div className="assistant-face"><i/><i/><span/></div>
    <div className="assistant-rings"><i/><i/><i/></div>
    {mood === "greeting" || mood === "goodbye" ? <b className="assistant-wave">👋</b> : null}
  </div>;
}

export function ListeningIndicator({ active = true }: { active?: boolean }) {
  return <div className={`listening-indicator ${active ? "active" : ""}`} aria-label="Micro đang lắng nghe">
    <span>●</span><div>{[1, 2, 3, 4, 5].map((bar) => <i key={bar}/>)}</div>
  </div>;
}

export function ScanningAnimation() {
  return <div className="verification-visual" role="status" aria-label="Đang xác minh danh tính">
    <div className="verification-portrait"><span>☺</span><i/></div>
    <div className="verification-progress"><i/></div>
  </div>;
}

export function CountdownAnimation({ value }: { value: number }) {
  return <div className="countdown-animation" key={value} aria-live="assertive">{value}</div>;
}

export function SuccessAnimation() {
  return <div className="success-animation" role="img" aria-label="Nhận diện thành công">
    <span>✓</span><i/><i/><i/>
  </div>;
}
