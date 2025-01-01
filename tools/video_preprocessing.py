class VideoProcessing:
    def __init__(self, video_path, output_path):
        self.video_path = video_path
        self.output_path = output_path

    def extract_frames(self):
        # Extract frames from video
        pass

    def resize_frames(self):
        # Resize frames
        pass

    def extract_audio(self):
        # Extract audio from video
        pass

    def extract_frames_and_audio(self):
        self.extract_frames()
        self.extract_audio()
