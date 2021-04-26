"""
Author --> Casper Nag
Release -> 25.04.2021
"""

import cv2
import sys
import time
from cameras import CameraController
from virtual_camera import VirtualCamera

cameras = [int(e) for e in sys.argv[1].split(',')]

vc = VirtualCamera((1920, 1080), 30)
cc = CameraController(cameras)

cc.start_cameras()

while True:

    frame = cc.read_selected_frame()
    vc.write(frame)

    try:
        if cv2.waitKey(10) & 0xFF == 27: break
    except KeyboardInterrupt:
        break

cc.active = False