from neopia import *


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


### Object detection
# od = ObjectDetection(target_fps=5)
# if od.camera_open(0):
#     while True:
#         obj = od.start_detection()
#         print(obj)


# import sys, keyboard
# def on_press(key): 
#     if key == Keyboard.ESC:
#     #   sys.exit()
#         return False
    
# def on_space():
#     print("pressed")
#     sys.exit()
# keyboard.add_hotkey('space', on_space)

gd = GestureDetection(target_fps=12)
if gd.camera_open(0):
    while True:
        category = gd.start_detection()
        if category == "Open_Palm":
            n.motor_move('forward')  
        elif category == "Closed_Fist":
            n.motor_stop()
        elif category == "Thumb_Up":
            n.motor_move('right')
        elif category == "Thumb_Down":
            n.motor_move('left')
        elif category == "Pointing_Up":
            n.motor_move('backward')


### QR code detection
# qr = QRDetection()
# if qr.camera_open(1):
#     while True:
#         decode_data = qr.start_detection()
#         if decode_data:
#             print(decode_data)
#             n.led_on()
#             n.buzzer()
#             n.led_off()


### Voice TTS / STT
# import time
# result = False
# while not result:
#     try:    
#         Voice.tts("I'm hearing. Please speak in 3 secconds.")
#         print("Eshityapman. 3 soniya ichida gapirib bering.")
#         result = Voice.stt()
#         print(result)
#         if result == "Chiroqni yoq":
#             n.led_on()
#             time.sleep(3)
#         elif result == "Chiroqni o'chir":
#             n.led_off()
#             time.sleep(3)
#     except:
#         result = False
