import tkinter as tk
from tkinter import filedialog
import cv2
from cvzone.HandTrackingModule import *
import pandas as pd

detector = HandDetector(detectionCon=0.8, maxHands=1)
data = pd.read_excel("Dataset.xlsx")

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected image:", file_path)
        detect_gesture(file_path)
        exit()

def detect_gesture(image_path):
    try:
        img = cv2.imread(image_path)
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            gesture = " ".join([str(int(f)) for f in fingers])
            print("Detected Gesture:", gesture)

            action = input("Enter an action for the detected gesture: ")

            new_data = pd.DataFrame({"Gesture": [gesture], "Action": [action]})

            updated_data = data._append(new_data, ignore_index=True)

            updated_data.to_excel("Dataset.xlsx", index=False)
            print("Detected gestures with actions saved to Dataset.xlsx")
            exit()

    except Exception as e:
        print("Error while detecting gesture:", e)

root = tk.Tk()
root.title("Image Gesture Detection")

upload_button = tk.Button(root, text="Upload Image", command=open_image)
upload_button.pack(pady=20)

root.mainloop()
