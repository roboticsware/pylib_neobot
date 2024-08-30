from neopia import *

n = Neosoco()

fd = FaceDetection()
if fd.camera_open(1):
    while True:
        if fd.start_detection() > 0:
            print('Kimdir kirdi!!!')
            n.led_on()
            n.buzzer()
            n.led_off()


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


# c = Camera()
# if c.camera_open(1) == True:
#     c.capture_frame('no_mask')