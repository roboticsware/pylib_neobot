# Part of the RoboticsWare project - https://roboticsware.uz
# Copyright (C) 2022 RoboticsWare (neopia.uz@gmail.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import cv2
import os, datetime

class Camera(object):
    def __init__(self):
        self._videoInput = None

    def camera_open(self, cameraId):
        # Open the a camera, the index of default camera is 0
        self._videoInput = cv2.VideoCapture(cameraId)
        if self._videoInput.isOpened() == False:
            raise Exception("Camera is not opened.")
        return True

    def camera_close(self):
        if self._videoInput:
            self._videoInput.release()

    def __del__(self):
        self.camera_close()

    def _make_root_dir(self, path):
        path = path.replace('\\', '/')
        if path[-1:] != '/':
            path += '/'
        os.makedirs(path, exist_ok=True)
        return path
    
    def _make_file_path(self, path, prefix_name):
        path = path.replace('\\', '/')
        extension = '.png'
        name = prefix_name + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        file_list = os.listdir(path)
        name += extension
        path += name
        return path

    def capture_frame(self, dir_path):
        if self._videoInput == None or self._videoInput.isOpened() == False:
            raise Exception("Camera is not opened. Please first open a camera.")
        
        dir_path = self._make_root_dir(dir_path)
        print(f"Save frame images to {dir_path} folder.")
        print("Press 'c' to capture a frame, or press 'q' to quit.")
        captured_total = 0

        while True:
            _, frame = self._videoInput.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow("For capturing frames", frame)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q'):  # 'q' pressed
                break
            elif k == ord('c'):  # 'c' pressed
                img_name = self._make_file_path(dir_path, 'photo')
                cv2.imwrite(img_name, frame)
                print(img_name, "saved.")
                captured_total += 1
                print(captured_total, "frame(s) captured.")
        self.camera_close()

    def get_frame(self):
        if self._videoInput == None or self._videoInput.isOpened() == False:
            raise Exception("Camera is not opened. Please first open a camera.")
        _, frame = self._videoInput.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('Getting frame', frame)
        cv2.waitKey(1)
        return frame
