<h1 align="center">Harassment Behavior Recognition Application</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

</div>

<p align="center">
  A desktop application for real-time harassment behavior detection and analysis using deep learning models.
</p>

## 📝 Table of Contents
- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [✨ Features ](#-features-)
  - [Video Processing](#video-processing)
  - [Processing Modes](#processing-modes)
  - [Workspace Management](#workspace-management)
- [💻 System Requirements ](#-system-requirements-)
- [⚙️ Installation ](#️-installation-)
- [🎈 Usage ](#-usage-)
- [📁 Project Structure ](#-project-structure-)
- [🛠️ Built With ](#️-built-with-)
- [✍️ Authors ](#️-authors-)
- [🎉 Acknowledgments ](#-acknowledgments-)

## 🧐 About <a name="about"></a>
This application provides real-time detection and analysis of harassment behavior in videos using state-of-the-art deep learning models. It supports both video file processing and live camera feeds, making it suitable for both post-event analysis and real-time monitoring.

## ✨ Features <a name="features"></a>

### Video Processing
- Support for multiple video formats (mp4, avi, mkv, mov)
- Real-time camera feed processing
- Adjustable frame size and FPS
- Person detection and tracking
- Behavior analysis and classification

### Processing Modes
- **None Mode**: Direct video playback
- **Inference Mode**: Real-time harassment behavior detection
- **Training Mode**: Model training capabilities (upcoming)

### Workspace Management
- Multi-job support
- Video organization
- Configuration management
- Result tracking

## 💻 System Requirements <a name="requirements"></a>
- Python 3.8+
- NVIDIA GPU (recommended for inference)
- 8GB RAM minimum
- Webcam (for camera mode)

## ⚙️ Installation <a name="installation"></a>

1. Clone the repository:
```bash
git clone https://github.com/HoangLeebadboiz/ThesisActionRecognitionAppDemo.git
cd ThesisActionRecognitionAppDemo
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required models:
- Place YOLO model (`yolo11s-pose.pt`) in `models/` directory
- Place VideoMAE model in `models/VideoMAE/` directory

## 🎈 Usage <a name="usage"></a>

1. Start the application:
```bash
python main.py
```

2. Login or create new account

3. Create a new job:
   - Click "Create Job"
   - Enter job name
   - Configure settings

4. Process videos:
   - Select video source (File/Camera)
   - Choose processing mode
   - Adjust frame size and FPS
   - Click "Show Video" to begin processing

## 📁 Project Structure <a name="structure"></a>
```
├── main.py                 # Application entry point
├── views/                  # UI components
├── tools/                  # Processing utilities
├── models/                 # AI models
├── database/              # User data
└── workspace/             # Job storage
```

## 🛠️ Built With <a name="built_with"></a>
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI Framework
- [OpenCV](https://opencv.org/) - Video Processing
- [PyTorch](https://pytorch.org/) - Deep Learning
- [Ultralytics YOLO](https://github.com/ultralytics/yolov5) - Object Detection
- [VideoMAE](https://github.com/MCG-NJU/VideoMAE) - Video Understanding

## ✍️ Authors <a name="authors"></a>
- [@HoangLee](https://github.com/HoangLeebadboiz) - Initial work

## 🎉 Acknowledgments <a name="acknowledgments"></a>
- VideoMAE team for the pre-trained models
- Ultralytics for YOLO implementation
- PyQt5 community for GUI components
