
import cv2
from cvzone.HandTrackingModule import *
from pynput.mouse import Button, Controller
import tkinter as tk
import pandas as pd

mouse = Controller()
width, height = 1280, 720
cap = None
detector = HandDetector(detectionCon=0.8, maxHands=1)

dataset = pd.read_excel("Dataset.xlsx")

gesture_dataset = pd.read_excel("LiveVideoGestures.xlsx")


def start_tracking():
    global cap
    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, width)
        cap.set(4, height)
        capture()
    except Exception as cap_error:
        status_label.config(text="Error: Camera initialization failed")

def stop_tracking():
    global cap
    if cap is not None:
        cap.release()
        status_label.config(text="Video Stream Stopped")
def perform_action(action):
    if action == "right click":
        mouse.press(Button.right)
        mouse.release(Button.right)
    elif action == "scroll up":
        mouse.move(0, -5)
    elif action == "scroll down":
        mouse.move(0, 5)
    elif action == "move left":
        mouse.move(-5, 0)
    elif action == "move right":

        mouse.move(5, 0)
    elif action == "left click":
        mouse.press(Button.left)
        mouse.release(Button.left)

def capture():
    try:
        ret, frame = cap.read()
        img = cv2.flip(frame, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            gesture = " ".join([str(int(f)) for f in fingers])
            print("Detected Gesture is:",gesture)

            matched_row = dataset[dataset['Gesture'] == gesture]

            if not matched_row.empty:
                action_label = matched_row.iloc[0]['Action']
                live_gestures = pd.DataFrame({"Gesture": [gesture], "Action": [action_label]})
                updated_dataset = gesture_dataset._append(live_gestures,ignore_index=True)
                updated_dataset.to_excel("LiveVideoGestures.xlsx", index=False)
                perform_action(action_label)

        cv2.imshow('Video', img)
        if cv2.waitKey(1) == ord('q'):
            return
        root.after(10, capture)

    except Exception as frame_processing_error:
        print("Error while processing frame:", frame_processing_error)

root = tk.Tk()
root.title("Mouse Control Application")

start_button = tk.Button(root, text="Start", command=start_tracking)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_tracking)
stop_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()