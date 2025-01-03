import json
import os

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoProcessor, VideoMAEForVideoClassification


class RunVideoMAEmodel:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.image_processor = AutoProcessor.from_pretrained(model_path)
        self.VideoMAE_model = VideoMAEForVideoClassification.from_pretrained(model_path)

        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.VideoMAE_model = self.VideoMAE_model.to(self.device)

    def transform(self, frames):
        """Transform frames for model input"""
        if len(frames) < 16:
            # Pad with last frame if needed
            last_frame = frames[-1]
            frames.extend([last_frame] * (16 - len(frames)))

        transformed = self.image_processor(frames, return_tensors="pt")
        return transformed["pixel_values"].to(self.device)

    def run(self, tensor_frames):
        with torch.no_grad():
            outputs = self.VideoMAE_model(tensor_frames)
            return outputs.logits

    def get_predict(self, logits):
        predicted_class_id = logits.argmax(-1).item()
        return self.VideoMAE_model.config.id2label[predicted_class_id]
