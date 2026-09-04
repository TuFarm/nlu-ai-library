import { useCallback, useEffect, useMemo, useRef, useState } from "react";

export type SpeakOptions = { lang?: string; rate?: number; pitch?: number; volume?: number };

export function useTextToSpeech() {
  const supported = typeof window !== "undefined" && "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const activeResolveRef = useRef<(() => void) | null>(null);
  const generationRef = useRef(0);

  useEffect(() => {
    if (!supported) return;
    const loadVoices = () => setVoices(window.speechSynthesis.getVoices());
    loadVoices();
    window.speechSynthesis.addEventListener("voiceschanged", loadVoices);
    return () => window.speechSynthesis.removeEventListener("voiceschanged", loadVoices);
  }, [supported]);

  const vietnameseVoice = useMemo(() => voices.find((voice) => voice.lang.toLowerCase().startsWith("vi")), [voices]);
  const notice = supported && voices.length > 0 && !vietnameseVoice
    ? "Trình duyệt chưa có giọng đọc tiếng Việt phù hợp." : null;

  const stop = useCallback(() => {
    generationRef.current += 1;
    if (supported) window.speechSynthesis.cancel();
    activeResolveRef.current?.();
    activeResolveRef.current = null;
    setIsSpeaking(false);
  }, [supported]);

  const speak = useCallback((text: string, options: SpeakOptions = {}) => new Promise<void>((resolve) => {
    if (!supported || !text.trim()) {
      if (!supported) setError("Trình duyệt hiện không hỗ trợ đọc văn bản.");
      resolve();
      return;
    }
    window.speechSynthesis.cancel();
    activeResolveRef.current?.();
    generationRef.current += 1;
    const generation = generationRef.current;
    activeResolveRef.current = resolve;
    setError(null);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = options.lang ?? "vi-VN";
    utterance.rate = options.rate ?? 0.95;
    utterance.pitch = options.pitch ?? 1;
    utterance.volume = options.volume ?? 1;
    if (vietnameseVoice) utterance.voice = vietnameseVoice;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => {
      if (generation === generationRef.current) { setIsSpeaking(false); activeResolveRef.current = null; }
      resolve();
    };
    utterance.onerror = (event) => {
      if (generation === generationRef.current) { setIsSpeaking(false); activeResolveRef.current = null; }
      if (event.error !== "canceled" && event.error !== "interrupted") setError("Không thể đọc câu trả lời thành tiếng.");
      resolve();
    };
    window.speechSynthesis.speak(utterance);
  }), [supported, vietnameseVoice]);

  useEffect(() => () => { if (supported) window.speechSynthesis.cancel(); }, [supported]);
  return { speak, stop, isSpeaking, isSupported: supported, error, notice, vietnameseVoice };
}
