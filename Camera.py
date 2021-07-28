import datetime
import time

import serial
import cv2
import numpy as nump

CAMERA_NUM = 2
ARDUINO_PORT = '/dev/ttyACM0'
ARDUINO_BAUD_RATE = 9600

TEST_PIXEL_X = 284
TEST_PIXEL_Y = 226
COUNT = 0

def isItShiny():
    while(True):
        
        #init Camera
        cap = cv2.VideoCapture(CAMERA_NUM)
        
        cap.set(15, -2.0)

        ret, frame = cap.read()

        cap.release()

        #frame = cv2.GaussianBlur(frame, (11, 11), 0)

        currentDateTimeString = datetime.datetime.today().strftime('%Y-%m-%d_T%H-%M-%S')

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # define range of what constitutes "magenta" in HSV
        lower_shiny = nump.array([140, 100, 100])
        upper_shiny = nump.array([160, 255, 255])

        # Threshold the HSV image to get a black and white image that is white (255) where the original image is magenta and white (0) if not.
        mask = cv2.inRange(hsv, lower_shiny, upper_shiny)

        # Apply a bitwise-AND between the mask and the original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        print('img_' + currentDateTimeString + '_frame.png')
        
        ogPic = str(COUNT) + "img_" + currentDateTimeString + "_frame.png"
        maskPic = str(COUNT) + "img_" + currentDateTimeString + "_mask.png"
        resPic = str(COUNT) + "img_" + currentDateTimeString + "_res.png"

        #Paint test pixel red
        frame[TEST_PIXEL_Y, TEST_PIXEL_X][2] = 255
        frame[TEST_PIXEL_Y, TEST_PIXEL_X][1] = 0
        frame[TEST_PIXEL_Y, TEST_PIXEL_X][0] = 0
        

        cv2.imwrite(ogPic, frame)
        cv2.imwrite(maskPic, mask)
        cv2.imwrite(resPic, res)
        

        if mask[TEST_PIXEL_Y, TEST_PIXEL_X] == 0:
            return False
        else:
            return True

if __name__ == '__main__':
    ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE)
    print (ser.readline())
    while True:
        # Empty line
        print()
        COUNT = COUNT + 1

        # Wait for message from Arduino
        #message = b'Command: checkIfShiny\r\n'
        message = ser.readline()
        print("Message from Arduino: ")
        print(message)
        
        if message == b'Command: checkIfShiny\r\n':
            if isItShiny():
                print('Shiny!')
                ser.write(b'y')
            else:
                print('Not shiny')
                ser.write(b'n')
        else:
            '''
            Do Nothing
            '''