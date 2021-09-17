import cv2
import socket
import numpy as np
from keras.models import load_model
import serial
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
import time

grey_low = np.array([0, 0, 0])
grey_high = np.array([255, 255, 220])

direction_predictor = load_model('self_drivefinal.h5')

port = "COM6"
bluetooth = serial.Serial(port, 9600)
bluetooth.flushInput()
print("Connected to bluetooth!")

cap = cv2.VideoCapture("http://192.168.68.167:81/stream")
print("Connected to ESP 32 Cam!")
frame_queue = []

init_time = time.time()
buffer_time_exceeded = False
buffer_time = 5

while True:
    if time.time() - init_time >= buffer_time or buffer_time_exceeded:
        frame = frame_queue.pop()

        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, grey_low, grey_high)
        frame[mask > 0] = (0, 0, 0)

        cv2.imshow("ESP32 Cam OpenCV", frame)

        img_resized = cv2.resize(frame, (150, 100))
        img_resized_array = img_to_array(img_resized)
        predict_img = img_resized_array.reshape(1, 150, 100, 3)

        result = direction_predictor.predict(predict_img / 255)
        max_index = np.argmax((result[0]))

        print(str(result) + "     " + str(max_index))
        print('\n')

        if max_index == 0:
            bluetooth.write(b'F')
        elif max_index == 1:
            bluetooth.write(b'L')
        else:
            bluetooth.write(b'R')

    _, frame = cap.read()
    frame_queue.append(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
bluetooth.close()