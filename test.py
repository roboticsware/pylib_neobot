from neobot import *

n =  Neosoco()

# case1) Turn on LED with 100% brightness during 1s
# n.led_on("out1", '100')
# wait(1000)

n.set_value("out1", 255)
wait(1000)

# case2) Turn on LED when the distance is under 10cm
# while True:
#   if n.get_value('in1') < 10:
#     n.led_on("out1", 255)
#   else:
#     n.led_on("out1", 0)