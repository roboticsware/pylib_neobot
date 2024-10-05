from neopia import *

n = Neosoco()

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
od = ObjectDetection(target_fps=3, center_point_xy=True) 
if od.camera_open(0):  # Try 0, 1 or 2
    while True:
        detection_result = od.start_detection()
        print(f"Objects: {detection_result}")
        if detection_result:
            obj_names, obj_coords = detection_result
            if 'sports ball' in obj_names:  # It has to be a football/soccer ball, or just use other objects
                n.led_on('out1', '100')
                n.motor_rotate('both', 'forward', '10')
                wait(1000)
                n.led_off('out1')
            else:
                n.motor_rotate('both', 'left', '10')


import sys, keyboard
def on_press(key): 
    if key == Keyboard.ESC:
    #   sys.exit()
        return False
    
def on_space():
    print("pressed")
    sys.exit()
keyboard.add_hotkey('space', on_space)

# gd = GestureDetection(target_fps=10)
# if gd.camera_open(0):
#     while True:
#         category = gd.start_detection()
#         if category == "Open_Palm":
#             n.motor_move('forward')  
#         elif category == "Closed_Fist":
#             n.motor_stop()
#         elif category == "Thumb_Up":
#             n.motor_move('right')
#         elif category == "Thumb_Down":
#             n.motor_move('left')
#         elif category == "Pointing_Up":
#             n.motor_move('backward')


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
