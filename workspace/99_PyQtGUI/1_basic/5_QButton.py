# PyQt5 buttons: How to create a button in PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Button App")
        self.setGeometry(500, 100, 600, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))

        self.button = QPushButton("Click Me", self)
        self.label = QLabel("Hello Python", self)
        self.initUI()
        self.counter = 0

    def initUI(self):
        self.button.setGeometry(150, 200, 200, 100)
        self.button.setStyleSheet('font-size: 20px; background-color: #5CB338; color: white;')
        self.button.clicked.connect(self.on_click)

        self.label.setGeometry(150, 300, 200, 100)
        self.label.setStyleSheet('font-size: 20px; background-color: #ECE852; color: black;')

    def on_click(self):
        # self.counter += 1
        # print("Button was clicked")
        # self.button.setText(f"Clicked {self.counter} times")
        # self.button.setDisabled(True)
        self.label.setText("Buy!!!")

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