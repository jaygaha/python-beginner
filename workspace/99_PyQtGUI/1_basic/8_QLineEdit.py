# PyQt5 LineEdit: How to create a LineEdit in PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python LineEdit App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Submit", self)
        self.initUI()

    def initUI(self):
        self.line_edit.setGeometry(10, 10, 200, 30)
        self.line_edit.setPlaceholderText("Enter your name")
        self.line_edit.setStyleSheet('font-size: 20px; font-family: Arial;')

        self.button.setGeometry(210, 10, 100, 30)
        self.button.setStyleSheet('font-size: 20px; font-family: Arial;')

        self.button.clicked.connect(self.on_click)

    def on_click(self):
        text = self.line_edit.text()
        print(f"Hello {text}")

def main():
    # Create an instance of QApplication;
    # sys.argv is a list in Python, which contains the command-line arguments passed to the script
    app = QApplication(sys.argv)
    window = MainWindow()
    # default is hidden
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()