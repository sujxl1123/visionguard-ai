import cv2
import time
import datetime

from config import CAMERA_INDEX, FRAME_INTERVAL
from database import upsert_detection


def run_entry_capture(session_id, conn, stop_event):
    # Mac-friendly camera backend
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("❌ Camera not opening")
        return

    print("✅ Camera opened")
    print("[CAPTURE] Press Q to stop manually.")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    frame_count = 0
    last_logged = {}

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue

        # Resize for speed
        frame = cv2.resize(frame, (640, 480))
        frame_count += 1

        # Show preview smoothly, but do detection only every 3rd frame
        if frame_count % 3 != 0:
            cv2.imshow("Smart Entrance Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:
            # Temporary dummy identity for testing
            student_id = "test_student"
            confidence = 0.90

            now_ts = time.time()

            # Avoid writing same student repeatedly every frame
            if student_id in last_logged and (now_ts - last_logged[student_id] < 2):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    student_id,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )
                continue

            last_logged[student_id] = now_ts
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            upsert_detection(conn, session_id, student_id, confidence, timestamp)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{student_id} ({confidence:.2f})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Smart Entrance Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(FRAME_INTERVAL)

    cap.release()
    cv2.destroyAllWindows()
    print("[CAPTURE] Stopped.")