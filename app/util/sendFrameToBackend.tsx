  // app/lib/sendFrame.ts
  export async function sendFrameToBackend(
    video: HTMLVideoElement | null,
    onResult?: (peopleCount: number) => void
  ) {
    if (!video) return;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL("image/jpeg");

    try {
      const res = await fetch("http://localhost:8000/process_frame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: frame }),
      });
      const data = await res.json();
      if (onResult && typeof data?.people_count === "number") {
        onResult(data.people_count);
      }
    } catch (err) {
      console.error("Error sending frame:", err);
    }
  }
