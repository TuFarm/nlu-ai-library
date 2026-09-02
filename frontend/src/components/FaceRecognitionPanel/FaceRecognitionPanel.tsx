export default function FaceRecognitionPanel() {
  return (
    <main data-screen="face-recognition">
      <h1>Nhận diện người dùng</h1>
      <p>FaceID chỉ phục vụ định danh; người dùng chưa nhận diện vẫn có thể tiếp tục.</p>
      {/* TODO: integrate consent-aware FaceID and record each attempt. */}
    </main>
  );
}
