# Hand Gesture Mouse Control

```
                                                               
                                                               
        CCCCCCCCCCCCC                                  lllllll 
     CCC::::::::::::C                                  l:::::l 
   CC:::::::::::::::C                                  l:::::l 
  C:::::CCCCCCCC::::C                                  l:::::l 
 C:::::C       CCCCCC   ooooooooooo      ooooooooooo    l::::l 
C:::::C               oo:::::::::::oo  oo:::::::::::oo  l::::l 
C:::::C              o:::::::::::::::oo:::::::::::::::o l::::l 
C:::::C              o:::::ooooo:::::oo:::::ooooo:::::o l::::l 
C:::::C              o::::o     o::::oo::::o     o::::o l::::l 
C:::::C              o::::o     o::::oo::::o     o::::o l::::l 
C:::::C              o::::o     o::::oo::::o     o::::o l::::l 
 C:::::C       CCCCCCo::::o     o::::oo::::o     o::::o l::::l 
  C:::::CCCCCCCC::::Co:::::ooooo:::::oo:::::ooooo:::::ol::::::l
   CC:::::::::::::::Co:::::::::::::::oo:::::::::::::::ol::::::l
     CCC::::::::::::C oo:::::::::::oo  oo:::::::::::oo l::::::l
        CCCCCCCCCCCCC   ooooooooooo      ooooooooooo   llllllll
                                                               
                                                               
                                                               
                                                               
                                                               
                                                               
                                                               
```

This project turns your webcam into a gesture-powered input device. Using OpenCV and MediaPipe, it detects hand landmarks in real time and maps them to mouse movement and clicks. In other words: your hand becomes the controller, and the cursor obeys your fingertips.

## What it can do

- Move the mouse pointer by moving your hand
- Trigger a left click by pinching your index finger and thumb
- Trigger a right click by pinching your middle finger and thumb
- Hold and drag items by keeping your index finger and thumb pinched
- Exit the application at any time by pressing q

## How it works

The app captures video from your webcam, runs hand landmark detection with MediaPipe, and uses the detected positions of key landmarks to:

- estimate the hand position
- compute distances between fingers
- translate those gestures into mouse actions using pynput

This makes the experience feel a bit like science fiction, except it is running locally on your machine.

## Requirements

All required Python dependencies are listed in [requirements.txt](requirements.txt). Install them with:

```bash
pip install -r requirements.txt
```

## Run the project

From the project folder, start the application with:

```bash
python main.py
```

## Notes

- A working webcam is required.
- The project expects the hand landmark model file named hand_landmarker.task to be present in the project directory.
- Make sure your camera permissions are enabled before launching the script.
- For the best experience, use good lighting and keep your hand visible to the camera.
