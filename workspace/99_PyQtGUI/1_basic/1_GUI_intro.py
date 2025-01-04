# PyQT5 Introduction
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("First Python App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))
        self.initUI()

    def initUI(self):
        pass

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