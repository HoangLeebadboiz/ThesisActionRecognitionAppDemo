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


class SignupView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setStyleSheet(qdarktheme.load_stylesheet())
        screen = QApplication.desktop().screenGeometry()
        # Set icon
        self.setWindowIcon(
            QtGui.QIcon(os.path.abspath(__file__ + "/../../icons/signup.png"))
        )
        # Set window size
        self.setFixedSize(screen.width() // 3, screen.height() // 2)

        # Create header label
        self.headerLabel = QLabel("Create Account")

        # Create form fields
        self.usernameLabel = QLabel("Username")
        self.emailLabel = QLabel("Email")
        self.passwordLabel = QLabel("Password")
        self.confirmPassLabel = QLabel("Confirm Password")

        self.usernameInput = QLineEdit()
        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.confirmPassInput = QLineEdit()

        # Create buttons
        self.signupBtn = QPushButton("Create Account")
        self.backToLoginBtn = QPushButton("Back to Login")

        # Create show/hide password buttons
        self.showPassBtn = QPushButton()
        self.showConfirmPassBtn = QPushButton()

        for btn in [self.showPassBtn, self.showConfirmPassBtn]:
            btn.setCheckable(True)
            btn.setFixedSize(48, 48)
            btn.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    background-image: url(icons/eye-off.png);
                    background-position: center;
                    background-repeat: no-repeat;
                }
                QPushButton:checked {
                    background-image: url(icons/eye.png);
                }
                """
            )

        self.showPassBtn.clicked.connect(
            lambda: self.toggle_password_visibility(
                self.passwordInput, self.showPassBtn
            )
        )
        self.showConfirmPassBtn.clicked.connect(
            lambda: self.toggle_password_visibility(
                self.confirmPassInput, self.showConfirmPassBtn
            )
        )

        self.InitUI()

    def InitUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(30)
        mainLayout.setContentsMargins(60, 50, 60, 50)

        # Style header
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
        mainLayout.addSpacing(10)

        # Form layout
        formLayout = QGridLayout()
        formLayout.setSpacing(20)
        formLayout.setColumnMinimumWidth(1, 300)

        # Style inputs and labels
        style = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 18px;
                padding: 12px;
                border: 2px solid #555;
                border-radius: 8px;
                background: #333;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """

        for label in [
            self.usernameLabel,
            self.emailLabel,
            self.passwordLabel,
            self.confirmPassLabel,
        ]:
            label.setStyleSheet(style)

        for input_field in [
            self.usernameInput,
            self.emailInput,
            self.passwordInput,
            self.confirmPassInput,
        ]:
            input_field.setStyleSheet(style)

        # Set placeholders and password echo mode
        self.usernameInput.setPlaceholderText("Choose a username")
        self.emailInput.setPlaceholderText("Enter your email")
        self.passwordInput.setPlaceholderText("Choose a password")
        self.confirmPassInput.setPlaceholderText("Confirm your password")
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmPassInput.setEchoMode(QLineEdit.EchoMode.Password)

        # Create password containers
        passContainer = QWidget()
        passLayout = QHBoxLayout(passContainer)
        passLayout.setContentsMargins(0, 0, 0, 0)
        passLayout.addWidget(self.passwordInput)
        passLayout.addWidget(self.showPassBtn)

        confirmPassContainer = QWidget()
        confirmPassLayout = QHBoxLayout(confirmPassContainer)
        confirmPassLayout.setContentsMargins(0, 0, 0, 0)
        confirmPassLayout.addWidget(self.confirmPassInput)
        confirmPassLayout.addWidget(self.showConfirmPassBtn)

        # Update form layout to use containers
        formLayout.addWidget(self.usernameLabel, 0, 0)
        formLayout.addWidget(self.usernameInput, 0, 1)
        formLayout.addWidget(self.emailLabel, 1, 0)
        formLayout.addWidget(self.emailInput, 1, 1)
        formLayout.addWidget(self.passwordLabel, 2, 0)
        formLayout.addWidget(passContainer, 2, 1)
        formLayout.addWidget(self.confirmPassLabel, 3, 0)
        formLayout.addWidget(confirmPassContainer, 3, 1)

        mainLayout.addLayout(formLayout)
        mainLayout.addSpacing(10)

        # Button styles
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

        # Style signup button
        self.signupBtn.setStyleSheet(
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

        # Style back button
        self.backToLoginBtn.setStyleSheet(
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

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(20)

        # Center the buttons
        buttonsContainer = QWidget()
        buttonsContainer.setLayout(buttonsLayout)

        # Add buttons
        buttonsLayout.addWidget(self.signupBtn)
        buttonsLayout.addWidget(self.backToLoginBtn)

        mainLayout.addWidget(buttonsContainer, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(mainLayout)

        # Connect buttons
        self.signupBtn.clicked.connect(self.signup)
        self.backToLoginBtn.clicked.connect(self.back_to_login)

    def signup(self):
        if not all(
            [
                self.usernameInput.text(),
                self.emailInput.text(),
                self.passwordInput.text(),
                self.confirmPassInput.text(),
            ]
        ):
            self.show_message(
                "Error", "Please fill in all fields", QMessageBox.Icon.Critical
            )
            return

        if self.passwordInput.text() != self.confirmPassInput.text():
            self.show_message(
                "Error", "Passwords do not match", QMessageBox.Icon.Critical
            )
            return

        # TODO: Add email validation
        # TODO: Add password strength validation
        # TODO: Implement actual user registration
        self.show_message(
            "Success", "Account created successfully!", QMessageBox.Icon.Information
        )
        self.close()

    def back_to_login(self):
        self.close()

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def toggle_password_visibility(self, input_field, button):
        if button.isChecked():
            input_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
