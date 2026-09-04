import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import { VoiceInputButton } from "../../components/kiosk/VoiceInputButton";
import { useKioskFlow } from "../../hooks/useKioskFlow";
import { useSpeechRecognition } from "../../hooks/useSpeechRecognition";
import { useTextToSpeech } from "../../hooks/useTextToSpeech";
import type { MessageInputMethod, VoiceState } from "../../types/kiosk";

const quickQuestions = [
  "Thư viện mở cửa lúc mấy giờ?", "Wifi thư viện là gì?", "Khu vực học nhóm ở đâu?",
  "Tôi muốn tìm sách theo chủ đề", "Làm sao để liên hệ lễ tân?",
];
const stateLabels: Record<VoiceState, { title: string; detail: string }> = {
  VOICE_IDLE: { title: "Sẵn sàng trò chuyện", detail: "Nhấn để nói lại hoặc nhập bằng bàn phím" },
  LISTENING: { title: "Tôi đang nghe...", detail: "Bạn có thể nói câu hỏi của mình" },
  USER_SPEAKING: { title: "Tôi đang nghe...", detail: "Hãy tiếp tục, tôi đang ghi nhận câu hỏi" },
  TRANSCRIBING: { title: "Đang nhận dạng giọng nói...", detail: "Vui lòng đợi trong giây lát" },
  PROCESSING_AI: { title: "Đang xử lý câu hỏi...", detail: "Trợ lý đang chuẩn bị câu trả lời" },
  AI_SPEAKING: { title: "Trợ lý đang trả lời...", detail: "Micro tạm dừng để không thu lại giọng của trợ lý" },
  VOICE_ERROR: { title: "Không thể dùng giọng nói", detail: "Bạn vẫn có thể nhập bằng bàn phím" },
};

export default function KioskVoiceChatScreen({ flow }: { flow: ReturnType<typeof useKioskFlow> }) {
  const [input, setInput] = useState("");
  const [voiceState, setVoiceState] = useState<VoiceState>("VOICE_IDLE");
  const mountedRef = useRef(true);
  const autoListenRef = useRef(true);
  const processingRef = useRef(false);
  const greetingStartedRef = useRef(false);
  const recognitionControlRef = useRef<{ start: () => void; stop: () => void; supported: boolean } | undefined>(undefined);
  const tts = useTextToSpeech();
  const speakRef = useRef(tts.speak);
  speakRef.current = tts.speak;

  const processTurn = useCallback(async (text: string, confidence?: number, method: MessageInputMethod = "VOICE") => {
    const clean = text.trim();
    if (!clean || processingRef.current || tts.isSpeaking) return;
    processingRef.current = true;
    recognitionControlRef.current?.stop();
    setVoiceState(method === "VOICE" ? "TRANSCRIBING" : "PROCESSING_AI");
    flow.setMicStatus("PROCESSING");
    const answer = await flow.submitMessage(clean, method, confidence);
    if (!mountedRef.current) return;
    if (!answer) {
      processingRef.current = false;
      setVoiceState("VOICE_ERROR");
      flow.setMicStatus("ERROR");
      return;
    }
    setVoiceState("AI_SPEAKING");
    await speakRef.current(answer);
    if (!mountedRef.current) return;
    processingRef.current = false;
    if (autoListenRef.current && recognitionControlRef.current?.supported) {
      setVoiceState("LISTENING");
      flow.setMicStatus("LISTENING");
      window.setTimeout(() => { if (mountedRef.current) recognitionControlRef.current?.start(); }, 250);
    } else {
      setVoiceState("VOICE_IDLE");
      flow.setMicStatus("IDLE");
    }
  }, [flow.submitMessage, flow.setMicStatus, tts.isSpeaking]);

  const recognition = useSpeechRecognition((text, confidence) => { void processTurn(text, confidence, "VOICE"); });
  recognitionControlRef.current = {
    start: recognition.startListening, stop: recognition.stopListening, supported: recognition.isSupported,
  };

  const startListening = useCallback(() => {
    if (processingRef.current || tts.isSpeaking) return;
    autoListenRef.current = true;
    setVoiceState("LISTENING");
    flow.setMicStatus("LISTENING");
    recognition.startListening();
  }, [flow.setMicStatus, recognition.startListening, tts.isSpeaking]);
  const stopListening = useCallback(() => {
    autoListenRef.current = false;
    recognition.stopListening();
    setVoiceState("VOICE_IDLE");
    flow.setMicStatus("IDLE");
  }, [flow.setMicStatus, recognition.stopListening]);

  useEffect(() => {
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);
  useEffect(() => {
    if (recognition.error) {
      setVoiceState("VOICE_ERROR");
      flow.setMicStatus(recognition.error.includes("cấp quyền") ? "DENIED" : "ERROR");
    } else if (recognition.interimTranscript && !processingRef.current) {
      setVoiceState("USER_SPEAKING");
    } else if (recognition.isListening && !processingRef.current) {
      setVoiceState("LISTENING");
    }
  }, [recognition.error, recognition.interimTranscript, recognition.isListening, flow.setMicStatus]);
  useEffect(() => {
    if (greetingStartedRef.current) return;
    greetingStartedRef.current = true;
    const greeting = flow.user
      ? `Xin chào ${flow.user.full_name}. Tôi là trợ lý AI thư viện. Hôm nay tôi có thể giúp gì cho bạn?`
      : "Xin chào bạn. Tôi là trợ lý AI thư viện. Bạn cần hỗ trợ gì hôm nay?";
    void (async () => {
      setVoiceState("AI_SPEAKING");
      flow.setMicStatus("PROCESSING");
      await speakRef.current(greeting);
      if (!mountedRef.current) return;
      if (recognitionControlRef.current?.supported) startListening();
      else { setVoiceState("VOICE_ERROR"); flow.setMicStatus("UNSUPPORTED"); }
    })();
    return () => {
      greetingStartedRef.current = false;
      recognitionControlRef.current?.stop();
      tts.stop();
    };
  }, []);

  async function send(event: FormEvent) {
    event.preventDefault();
    const text = input.trim();
    if (!text) return;
    setInput("");
    await processTurn(text, undefined, "TEXT");
  }
  const status = stateLabels[voiceState];
  return <div className="kiosk-chat voice-chat">
    <div className="voice-chat-heading">
      <div className={`voice-assistant-avatar ${voiceState === "AI_SPEAKING" ? "speaking" : ""}`}>☺<i/><i/><i/></div>
      <div><span className="kiosk-kicker">TRỢ LÝ AI THƯ VIỆN</span>
        <h1>{flow.user ? `Xin chào, ${flow.user.full_name}!` : "Xin chào bạn!"}</h1></div>
      <div className={`voice-state-badge ${voiceState.toLowerCase()}`}><span/><strong>{status.title}</strong><small>{status.detail}</small></div>
    </div>
    <div className="voice-conversation">
      <div className="voice-transcript-panel">
        <span>BẠN ĐANG NÓI</span>
        <p>{recognition.interimTranscript || recognition.transcript || flow.currentTranscript || "Câu hỏi của bạn sẽ xuất hiện tại đây..."}</p>
        {(recognition.isListening || voiceState === "USER_SPEAKING") && <div className="sound-bars">{[1,2,3,4,5,6].map((bar) => <i key={bar}/>)}</div>}
      </div>
      <div className="kiosk-chat-log" aria-live="polite">
        {flow.messages.map((message) => <div className={`kiosk-bubble ${message.role}`} key={message.id}>
          <span>{message.role === "assistant" ? "☺" : "Bạn"}</span><p>{message.text}</p>
        </div>)}
        {flow.isProcessing && <div className="kiosk-bubble assistant"><span>☺</span><p>Đang xử lý câu hỏi...</p></div>}
      </div>
    </div>
    <div className="kiosk-chips">{quickQuestions.map((question) =>
      <button key={question} disabled={processingRef.current || tts.isSpeaking} onClick={() => { void processTurn(question, undefined, "TEXT"); }}>{question}</button>)}</div>
    <form className="kiosk-input" onSubmit={send}>
      <VoiceInputButton isListening={recognition.isListening} isProcessing={flow.isProcessing || tts.isSpeaking}
        disabled={!recognition.isSupported} onStart={startListening} onStop={stopListening}/>
      <input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Nhập bằng bàn phím" aria-label="Nhập câu hỏi bằng bàn phím"/>
      <button disabled={!input.trim() || flow.isProcessing || tts.isSpeaking}>Gửi câu hỏi ↑</button>
    </form>
    <div className="voice-chat-actions">
      <span>{recognition.error ?? tts.error ?? tts.notice ?? (!recognition.isSupported
        ? "Trình duyệt hiện không hỗ trợ nhận dạng giọng nói. Bạn có thể nhập câu hỏi bằng bàn phím." : "Hội thoại giọng nói theo lượt · vi-VN")}</span>
      <button className="text-action" onClick={flow.openBooks}>Gợi ý sách</button>
      <button className="text-action" onClick={flow.openSurvey}>Khảo sát</button>
      <button className="text-action danger" onClick={() => { tts.stop(); recognition.stopListening(); void flow.resetToIdle("USER_EXIT"); }}>Kết thúc</button>
    </div>
    {import.meta.env.DEV && String(import.meta.env.VITE_ENABLE_DEV_CONTROLS ?? "true") === "true" &&
      <div className="voice-dev-controls"><button onClick={() => { autoListenRef.current = false; recognition.stopListening(); tts.stop(); setVoiceState("VOICE_IDLE"); }}>Dừng voice</button>
        <button onClick={() => { void tts.speak("Xin chào. Đây là kiểm tra giọng đọc tiếng Việt."); }}>Test TTS</button></div>}
  </div>;
}
