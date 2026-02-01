# Gesture Interface

This is a local project for tracking hands and fingers in real-time using Python and MediaPipe.  
It can visualize hand skeletons, detect simple gestures, and send the data to a frontend via WebSockets.

## What it does

- Tracks hands and fingers using your webcam  
- Draws the skeleton of each hand on a canvas  
- Recognizes some basic gestures (like pinch or swipe)  
- Sends hand and gesture data to a browser for visualization or further use  
- Structured so you can easily add more gestures or other features

## Tech Stack

- Python 3
- MediaPipe
- OpenCV
- WebSockets
- HTML / Canvas for frontend

## How to run

1. Make sure Python 3 is installed  
2. Install dependencies:

```bash
pip install opencv-python mediapipe websockets numpy