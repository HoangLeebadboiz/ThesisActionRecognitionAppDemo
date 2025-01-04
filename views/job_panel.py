import os

import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from tools.video_preprocessing import VideoPreprocessing
from views.video_viewer import VideoViewer


class JobPanel(QFrame):
    # Add signal to communicate with main window
    videoSelected = QtCore.pyqtSignal(str)  # Signal to emit video path
    closed = QtCore.pyqtSignal()  # Add closed signal
    processedVideoReady = QtCore.pyqtSignal(list, int)  # For processed frames

    def __init__(self, job_path: str):
        super().__init__()
        self.job_path = job_path
        self.job_name = os.path.basename(job_path)

        # Set frame properties
        self.setObjectName("jobPanel")
        self.setStyleSheet(
            """
            #jobPanel {
                background: #1E1E1E;
                border-left: 2px solid #444;
                border-bottom: 2px solid #444;
                border-bottom-left-radius: 15px;
            }
        """
        )

        # Get screen size for panel dimensions
        screen = QApplication.desktop().screenGeometry()
        self.panel_width = screen.width() // 4
        # self.panel_height = int(
        #     screen.height() * 2 / 3
        # )  # Set height to 2/3 of screen height

        # Create widgets
        self.headerLabel = QLabel(self.job_name)
        self.closeBtn = QPushButton()  # Add close button
        self.widthInput = QSpinBox()
        self.heightInput = QSpinBox()
        self.fpsInput = QSpinBox()

        # Add mode and model combo boxes
        self.modeComboBox = QComboBox()
        self.modelComboBox = QComboBox()
        self.sourceComboBox = QComboBox()

        # Add video control buttons
        self.showVideosBtn = QPushButton("Show Video")
        self.addVideoBtn = QPushButton("Add Videos")

        # Setup combo boxes
        self.modeComboBox.addItems(["None", "Train", "Inference"])
        self.modelComboBox.addItems(["VideoMAE", "ViViT", "Pose+Transformer"])
        self.sourceComboBox.addItems(["Video", "Camera"])

        # Style all combo boxes
        combo_style = """
            QComboBox {
                font-size: 30px;
                padding: 12px;
                border: 2px solid #444;
                border-radius: 8px;
                background: #2A2A2A;
                color: white;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #2196F3;
                background: #333333;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow-down.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                font-size: 20px;
                background: #2A2A2A;
                border: 2px solid #2196F3;
                border-radius: 8px;
                selection-background-color: #2196F3;
                padding: 8px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 35px;
                padding: 8px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: rgba(33, 150, 243, 0.1);
            }
        """

        # Apply style to all combo boxes
        for combo in [self.modeComboBox, self.modelComboBox, self.sourceComboBox]:
            combo.setStyleSheet(combo_style)

        # Style close button
        self.closeBtn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
            """
        )

        # Set close button icon
        icon_path = os.path.dirname(os.path.abspath(__file__))
        self.closeBtn.setIcon(
            QtGui.QIcon(os.path.join(icon_path, "../icons/close.png"))
        )
        self.closeBtn.setIconSize(QtCore.QSize(48, 48))
        self.closeBtn.setFixedSize(50, 50)

        # Configure spinboxes
        for spinbox in [self.widthInput, self.heightInput]:
            spinbox.setRange(1, 9999)
            spinbox.setSingleStep(10)

        self.fpsInput.setRange(1, 120)
        self.fpsInput.setSingleStep(1)

        # Set default values
        self.widthInput.setValue(1920)
        self.heightInput.setValue(1080)
        self.fpsInput.setValue(30)

        # Style spinboxes
        spinbox_style = """
            QSpinBox {
                font-size: 30px;
                padding: 8px 15px;
                border: 2px solid #444;
                border-radius: 8px;
                background: #2A2A2A;
                color: white;
                min-width: 200px;
                min-height: 50px;
            }
            QSpinBox:hover {
                border-color: #2196F3;
                background: #333333;
            }
            QSpinBox:focus {
                border-color: #2196F3;
                background: #333333;
            }
            QSpinBox::up-button {
                width: 20px;
                height: 8px;  /* Half of min-height - 1px border */
                border: none;
                border-left: 2px solid #444;
                border-bottom: 1px solid #444;
                background: #2A2A2A;
                border-top-right-radius: 8px;
                margin-right: 5px;  /* Add margin from right edge */
            }
            QSpinBox::down-button {
                width: 20px;
                height: 8px;  /* Half of min-height - 1px border */
                border: none;
                border-left: 2px solid #444;
                border-top: 1px solid #444;
                background: #2A2A2A;
                border-bottom-right-radius: 8px;
                margin-right: 5px;  /* Add margin from right edge */
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #404040;
            }
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
                background: #505050;
            }
            QSpinBox::up-arrow {
                image: url(icons/arrow-up.png);
                width: 16px;
                height: 16px;
                margin-top: 5px;  /* Center arrow vertically */
            }
            QSpinBox::down-arrow {
                image: url(icons/arrow-down.png);
                width: 16px;
                height: 16px;
                margin-bottom: 5px;  /* Center arrow vertically */
            }
            QSpinBox::up-arrow:disabled, QSpinBox::down-arrow:disabled {
                opacity: 0.5;
            }
        """

        self.widthInput.setStyleSheet(spinbox_style)
        self.heightInput.setStyleSheet(spinbox_style)
        self.fpsInput.setStyleSheet(spinbox_style)

        self.InitUI()
        self.setupAnimation()

        # Store model paths
        self.yolo_path = os.path.join(
            os.path.dirname(__file__), "../models/yolo11s-pose.pt"
        )

        # Connect signals
        self.modeComboBox.currentTextChanged.connect(self.onModeChanged)
        self.showVideosBtn.clicked.connect(self.showVideos)

        # Initially disable add video button if mode is None
        self.addVideoBtn.setEnabled(False)

    def InitUI(self):
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)

        # Create header layout with close button
        headerLayout = QHBoxLayout()
        headerLayout.addWidget(
            self.closeBtn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        headerLayout.addStretch()
        headerLayout.addWidget(
            self.headerLabel, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        headerLayout.addStretch()

        mainLayout.addLayout(headerLayout)

        # Style header
        self.headerLabel.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2196F3;
                padding: 10px 0;
            }
        """
        )

        # Style group boxes
        group_style = """
            QGroupBox {
                font-size: 22px;
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 12px;
                margin-top: 20px;
                padding: 25px;
                background: rgba(42, 42, 42, 0.7);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px;
                color: #2196F3;
            }
        """

        # Create and style video settings group box
        videoSettingsGroup = QGroupBox("Video Settings")
        videoSettingsGroup.setStyleSheet(group_style)

        # Form layout for settings
        formLayout = QFormLayout()
        formLayout.setSpacing(15)
        formLayout.setContentsMargins(20, 25, 20, 25)

        # Add form fields in correct order
        formLayout.addRow("Width:", self.widthInput)
        formLayout.addRow("Height:", self.heightInput)
        formLayout.addRow("FPS:", self.fpsInput)
        formLayout.addRow("Mode:", self.modeComboBox)
        formLayout.addRow("Model:", self.modelComboBox)
        formLayout.addRow("Source:", self.sourceComboBox)  # Move to bottom of form

        videoSettingsGroup.setLayout(formLayout)

        # Style buttons
        button_style = """
            QPushButton {
                font-size: 30px;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                border: none;
                color: white;
                min-width: 160px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #42A5F5, stop:1 #1E88E5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #1976D2, stop:1 #1565C0);
                padding-top: 16px;
                padding-bottom: 14px;
            }
        """

        # Load button style
        self.showVideosBtn.setStyleSheet(button_style)
        self.addVideoBtn.setStyleSheet(button_style)

        # Create video control group box with same style
        videoControlGroup = QGroupBox("Video Control")
        videoControlGroup.setStyleSheet(group_style)

        # Add shadow effect to group boxes
        for group in [videoSettingsGroup, videoControlGroup]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QtGui.QColor(0, 0, 0, 80))
            shadow.setOffset(0, 5)
            group.setGraphicsEffect(shadow)

        # Create layout for video control buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(15)
        buttonLayout.setContentsMargins(20, 25, 20, 25)

        # Add icons to buttons
        icon_path = os.path.dirname(os.path.abspath(__file__))
        self.showVideosBtn.setIcon(
            QtGui.QIcon(os.path.join(icon_path, "../icons/show-video.png"))
        )
        self.addVideoBtn.setIcon(
            QtGui.QIcon(os.path.join(icon_path, "../icons/add-video.png"))
        )

        for btn in [self.showVideosBtn, self.addVideoBtn]:
            btn.setIconSize(QtCore.QSize(24, 24))

        # Add buttons to layout
        buttonLayout.addWidget(self.showVideosBtn)
        buttonLayout.addWidget(self.addVideoBtn)

        videoControlGroup.setLayout(buttonLayout)

        # Add all widgets to main layout
        mainLayout.addWidget(videoSettingsGroup)
        mainLayout.addStretch(8)
        mainLayout.addWidget(videoControlGroup)
        mainLayout.addStretch(1)

        # Connect buttons
        self.closeBtn.clicked.connect(self.closePanel)
        self.addVideoBtn.clicked.connect(self.addVideo)
        self.showVideosBtn.clicked.connect(self.showVideos)

        self.setLayout(mainLayout)
        self.setFixedWidth(self.panel_width)
        # self.setFixedHeight(self.panel_height)  # Set fixed height

        # Set initial position off-screen to the right and align top
        self.move(QApplication.desktop().screenGeometry().width(), 0)

    def setupAnimation(self):
        # Create slide animation from right
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        screen_width = QApplication.desktop().screenGeometry().width()
        # Keep the panel at top of screen
        self.animation.setStartValue(QtCore.QPoint(screen_width, 0))
        self.animation.setEndValue(QtCore.QPoint(screen_width - self.panel_width, 0))
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        QtCore.QTimer.singleShot(100, self.animation.start)

    def addVideo(self):
        # TODO: Implement video addition functionality
        pass

    def showVideos(self):
        if self.sourceComboBox.currentText() == "Video":
            # Existing video file selection code
            file_dialog = QFileDialog()
            video_path, _ = file_dialog.getOpenFileName(
                self,
                "Select Video",
                "",
                "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)",
            )

            if not video_path:
                return

            if self.modeComboBox.currentText() == "None":
                self.videoSelected.emit(video_path)
            else:
                # Process video for inference mode
                # Get settings from input fields
                frame_size = (self.widthInput.value(), self.heightInput.value())
                fps = self.fpsInput.value()

                try:
                    # Initialize video preprocessing
                    video_processor = VideoPreprocessing(
                        video_path=video_path,
                        frame_size=frame_size,
                        fps=fps,
                        yolo_path=self.yolo_path,
                    )

                    # Process video
                    frames_dict = video_processor.process_video()
                    processed_frames = frames_dict["processed_frames"]

                    # Convert frames from BGR to RGB
                    rgb_frames = []
                    for frame in processed_frames:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        rgb_frames.append(frame_rgb)

                    # Emit signal with processed frames and fps
                    self.processedVideoReady.emit(rgb_frames, fps)

                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Error processing video: {str(e)}",
                        QMessageBox.Ok,
                    )

        elif self.sourceComboBox.currentText() == "Camera":
            # Get settings from input fields
            frame_size = (self.widthInput.value(), self.heightInput.value())
            fps = self.fpsInput.value()

            if self.modeComboBox.currentText() == "None":
                self.videoSelected.emit("camera://0")
            else:  # Inference mode
                self.videoSelected.emit(
                    f"camera://0?inference=true&fps={fps}&width={frame_size[0]}&height={frame_size[1]}"
                )

    def closePanel(self):
        # Create reverse animation
        self.closeAnimation = QPropertyAnimation(self, b"pos")
        self.closeAnimation.setDuration(300)
        screen_width = QApplication.desktop().screenGeometry().width()

        # Animate panel back to the right
        self.closeAnimation.setStartValue(
            QtCore.QPoint(screen_width - self.panel_width, 0)
        )
        self.closeAnimation.setEndValue(QtCore.QPoint(screen_width, 0))
        self.closeAnimation.setEasingCurve(QtCore.QEasingCurve.InCubic)

        # Connect animation finished signal
        def onFinished():
            self.closed.emit()
            self.deleteLater()

        self.closeAnimation.finished.connect(onFinished)
        self.closeAnimation.start()

    def onModeChanged(self, mode: str):
        """Handle mode selection change"""
        # Enable show video button for all modes
        self.showVideosBtn.setEnabled(True)

        # Only disable add video button
        self.addVideoBtn.setEnabled(False)

        # Update button styles
        self.updateButtonStyle(self.addVideoBtn, False)
        self.updateButtonStyle(self.showVideosBtn, True)

    def updateButtonStyle(self, button, enabled):
        """Update button style based on enabled state"""
        if not enabled:
            button.setStyleSheet(
                """
                QPushButton {
                    font-size: 30px;
                    font-weight: bold;
                    padding: 15px 25px;
                    border-radius: 10px;
                    background: #2A2A2A;
                    border: 2px solid #444;
                    color: #666666;
                    min-width: 160px;
                    opacity: 0.7;
                }
                QPushButton:disabled {
                    background: #2A2A2A;
                    border: 2px solid #444;
                    color: #666666;
                }
                """
            )
        else:
            button.setStyleSheet(
                """
                QPushButton {
                    font-size: 30px;
                    font-weight: bold;
                    padding: 15px 25px;
                    border-radius: 10px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #2196F3, stop:1 #1976D2);
                    border: none;
                    color: white;
                    min-width: 160px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #42A5F5, stop:1 #1E88E5);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #1976D2, stop:1 #1565C0);
                }
                """
            )
