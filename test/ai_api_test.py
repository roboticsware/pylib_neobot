from neopia import *

# n = Neosoco()

### WebCam or Notebook Camera
# c = Camera()
# if c.camera_open(1):
#     while True:
#         c.get_frame()


### Face detection
# fd = FaceDetection()
# if fd.camera_open(1):
#     while True:
#         if fd.start_detection() > 0:
#             print('Kimdir kirdi!!!')
            # n.led_on()
            # n.buzzer()
            # n.led_off()


### Face mesh detection
# fd = FaceMeshDetection()
# if fd.camera_open(1):
#     while True:
#         if fd.start_detection() > 0:
#             print('Kimdir kirdi!!!')
            # n.led_on()
            # n.buzzer()
            # n.led_off()


### Pose detection
# pd = PoseDetection()
# if pd.camera_open(1):
#     while True:
#         nose = pd.start_detection()
#         print(nose)


### Object detection
od = ObjectDetection()
if od.camera_open(1):
    while True:
        obj = od.start_detection()
        print(obj)


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
# result = False
# while not result:
#     try:    
#         Voice.tts("I'm hearing. Please speak in 3 secconds.")
#         print("Eshityapman. 3 soniya ichida gapirib bering.")
#         result = Voice.stt()
#         print(result)
#         if result == "Chiroqni yoq":
#             n.led_on()
#         elif result == "Chiroqni o'chir":
#             n.led_off()
#     except:
#         result = False

