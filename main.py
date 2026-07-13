from pynput.mouse import Controller, Button
import cv2
from typing import Any
import mediapipe as mp
import time
import numpy as np

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

index = [0,0]
frame: Any
canvas = None

def callback(result, output_image, timestamp_ms):
    global index
    #print(result)
    if len(result.hand_landmarks) > 0:
        if len(result.hand_landmarks[0]) > 0:
            index[0] = int(result.hand_landmarks[0][8].x * frame.shape[1])
            index[1] = int(result.hand_landmarks[0][8].y * frame.shape[0])
        else:
            index[0] = int(result.hand_landmarks[1][8].x * frame.shape[1])
            index[1] = int(result.hand_landmarks[1][8].y * frame.shape[0])
    else:
        index[0] = 0
        index[1] = 0

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    min_hand_detection_confidence=0.5,
    num_hands=2,
    result_callback=callback)

with HandLandmarker.create_from_options(options) as landmarker:

    cap = cv2.VideoCapture(0)
    
    last_timestamp_ms = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        canvas = np.zeros_like(frame)

        mp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now_ms = int(time.monotonic() * 1000)
        if now_ms <= last_timestamp_ms:
            now_ms = last_timestamp_ms + 1
        last_timestamp_ms = now_ms

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, last_timestamp_ms)
        
        if index != [0,0]:
            canvas = cv2.circle(canvas, (index[0], index[1]), 4, (256, 256, 256), -1)

        frame = cv2.add(frame, canvas)

        cv2.imshow("Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()