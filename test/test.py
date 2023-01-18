from neopia import *

n =  Neosoco()

## LED
# case1) Turn on LED with 100% brightness during 1s
# n.led_on('out1', '100')
# wait(1000)

# case2) Turn on LED with 100% brightness during 1s
# n.set_value('out1', 255)
# wait(1000)


## LED, distance sensor
# case3) Turn on LED when the distance is under 10cm
# while True:
#   if n.get_value('in1') < 10:
#     n.led_on('out1', '100')
#   else:
#     n.led_off('out1')

# case4) Control LED's brightness with sensor
# while True:
#     n.led_by_port('in1', 'out1')


## Motors
# case5) Move forth and back during 1s and stop
# n.motor_move('forward')
# wait(500)
# n.motor_move('backward')
# wait(500)
# n.motor_move('stop')

# case6) Moving control by direction keys on the keyboard
# while True:
#   key = Keyboard.read()

#   if key == Keyboard.UP:
#     n.motor_move('forward')
#   elif key == Keyboard.DOWN:
#     n.motor_move('backward')
#   elif key == Keyboard.LEFT:
#     n.motor_move('left')
#   elif key == Keyboard.RIGHT:
#     n.motor_move('right')
#   elif key == ' ':
#     n.motor_move('stop')

# case7) Move forth and back with speed 30% during 1s and stop
# n.motor_rotate('both', 'forward', '30')
# wait(500)
# n.motor_rotate('both', 'backward', '30')
# wait(500)
# n.motor_stop('both')


## Buzzer, Distance sensor
# case8) Play same note by pitch, sharp and flat, and a length of note
# n.buzzer('3', n.NOTE_NAME_C)
# n.buzzer('3', 'c')

# n.buzzer('4', n.NOTE_NAME_C_SHARP, '8')
# n.buzzer('4', 'c#', '8')

# n.buzzer('5', n.NOTE_NAME_D_FLAT, '16')
# n.buzzer('5', 'db', '16')

# case9) Play a sound by value from input port and Turn off buzzer if the distance is under 10cm
# while True:
#   if n.get_value('in1') < 10:
#     n.buzzer_stop()
#   else:
#     n.buzzer_by_port('in1')


## LED, Angle sensor
# case10) # Turn on LED when a degree of the angle sensor is under 90 degrees
# while True:
#   if n.get_angle('in1') < 90:
#     n.led_on('out1', '100')
#   else:
#     n.led_off('out1')


# Servo Motor
# case 11) Rotate servo motor forth and back with speed 50% during 5s and stop
# n.servo_rotate('out2', 'forward', '50')
# wait(2000)
# n.servo_rotate('out2', 'forward', '0')
# wait(1000)
# n.servo_rotate('out2', 'backward', '50')
# wait(2000)
# n.servo_stop('out2')
# wait(1000)

# case 12) Rotate servo motor forward by 120 degrees at 50% speed within 3 seconds
# n.servo_reset_degree('out1')
# n.servo_rotate_by_degree('out1', 'forward', '50', '120')
# wait(3000)


## Remote Controller
# case 13) When the 1 button of remote controller is pressed, turn on the LED
# while True:
#   if n.remote_button('1'):
#     n.led_on() # By default value
#   else:
#     n.led_off()


## Color LED / sensor
# case 14) Turn on LED when sensor detects green color
# while True:
#   print(n.get_value('in1'))
#   wait(500)
#   if n.check_color('in1', 'Green'):
#     n.led_on('out1', '100')
#   else:
#     n.led_off('out1')

# case 15) Turn on color LED with red color during 3s
# n.color_led_on('out1', 255, 0, 0)
# wait(3000)