import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import cv2 as cv
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial
import csv

class ImageProcessingThread(QThread):
    image_processed = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.lower_bound_red = np.array([0, 0, 0])
        self.upper_bound_red = np.array([255, 255, 255])
        self.lower_bound_blue = np.array([0, 0, 0])
        self.upper_bound_blue = np.array([255, 255, 255])
        self.color_to_calibrate = "red"

    def calibrate_color(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            color = self.frame[y, x]
            if self.color_to_calibrate == "red":
                self.lower_bound_red = np.array([color[0] - 40, color[1] - 40, color[2] - 100])
                self.upper_bound_red = np.array([color[0] + 40, color[1] + 40, color[2] + 100])
                self.color_to_calibrate = "blue"
            elif self.color_to_calibrate == "blue":
                hsv_color = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)[0][0]
                self.lower_bound_blue = np.array([hsv_color[0] - 10, 100, 100])
                self.upper_bound_blue = np.array([hsv_color[0] + 10, 255, 255])
                self.color_to_calibrate = "red"

    def run(self):
        with open('coordenadas.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for capture in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                self.frame = capture.array
                hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

                mask_red = cv.inRange(self.frame, self.lower_bound_red, self.upper_bound_red)
                mask_blue = cv.inRange(hsv, self.lower_bound_blue, self.upper_bound_blue)

                filtered_frame_red = cv.bitwise_and(self.frame, self.frame, mask=mask_red)
                filtered_frame_blue = cv.bitwise_and(self.frame, self.frame, mask=mask_blue)

                self.image_processed.emit(self.frame, filtered_frame_red, filtered_frame_blue)

                contours_red, _ = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                if contours_red:
                    largest_contour_red = max(contours_red, key=cv.contourArea)
                    M = cv.moments(largest_contour_red)
                    if M["m00"] != 0:
                        cX1 = int(M["m10"] / M["m00"])
                        cY1 = int(M["m01"] / M["m00"])
                        cv.circle(self.frame, (cX1, cY1), 5, (0, 0, 255), -1)
                        position_str = f"X1: {cX1}, Y1: {cY1}"
                        cv.putText(self.frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                contours_blue, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                if contours_blue:
                    largest_contour_blue = max(contours_blue, key=cv.contourArea)
                    M = cv.moments(largest_contour_blue)
                    if M["m00"] != 0:
                        cX2 = int(M["m10"] / M["m00"])
                        cY2 = int(M["m01"] / M["m00"])
                        cv.circle(self.frame, (cX2, cY2), 5, (255, 0, 0), -1)
                        position_str = f"X2: {cX2}, Y2: {cY2}"
                        cv.putText(self.frame, position_str, (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                data_string = "{},{},{},{}\n".format(cX1, cY1, cX2, cY2)
                ser.write(data_string.encode())

                csv_writer.writerow([cX1, cY1, cX2, cY2])

                self.rawCapture.truncate(0)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

        cv.destroyAllWindows()