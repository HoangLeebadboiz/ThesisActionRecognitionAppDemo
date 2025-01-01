import json
import os

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class OpenJobView(QWidget):
    openJobSuccess = QtCore.pyqtSignal(str)  # Signal to emit job path

    def __init__(self, workspace_path: str):
        super().__init__()
        self.setWindowTitle("Open Job")
        self.setStyleSheet(qdarktheme.load_stylesheet())
        self.workspace_path = workspace_path

        # Set window size
        screen = QApplication.desktop().screenGeometry()
        self.setFixedSize(screen.width() // 4, screen.height() // 3)

        # Create widgets
        self.headerLabel = QLabel("Select Job")
        self.jobList = QListWidget()
        self.openBtn = QPushButton("Open")
        self.cancelBtn = QPushButton("Cancel")

        # Load jobs
        self.loadJobs()

        self.InitUI()

    def InitUI(self):
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(30, 25, 30, 25)
        mainLayout.setSpacing(20)

        # Style header
        self.headerLabel.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2196F3;
            }
        """
        )
        mainLayout.addWidget(self.headerLabel, alignment=QtCore.Qt.AlignCenter)

        # Style job list
        self.jobList.setStyleSheet(
            """
            QListWidget {
                font-size: 18px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #333;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background: #2196F3;
                color: white;
            }
            QListWidget::item:hover {
                background: rgba(33, 150, 243, 0.1);
            }
        """
        )
        mainLayout.addWidget(self.jobList)

        # Button style
        button_style = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                min-width: 120px;
            }
        """

        # Style open button
        self.openBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: #2196F3;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background: #1976D2;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
        """
        )

        # Style cancel button
        self.cancelBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: transparent;
                border: 2px solid #2196F3;
                color: #2196F3;
            }
            QPushButton:hover {
                background: rgba(33, 150, 243, 0.1);
            }
            QPushButton:pressed {
                background: rgba(33, 150, 243, 0.2);
            }
        """
        )

        # Create buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(15)
        buttonsLayout.addWidget(self.openBtn)
        buttonsLayout.addWidget(self.cancelBtn)

        # Add buttons layout
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

        # Connect buttons
        self.cancelBtn.clicked.connect(self.close)
        self.openBtn.clicked.connect(self.openJob)
        self.jobList.itemDoubleClicked.connect(self.openJob)

    def loadJobs(self):
        datajobs_path = os.path.join(self.workspace_path, "datajobs.json")
        if os.path.exists(datajobs_path):
            with open(datajobs_path, "r") as f:
                jobs = json.load(f)
                for job_name in jobs:
                    self.jobList.addItem(job_name)

    def openJob(self):
        if self.jobList.currentItem():
            job_name = self.jobList.currentItem().text()
            datajobs_path = os.path.join(self.workspace_path, "datajobs.json")
            with open(datajobs_path, "r") as f:
                jobs = json.load(f)
                if job_name in jobs:
                    job_path = jobs[job_name]["path"]
                    self.openJobSuccess.emit(job_path)
                    self.close()
