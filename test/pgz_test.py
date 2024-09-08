import pgzrun
from pgzhelper import *
from pgzhelper import Util
from neopia import *

# n = Neosoco()

WIDTH = 640
HEIGHT =  480
pygame_img = None

#### Camera
# c = Camera()
# if c.camera_open(1) is False:
#     game.exit()

# def draw():
#     screen.blit(pygame_img, (0, 0))

# def update():
#     global pygame_img
#     frame = c.get_frame()
#     pygame_img = Util.opencv_to_pygame_img(frame)


#### Face detection
# detected = False
# red_led = Actor('red_led_off', (600, 60))
# red_led.images = ['red_led_on', 'red_led_off']
# red_led.scale = 0.5
# red_led.fps = 15

# fd = FaceDetection()
# if fd.camera_open(1) is False:
#     game.exit()

# def draw():
#     if detected:
#         screen.blit(pygame_img, (0, 0))
#         red_led.draw()
#         n.led_on()
#         n.buzzer()
#         n.led_off()
#     else:
#         screen.blit('living_room', (0, 0))

# def update():
#     global pygame_img
#     global detected

#     frame, faces = fd.start_detection(just_rtn_frame=True)
#     pygame_img = Util.opencv_to_pygame_img(frame)

#     if faces > 0:
#         detected = True
#         red_led.next_image()
#         print('Detected!!!')
#     else:
#         detected = False


# def on_key_down(key):
#     if key == keys.SPACE: 
#         game.exit()


#### Face mesh detection
# fd = FaceMeshDetection()
# if fd.camera_open(1) is False:
#     game.exit()

# def draw():
#     screen.blit(pygame_img, (0, 0))

# def update():
#     global pygame_img
#     frame = fd.start_detection(just_rtn_frame=True)
#     pygame_img = Util.opencv_to_pygame_img(frame)


#### Object detection
# od = ObjectDetection()
# if od.camera_open(1) is False:
#     game.exit()

# def draw():
#     screen.blit(pygame_img, (0, 0))

# def update():
#     global pygame_img
#     frame = od.start_detection(just_rtn_frame=True)
#     pygame_img = Util.opencv_to_pygame_img(frame)


#### Pose detection
# detected = False
# nose_pos = None
# soch = Actor('soch_qiz.png')
# soch.scale = 0.3

# pd = PoseDetection()
# if pd.camera_open(1) is False:
#     game.exit()

# def draw():
#     screen.blit(pygame_img, (0, 0))
#     if detected:
#         soch.midbottom = nose_pos
#         soch.draw()

# def update():
#     global pygame_img, detected, nose_pos
#     frame, pos = pd.start_detection(just_rtn_frame=True)
#     nose_pos = pos
#     pygame_img = Util.opencv_to_pygame_img(frame)
#     if nose_pos is not (0, 0):
#         detected = True
#     else:
#         detected = False


## Gesture detection
entrybot = Actor('entrybot', (400, 150))
entrybot.scale = 0.5

category = None
gd = GestureDetection()
if gd.camera_open(1) is False:
    game.exit()

def draw():
    screen.blit(pygame_img, (0, 0))
    entrybot.draw()
    if category == "Thumb_Up":
        entrybot.say("Assalomu alaykum aziz o'quvchilar.", 200, 80)
        Voice.playsound("sounds/1.mp3")
    elif category == "ILoveYou":
        entrybot.say("Hamma sizlarni sevaman. Rahmat.", 200, 80)
        Voice.playsound("sounds/5.mp3")

def update():
    global pygame_img, category
    frame, gesture = gd.start_detection(just_rtn_frame=True)
    category = gesture
    pygame_img = Util.opencv_to_pygame_img(frame)

pgzrun.go()




