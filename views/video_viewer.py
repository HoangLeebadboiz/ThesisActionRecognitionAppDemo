import os
from typing import Optional

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRectF, QSize, QSizeF, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QSlider,
    QStyle,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class VideoViewer(QWidget):
    def __init__(self, video_path: str = None):
        super().__init__()

        # Create media player first
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create and setup video item
        self.videoItem = QGraphicsVideoItem()
        self.mediaPlayer.setVideoOutput(self.videoItem)

        # Create scene and add video item
        self.scene = QGraphicsScene()
        self.scene.addItem(self.videoItem)

        # Create and setup view
        self.view = QGraphicsView(self.scene)
        self.setupView()  # Move view setup to separate method

        # Load video if path provided
        if video_path and os.path.exists(video_path):
            self.loadVideo(video_path)

        # Rest of initialization...
        self.setupUI()

    def loadVideo(self, video_path):
        """Load video without showing file dialog"""
        media = QMediaContent(QUrl.fromLocalFile(os.path.abspath(video_path)))
        self.mediaPlayer.setMedia(media)

    def setupView(self):
        self.view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet(
            """
            QGraphicsView {
                background: #121212;
                border: 2px solid #333333;
                border-radius: 12px;
            }
        """
        )

    def setupUI(self):
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

        # Create progress slider
        self.progressSlider = QSlider(Qt.Horizontal)
        self.progressSlider.setStyleSheet(
            """
            QSlider {
                height: 30px;
                background: transparent;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
                background: #2196F3;
            }
            QSlider::handle:horizontal:hover {
                background: #42A5F5;
                width: 24px;
                height: 24px;
                margin: -8px 0;
            }
            QSlider::handle:horizontal:pressed {
                background: #1976D2;
            }
            QSlider::sub-page:horizontal {
                background: #2196F3;
                border-radius: 4px;
            }
            """
        )
        self.progressSlider.setEnabled(False)  # Disabled by default
        self.progressSlider.setTracking(False)  # Only update when released
        self.progressSlider.setPageStep(5000)  # 5 seconds jump for page step

        # Connect media player signals
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.progressSlider.sliderMoved.connect(self.setPosition)
        self.progressSlider.sliderPressed.connect(self.sliderPressed)
        self.progressSlider.sliderReleased.connect(self.sliderReleased)
        self.progressSlider.mouseReleaseEvent = (
            self.sliderMouseReleaseEvent
        )  # Override mouse release
        self.progressSlider.mousePressEvent = (
            self.sliderMousePressEvent
        )  # Override mouse press

        # Create layout for progress bar
        progressLayout = QHBoxLayout()
        progressLayout.setContentsMargins(10, 0, 10, 10)
        progressLayout.addWidget(self.progressSlider)

        # Add widgets to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)
        layout.addLayout(progressLayout)

        # Set layout stretch
        layout.setStretchFactor(self.toolbar, 0)
        layout.setStretchFactor(self.view, 1)
        layout.setStretchFactor(progressLayout, 0)

        self.setLayout(layout)

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()

    def fit_to_window(self):
        # Reset zoom factor
        self.zoom_factor = 1.0

        # Get the size of the view
        view_size = self.view.size()
        scene_rect = self.scene.itemsBoundingRect()

        # Check if scene has valid size
        if scene_rect.width() <= 0 or scene_rect.height() <= 0:
            # Set default size if no video or invalid size
            self.videoItem.setSize(QSizeF(view_size.width(), view_size.height()))
            scene_rect = self.scene.itemsBoundingRect()

        # Calculate scale factors
        if scene_rect.width() > 0 and scene_rect.height() > 0:
            scale_x = view_size.width() / scene_rect.width()
            scale_y = view_size.height() / scene_rect.height()

            # Use the smaller scale factor to fit the entire video
            scale = min(scale_x, scale_y)
            self.zoom_factor = scale

            self.update_zoom()

    def update_zoom(self):
        # Ensure minimum and maximum zoom levels
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))

        # Save current center point
        center = self.view.mapToScene(self.view.viewport().rect().center())

        # Reset transformation and apply new scale
        self.view.resetTransform()
        self.view.scale(self.zoom_factor, self.zoom_factor)

        # Restore center point
        self.view.centerOn(center)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Only fit to window if we have a valid video
        if self.mediaPlayer.media().isNull():
            return
        self.fit_to_window()

    def durationChanged(self, duration):
        self.progressSlider.setRange(0, duration)
        self.progressSlider.setEnabled(True)

    def positionChanged(self, position):
        if not self.progressSlider.isSliderDown():
            self.progressSlider.setValue(position)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def sliderPressed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def sliderReleased(self):
        self.setPosition(self.progressSlider.value())
        if self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            self.mediaPlayer.play()

    def sliderMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate position from click
            value = QStyle.sliderValueFromPosition(
                self.progressSlider.minimum(),
                self.progressSlider.maximum(),
                event.x(),
                self.progressSlider.width(),
            )
            self.progressSlider.setValue(value)
            self.mediaPlayer.pause()
            self.setPosition(value)

        # Call original mousePressEvent
        QSlider.mousePressEvent(self.progressSlider, event)

    def sliderMouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate position from release point
            value = QStyle.sliderValueFromPosition(
                self.progressSlider.minimum(),
                self.progressSlider.maximum(),
                event.x(),
                self.progressSlider.width(),
            )
            self.progressSlider.setValue(value)
            self.setPosition(value)
            self.mediaPlayer.play()

        # Call original mouseReleaseEvent
        QSlider.mouseReleaseEvent(self.progressSlider, event)

    def playFrames(self, frames, fps):
        """Play a list of frames at specified fps"""
        if not frames:
            return

        # Get initial frame size for consistent display
        init_height, init_width = frames[0].shape[:2]

        # Set scene size to match initial frame
        self.scene.setSceneRect(0, 0, init_width, init_height)

        for frame in frames:
            # Convert numpy array to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QtGui.QImage(
                frame.data,
                width,
                height,
                bytes_per_line,
                QtGui.QImage.Format_RGB888,
            )

            # Convert to QPixmap
            pixmap = QtGui.QPixmap.fromImage(q_img)

            # Create QGraphicsPixmapItem and add to scene
            if hasattr(self, "pixmap_item"):
                self.scene.removeItem(self.pixmap_item)
            self.pixmap_item = self.scene.addPixmap(pixmap)

            # Center the pixmap in scene
            self.pixmap_item.setPos(
                (init_width - width) / 2, (init_height - height) / 2
            )

            # Process events and add delay
            QApplication.processEvents()
            QtCore.QThread.msleep(int(1000 / fps))
