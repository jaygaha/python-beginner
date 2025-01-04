# PyQt5 images: How to display an image using QLabel

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("First Python App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("workspace/assets/letter-j.png"))

        label = QLabel("Hello Python", self)
        label.setFont(QFont("Arial", 20))
        label.setGeometry(0, 0, 800, 100)
        label.setStyleSheet("color: #ECE852; background-color: #5CB338;")

        # Qt.AlignCenter, Qt.AlignRight, Qt.AlignLeft, Qt.AlignTop, Qt.AlignBottom, Qt.AlignVCenter, Qt.AlignHCenter, Qt.AlignJustify
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignLeft)
        label.setAlignment(Qt.AlignCenter)

        lbl_image = QLabel(self)
        lbl_image.setGeometry(10, 110, 250, 250)
        pixmap = QPixmap("workspace/assets/letter-j.png")
        lbl_image.setPixmap(pixmap)

        lbl_image.setScaledContents(True)
        lbl_image.setGeometry((self.width()- lbl_image.width()) // 2, # // is floor division / is normal division
                              (self.height()-lbl_image.height()) // 2,
                              lbl_image.width(),
                              lbl_image.height())


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