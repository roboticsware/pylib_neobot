from neopia import *

n =  Neosoco()

# case1) Turn on LED with 100% brightness during 1s
# n.led_on('out1', '100')
# wait(1000)

# case2) Turn on LED with 100% brightness during 1s
# n.set_value('out1', 255)
# wait(1000)

# case3) Turn on LED when the distance is under 10cm
# while True:
#   if n.get_value('in1') < 10:
#     n.led_on('out1', '100')
#   else:
#     n.led_off('out1')

# case4) Move forth and back during 1s and stop
# n.motor_move('forward')
# wait(500)
# n.motor_move('backward')
# wait(500)
# n.motor_move('stop')



# case5) Moving cotrol by direction keys on the keyboard
# while True:
#   key = Keyboard.read()
# 
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


# case6) Turn on motor when the distance is under 10cm
while True:
  if n.get_value('in1') < 10:
    n.motor_stop('both')
  else:
    n.motor_move('forward')