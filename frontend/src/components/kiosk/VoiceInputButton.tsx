export function VoiceInputButton({ isListening, isProcessing, disabled, onStart, onStop }: {
  isListening: boolean; isProcessing: boolean; disabled?: boolean; onStart: () => void; onStop: () => void;
}) {
  const label = isProcessing ? "Đang xử lý…" : isListening ? "Dừng ghi âm" : "Nhấn để nói";
  return <button type="button" className={`voice-button ${isListening ? "listening" : ""}`}
    disabled={disabled || isProcessing} onClick={isListening ? onStop : onStart} aria-pressed={isListening} title={label}>
    <span aria-hidden="true">{isListening ? "■" : "⌁"}</span><small>{label}</small>
  </button>;
}
