"use client";

import React, { useEffect, useRef, useState } from "react";
import CameraPreview from "./components/CameraPreview";
import { connectToBackendWebSocket } from "./util/sendFrameToBackend";
export default function Home() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [peopleCount, setPeopleCount] = useState<number | null>(null);

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
  let ws: WebSocket | null = null;
  let mounted = true;

  connectToBackendWebSocket(videoRef.current, (count) => {
    setPeopleCount(count);
  })
    .then((socket) => {
      if (!mounted) {
        socket.close();
        return;
      }
      ws = socket;
    })
    .catch((err) => {
      console.error("WebSocket connection failed:", err);
    });

  return () => {
    mounted = false;
    if (ws) ws.close();
  };
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
      <div className="mt-6 p-4 rounded-2xl bg-white/80 shadow-md dark:bg-zinc-900">
        {error ? (
          <p className="text-red-500 font-medium">Error: {error}</p>
        ) : peopleCount !== null ? (
          <p className="text-3xl font-semibold text-zinc-800 dark:text-white">
            👥 People detected: <span className="text-blue-600">{peopleCount}</span>
          </p>
        ) : (
          <p className="text-zinc-500 italic">Detecting people...</p>
        )}
      </div>

    </div>
  );
}
