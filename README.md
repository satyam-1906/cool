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

Tired of pushing a physical plastic mouse around your desk like a peasant from the early 2000s? Ever wished you could look like you're aggressively casting a magic spell at your monitor just to close a browser tab? 

Well, welcome to the future. This project turns your webcam into a gesture-powered tracking device. Using OpenCV and Google's MediaPipe, it watches your hand landmarks in real time and maps them to your mouse cursor. Yes, you can now control your computer by waving your hands in the air like a sci-fi character—or someone trying to shoo away a very persistent fly. 

*(Warning: May cause your coworkers/roommates to think you've lost your mind.)*


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
