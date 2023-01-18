from neopia import *

socos = (Neosoco(0), Neosoco(1))

# wait until two robots are ready
wait_until_ready()

def init():
  for soco in socos:
    soco.servo_reset_degree() # servo moto init

def ready_condition(soco):
  print(soco.get_value('in3'))
  return soco.get_value('in3') < 30

def act_condition(soco):
  print(soco.get_value('in3'))
  return soco.get_value('in3') > 70 # when recognize a clap

def led_blink(soco):
  soco.led_on('out3')
  wait(500)
  soco.led_off('out3')
  wait(500)

def wag_tail(soco):
  soco.servo_rotate_by_degree('out1', 'forward', '100', '60')
  soco.servo_rotate_by_degree('out1', 'backward', '100', '0')
  soco.servo_rotate_by_degree('out1', 'backward', '100', '60')
  soco.servo_rotate_by_degree('out1', 'forward', '100', '0')

def move_forth_back(soco, reverse=False):
  if reverse:
    dir1 = 'backward'
    dir2 = 'forward' 
  else:
    dir1 = 'forward'
    dir2 = 'backward'

  soco.motor_move(dir1)
  wait(1000)
  soco.motor_move(dir2)
  wait(1000)
  soco.motor_stop('both')

def turn_right_left(soco, reverse=False):
  if reverse:
    wheel1 = 'right'
    wheel2 = 'left'
  else:
    wheel1 = 'left'
    wheel2 = 'right'
    
  soco.motor_rotate(wheel1, 'forward', '30') # turn right
  soco.motor_rotate(wheel2, 'backward', '30')
  wait(2000)
  soco.motor_rotate(wheel2, 'forward', '30') # turn left
  soco.motor_rotate(wheel1, 'backward', '30')
  wait(2000)
  soco.motor_stop('both')

def dance(soco):
  move_forth_back(soco)
  move_forth_back(soco, True)
  turn_right_left(soco)
  turn_right_left(soco, True)

  soco.motor_move('forward')
  wait(1000)
  soco.motor_stop('both')

init()
for soco in socos:
  while_do(ready_condition, led_blink, soco)
  while_do(ready_condition, wag_tail, soco)
  when_do(act_condition, dance, soco)
wait(-1) # wait forever