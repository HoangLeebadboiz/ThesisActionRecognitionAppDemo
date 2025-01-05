import json
import os

import qdarktheme
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginView(QWidget):
    loginSuccess = QtCore.pyqtSignal()  # Add signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setStyleSheet(qdarktheme.load_stylesheet())
        screen = QApplication.desktop().screenGeometry()
        # Adjust window size for better proportions
        self.setFixedSize(screen.width() // 3, screen.height() // 2)

        # Create header label
        self.headerLabel = QLabel("Welcome Back")
        self.userLabel = QLabel("Username")
        self.passLabel = QLabel("Password")
        self.userInput = QLineEdit()
        self.passInput = QLineEdit()
        self.loginBtn = QPushButton("Login")
        # Create show/hide password button
        self.showPassBtn = QPushButton()
        self.showPassBtn.setCheckable(True)
        self.showPassBtn.setFixedSize(48, 48)

        # Set icons for show/hide password
        icon_path = os.path.dirname(os.path.abspath(__file__))
        self.showPassBtn.setIcon(
            QtGui.QIcon(os.path.join(icon_path, "../icons/eye-off.png"))
        )
        self.showPassBtn.setIconSize(QtCore.QSize(24, 24))

        self.showPassBtn.clicked.connect(self.toggle_password_visibility)
        self.InitUI()

    def InitUI(self):
        # Use VBox as main layout with adjusted spacing
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(30)  # Increased spacing between elements
        mainLayout.setContentsMargins(60, 50, 60, 50)  # Larger margins

        # Style header with adjusted size
        self.headerLabel.setStyleSheet(
            """
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #2196F3;
                margin-bottom: 20px;
            }
        """
        )
        mainLayout.addWidget(self.headerLabel, alignment=QtCore.Qt.AlignCenter)

        # Add some spacing after header
        mainLayout.addSpacing(10)

        # Form layout with adjusted spacing
        formLayout = QGridLayout()
        formLayout.setSpacing(20)
        formLayout.setColumnMinimumWidth(1, 300)  # Set minimum width for input fields

        # Style labels and inputs with adjusted sizes
        style = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 24px;
                padding: 15px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #333;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """
        self.userLabel.setStyleSheet(style)
        self.passLabel.setStyleSheet(style)
        self.userInput.setStyleSheet(style)
        self.passInput.setStyleSheet(style)

        self.userInput.setPlaceholderText("Enter username")
        self.passInput.setPlaceholderText("Enter password")
        self.passInput.setEchoMode(QLineEdit.EchoMode.Password)

        formLayout.addWidget(self.userLabel, 0, 0)
        formLayout.addWidget(self.userInput, 0, 1)

        # Create password container
        passContainer = QWidget()
        passLayout = QHBoxLayout(passContainer)
        passLayout.setContentsMargins(0, 0, 0, 0)
        passLayout.addWidget(self.passInput)
        passLayout.addWidget(self.showPassBtn)

        # Update grid layout to use password container
        formLayout.addWidget(self.passLabel, 1, 0)
        formLayout.addWidget(passContainer, 1, 1)

        mainLayout.addLayout(formLayout)

        # Button style with adjusted sizes
        buttonStyle = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                min-width: 160px;
                min-height: 30px;
            }
        """

        # Login button style
        self.loginBtn.setStyleSheet(
            buttonStyle
            + """
            QPushButton {
                background: #2196F3;
                border: none;
            }
            QPushButton:hover {
                background: #1976D2;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
        """
        )

        # Create and style signup button
        self.signupBtn = QPushButton("Sign Up")
        self.signupBtn.setStyleSheet(
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

        # Create buttons layout with adjusted spacing
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(20)

        # Add some spacing before buttons
        mainLayout.addSpacing(10)

        # Center the buttons layout
        buttonsContainer = QWidget()
        buttonsContainer.setLayout(buttonsLayout)
        mainLayout.addWidget(buttonsContainer, alignment=QtCore.Qt.AlignCenter)

        # Add buttons to horizontal layout
        buttonsLayout.addWidget(self.loginBtn)
        buttonsLayout.addWidget(self.signupBtn)

        self.setLayout(mainLayout)
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.signup)

        # Enhanced login form style
        self.setStyleSheet(
            """
            QWidget {
                background: #121212;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 24px;
                padding: 12px;
                border: 2px solid #333;
                border-radius: 10px;
                background: #1E1E1E;
                color: white;
                min-width: 300px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 10px;
                min-width: 150px;
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
            """
        )

    def login(self):
        msg = QMessageBox()
        if self.userInput.text() == "":
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Please enter your username")
            msg.exec_()
        elif self.passInput.text() == "":
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Please enter your password")
            msg.exec_()
        else:
            username = self.userInput.text()
            password = self.passInput.text()
            with open(
                os.path.abspath(__file__ + "/../../database/users/users.json"), "r"
            ) as file:
                data = dict(json.load(file))
                if username in data.keys() and data[username]["password"] == password:
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setWindowTitle("Success")
                    msg.setText("Login successfully")
                    msg.exec_()
                    self.loginSuccess.emit()  # Emit signal on successful login
                    self.close()
                else:
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setWindowTitle("Error")
                    msg.setText("Username or Password is incorrect")
                    msg.exec_()

    def signup(self):
        from views.signup import SignupView

        self.signup_window = SignupView()
        self.signup_window.show()
        self.close()  # Close login window when opening signup

    def toggle_password_visibility(self):
        if self.showPassBtn.isChecked():
            self.passInput.setEchoMode(QLineEdit.EchoMode.Normal)
            self.showPassBtn.setIcon(
                QtGui.QIcon(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "../icons/eye.png"
                    )
                )
            )
        else:
            self.passInput.setEchoMode(QLineEdit.EchoMode.Password)
            self.showPassBtn.setIcon(
                QtGui.QIcon(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "../icons/eye-off.png",
                    )
                )
            )
