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
#     n.set_value('out1', 0)

# case4) Move forth and back during 1s and stop
n.motor_move('forward')
wait(500)
n.motor_move('backward')
wait(500)
n.motor_move('stop')