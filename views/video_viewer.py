import os

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QAction, QToolBar, QToolButton, QVBoxLayout, QWidget


class VideoViewer(QWidget):
    def __init__(self, video_path: str):
        super().__init__()
        self.video_path = video_path

        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet(
            """
            QToolBar {
                background: #1E1E1E;
                border: none;
                padding: 5px;
                spacing: 10px;
            }
        """
        )

        # Create media player and video widget
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet(
            """
            QVideoWidget {
                background: #121212;
                border: 2px solid #333333;
                border-radius: 12px;
            }
        """
        )

        # Setup media player
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        if os.path.exists(video_path):
            media_content = QMediaContent(
                QUrl.fromLocalFile(os.path.abspath(video_path))
            )
            self.mediaPlayer.setMedia(media_content)

        self.InitUI()

    def InitUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Get icon path
        icon_path = os.path.dirname(os.path.abspath(__file__))

        # Create actions with icons
        zoom_in_action = QAction(
            QtGui.QIcon(os.path.join(icon_path, "../icons/zoom-in.png")),
            "Zoom In",
            self,
        )
        zoom_out_action = QAction(
            QtGui.QIcon(os.path.join(icon_path, "../icons/zoom-out.png")),
            "Zoom Out",
            self,
        )
        fit_action = QAction(
            QtGui.QIcon(os.path.join(icon_path, "../icons/fit-to-window.png")),
            "Fit to Window",
            self,
        )
        play_action = QAction(
            QtGui.QIcon(os.path.join(icon_path, "../icons/play.png")), "Play", self
        )

        # Style toolbar buttons
        button_style = """
            QToolButton {
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 6px;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QToolButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """

        # Add actions to toolbar
        self.toolbar.addAction(zoom_in_action)
        self.toolbar.addAction(zoom_out_action)
        self.toolbar.addAction(fit_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(play_action)

        # Set toolbar button size
        for action in self.toolbar.actions():
            if isinstance(action, QAction):
                button = QToolButton()
                button.setDefaultAction(action)
                button.setStyleSheet(button_style)
                button.setIconSize(QSize(24, 24))
                button.setFixedSize(36, 36)
                # self.toolbar.addWidget(button)

        # Connect actions
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_out_action.triggered.connect(self.zoom_out)
        fit_action.triggered.connect(self.fit_to_window)
        play_action.triggered.connect(self.play)

        # Add widgets to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.videoWidget)

        # Set layout stretch
        layout.setStretchFactor(self.toolbar, 0)
        layout.setStretchFactor(self.videoWidget, 1)

        self.setLayout(layout)

    def zoom_in(self):
        # TODO: Implement zoom in functionality
        pass

    def zoom_out(self):
        # TODO: Implement zoom out functionality
        pass

    def fit_to_window(self):
        # TODO: Implement fit to window functionality
        pass

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
