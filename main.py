import cv2
import os

from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
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





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webcam To Ascii")

        self.text = QLabel()
        self.text.setFont(QFont("Courier", 6))
        

        layout = QVBoxLayout()
        layout.addWidget(self.text)

        container = QWidget()
        container.setLayout(layout)

        imageThread = threading.Thread(target=self.webcam_to_ascii)

        imageThread.start()

        self.setCentralWidget(container)


    def webcam_to_ascii(self, x=128,y=64):
        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (x,y))
            #cv2.imshow('Camera', frame)

            ascii_frame = create_ascii_frame(frame)

            self.text.setText(ascii_frame)

            #os.system('cls' if os.name == 'nt' else 'clear')
            #print(ascii_frame)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()