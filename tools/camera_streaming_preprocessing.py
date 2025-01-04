import threading
from queue import Queue

import cv2
import numpy as np
from ultralytics import YOLO

from tools.run_VideoMAEmodel import RunVideoMAEmodel


class CameraStreamingPreprocessing:
    def __init__(self, frame_size: tuple, fps: int, yolo_path: str):
        self.frame_size = frame_size
        self.fps = fps
        self.yolo = YOLO(yolo_path)
        self.previous_center = None
        self.selected_group = None
        self.attention_frames = []
        self.current_prediction = None

        # Initialize VideoMAE model
        self.videomae = RunVideoMAEmodel("models/VideoMAE")

        # Create queue for attention frames
        self.attention_queue = Queue()

        # Start prediction thread
        self.prediction_thread = threading.Thread(target=self.prediction_worker)
        self.prediction_thread.daemon = True
        self.prediction_thread.start()

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

                if any(
                    self.euclidean_distance(centers[k], centers[j]) < threshold
                    for k in group
                ):
                    group.append(j)
                    visited[j] = True

            groups.append(group)

        return groups

    def process(self, frame):
        person_boxes = []
        centers = []

        resized_frame = cv2.resize(frame, self.frame_size)
        origin_frame = resized_frame.copy()  # Save the origin for attention

        results = self.yolo.track(resized_frame, stream=True)

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
                    cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        resized_frame,
                        f"{box.conf[0]:.2f}",
                        (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

        groups = self.group_people(centers)
        attention_fr = None

        for group in groups:
            if len(group) < 2:  # Minimum 2 people
                if self.previous_center:
                    prev_x, prev_y = self.previous_center
                    self.selected_group = (prev_x, prev_y)
                continue

            if len(group) > 4:  # Maximum 4 people
                group = group[:4]

            group_centers = [centers[idx] for idx in group]
            avg_center_x = int(np.mean([c[0] for c in group_centers]))
            avg_center_y = int(np.mean([c[1] for c in group_centers]))

            if self.previous_center:
                prev_x, prev_y = self.previous_center
                if (
                    self.euclidean_distance(
                        (avg_center_x, avg_center_y), (prev_x, prev_y)
                    )
                    > 20
                ):
                    self.selected_group = (prev_x, prev_y)
                    continue
            self.previous_center = (avg_center_x, avg_center_y)
            self.selected_group = (avg_center_x, avg_center_y)

        if self.selected_group:
            avg_center_x, avg_center_y = self.selected_group
            size = 320
            half_size = size // 2
            top_left_x = max(avg_center_x - half_size, 0)
            top_left_y = max(avg_center_y - half_size, 0)
            bottom_right_x = min(avg_center_x + half_size, frame.shape[1])
            bottom_right_y = min(avg_center_y + half_size, frame.shape[0])
            cv2.rectangle(
                resized_frame,
                (top_left_x, top_left_y),
                (bottom_right_x, bottom_right_y),
                (255, 0, 0),
                2,
            )

            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            attention_fr = origin_frame[
                top_left_y:bottom_right_y, top_left_x:bottom_right_x
            ]

        return resized_frame, attention_fr

    def update(self, frame):
        """Process frame and update prediction"""
        processed_frame, attention_frame = self.process(frame)

        # Add attention frame to batch if exists
        if attention_frame is not None:
            self.attention_frames.append(attention_frame)
            if len(self.attention_frames) == 16:
                # Put batch in queue for processing
                self.attention_queue.put(self.attention_frames.copy())
                self.attention_frames = []

        # Draw current prediction if exists
        if self.current_prediction:
            cv2.putText(
                processed_frame,
                f"Prediction: {self.current_prediction}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        return processed_frame

    def prediction_worker(self):
        """Worker thread for processing attention frames"""
        while True:
            attention_batch = self.attention_queue.get()
            if attention_batch is None:
                break

            try:
                # Process through VideoMAE
                tensor_frames = self.videomae.transform(attention_batch)
                logits = self.videomae.run(tensor_frames)
                self.current_prediction = self.videomae.get_predict(logits)
            except Exception as e:
                print(f"Prediction error: {str(e)}")

    def cleanup(self):
        """Clean up resources"""
        self.attention_queue.put(None)  # Signal thread to stop
        if hasattr(self, "prediction_thread"):
            self.prediction_thread.join()
