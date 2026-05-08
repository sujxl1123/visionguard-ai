import cv2
import numpy as np
import os
from datetime import datetime

class SmartRegistration:
    def __init__(self):
        self.fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.angles = ["straight","left","right","up","close"]
        self.texts = ["Look STRAIGHT","Turn LEFT","Turn RIGHT","Tilt UP","Move CLOSER"]
    
    def ok(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        light = 60 < np.mean(gray) < 200
        blur = cv2.Laplacian(gray, cv2.CV_64F).var() > 100
        faces = self.fc.detectMultiScale(gray, 1.1, 5, minSize=(100,100))
        face_ok = len(faces) == 1
        return light and blur and face_ok, faces[0] if face_ok else None
    
    def register(self, name):
        folder = os.path.join("dataset", name)
        os.makedirs(folder, exist_ok=True)
        cap = cv2.VideoCapture(0)
        for i, (angle, text) in enumerate(zip(self.angles, self.texts)):
            print(f"{text}...")
            ready = 0
            while True:
                ret, frame = cap.read()
                if not ret: break
                frame = cv2.flip(frame, 1)
                ok, face = self.ok(frame)
                if ok:
                    ready += 1
                    if ready >= 5:
                        cv2.imwrite(f"{folder}/{angle}.jpg", frame)
                        print(f"  Saved {angle}")
                        break
                else:
                    ready = 0
                cv2.imshow("Register", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"): break
        cap.release()
        cv2.destroyAllWindows()
        print(f"Done! Photos saved to {folder}/")

if __name__ == "__main__":
    name = input("Enter student name: ")
    sr = SmartRegistration()
    sr.register(name)
