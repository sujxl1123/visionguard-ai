import cv2
import numpy as np
from ultralytics import YOLO

class CrowdCounter:
    def __init__(self, model_size='n'):
        self.model = YOLO(f'yolov8{model_size}.pt')
        self.total_count = 0
        self.density_map = None
        
    def count_people(self, frame):
        results = self.model(frame, classes=[0], verbose=False)
        count = 0
        boxes = None
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                count = len(boxes)
        return count, boxes
    
    def get_risk_level(self, count, capacity=100):
        ratio = count / capacity if capacity > 0 else 0
        if ratio < 0.5:
            return "Low", "#00C851"
        elif ratio < 0.75:
            return "Medium", "#ffbb33"
        elif ratio < 0.9:
            return "High", "#ff8800"
        else:
            return "Critical", "#ff4444"
    
    def process_video(self, video_path, skip_frames=5):
        cap = cv2.VideoCapture(video_path)
        counts = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            count, _ = self.count_people(frame)
            counts.append(count)
        cap.release()
        return {
            "max": max(counts) if counts else 0,
            "avg": sum(counts)/len(counts) if counts else 0,
            "counts": counts
        }