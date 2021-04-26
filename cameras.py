"""
Author --> Casper Nag
Release -> 25.04.2021
"""

import cv2
import sys
import time
import threading
import numpy as np
from multiprocessing import Process


class CameraController():

    def __init__(self, cameras):

        self.cameras = cameras
        self.frames = [[0, 0]]*len(self.cameras)
        self.faces = [0]*len(self.cameras)
        self.active = True
        self.selected_frame = 0


    def _read_frames(self, camera):

        cap = cv2.VideoCapture(camera)        

        while self.active:

            frame = cap.read()

            if frame[0]:
                self.frames[self.cameras.index(camera)] = frame
            else:    
                self.frames[self.cameras.index(camera)] = [0, np.zeros((1024, 576), np.float32)]

        cap.release()


    def _detector(self, camera):

        faceClassifier = cv2.CascadeClassifier("face.xml")
        eyeClassifier = cv2.CascadeClassifier("eye.xml")

        while self.active:

            total_frame = self.frames[camera]

            if total_frame[0]:
                frame = cv2.cvtColor(total_frame[1], cv2.COLOR_BGR2GRAY)

                eyes_ = 0
                faces = faceClassifier.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                eyes = eyeClassifier.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
                for (x, y, w, h) in faces:
                    for (ex, ey, ew, eh) in eyes:
                        if ex > x and ex < x+w:
                            if ey > y and ey < y+h:
                                eyes_ += 1


                self.faces[self.cameras.index(camera)] = len(faces)+eyes_
                selected = self.faces.index(max(self.faces))

                if not selected == self.cameras.index(camera):
                    self.selected_frame = selected
                    print(f"[LIVE] Camera {camera}")


    def read_selected_frame(self):

        return self.frames[self.selected_frame]


    def start_cameras(self):

        for camera in self.cameras:

            threading._start_new_thread(self._read_frames, (camera,))
            threading._start_new_thread(self._detector, (camera,))