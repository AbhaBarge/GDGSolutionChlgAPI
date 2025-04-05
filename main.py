from fastapi import FastAPI, Query
from pydantic import BaseModel
import yt_dlp
import cv2
import numpy as np
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/extract_frames/")
def extract_frames(video_url: str = Query(..., description="YouTube video URL")):
    frames = []
    stream_url = None

    ydl_opts = {"quiet": True, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        stream_url = info["url"]

    print(f"Stream URL: {stream_url}")
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        return JSONResponse(content={"error": "Could not open video stream"}, status_code=500)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count < 10:
            _, buffer = cv2.imencode(".jpg", frame)
            frames.append(buffer.tobytes())  # or encode to base64 if sending over JSON
        else:
            break
        frame_count += 1

    cap.release()
    return {"frame_count": len(frames), "message": "Frames extracted successfully"}

