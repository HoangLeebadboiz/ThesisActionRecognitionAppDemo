import json
import os

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tools.database import JobDatabase


class OpenJobView(QWidget):
    openJobSuccess = QtCore.pyqtSignal(str)  # Signal to emit job path

    def __init__(self, workspace_path: str):
        super().__init__()
        self.workspace_path = workspace_path
        self.list_jobs = []
        self.setWindowTitle("Open Job")
        screen = QApplication.desktop().screenGeometry()
        self.setFixedSize(screen.width() // 2, screen.height() // 2)
        self.setStyleSheet(qdarktheme.load_stylesheet())

        # Set window background
        self.setStyleSheet(
            """
            QWidget {
                background: #1E1E1E;
            }
            """
        )

        # Create widgets
        self.jobList = QListWidget()
        self.jobList.setIconSize(QSize(48, 48))  # Set icon size for all items
        self.jobList.setStyleSheet(
            """
            QListWidget {
                font-size: 22px;
                background: #2A2A2A;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 15px;
            }
            QListWidget::item {
                background: #333;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 35px;  /* Increased padding */
                padding-left: 80px;  /* Room for icon */
                margin-bottom: 15px;
                color: #FFFFFF;
                line-height: 180%;  /* Adjusted line spacing */
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                border: 1px solid #2196F3;
            }
            QListWidget::item:hover:!selected {
                background: #404040;
                border: 1px solid #555;
            }
            """
        )

        # Create buttons with updated dark theme
        self.openBtn = QPushButton("Open")
        self.deleteBtn = QPushButton("Delete")  # Add delete button
        self.cancelBtn = QPushButton("Cancel")

        # Style buttons
        button_style = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 8px;
                min-width: 120px;
            }
        """

        # Style delete button
        self.deleteBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: transparent;
                border: 2px solid #f44336;
                color: #f44336;
            }
            QPushButton:hover {
                background: rgba(244, 67, 54, 0.1);
            }
            QPushButton:pressed {
                background: rgba(244, 67, 54, 0.2);
            }
            """
        )

        self.openBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                border: none;
                color: white;
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

        self.cancelBtn.setStyleSheet(
            button_style
            + """
            QPushButton {
                background: transparent;
                border: 2px solid #555;
                color: #CCC;
            }
            QPushButton:hover {
                border-color: #666;
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                border-color: #777;
                background: rgba(255, 255, 255, 0.2);
            }
            """
        )

        # Add title with updated style
        title = QLabel("Select a Job")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #2196F3;
                margin-bottom: 30px;
                padding: 15px;
                background: transparent;
            }
            """
        )

        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Add title
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Add job list
        layout.addWidget(self.jobList)

        # Add buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.openBtn)
        buttonLayout.addWidget(self.deleteBtn)  # Add delete button
        buttonLayout.addWidget(self.cancelBtn)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        # Connect events
        self.openBtn.clicked.connect(self.openJob)
        self.cancelBtn.clicked.connect(self.close)
        self.jobList.itemDoubleClicked.connect(self.openJob)

        # Connect delete button
        self.deleteBtn.clicked.connect(self.deleteJob)

        # Load jobs
        self.loadJobs()

    def loadJobs(self):
        database_path = os.path.abspath(__file__ + "/../../database")
        print(database_path)
        job_database = JobDatabase(database_path)
        # items = QListWidgetItem()
        self.list_jobs = job_database.get_all()
        job_database.close()
        for job in self.list_jobs:
            item = QListWidgetItem()
            item.setText(
                f"Job: {job[1]} \t\t\t\t Responsible Person: {job[6]}\nCreated: {job[4]} \t Updated: {job[5]}"
            )
            item.setData(Qt.UserRole, job[1])
            font = item.font()
            font.setPointSize(14)
            font.setFamily("Consolas")
            item.setFont(font)
            item.setForeground(QtGui.QColor("#FFFFFF"))
            item.setSizeHint(QSize(0, 180))
            # Add icon to item
            icon_path = os.path.join(os.path.dirname(__file__), "../icons/job.png")
            if os.path.exists(icon_path):
                item.setIcon(QtGui.QIcon(icon_path))
                # # size of icon
                # item.icon(QSize(48, 48))
            self.jobList.addItem(item)
        self.jobList.setIconSize(QSize(60, 60))

    def openJob(self):
        if self.jobList.currentItem():
            job_name = self.jobList.currentItem().data(
                Qt.UserRole
            )  # Get stored job name
            job_path = self.list_jobs[self.jobList.currentRow()][3]
            self.openJobSuccess.emit(job_path)
            self.close()

    def deleteJob(self):
        if not self.jobList.currentItem():
            return

        # Get selected job
        job_name = self.jobList.currentItem().data(Qt.UserRole)

        # Style for message boxes
        msg_style = """
            QMessageBox {
                background-color: #1E1E1E;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 18px;
                min-width: 400px;
                padding: 20px;
            }
            QMessageBox QPushButton {
                background: #2A2A2A;
                border: 2px solid #2196F3;
                border-radius: 6px;
                padding: 8px 20px;
                color: #FFFFFF;
                font-size: 16px;
                min-width: 100px;
                min-height: 30px;
            }
            QMessageBox QPushButton:hover {
                background: #333333;
                border-color: #42A5F5;
            }
            QMessageBox QPushButton:pressed {
                background: #1E1E1E;
            }
            QMessageBox QIcon {
                width: 48px;
                height: 48px;
            }
        """

        # Confirm deletion
        confirm_box = QMessageBox(self)
        confirm_box.setStyleSheet(msg_style)
        confirm_box.setWindowTitle("Confirm Deletion")
        confirm_box.setText(f"Are you sure you want to delete job '{job_name}'?")
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        reply = confirm_box.exec_()

        if reply == QMessageBox.Yes:
            # Remove job from database
            job_database = JobDatabase(os.path.abspath(__file__ + "/../../database"))
            job_database.delete(job_name)
            job_database.close()

            # Show success message
            success_box = QMessageBox(self)
            success_box.setStyleSheet(msg_style)
            success_box.setWindowTitle("Success")
            success_box.setText(f"Job '{job_name}' has been deleted.")
            success_box.setIcon(QMessageBox.Information)
            success_box.exec_()
