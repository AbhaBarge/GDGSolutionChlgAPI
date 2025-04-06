from fastapi import FastAPI, Query
import yt_dlp
import cv2
import base64
import numpy as np

app = FastAPI()

@app.get("/extract-frames")
def extract_frames(video_url: str):
    frames = []
    stream_url = None

    # Use yt-dlp to get the streamable URL
    ydl_opts = {"quiet": True, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        stream_url = info["url"]

    # Open video stream
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        return {"error": "Could not open video."}

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= 10:
            break

        # Convert frame to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Encode frame as JPG
        _, img_encoded = cv2.imencode('.jpg', rgb)
        
        # Convert to base64 string
        img_b64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')
        frames.append(img_b64)

        frame_count += 1

    cap.release()

    return {"frame_count": len(frames), "frames": frames}
