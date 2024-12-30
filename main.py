import os
import sys

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QOpenGLWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from views.login import LoginView
from views.signup import SignupView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Action Recognition")
        self.setStyleSheet(qdarktheme.load_stylesheet())

        # Set window icon
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(__file__ + "/../icons/app.png")))

        # Get screen size and set window geometry
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Create widgets
        self.widget = QWidget()
        self.loginBtn = QPushButton("Login")
        self.signupBtn = QPushButton("Sign Up")
        self.jobComboBox = QComboBox()
        self.videoWidget = QOpenGLWidget()

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
                font-size: 24px;
                padding: 12px 20px;
                border: 2px solid #2196F3;
                border-radius: 10px;
                background: #1E1E1E;
                min-width: 300px;
                color: #FFFFFF;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow-down.png);
                width: 16px;
                height: 16px;
            }
            QComboBox:hover {
                border-color: #42A5F5;
                background: #262626;
            }
            QComboBox QAbstractItemView {
                background: #1E1E1E;
                border: 2px solid #2196F3;
                border-radius: 10px;
                padding: 10px;
                selection-background-color: #2196F3;
                selection-color: white;
                font-size: 24px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 45px;
                padding: 8px;
            }
        """
        )

        # Set job combobox items and size
        self.jobComboBox.addItems(["New Job", "Open Job", "Save Job"])
        self.jobComboBox.setPlaceholderText("Job")
        self.jobComboBox.setFixedHeight(60)  # Increased height

        # Style buttons
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
            }
            QPushButton:hover {
                background: #42A5F5;
            }
            QPushButton:pressed {
                background: #1E88E5;
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
            }
            QPushButton:hover {
                background: rgba(33, 150, 243, 0.1);
            }
            QPushButton:pressed {
                background: rgba(33, 150, 243, 0.2);
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

        # Style video widget
        self.videoWidget.setStyleSheet(
            """
            QOpenGLWidget {
                background: #121212;
                border: 2px solid #333333;
                border-radius: 12px;
            }
        """
        )

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

    def login(self):
        self.loginView = LoginView()
        self.loginView.show()

    def signup(self):
        self.signupView = SignupView()
        self.signupView.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
