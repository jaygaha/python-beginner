# PyQt5 layouts: How to use QGridLayout

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QT Layout App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label1 = QLabel("Label 1", self)
        label2 = QLabel("Label 2", self)
        label3 = QLabel("Label 3", self)
        label4 = QLabel("Label 4", self)
        label5 = QLabel("Label 5", self)

        label1.setStyleSheet("background-color: #5CB338;")
        label2.setStyleSheet("background-color: #ECE852;")
        label3.setStyleSheet("background-color: #5CB338;")
        label4.setStyleSheet("background-color: #ECE852;")
        label5.setStyleSheet("background-color: #5CB338;")

        # vbox = QVBoxLayout()
        # vbox.addWidget(label1)
        # vbox.addWidget(label2)
        # vbox.addWidget(label3)
        # vbox.addWidget(label4)
        # vbox.addWidget(label5)

        # central_widget.setLayout(vbox)

        # hbox = QHBoxLayout()

        # hbox.addWidget(label1)
        # hbox.addWidget(label2)
        # hbox.addWidget(label3)
        # hbox.addWidget(label4)
        # hbox.addWidget(label5)

        # central_widget.setLayout(hbox)

        grid = QGridLayout()

        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 1)
        grid.addWidget(label3, 1, 0)
        grid.addWidget(label4, 1, 1)
        grid.addWidget(label5, 2, 2)

        central_widget.setLayout(grid)



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