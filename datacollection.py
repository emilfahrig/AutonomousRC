import cv2
import socket
import numpy as np
from keras.models import load_model
import serial
import keyboard


direction_predictor = load_model('self_drivefinal.h5')

counter = 0
forward_counter = 0
left_counter = 0
right_counter = 0
stop_counter = 0

grey_low = np.array([0, 0, 0])
grey_high = np.array([255, 255, 200])

port = "COM5"
bluetooth = serial.Serial(port, 9600)
bluetooth.flushInput()
print("Connected to bluetooth!")

cap = cv2.VideoCapture("http://192.168.68.167:81/stream")
print("Connected to ESP 32 Cam!")

current_car_state = b'B'

while True:
    _, frame = cap.read()

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, grey_low, grey_high)
    frame[mask > 0] = (0, 0, 0)

    cv2.imshow("ESP32 Cam OpenCV", frame)

    if keyboard.is_pressed('w'):
        current_car_state = b'F'
    elif keyboard.is_pressed('a'):
        current_car_state = b'L'
    elif keyboard.is_pressed('d'):
        current_car_state = b'R'
    elif keyboard.is_pressed('b'):
        current_car_state = b'B'

    print(current_car_state)

    if current_car_state.decode().strip() is "F":
        print("Frame saved in F")
        forward_counter = forward_counter + 1
        cv2.imwrite("C:/Users/emilx/PycharmProjects/AutonoCar/TRAINIMPROVETEST/Forward/carvision{}.jpeg".format(
            forward_counter), frame)
    elif current_car_state.decode().strip() is "L":
        print("Frame saved in L")
        left_counter = left_counter + 1
        cv2.imwrite(
            "C:/Users/emilx/PycharmProjects/AutonoCar/TRAINIMPROVETEST/Left/carvision{}.jpeg".format(left_counter),
            frame)
    elif current_car_state.decode().strip() is "R":
        print("Frame saved in R")
        right_counter = right_counter + 1
        cv2.imwrite(
            "C:/Users/emilx/PycharmProjects/AutonoCar/TRAINIMPROVETEST/Right/carvision{}.jpeg".format(right_counter),
            frame)
    else:
        print("Frame not saved")
        # stop_counter = stop_counter + 1
        # cv2.imwrite("C:/Users/emilx/PycharmProjects/AutonoCar/recordingdata/Stop/carvision{}.jpeg".format(right_counte
    
    bluetooth.write(current_car_state)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(str(forward_counter + left_counter + right_counter + stop_counter) + " frames saved!")
cap.release()
cv2.destroyAllWindows()
bluetooth.close()



