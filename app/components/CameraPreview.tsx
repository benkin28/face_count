"use client"


export default function CameraPreview({ videoRef, error, startCamera,stream, setStream }: {
    videoRef: React.RefObject<HTMLVideoElement>;
    error: string | null;
    startCamera: () => Promise<void>;
    stream: MediaStream | null;
    setStream: React.Dispatch<React.SetStateAction<MediaStream | null>>;
}
) {

    return (
            <main className="flex w-full max-w-3xl flex-col items-center gap-6 py-32 px-4">
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
          Camera Preview
        </h1>

        <div className="flex flex-col items-center gap-4">
          <div className="rounded-lg border border-black/10 bg-black shadow-lg w-[640px] max-w-full aspect-video overflow-hidden">
            <video
              ref={videoRef}
              className="h-full w-full object-cover"
              playsInline
              autoPlay
            />
          </div>

          {error ? (
            <div className="text-sm text-red-600 dark:text-red-400">
              {error}
            </div>
          ) : null}

          <div className="flex gap-3">
            <button
              onClick={startCamera}
              className="rounded-full bg-foreground px-4 py-2 text-white transition hover:opacity-90"
              type="button"
            >
              Request / Retry Access
            </button>
            <button
              onClick={() => {
                if (stream) {
                  stream.getTracks().forEach((t) => t.stop());
                  setStream(null);
                  if (videoRef.current) videoRef.current.srcObject = null;
                }
              }}
              className="rounded-full border px-4 py-2"
              type="button"
            >
              Stop
            </button>
          </div>
        </div>
      </main>
    );
}