import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class JobPanel(QFrame):
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
                border-left: 2px solid #333;
                border-bottom: 2px solid #333;
                border-bottom-left-radius: 10px;
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
        self.widthInput = QLineEdit()
        self.heightInput = QLineEdit()
        self.fpsInput = QLineEdit()
        self.addVideoBtn = QPushButton("Add Video")

        # Set validators for numeric input
        self.widthInput.setValidator(QtGui.QIntValidator(1, 9999))
        self.heightInput.setValidator(QtGui.QIntValidator(1, 9999))
        self.fpsInput.setValidator(QtGui.QIntValidator(1, 120))

        # Set default values
        self.widthInput.setText("1920")
        self.heightInput.setText("1080")
        self.fpsInput.setText("30")

        self.InitUI()
        self.setupAnimation()

    def InitUI(self):
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)

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
        mainLayout.addWidget(self.headerLabel, alignment=QtCore.Qt.AlignCenter)

        # Create and style group box
        videoSettingsGroup = QGroupBox("Video Settings")
        videoSettingsGroup.setStyleSheet(
            """
            QGroupBox {
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """
        )

        # Form layout for settings
        formLayout = QFormLayout()
        formLayout.setSpacing(15)
        formLayout.setContentsMargins(20, 25, 20, 25)

        # Style inputs
        input_style = """
            QLineEdit {
                font-size: 20px;
                padding: 12px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #333;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
            QLabel {
                font-size: 20px;
                color: white;
                font-weight: bold;
            }
        """
        self.widthInput.setStyleSheet(input_style)
        self.heightInput.setStyleSheet(input_style)
        self.fpsInput.setStyleSheet(input_style)

        # Add form fields
        formLayout.addRow("Width:", self.widthInput)
        formLayout.addRow("Height:", self.heightInput)
        formLayout.addRow("FPS:", self.fpsInput)

        videoSettingsGroup.setLayout(formLayout)

        # Style add video button
        self.addVideoBtn.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 8px;
                background: #2196F3;
                border: none;
                color: white;
                min-width: 150px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
        """
        )

        # Add icon to button
        icon_path = os.path.dirname(os.path.abspath(__file__))
        self.addVideoBtn.setIcon(
            QtGui.QIcon(os.path.join(icon_path, "../icons/add-video.png"))
        )
        self.addVideoBtn.setIconSize(QtCore.QSize(24, 24))

        mainLayout.addWidget(videoSettingsGroup)
        mainLayout.addStretch(10)
        mainLayout.addWidget(self.addVideoBtn, alignment=QtCore.Qt.AlignCenter)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)
        self.setFixedWidth(self.panel_width)
        # self.setFixedHeight(self.panel_height)  # Set fixed height

        # Set initial position off-screen to the right and align top
        self.move(QApplication.desktop().screenGeometry().width(), 0)

        # Connect button
        self.addVideoBtn.clicked.connect(self.addVideo)

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
