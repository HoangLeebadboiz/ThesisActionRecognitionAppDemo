import json
import os
import sys

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from views.create_job import CreateJobView  # Import CreateJobView
from views.job_panel import JobPanel
from views.login import LoginView
from views.open_job import OpenJobView
from views.signup import SignupView
from views.video_viewer import VideoViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Action Recognition")
        self.setStyleSheet(qdarktheme.load_stylesheet())

        # Set window icon
        icon_path = os.path.abspath(__file__ + "/../icons/appicon.png")
        app_icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(app_icon)
        # Also set the application-wide icon
        QApplication.setWindowIcon(app_icon)

        # Get screen size and set window geometry
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Create widgets
        self.widget = QWidget()
        self.loginBtn = QPushButton("Login")
        self.signupBtn = QPushButton("Sign Up")
        self.jobComboBox = QComboBox()
        self.videoWidget = VideoViewer()

        # Disable job combo box and video viewer before login
        self.jobComboBox.setEnabled(False)
        self.videoWidget.setEnabled(False)
        self.videoWidget.toolbar.setEnabled(False)

        # Set icons for buttons
        icon_path = os.path.dirname(os.path.abspath(__file__))
        self.loginBtn.setIcon(QtGui.QIcon(os.path.join(icon_path, "icons/login.png")))
        self.signupBtn.setIcon(QtGui.QIcon(os.path.join(icon_path, "icons/signup.png")))

        # Set icon sizes
        self.loginBtn.setIconSize(QtCore.QSize(24, 24))
        self.signupBtn.setIconSize(QtCore.QSize(24, 24))
        self.jobComboBox.setIconSize(QtCore.QSize(32, 32))

        # Add items with job icon
        job_icon = QtGui.QIcon(os.path.join(icon_path, "icons/job.png"))
        self.jobComboBox.addItem(job_icon, "New Job")
        self.jobComboBox.addItem(job_icon, "Open Job")
        self.jobComboBox.addItem(job_icon, "Save Job")

        # Init workspace path
        self.workspace_path = os.path.abspath(__file__ + "/../workspace")
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)
        datajobs_path = os.path.join(self.workspace_path, "datajobs.json")
        if not os.path.exists(datajobs_path):
            with open(datajobs_path, "w") as f:
                json.dump({}, f)
        self.job_path = None

        # Create a container for the job panel
        self.panelContainer = QWidget(self)
        self.panelContainer.setFixedWidth(0)  # Start with zero width

        # Create job panel (hidden by default)
        self.jobPanel = None

        # user name
        self.username = None

        # Create reopen job button (hidden by default)
        self.reopenBtn = QPushButton()
        self.reopenBtn.setParent(self)  # Make it a child of MainWindow
        self.reopenBtn.setIcon(QtGui.QIcon(os.path.join(icon_path, "icons/reopen.png")))
        self.reopenBtn.setIconSize(QtCore.QSize(32, 32))
        self.reopenBtn.setFixedSize(50, 50)
        self.reopenBtn.hide()
        self.reopenBtn.setStyleSheet(
            """
            QPushButton {
                background: #2196F3;
                border: none;
                border-radius: 25px;
                padding: 5px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
            """
        )
        self.reopenBtn.clicked.connect(self.reopenJob)

        # Store video viewer reference
        self.videoViewer = None

        # Enhanced main window style
        self.setStyleSheet(
            """
            QMainWindow {
                background: #121212;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #FFFFFF;
            }
            QComboBox {
                font-size: 24px;
                padding: 12px 20px;
                border: 2px solid #2196F3;
                border-radius: 12px;
                background: #1E1E1E;
                color: white;
                min-width: 250px;
            }
            QComboBox:hover {
                border-color: #42A5F5;
                background: #262626;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow-down.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                background: #1E1E1E;
                border: 2px solid #2196F3;
                border-radius: 12px;
                selection-background-color: #2196F3;
                padding: 8px;
            }
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 10px;
                min-width: 120px;
            }
            QPushButton#loginBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                border: none;
                color: white;
            }
            QPushButton#loginBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #42A5F5, stop:1 #1E88E5);
            }
            QPushButton#signupBtn {
                background: transparent;
                border: 2px solid #2196F3;
                color: #2196F3;
            }
            QPushButton#signupBtn:hover {
                background: rgba(33, 150, 243, 0.1);
            }
            """
        )

        self.initUI()
        self.showMaximized()

    def initUI(self):
        # Create main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create top layout with modern styling
        toplayout = QHBoxLayout()
        toplayout.setSpacing(15)

        # Style job combobox
        self.jobComboBox.setStyleSheet(
            """
            QComboBox {
                font-size: 28px;
                padding: 15px 25px;
                border: 2px solid #2196F3;
                border-radius: 10px;
                background: #1E1E1E;
                min-width: 200px;
                color: #FFFFFF;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow-down.png);
                width: 20px;
                height: 20px;
            }
            QComboBox:hover {
                border-color: #42A5F5;
                background: #262626;
            }
            QComboBox QAbstractItemView {
                background: #1E1E1E;
                border: 2px solid #2196F3;
                border-radius: 10px;
                padding: 15px;
                selection-background-color: #2196F3;
                selection-color: white;
                font-size: 28px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 50px;
                padding: 10px;
            }
        """
        )

        # Set job combobox items and size
        # self.jobComboBox.addItems(["New Job", "Open Job", "Save Job"])
        self.jobComboBox.setCurrentIndex(-1)
        self.jobComboBox.setLineEdit(QLineEdit())
        self.jobComboBox.lineEdit().setText("Select Job")
        self.jobComboBox.lineEdit().setReadOnly(True)
        self.jobComboBox.setFixedHeight(70)

        # Define button base style
        button_style = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 8px;
                min-width: 100px;
                height: 40px;
            }
        """

        # Style login button
        self.loginBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: #2196F3;
                border: none;
                color: white;
                padding-left: 10px;
            }
            QPushButton:hover {
                background: #42A5F5;
            }
            QPushButton:pressed {
                background: #1E88E5;
            }
            QPushButton::icon {
                width: 24px;
                height: 24px;
                position: absolute;
                left: 10px;
                filter: brightness(0) invert(1);  /* Makes the icon white */
            }
        """
        )

        # Style signup button
        self.signupBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: transparent;
                border: 2px solid #2196F3;
                color: #2196F3;
                padding-left: 10px;
            }
            QPushButton:hover {
                background: rgba(33, 150, 243, 0.1);
            }
            QPushButton:pressed {
                background: rgba(33, 150, 243, 0.2);
            }
            QPushButton::icon {
                width: 24px;
                height: 24px;
                position: absolute;
                left: 10px;
                filter: brightness(0) saturate(100%) invert(48%) sepia(57%) saturate(2303%) hue-rotate(190deg) brightness(97%) contrast(95%);
            }
        """
        )

        # Style video widget
        self.videoWidget.setStyleSheet(
            """
            QVideoWidget {
                background: #121212;
                border: 2px solid #333333;
                border-radius: 12px;
            }
        """
        )

        # Add widgets to top layout
        toplayout.addStretch(2)  # More stretch before combo box
        toplayout.addWidget(
            self.jobComboBox,
            alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        toplayout.addStretch(2)  # More stretch before buttons
        toplayout.addWidget(self.loginBtn)
        toplayout.addWidget(self.signupBtn)
        toplayout.addSpacing(10)

        # Add layouts and widgets
        layout.addLayout(toplayout)
        layout.addWidget(self.videoWidget)

        # Set ratio of rows
        layout.setStretchFactor(toplayout, 1)
        layout.setStretchFactor(self.videoWidget, 8)

        # Set layout
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        # Connect events
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.signup)
        # Event when click item in combobox
        self.jobComboBox.currentIndexChanged.connect(self.jobComboBoxSelected)

    def login(self):
        self.loginView = LoginView()
        # Connect login success signal
        self.loginView.loginSuccess.connect(self.onLoginSuccess)
        self.loginView.username.connect(self.onUsername)
        self.loginView.show()

    def onLoginSuccess(self):
        # Enable features after successful login
        self.jobComboBox.setEnabled(True)
        self.videoWidget.setEnabled(True)
        self.videoWidget.toolbar.setEnabled(True)

    def onUsername(self, username):
        self.username = username

    def signup(self):
        self.signupView = SignupView()
        self.signupView.show()

    def jobComboBoxSelected(self, index):
        if index == -1:
            pass
        elif index == 0:
            self.createJobView = CreateJobView(self.username, self.workspace_path)
            self.createJobView.createJobSuccess.connect(self.onJob)
            self.createJobView.show()
        elif index == 1:  # Open Job
            self.openJobView = OpenJobView(self.workspace_path)
            self.openJobView.openJobSuccess.connect(self.onJob)
            self.openJobView.show()

    def onJob(self, job_path):
        self.job_path = job_path
        self.jobComboBox.setCurrentIndex(-1)
        self.jobComboBox.lineEdit().setText(os.path.basename(job_path))

        # Hide reopen button when opening job
        self.reopenBtn.hide()

        # Remove previous panel if exists
        try:
            if self.jobPanel is not None:
                self.jobPanel.close()  # Use close() instead of deleteLater()
                return  # Return to prevent creating new panel during animation
        except RuntimeError:
            # Panel was already deleted, just set to None
            self.jobPanel = None

        # Create new panel
        self.jobPanel = JobPanel(job_path)

        # Connect video selection signal
        self.jobPanel.videoSelected.connect(self.updateVideo)
        self.jobPanel.processedVideoReady.connect(self.showProcessedVideo)

        # Connect close signal
        self.jobPanel.closed.connect(self.onJobClosed)

        # Set panel geometry
        screen = QApplication.desktop().screenGeometry()
        self.jobPanel.setFixedHeight(screen.height())
        self.jobPanel.move(0, 0)

        # Make panel a child of the main window
        self.jobPanel.setParent(self)

        # Ensure panel is on top
        self.jobPanel.raise_()
        self.jobPanel.show()

    def updateVideo(self, video_path):
        """Update video widget with new video"""
        if video_path.startswith("camera://"):
            if video_path == "camera://close":
                if hasattr(self, "videoWidget"):
                    self.videoWidget.stopCamera()
                return
            # Parse camera URL for settings
            if "inference=true" in video_path:
                # Get settings from URL
                import urllib.parse as urlparse

                params = dict(urlparse.parse_qs(video_path.split("?")[1]))
                fps = int(params["fps"][0])
                width = int(params["width"][0])
                height = int(params["height"][0])

                # Create or reuse video viewer with inference
                if not hasattr(self, "videoWidget"):
                    self.videoWidget = VideoViewer()
                    mainLayout = self.widget.layout()
                    mainLayout.replaceWidget(
                        mainLayout.itemAt(1).widget(), self.videoWidget
                    )

                # Start camera with inference
                self.videoWidget.loadCamera(
                    fps, inference_mode=True, frame_size=(width, height)
                )
            else:
                # Normal camera mode
                fps = self.jobPanel.fpsInput.value()
                if not hasattr(self, "videoWidget"):
                    self.videoWidget = VideoViewer()
                    mainLayout = self.widget.layout()
                    mainLayout.replaceWidget(
                        mainLayout.itemAt(1).widget(), self.videoWidget
                    )
                self.videoWidget.loadCamera(fps)

        else:
            # Handle normal video file
            if video_path and os.path.exists(video_path):
                if hasattr(self, "videoWidget"):
                    self.videoWidget.loadVideo(video_path)
                else:
                    self.videoWidget = VideoViewer(video_path)
                    mainLayout = self.widget.layout()
                    mainLayout.replaceWidget(
                        mainLayout.itemAt(1).widget(), self.videoWidget
                    )

    def onJobClosed(self):
        # Position and show reopen button
        screen = QApplication.desktop().screenGeometry()
        self.reopenBtn.move(screen.width() - 70, 20)  # Position in top-right
        self.reopenBtn.show()
        self.reopenBtn.raise_()

    def reopenJob(self):
        if self.job_path:
            self.onJob(self.job_path)

    def showProcessedVideo(self, frames, fps):
        """Display processed video frames in the existing video viewer"""
        if frames:
            # Update layout to ensure video viewer is visible
            mainLayout = self.widget.layout()
            self.videoWidget.playFrames(frames, fps)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
