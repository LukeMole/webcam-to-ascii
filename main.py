import cv2
import os

from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import threading

def create_ascii_frame(img_array):
    #goes through every row in the grayscale image and assigns ASCII characters based on brightness
    ascii_frame = ''
    for row in img_array:
        ascii_row = ''
        for item in row:
            if item > 200:
                ascii_row += '#'
            elif item > 125:
                ascii_row += '?'
            elif item > 50:
                ascii_row += '/'
            else:
                ascii_row += '.'
        #creates a full text based ASCII image and returns it
        ascii_frame += ascii_row + '\n'
    
    return ascii_frame


def webcam_to_ascii(camera, x=128,y=64):
    ret, frame = camera.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (x,y))
    frame = cv2.flip(frame, 1)
    #cv2.imshow('Camera', frame)

    ascii_frame = create_ascii_frame(frame)

    return ascii_frame

    #os.system('cls' if os.name == 'nt' else 'clear')
    #print(ascii_frame)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webcam To Ascii")

        #ascii image UI elements
        self.textImage = QLabel()
        self.textImage.setFont(QFont("Courier", 6))
        self.textImage.setMaximumWidth(round((self.width()/1.25)))
        self.textImage.setMaximumHeight(round((self.width()/1.25)))



        #button control UI elements
        self.updateButton = QPushButton("Update")
        self.setColor = QPushButton("Color")
        self.resolutionXLabel = QLabel("Vertical Resolution")
        self.resolutionXEdit = QLineEdit("")
        self.resolutionYLabel = QLabel("Horizontal Resolution")
        self.resolutionYEdit = QLineEdit("")
        self.fontSizeLabel = QLabel("Font Size")
        self.fontSizeEdit = QLineEdit("")

        #layout code
        buttonLayout = QVBoxLayout()
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        buttonContainer =QWidget()
        buttonContainer.setLayout(buttonLayout)

        #buttonContainer.setMaximumHeight(round(self.height()/1.75))

        buttonLayout.addWidget(self.resolutionXLabel)
        buttonLayout.addWidget(self.resolutionXEdit)
        buttonLayout.addWidget(self.resolutionYLabel)
        buttonLayout.addWidget(self.resolutionYEdit)
        buttonLayout.addWidget(self.fontSizeLabel)
        buttonLayout.addWidget(self.fontSizeEdit)

        buttonLayout.addWidget(self.setColor)
        buttonLayout.addWidget(self.updateButton)

        layout = QHBoxLayout()
        layout.addWidget(self.textImage)
        layout.addWidget(buttonContainer)


        container = QWidget()
        container.setLayout(layout)

        #start the ASCII image updating on a separate thread to keep main UI responsive
        imageThread = threading.Thread(target=self.update_frame)

        imageThread.start()

        #set main widget
        self.setCentralWidget(container)


    def update_frame(self):
        camera = cv2.VideoCapture(0)
        while True:
            frame = webcam_to_ascii(camera)
            self.textImage.setText(frame)





if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()