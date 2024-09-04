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
import speech_recognition as sr
import gtts
import uuid, os
import playsound
from neopia.opencv_camera import Camera
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# For face mesh:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

class FaceMeshDetection(Camera):
    def __init__(self):
        super().__init__()

    def start_detection(self):
        result = False
        _, frame = self._videoInput.read()
        frame = cv2.flip(frame, 1)
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on the image.
        if results.multi_face_landmarks:
            annotated_image = frame.copy()
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
            # Show mesh on faces
            cv2.imshow('Face detection', annotated_image)
            result = True
        else:
            cv2.imshow('Face detection', frame)
            result = False
        cv2.waitKey(1)
    
        return result

    def __del__(self):
        super().__del__()


class FaceDetection(Camera):
    def __init__(self):
        super().__init__()
        self._face_cascade = cv2.CascadeClassifier(
            os.path.join(os.path.dirname(__file__), 'model', 'haarcascade_frontalface_default.xml'))

    def start_detection(self):
        _, frame = self._videoInput.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(gray, 1.1, 5)
        
        # Show rect on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Face detection', frame)
        cv2.waitKey(1)
    
        return len(faces)

    def __del__(self):
        super().__del__()


class QRDetection(Camera):
    def __init__(self):
        super().__init__()
        self._detector = cv2.QRCodeDetector()

    def start_detection(self):
        _, frame = self._videoInput.read()
        frame = cv2.flip(frame, 1)
        data, bbox, _ = self._detector.detectAndDecode(frame)

        if bbox is not None:
            bb_pts = bbox.astype(int).reshape(-1, 2)
            num_bb_pts = len(bb_pts)
            for i in range(num_bb_pts):
                cv2.line(frame, tuple(bb_pts[i]), tuple(bb_pts[(i+1) % num_bb_pts]),
                        color=(255, 0, 0), thickness=2)
                cv2.putText(frame, data, (bb_pts[0][0], bb_pts[0][1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)        
        cv2.imshow('QR detection', frame)
        cv2.waitKey(1)
        return data

    def __del__(self):
        super().__del__()


class Voice(object):
    @staticmethod
    def stt(audioId=0, language='uz-UZ'):
        r = sr.Recognizer()
        mic = sr.Microphone(audioId)
        audio = None
        with mic:
            r.adjust_for_ambient_noise(mic)
            audio = r.listen(mic, 3)  # Timeout in 3 sec
        try:
            result = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:  # The speech is unintelligible
            result = False
        except Exception as error:
            raise error
        return result
    
    @staticmethod
    def tts(text, lang='en'):
        tts = gtts.gTTS(text=text, lang=lang)
        fname = str(uuid.uuid1()) + ".mp3"
        with open(fname, 'wb+') as f:
            tts.write_to_fp(f)
        playsound.playsound(fname)
        os.remove(fname)

