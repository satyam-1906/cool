# Hand Gesture Mouse Control

This project uses OpenCV and MediaPipe to control your computer mouse with hand gestures.

## Features

- Move the mouse pointer by moving your hand
- Perform a left click by pinching your index finger and thumb
- Perform a right click by pinching your middle finger and thumb
- Hold and drag items by keeping your index finger and thumb pinched
- Quit the program by pressing q

## Requirements

Install the following Python packages:

```bash
pip install opencv-python mediapipe pynput keyboard numpy
```

## How to run

From the project folder, run:

```bash
python main.py
```

## Notes

- A webcam is required.
- The program uses the hand landmark model file named hand_landmarker.task.
- Make sure your camera is available and enabled before starting.
