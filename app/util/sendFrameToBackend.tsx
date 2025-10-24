// app/lib/sendFrame.ts
export async function connectToBackendWebSocket(
  video: HTMLVideoElement,
  onResult: (peopleCount: number) => void
) {
  const ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => {
    console.log("✅ Connected to backend WebSocket");
  };

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === "image_analysis" && msg.data?.people_count != null) {
        onResult(msg.data.people_count);
      } else if (msg.type === "error") {
        console.error("Server error:", msg.message);
      } else {
        console.log("Message from server:", msg);
      }
    } catch (e) {
      console.error("Invalid message from backend:", event.data);
    }
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
  };

  // ⏱️ Send frames periodically
  const sendFrame = () => {
    if (video.readyState >= 2 && ws.readyState === WebSocket.OPEN) {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const frame = canvas.toDataURL("image/jpeg");

      ws.send(frame); // send base64 frame to FastAPI
    }
  };

  const interval = setInterval(sendFrame, 3000);

  ws.onclose = () => {
    console.log("🔌 WebSocket closed");
    clearInterval(interval);
  };

  return ws;
}
