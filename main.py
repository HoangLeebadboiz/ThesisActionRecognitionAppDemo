import PyQt5
import qdarktheme
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QOpenGLWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark Theme")
        self.setStyleSheet(qdarktheme.load_stylesheet())
        # Set full screen
        self.showMaximized()
        widget = QWidget()
        self.loginBtn = QPushButton("Login")
        self.jobComboBox = QComboBox()

    def initUI(self):
        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.loginBtn)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
