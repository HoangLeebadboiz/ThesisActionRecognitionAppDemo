import cv2
import torch
import numpy as np
from ultralytics import YOLO

#Load the model 
yolo_path = "HarassmentBehaviorDetectionThesisProject\yolo11s-pose.pt"

video_path = "Data_test\Test_00002_KhanhToan.mp4"

class VideoProcessing:
    def __init__(self, frame, yolo_path):
       self.frame = frame
       self.yolo = YOLO(yolo_path)
       self.frame_size = (640,480)
       self.previous_center = None
       self.attention = 320

    def euclidean_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    def group_people(self, centers, threshold=120):
        n = len(centers)
        groups = []
        visited = [False] * n

        for i in range(n):
            if visited[i]:
                continue

            group = [i]
            visited[i] = True

            for j in range(i + 1, n):
                if visited[j]:
                    continue

                if any(self.euclidean_distance(centers[k], centers[j]) < threshold for k in group):
                    group.append(j)
                    visited[j] = True

            groups.append(group)

        return groups

    def process(self):

        person_boxes = []
        centers = []

        frame = cv2.resize(self.frame, (640,480))
        origin_frame = frame.copy() # Save the origin for attention
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.yolo.track(frame, stream=True)

        for result in results:
            classes_names = result.names
            for box in result.boxes:
                if box.conf[0] > 0.5:
                    [x1, y1, x2, y2] = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cls = int(box.cls[0])
                    class_name = classes_names[cls]

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    person_boxes.append((x1, y1, x2, y2))
                    centers.append((cx, cy))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f'{box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        groups = self.group_people(centers)
        selected_group = None

        for group in groups:
            if len(group) < 2: # Giới hạn dưới là 2 người
                continue

            if len(group) > 4:  # Giới hạn tối đa 4 người
                group = group[:4]

            group_centers = [centers[idx] for idx in group]
            avg_center_x = int(np.mean([c[0] for c in group_centers]))
            avg_center_y = int(np.mean([c[1] for c in group_centers]))

            if self.previous_center:
                prev_x, prev_y = self.previous_center
                if self.euclidean_distance((avg_center_x, avg_center_y), (prev_x, prev_y)) > 50:
                    selected_group = (prev_x, prev_y)
                    continue
            self.previous_center = (avg_center_x, avg_center_y)
            selected_group = (avg_center_x, avg_center_y)

        if selected_group:
            avg_center_x, avg_center_y = selected_group
            size = 320
            half_size = size // 2
            top_left_x = max(avg_center_x - half_size, 0)
            top_left_y = max(avg_center_y - half_size, 0)
            bottom_right_x = min(avg_center_x + half_size, frame.shape[1])
            bottom_right_y = min(avg_center_y + half_size, frame.shape[0])
            cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255,0,0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            attention_frame = origin_frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
            # attention_frame = origin_frame
            # print(f'Frame size: {frame.shape}')
            # print(f'Origin Frame size: {origin_frame.shape}')

        return frame, attention_frame


# yolo = YOLO("weight\yolo11s-pose.pt")

# video_path = "Data_test\Test_00002_KhanhToan.mp4"
# videoCap = cv2.VideoCapture(video_path)


# while True:
#     ret, frame = videoCap.read()
#     Task1 = VideoProcessing(frame, yolo_path)
#     show_frame, recognition_frame = VideoProcessing.process(Task1)

#     cv2.imshow('Show Frame', show_frame)
#     cv2.imshow('Attention Frame', recognition_frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
# videoCap.release()
# cv2.destroyAllWindows()

