from neopia import *

# n = Neosoco()

### Face detection
# fd = FaceDetection()
# if fd.camera_open(0):
#     while True:
#         if fd.start_detection() > 0:
#             print('Kimdir kirdi!!!')
#             n.led_on()
#             n.buzzer()
#             n.led_off()


### Face mesh detection
# fd = FaceMeshDetection()
# if fd.camera_open(0):
#     while True:
#         if fd.start_detection() > 0:
#             print('Kimdir kirdi!!!')
#             n.led_on()
#             n.buzzer()
#             n.led_off()


### Pose detection
# pd = PoseDetection()
# if pd.camera_open(0):
#     while True:
#         nose = pd.start_detection()
#         print(nose)


### Object detection (Following a sports ball)
# od = ObjectDetection() 
# if od.camera_open(0):  # Try 0, 1 or 2
#     while True:
#         detection_result = od.start_detection()
#         if detection_result:
#             obj_names, obj_coords = detection_result
#             print(f"Objects: {detection_result}")
#             if 'sports ball' in obj_names:  # It has to be a football/soccer ball, or just use other objects
#                 n.led_on('out1', '100')
#                 n.motor_rotate('both', 'forward', '10')
#                 wait(1000)
#                 n.led_off('out1')
#             else:
#                 n.motor_rotate('both', 'left', '10')


## Gesture detection
# gd = GestureDetection(target_fps=10)
# if gd.camera_open(0):
#     while True:
#         category = gd.start_detection()
#         if category == "Open_Palm":
#             print("Forward")
#             n.motor_move('forward')  
#         elif category == "Closed_Fist":
#             print("Stop")
#             n.motor_stop()
#         elif category == "Thumb_Up":
#             print("Right")
#             n.motor_move('right')
#         elif category == "Thumb_Down":
#             print("Left")
#             n.motor_move('left')
#         elif category == "Pointing_Up":
#             print("Backward")
#             n.motor_move('backward')


### QR code detection
# qr = QRDetection()
# if qr.camera_open(0):
#     while True:
#         decode_data = qr.start_detection()
#         if decode_data:
#             print(decode_data)
#             n.led_on()
#             n.buzzer()
#             n.led_off()


### Voice TTS / STT
# import time
# while True:
#     Voice.tts("I'm hearing. Please speak in 3 secconds.")
#     print("Eshityapman. 3 soniya ichida gapirib bering.")
#     result = Voice.stt()
#     print(result)
#     if result == "yoqing" or result == "yuking":
#         n.led_on()
#         time.sleep(3)
#         break
#     elif result == "o'chiring" or result == "uchiring":
#         n.led_off()
#         break