export function hasLiveVideoTrack(stream: MediaStream | null) {
  return Boolean(stream?.getVideoTracks().some((track) => track.readyState === "live"));
}

export function isVideoFrameReady(video: HTMLVideoElement | null) {
  return Boolean(video && video.readyState >= 2 && video.videoWidth > 0 && video.videoHeight > 0);
}

export async function waitForVideoFrame(video: HTMLVideoElement, timeoutMs = 2500) {
  const started = performance.now();
  while (!isVideoFrameReady(video) && performance.now() - started < timeoutMs) {
    await new Promise<void>((resolve) => window.setTimeout(resolve, 50));
  }
  return isVideoFrameReady(video);
}
