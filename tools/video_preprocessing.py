import os

import cv2
import numpy as np
import torch
from ultralytics import YOLO


class VideoProcessing:
    def __init__(self, video_path: str, fps: int, yolo_path: str):
        self.video_path = video_path
        self.fps = fps
        self.yolo = YOLO(yolo_path)
        self.frame_size = (640, 480)
        self.previous_center = None
        self.attention = 320
        self.selected_group = None

    def euclidean_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def group_people(self, centers, threshold=150):
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
                    self.euclidean_distance(centers[k], centers[j]) < threshold for k in group
                ):
                    group.append(j)
                    visited[j] = True

            groups.append(group)

        return groups

    def process(self, frame):

        person_boxes = []
        centers = []
        

        resized_frame = cv2.resize(frame, (640, 480))

        origin_frame = resized_frame.copy()  # Save the origin for attention
        # print(origin_frame.shape)

        results = self.yolo.track(resized_frame, stream=True)

        for result in results:
            for box in result.boxes:
                if box.conf[0] > 0.4:
                    [x1, y1, x2, y2] = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cls = int(box.cls[0])

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

        print(f'Group people: {groups}')
        print(f'1st Previous = {self.previous_center}')
        

        for group in groups:

            if len(group) < 2:  # Giới hạn dưới là 2 người
                prev_x, prev_y = self.previous_center
                self.selected_group = (prev_x, prev_y)
                continue

            if len(group) > 4:  # Giới hạn tối đa 4 người
                group = group[:4]

            group_centers = [centers[idx] for idx in group]
            avg_center_x = int(np.mean([c[0] for c in group_centers]))
            avg_center_y = int(np.mean([c[1] for c in group_centers]))

            if self.previous_center:
                prev_x, prev_y = self.previous_center
                if (
                    self.euclidean_distance((avg_center_x, avg_center_y), (prev_x, prev_y) ) > 50):
                    self.selected_group = (prev_x, prev_y)
                    continue
            
            print(f"Center: {avg_center_x}, {avg_center_y}")
            
            self.previous_center = (avg_center_x, avg_center_y)
            self.selected_group = (avg_center_x, avg_center_y)

        print(f'Select group:{self.selected_group}')
        print("-------------------------------------------------")

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
            # attention_fr = None
            attention_fr = origin_frame[
                top_left_y:bottom_right_y, top_left_x:bottom_right_x
            ]
            # attention_frame = origin_frame
            # print(f"Frame size: {frame.shape}")
            # print(f"Origin Frame size: {origin_frame.shape}")
        print(f'2nd Previous = {self.previous_center}')

        return resized_frame, attention_fr
        
        

    def process_video(self):
        """Process video and extract frames with attention detection

        Returns:
            dict: Dictionary containing:
                - original_frames: List of original frames without any processing
                - processed_frames: List of frames with detection boxes and attention window
                - attention_frames: List of cropped attention frames
                - frames: List of resized frames with detection
                - total_frames: Total number of frames in video
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Error opening video file: {self.video_path}")

        original_frames = []  # Store original frames
        processed_frames = []  # Store frames with boxes at original size
        frames = []  # Store resized frames with detection
        attention_frames = []  # Store cropped attention frames

        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_size = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

        # Calculate frame sampling interval
        sample_interval = max(1, int(video_fps / self.fps))
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame according to fps
            if frame_count % sample_interval == 0:
                # try:
                # attention_frame = None
                # Store original frame
                original_frames.append(frame.copy())

                # Process frame and get results
                processed_frame, attention_frame = self.process(frame)

                # print(f"Frame size: {processed_frame.shape}")
                # print(f"Origin Frame size: {attention_frame.shape}")

                # Resize processed frame back to original size
                processed_frame_orig_size = cv2.resize(
                    processed_frame, (original_size[0], original_size[1])
                )

                # Store all frame types
                frames.append(processed_frame)  # Resized with detection
                processed_frames.append(
                    processed_frame_orig_size
                )  # Original size with detection
                if attention_frame is not None:
                    attention_frames.append(attention_frame)

                # except Exception as e:
                #     print(f"Error processing frame {frame_count}: {str(e)}")

            frame_count += 1

        cap.release()
        return {
            "original_frames": original_frames,  # Original frames without processing
            "processed_frames": processed_frames,  # Original size with detection boxes
            "frames": frames,  # Resized frames with detection
            "attention_frames": attention_frames,  # Cropped attention frames
            "total_frames": total_frames,
        }

    def show_processed_video(self, frames, fps=30, window_name="Processed Video"):
        """Show processed frames as video

        Args:
            frames: List of frames to display
            fps: Frames per second for display
            window_name: Name of the display window
        """
        if not frames:
            print("No frames to display")
            return

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        for frame in frames:
            cv2.imshow(window_name, frame)

            # Break loop on 'q' press
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()


# Example usage:
video_preprocessing = VideoProcessing(
    video_path="Data\Physical Harassment\Physical_00068_HoangLee.mp4",
    fps=20,
    yolo_path="HarassmentBehaviorDetectionThesisProject\yolo11n-pose.pt",
)

frames_dict = video_preprocessing.process_video()
processed_frames = frames_dict["attention_frames"]

# Show the processed video
video_preprocessing.show_processed_video(processed_frames, fps=30)
