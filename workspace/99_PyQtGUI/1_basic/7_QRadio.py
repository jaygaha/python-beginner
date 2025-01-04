# PyQt5 Radio button: How to create a radio button in PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Checkbox App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))
        self.radio1 = QRadioButton("JCB", self)
        self.radio2 = QRadioButton("Visa", self)
        self.radio3 = QRadioButton("Gift Cards", self)
        self.radio4 = QRadioButton("IN-Store", self)
        self.radio5 = QRadioButton("Online", self)
        self.button_group1 = QButtonGroup(self)
        self.button_group2 = QButtonGroup(self)

        self.initUI()

    def initUI(self):
        self.radio1.setGeometry(0, 0, 200, 50)
        self.radio2.setGeometry(0, 50, 200, 50)
        self.radio3.setGeometry(0, 100, 200, 50)
        self.radio4.setGeometry(0, 150, 200, 50)
        self.radio5.setGeometry(0, 200, 200, 50)

        self.setStyleSheet('QRadioButton{font-size: 20px; background-color: #5CB338; color: white;}')

        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group1.addButton(self.radio3)

        self.button_group2.addButton(self.radio4)
        self.button_group2.addButton(self.radio5)

        self.radio1.toggled.connect(self.radio_botton_changed)
        self.radio2.toggled.connect(self.radio_botton_changed)
        self.radio3.toggled.connect(self.radio_botton_changed)
        self.radio4.toggled.connect(self.radio_botton_changed)
        self.radio5.toggled.connect(self.radio_botton_changed)

    def radio_botton_changed(self):
        radion_button = self.sender()
        if radion_button.isChecked():
            print(f"{radion_button.text()} is selected")
        else:
            print(f"{radion_button.text()} is deselected")


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