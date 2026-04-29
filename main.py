import cv2
import os
import json
import pandas as pd
from deepface import DeepFace
from datetime import datetime
import numpy as np

DATASET_PATH = "dataset"
STUDENTS_CSV = "students.csv"
VIDEO_PATH = "input.mp4"

FACE_MATCH_THRESHOLD = 0.25
MIN_DETECTIONS = 2
FRAME_SKIP = 5
MIN_FACE_SIZE = 4000

df_students = pd.read_csv(STUDENTS_CSV)
df_students["Name"] = df_students["Name"].astype(str).str.strip()
name_to_id = dict(zip(df_students["Name"], df_students["Student ID"]))
valid_names = set(df_students["Name"])

known_people = []
for p in os.listdir(DATASET_PATH):
    folder_path = os.path.join(DATASET_PATH, p)
    if os.path.isdir(folder_path):
        for name in valid_names:
            if p.lower() in name.lower() or name.lower() in p.lower():
                known_people.append(name)
                break

print(f"Students: {len(valid_names)}, Matched: {len(known_people)}")

attendance = {name: {"count": 0, "present": False, "first_seen": None} for name in valid_names}
dataset_embeddings = {}

for person in known_people:
    folder_name = None
    for p in os.listdir(DATASET_PATH):
        if os.path.isdir(os.path.join(DATASET_PATH, p)) and (p.lower() in person.lower() or person.lower() in p.lower()):
            folder_name = p; break
    if folder_name:
        person_path = os.path.join(DATASET_PATH, folder_name)
        for img_file in os.listdir(person_path):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    emb = DeepFace.represent(img_path=os.path.join(person_path, img_file), model_name="Facenet", enforce_detection=False)
                    if emb and len(emb) > 0:
                        dataset_embeddings[person] = emb[0]["embedding"]; break
                except: pass

print(f"Embeddings: {len(dataset_embeddings)}")

def cosine_distance(a, b):
    a, b = np.array(a), np.array(b)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0: return 1.0
    return float(1 - (np.dot(a, b) / (na * nb)))

def find_best_match(face_img):
    try:
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        emb_obj = DeepFace.represent(img_path=face_rgb, model_name="Facenet", enforce_detection=False)
        if not emb_obj: return "Unknown", 1.0
        face_emb = emb_obj[0]["embedding"]
    except: return "Unknown", 1.0
    best_name, best_dist = "Unknown", 1.0
    for person, ref_emb in dataset_embeddings.items():
        dist = cosine_distance(face_emb, ref_emb)
        if dist < best_dist:
            best_dist = dist
            best_name = person if dist < FACE_MATCH_THRESHOLD else "Unknown"
    return best_name, best_dist

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Cannot open video!"); exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
frame_count = 0
print("Processing...")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame_count += 1
    if frame_count % FRAME_SKIP != 0: continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(70, 70))
    for (x, y, w, h) in faces:
        if w * h < MIN_FACE_SIZE: continue
        face_crop = frame[y:y+h, x:x+w]
        name, dist = find_best_match(face_crop)
        if name != "Unknown" and name in attendance:
            attendance[name]["count"] += 1
            if attendance[name]["first_seen"] is None:
                attendance[name]["first_seen"] = datetime.now().strftime("%H:%M:%S")
            if attendance[name]["count"] >= MIN_DETECTIONS:
                attendance[name]["present"] = True

cap.release()

results = {"attendance": attendance, "name_to_id": name_to_id}
with open("attendance_results.json", "w") as f:
    json.dump(results, f, indent=2)

rows = []
for name, rec in attendance.items():
    rows.append({"Name": name, "ID": name_to_id.get(name, "N/A"), "Status": "Present" if rec["present"] else "Absent", "Detections": rec["count"]})
pd.DataFrame(rows).to_csv("attendance.csv", index=False)

present = sum(1 for r in attendance.values() if r["present"])
print(f"DONE! Present: {present}/{len(attendance)}")
