import cv2
import os


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


def webcam_to_ascii(x=128,y=64):
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (x,y))
        #cv2.imshow('Camera', frame)

        ascii_frame = create_ascii_frame(frame)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame)


if __name__ == '__main__':
    webcam_to_ascii()