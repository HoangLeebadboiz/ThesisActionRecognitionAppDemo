import json
import os
from datetime import datetime

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CreateJobView(QWidget):
    createJobSuccess = QtCore.pyqtSignal(str)  # Change signal to include job path

    def __init__(self, workspacePath: str = "workspace"):
        super().__init__()
        self.setWindowTitle("Create New Job")
        self.setStyleSheet(qdarktheme.load_stylesheet())

        # Set window size (smaller)
        screen = QApplication.desktop().screenGeometry()
        self.setFixedSize(screen.width() // 5, screen.height() // 5)

        # Create widgets
        self.headerLabel = QLabel("Create New Job")
        self.jobNameLabel = QLabel("Job Name")
        self.jobNameInput = QLineEdit()
        self.createBtn = QPushButton("Create")
        self.cancelBtn = QPushButton("Cancel")

        self.workspacePath = workspacePath

        self.InitUI()

    def InitUI(self):
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(15)
        mainLayout.setContentsMargins(30, 25, 30, 25)

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

        # Style job name label and input
        style = """
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 24px;
                padding: 12px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #333;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """
        self.jobNameLabel.setStyleSheet(style)
        self.jobNameInput.setStyleSheet(style)
        self.jobNameInput.setPlaceholderText("Enter job name")

        # Add job name input section
        mainLayout.addWidget(self.jobNameLabel)
        mainLayout.addWidget(self.jobNameInput)

        # Add spacing before buttons
        mainLayout.addSpacing(10)

        # Button style
        buttonStyle = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                min-width: 120px;
            }
        """

        # Style create button
        self.createBtn.setStyleSheet(
            buttonStyle
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
            buttonStyle
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
        buttonsLayout.addWidget(self.createBtn)
        buttonsLayout.addWidget(self.cancelBtn)

        # Add buttons layout
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

        # Connect buttons
        self.cancelBtn.clicked.connect(self.close)
        self.createBtn.clicked.connect(self.createJob)

    def createJob(self):
        if self.jobNameInput.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Job name cannot be empty.")
            msg.exec_()
        else:
            jobName = self.jobNameInput.text()
            jobPath = os.path.join(self.workspacePath, jobName)
            if not os.path.exists(jobPath):
                os.makedirs(jobPath)
                os.makedirs(os.path.join(jobPath, "videos"))
                with open(os.path.join(jobPath, "config.json"), "w") as f:
                    json.dump({}, f)
                with open(os.path.join(self.workspacePath, "datajobs.json"), "r+") as f:
                    datajobs = dict(json.load(f))
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    datajobs[jobName] = {"path": jobPath, "Create Time": current_time}
                    f.seek(0)
                    f.truncate()
                    json.dump(datajobs, f, indent=4)
            with open(os.path.join(jobPath, "config.json"), "r+") as f:
                jobs = dict(json.load(f))
                f.seek(0)
                f.truncate()
                jobs[jobName] = {"path": jobPath, "classes": {}}
                json.dump(jobs, f, indent=4)
            self.createJobSuccess.emit(jobPath)  # Emit job path
            self.close()
