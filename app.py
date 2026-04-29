import cv2
import os
import pandas as pd
from deepface import DeepFace
from datetime import datetime
import numpy as np
from collections import defaultdict


DATASET_PATH = "dataset"
STUDENTS_CSV = "students.csv"
VIDEO_PATH = "input.mp4"

FACE_MATCH_THRESHOLD = 0.38  
MIN_DETECTIONS = 3  
FRAME_SKIP = 5      


MIN_FACE_SIZE = 6000 
BLUR_THRESHOLD = 40  
BRIGHTNESS_MIN = 35  
BRIGHTNESS_MAX = 240  
TEMPORAL_WINDOW = 2   
SECOND_BEST_MARGIN = 0.08  
ADAPTIVE_MARGIN = 0.02  
CONSISTENCY_BUFFER = 2  




df_students = pd.read_csv(STUDENTS_CSV)
df_students["Name"] = df_students["Name"].str.strip()


EXCLUDE_NAMES = {"Sujal"} 
df_students = df_students[~df_students["Name"].isin(EXCLUDE_NAMES)].reset_index(drop=True)

name_to_id = dict(zip(df_students["Name"], df_students["ID"]))


valid_names = set(df_students["Name"])

known_people = [
    p for p in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, p))
    and p not in EXCLUDE_NAMES
    and p in df_students["Name"].values
]


attendance = {}
for name in valid_names:
    attendance[name] = {
        "count": 0,
        "distances": [],
        "present": False,
        "first_seen": None
    }


print("\n📊 Pre-computing face embeddings...")


dataset_embeddings = {}  

for person in known_people:
    person_path = os.path.join(DATASET_PATH, person)
    dataset_embeddings[person] = []
    
    for img_file in os.listdir(person_path):
        if not img_file.lower().endswith((".jpg", ".png", ".jpeg")):
            continue
        
        img_path = os.path.join(person_path, img_file)
        
        try:
            
            embedding_obj = DeepFace.represent(
                img_path=img_path,
                model_name="Facenet",
                enforce_detection=False
            )
            
            if embedding_obj and len(embedding_obj) > 0:
                embedding = embedding_obj[0]["embedding"]
                dataset_embeddings[person].append(embedding)
                
        except Exception as e:
            print(f"  ⚠️ Failed to embed {img_file}: {str(e)[:30]}")
            continue
    
    if dataset_embeddings[person]:
        print(f"  ✅ {person}: {len(dataset_embeddings[person])} embeddings")
    else:
        print(f"  ❌ {person}: No valid embeddings!")

print("✅ Embeddings ready\n")


def cosine_distance(emb1, emb2):
    """Calculate cosine distance between two embeddings"""
    emb1 = np.array(emb1)
    emb2 = np.array(emb2)
    
    
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    
    if norm1 == 0 or norm2 == 0:
        return 1.0
    
    similarity = dot_product / (norm1 * norm2)
    distance = 1.0 - similarity
    
    
    if np.isnan(distance):
        return 1.0
    
    return max(0.0, min(distance, 1.0)) 


def check_blur(image):
    """Check if face is too blurry using Laplacian variance"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var, laplacian_var >= BLUR_THRESHOLD

def check_brightness(image):
    """Check if face brightness is acceptable"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    return avg_brightness, (BRIGHTNESS_MIN <= avg_brightness <= BRIGHTNESS_MAX)


recent_detections = [] 
detection_history = defaultdict(list)  


cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ Cannot open video")
    exit()


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

frame_count = 0

print("\n🎬 Processing video...\n")


def find_best_match(face_img):
    """
    Enhanced matching with:
    - Pre-computed embeddings
    - Cosine distance
    - Second-best margin check
    """
    best_match = "Unknown"
    best_distance = 1.0
    all_distances = {}
    
    
    try:
        
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        
        
        embedding_obj = DeepFace.represent(
            img_path=face_rgb,
            model_name="Facenet",
            enforce_detection=False
        )
        
        if not embedding_obj or len(embedding_obj) == 0:
            return "Unknown", 1.0
        
        face_embedding = embedding_obj[0]["embedding"]
        
    except Exception as e:
        return "Unknown", 1.0
    
    
    for person in known_people:
        if person not in dataset_embeddings or not dataset_embeddings[person]:
            continue
        
        distances = []
        
        
        for ref_embedding in dataset_embeddings[person]:
            dist = cosine_distance(face_embedding, ref_embedding)
            distances.append(dist)
        
        if distances:
            min_dist = min(distances)
            all_distances[person] = min_dist
            
            if min_dist < best_distance:
                best_distance = min_dist
                best_match = person
    
   
    if best_match != "Unknown" and len(all_distances) >= 2:
        sorted_matches = sorted(all_distances.items(), key=lambda x: x[1])
        
        
        if len(sorted_matches) >= 2:
            second_best_dist = sorted_matches[1][1]
            margin = second_best_dist - best_distance
            
            if margin < SECOND_BEST_MARGIN:
                
                return "Unknown", best_distance
    
    
    if best_distance > (FACE_MATCH_THRESHOLD + 0.02):  
        return "Unknown", best_distance
    
    
    if best_distance > FACE_MATCH_THRESHOLD:
        return "Unknown", best_distance
    
    return best_match, best_distance



while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    if frame_count % FRAME_SKIP != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(80, 80)
    )

    print(f"Frame {frame_count} | Faces: {len(faces)}")

    
    current_frame_matches = []
    
    for (x, y, w, h) in faces:
       
        aspect_ratio = w / float(h)
        area = w * h

        if aspect_ratio < 0.75 or aspect_ratio > 1.5:
            continue

        if area < MIN_FACE_SIZE:  
            continue

        
        pad = int(0.2 * w)
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(frame.shape[1], x + w + pad)
        y2 = min(frame.shape[0], y + h + pad)

        face_crop = frame[y1:y2, x1:x2]
        
        
        if face_crop.size == 0:
            continue
            
        
        blur_value, is_sharp = check_blur(face_crop)
        
        if area > 15000:
            is_sharp = blur_value >= (BLUR_THRESHOLD * 0.7)
        if not is_sharp:
            print(f"  ⚠️ Face too blurry (var={blur_value:.1f})")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (128, 128, 128), 2)
            cv2.putText(frame, "Blurry", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            continue
        
        
        brightness, is_good_brightness = check_brightness(face_crop)
        
        if area > 15000:
            is_good_brightness = (30 <= brightness <= 255)
        if not is_good_brightness:
            print(f"  ⚠️ Face brightness issue ({brightness:.1f})")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (128, 128, 128), 2)
            cv2.putText(frame, "Bad light", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            continue

        
        name, distance = find_best_match(face_crop)

        
        if len(current_frame_matches) > 0:
            recent_names = [n for n, fc in current_frame_matches if n == name]
            if len(recent_names) < 1:
                continue

        if name != "Unknown":
            if name not in attendance:
                continue
            record = attendance[name]

            
            if len(record["distances"]) > 0:
                avg = sum(record["distances"]) / len(record["distances"])
               
                if abs(distance - avg) > 0.15:  
                    print(f"  ⚠️ {name} distance unstable ({distance:.3f} vs avg {avg:.3f})")
                    label = f"{name} (unstable)"
                    color = (0, 165, 255) 
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, label, (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    continue

           
            current_frame_matches.append((name, distance))
            detection_history[name].append(frame_count)
            
            
            detection_history[name] = [fc for fc in detection_history[name] 
                                       if frame_count - fc < 50]
            
            
            recent_appearances = sum(1 for fc in detection_history[name] 
                                     if frame_count - fc < TEMPORAL_WINDOW * FRAME_SKIP)
            
            if recent_appearances < 1:
                print(f"  ⚠️ {name} - waiting for temporal consistency ({recent_appearances}/2)")
                label = f"{name} (verifying...)"
                color = (0, 255, 255)  #black
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label, (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                continue

            
            record["count"] += 1
            record["distances"].append(distance)

            if record["first_seen"] is None:
                record["first_seen"] = datetime.now().strftime("%H:%M:%S")

            if record["count"] >= MIN_DETECTIONS:
                record["present"] = True

            label = f"{name} ({name_to_id.get(name, 'N/A')})"
            print(f"✅ MATCH: {label} | dist={distance:.3f} | count={record['count']}")
            color = (0, 255, 0)

        else:
            label = "Unknown"
            color = (0, 0, 255)

        
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x, y - text_h - 10), (x + text_w + 10, y), color, -1)
        cv2.putText(frame, label, (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        
        if name != "Unknown":
            confidence = max(0, 1 - distance)
            bar_width = int(w * confidence)
            cv2.rectangle(frame, (x, y+h+20), (x + bar_width, y+h+25), color, -1)
        
        
        if name != "Unknown":
            dist_text = f"d={distance:.3f}"
            cv2.putText(frame, dist_text, (x, y + h + 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

   
    present_count = sum(1 for x in attendance.values() if x["present"])
    
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (300, 80), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)
    
    cv2.putText(frame, f"Present: {present_count}/{len(attendance)}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    
    cv2.putText(frame, f"Frame: {frame_count}",
                (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

    cv2.imshow("AI Attendance", frame)

    if cv2.waitKey(30) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()


print("\n📊 FINAL ATTENDANCE\n")

present = []
absent = []

for name, data in attendance.items():
    student_id = name_to_id.get(name, "N/A")

    if data["present"]:
        present.append(name)
        print(f"✅ {name} (ID: {student_id}) - {data['count']} detections")
    else:
        absent.append(name)

print("\n❌ ABSENT:")
for name in absent:
    print(f"• {name} (ID: {name_to_id.get(name, 'N/A')}) - {attendance[name]['count']} detections")