import cv2
import numpy as np
from ultralytics import YOLO


class VideoPreprocessing:
    def __init__(self, video_path: str, frame_size, fps: int, yolo_path: str):
        self.video_path = video_path
        self.fps = fps
        self.yolo = YOLO(yolo_path)
        self.frame_size = frame_size
        self.previous_center = None
        self.attention = 320
        self.selected_group = None

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

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Error opening video file: {self.video_path}")

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_interval = max(1, int(video_fps / self.fps))

        processed_frames = []
        attention_frames = []
        frame_indices = []  # Track which frames have attention
        current_prediction = None
        frame_count = 0
        current_idx = 0

        # Initialize VideoMAE model
        from tools.run_VideoMAEmodel import RunVideoMAEmodel

        videomae = RunVideoMAEmodel("models/VideoMAE")

        while cap.isOpened():
            ret, frame = cap.read()
            # original_size = frame.size
            if not ret:
                break

            if frame_count % sample_interval == 0:
                original_size = frame.shape
                processed_frame, attention_frame = self.process(frame)

                if attention_frame is not None:
                    attention_frames.append(attention_frame)
                    frame_indices.append(current_idx)

                    # When we have 16 attention frames, process them
                    if len(attention_frames) == 16:
                        # Get prediction from VideoMAE
                        tensor_frames = videomae.transform(attention_frames)
                        logits = videomae.run(tensor_frames)
                        new_prediction = videomae.get_predict(logits)

                        # Update prediction if changed
                        if new_prediction != current_prediction:
                            current_prediction = new_prediction

                        # Clear batch
                        attention_frames = []
                        frame_indices = []

                # Draw current prediction if exists
                if current_prediction:
                    cv2.putText(
                        processed_frame,
                        f"Prediction: {current_prediction}",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )

                processed_frames.append(
                    cv2.resize(processed_frame, (original_size[1], original_size[0]))
                )
                current_idx += 1

            frame_count += 1

        # Process remaining attention frames if any
        if attention_frames:
            # Pad to 16 frames if needed
            while len(attention_frames) < 16:
                attention_frames.append(attention_frames[-1])

            tensor_frames = videomae.transform(attention_frames)
            logits = videomae.run(tensor_frames)
            current_prediction = videomae.get_predict(logits)

        cap.release()

        return {
            "processed_frames": processed_frames,
            "total_frames": total_frames,
        }
