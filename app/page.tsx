"use client";

import React, { useEffect, useRef, useState } from "react";
import CameraPreview from "./components/CameraPreview";
import { sendFrameToBackend } from "./util/sendFrameToBackend";
export default function Home() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  async function startCamera() {
    setError(null);
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(s);
      if (videoRef.current) {
        videoRef.current.srcObject = s;
        // muted + playsInline improves autoplay reliability on mobile
        videoRef.current.muted = true;
        await videoRef.current.play().catch(() => {});
      }
    } catch (err) {
      setError((err as Error).message || String(err));
    }
  }

  useEffect(() => {
    if (!videoRef.current) return;

    const interval = setInterval(() => {
      sendFrameToBackend(videoRef.current, (peopleCount) => {
        console.log("People count:", peopleCount);
      }
      );
    }, 3000); // every 3 seconds

    return () => clearInterval(interval);
  }, [videoRef]);

  // 🧹 Clean up stream on unmount
  useEffect(() => {
    startCamera();
    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <CameraPreview
        videoRef={videoRef as React.RefObject<HTMLVideoElement>}
        error={error}
        startCamera={startCamera}
        stream={stream}
        setStream={setStream}
      />

    </div>
  );
}
