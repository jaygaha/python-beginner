# PyQt5 Checkbox: How to create a checkbox in PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Checkbox App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))
        self.checkbox = QCheckBox("Are are sure?", self)
        self.initUI()

    def initUI(self):
        self.checkbox.setGeometry(10, 0, 200, 100)
        self.checkbox.setStyleSheet('font-size: 20px; background-color: #5CB338; color: white;')
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.on_click)

    def on_click(self, state):
        if state == Qt.Checked:
            print("Yes")
        else:
            print("No")
        # if self.checkbox.isChecked():
        #     print("Checkbox is checked")
        # else:
        #     print("Checkbox is unchecked")

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