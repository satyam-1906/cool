from pynput.mouse import Controller, Button
import cv2
from typing import Any
import mediapipe as mp
import time
import numpy as np
import check
import threading

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

right_index = [0,0]
right_thumb = [0,0]
posx = [0,0,0,0,0]
posy = [0,0,0,0,0]
final = [0,0]

frame: Any
canvas = None
click_threshold = 18
release_threshold = 20
click = False
distance = 0
t: Any
hold = False
sf = 3
prev_x, prev_y = 0, 0
bias = 1.8

mouse = Controller()
cursor_position = [0,0]
dimensions = check.dimensions()
#check.destroy()

def callback(result, output_image, timestamp_ms):
    global right_index, right_thumb, cursor_position, prev_x, prev_y, final
    #print(result)
    if len(result.hand_landmarks) == 2:
        if result.handedness[0][0].display_name == 'Right':
            hand = result.hand_landmarks[0]
            right_index[0] = int(hand[8].x * frame.shape[1])
            right_index[1] = int(hand[8].y * frame.shape[0])
            right_thumb[0] = int(hand[4].x * frame.shape[1])
            right_thumb[1] = int(hand[4].y * frame.shape[0])
            posx = [hand[0].x, hand[5].x, hand[9].x, hand[13].x, hand[17].x]
            posy = [hand[0].y, hand[5].y, hand[9].y, hand[13].y, hand[17].y]
        else:
            hand = result.hand_landmarks[1]
            right_index[0] = int(hand[8].x * frame.shape[1])
            right_index[1] = int(hand[8].y * frame.shape[0])
            right_thumb[0] = int(hand[4].x * frame.shape[1])
            right_thumb[1] = int(hand[4].y * frame.shape[0])
            posx = [hand[0].x, hand[5].x, hand[9].x, hand[13].x, hand[17].x]
            posy = [hand[0].y, hand[5].y, hand[9].y, hand[13].y, hand[17].y]
    elif len(result.hand_landmarks) == 1 and result.handedness[0][0].display_name == 'Right':
        hand = result.hand_landmarks[0]
        right_index[0] = int(result.hand_landmarks[0][8].x * frame.shape[1])
        right_index[1] = int(result.hand_landmarks[0][8].y * frame.shape[0])
        right_thumb[0] = int(result.hand_landmarks[0][4].x * frame.shape[1])
        right_thumb[1] = int(result.hand_landmarks[0][4].y * frame.shape[0])
        posx = [hand[0].x, hand[5].x, hand[9].x, hand[13].x, hand[17].x]
        posy = [hand[0].y, hand[5].y, hand[9].y, hand[13].y, hand[17].y]
    else:
        right_index = [0,0]
        right_thumb = [0,0]
        posx = [0,0,0,0,0]
        posy = [0,0,0,0,0]
        cursor_position = [0,0]
    #print(right_index)
    normalized_posx = [int(((x-0.5)*bias+0.5)*frame.shape[1]) for x in posx]
    normalized_posy = [int(((y-0.5)*bias+0.5)*frame.shape[0]) for y in posy]

    normalized_final = [int(sum(normalized_posx)/5), int(sum(normalized_posy)/5)]
    final = [int(sum(posx)*frame.shape[1]/5), int(sum(posy)*frame.shape[0]/5)]
    #print(final)
    if final != [0,0]:
        cursor_position[0] = prev_x + int((dimensions[0] - int(normalized_final[0] * dimensions[0]/frame.shape[1]) - prev_x)/sf)
        cursor_position[1] = prev_y + int((int(normalized_final[1] * dimensions[1]/frame.shape[0]) - prev_y)/sf)
        prev_x, prev_y = cursor_position[0], cursor_position[1]


def mouse_left_hold():
    mouse.press(Button.left)
    mouse_left_release()
    

def mouse_left_release():
    if distance > release_threshold:
        mouse.release(Button.left)
    else:
        threading.Timer(0.5, mouse_left_release).start()

def left_click():
    mouse.click(Button.left, 1)

def reset():
    global click, t, hold
    if distance > release_threshold and click and not hold:
        click = False
    else:
        t = threading.Timer(0.25, reset)
        t.start()

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
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
        
        if right_index != [0,0]:
            canvas = cv2.circle(canvas, (right_index[0], right_index[1]), 4, (256, 256, 256), -1)

        if right_thumb != [0,0]:
            canvas = cv2.circle(canvas, (right_thumb[0], right_thumb[1]), 4, (256, 256, 256), -1)

        if final != [0,0]:
            canvas = cv2.circle(canvas, (final[0], final[1]), 4, (256, 256, 256), -1)

        if cursor_position != [0,0]:
            mouse.position = (int(cursor_position[0]), int(cursor_position[1]))

        #prev = click
        distance = ((right_index[0]-right_thumb[0])**2 + (right_index[1]-right_thumb[1])**2)**0.5
        #if prev == True and distance <= click_threshold:
            #mouse_left_hold()
        if right_index != [0,0] and right_thumb != [0,0] and distance <= click_threshold and not click:
            click = True
            left_click()
            threading.Timer(0.25, reset).start()

        frame = cv2.add(frame, canvas)
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f'Distance: {distance:.2f}', (20, 35), cv2.FONT_HERSHEY_PLAIN, 1.4, (256, 256, 256), 2)

        cv2.imshow("Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()