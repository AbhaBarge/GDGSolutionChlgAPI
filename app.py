from fastapi import FastAPI, Query
import yt_dlp
import cv2
import base64
import numpy as np

app = FastAPI()

@app.get("/extract-frames")
def extract_frames(video_url: str):
    frames = []

    ydl_opts = {"quiet": True, "format": "best", "cookies": "cookies.txt"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        stream_url = info["url"]

    print(stream_url)

    # Open video stream using OpenCV
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return frames

    frame_count = 0

    while True:
        ret, frame = cap.read()
        print("Frame : ")
        cv2_imshow(frame)
        if not ret:
            break
        if frame_count < 10:  # Extract only every `frame_interval`th frame
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert to RGB
        else :
            break

        frame_count += 1

    cap.release()

    return {"frame_count": len(frames), "frames": frames}
