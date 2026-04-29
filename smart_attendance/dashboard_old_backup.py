import cv2
import json
from datetime import datetime
from ultralytics import YOLO

# ================= CONFIG =================
VIDEO_PATH = "crowd_input.mp4"
OUTPUT_JSON = "crowd_results.json"
OUTPUT_CSV = "crowd_frame_counts.csv"

MODEL_NAME = "yolov8s.pt"
CONF = 0.40
IOU = 0.55
FRAME_SKIP = 2
MIN_BOX_AREA = 2500

# ================= INIT =================
model = YOLO(MODEL_NAME)

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError("❌ Cannot open crowd_input.mp4")

frame_no = 0
processed_frames = 0

frame_data = []
max_people_in_frame = 0
total_people_sum = 0

print("🚀 Visible Crowd Counter Started")

# ================= HELPERS =================
def box_area(box):
    x1, y1, x2, y2 = box
    return max(0, (x2 - x1)) * max(0, (y2 - y1))


# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_no += 1

    if frame_no % FRAME_SKIP != 0:
        continue

    processed_frames += 1

    results = model(
        frame,
        classes=[0],  # person only
        conf=CONF,
        iou=IOU,
        verbose=False
    )

    people_in_frame = 0

    if results and len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()

        for box in boxes:
            if box_area(box) < MIN_BOX_AREA:
                continue
            people_in_frame += 1

    max_people_in_frame = max(max_people_in_frame, people_in_frame)
    total_people_sum += people_in_frame

    frame_data.append({
        "frame": int(frame_no),
        "people_in_frame": int(people_in_frame),
        "unique_people_so_far": int(max_people_in_frame)
    })

    if frame_no % 50 == 0:
        print(
            f"Frame {frame_no} | People visible: {people_in_frame} | "
            f"Estimated total people: {max_people_in_frame}"
        )

cap.release()

# ================= FINAL =================
estimated_total_people = max_people_in_frame
average_people = round(total_people_sum / processed_frames, 2) if processed_frames else 0

if estimated_total_people < 50:
    risk = "Low"
elif estimated_total_people < 150:
    risk = "Medium"
elif estimated_total_people < 300:
    risk = "High"
else:
    risk = "Critical"

result = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_unique_people": int(estimated_total_people),
    "max_people_in_frame": int(max_people_in_frame),
    "average_people_per_frame": float(average_people),
    "risk": risk,
    "frames_processed": int(processed_frames),
    "model": MODEL_NAME,
    "confidence": CONF,
    "counting_mode": "Maximum visible people in video",
    "frames": frame_data
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(result, f, indent=4)

with open(OUTPUT_CSV, "w") as f:
    f.write("frame,people_in_frame,unique_people_so_far\n")
    for row in frame_data:
        f.write(
            f"{row['frame']},{row['people_in_frame']},{row['unique_people_so_far']}\n"
        )

print("\n✅ crowd_results.json saved")
print("✅ crowd_frame_counts.csv saved")
print(f"Estimated Total People: {estimated_total_people}")
print(f"Max People in Frame: {max_people_in_frame}")
print(f"Average People per Frame: {average_people}")
print(f"Risk: {risk}")