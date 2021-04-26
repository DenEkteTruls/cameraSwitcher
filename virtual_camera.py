"""
Author --> Casper Nag
Release -> 25.04.2021
"""

import cv2
import numpy as np
import pyvirtualcam as pvc

class VirtualCamera():

    """
    Viktige variabler: (self.active, self.write(self, frame))
    """

    def __init__(self, size, FPS):

        self.size = size
        self.active = True
        self.camera = pvc.Camera(width=size[0], height=size[1], fmt=pvc.PixelFormat.BGR, fps=FPS)
        print(f"Skriver til {self.camera.device} :)")


    def write(self, frame):

        if frame[0]:
            self.camera.send(cv2.resize(frame[1], self.size))
            self.camera.sleep_until_next_frame()