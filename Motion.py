__author__ = 'Arthur'
'''
A set of classes to support basic motions for medium motors(for ultra sensor platform), and large motors(for moving).
'''
from ev3.ev3dev import Motor
from Sensor import Gyro
import time

# Driver class used for motion control and attitude adjust
class Driver():

  # Wheel motors
  left=None
  right=None

  # Sensors
  gyro=None

  # Paras
  Rrio=2.15 # 60/28=2.14285

  # Configs
  angle=240
  rmp_sp=200
  run_sp=500 # running speed
  t_sp=400 # turning speed

  t_accuracy=2

  def __init__(self):
    self.left=Motor(port=Motor.PORT.B)
    self.right=Motor(port=Motor.PORT.C)
    self.reset()

    self.gyro=Gyro()

  def reset(self):
    self.left.reset()
    self.right.reset()

  def runForward(self):
    self.reset()
    self.left.setup_forever(self.run_sp,speed_regulation = True)
    self.right.setup_forever(self.run_sp,speed_regulation = True)
    self.left.start()
    self.right.start()

  # def forwardDistance(self):

  def runBackward(self):
    self.reset()
    self.left.setup_forever(-self.run_sp,speed_regulation = True)
    self.right.setup_forever(-self.run_sp,speed_regulation = True)
    self.left.start()
    self.right.start()

  # def backwardDistance(self):

  def stop(self):
    self.left.stop()
    self.right.stop()

  def turnRightbyAngle(self, ang):
    angtruth = 0
    angtmp = ang
    # adjust loop
    while (abs(angtmp)>self.t_accuracy):
      angtruth=self.oneAngleTurnRight(angtmp)
      angtmp=angtmp-angtruth
      #print "Diff: "+str(angtmp)

  def oneAngleTurnRight(self, ang):
    before=self.gyro.readAngle()
    #print "Before right turn: "+str(before)
    self.reset()
    self.left.position=0
    self.left.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.right.position=0
    self.right.setup_position_limited(position_sp=-int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.left.start()
    self.right.start()
    time.sleep(2)
    self.stop()
    after=self.gyro.readAngle()
    #print "After right turn: "+str(after)

    return after - before

  def turnLeftbyAngle(self, ang):
    angtruth = 0
    angtmp = ang
    # adjust loop
    while (abs(angtmp)>self.t_accuracy):
      angtruth=self.oneAngleTurnLeft(angtmp)
      angtmp=angtmp+angtruth
      print "Diff: "+str(angtmp)

  def oneAngleTurnLeft(self, ang):
    before=self.gyro.readAngle()
    #print "Before right turn: "+str(before)
    self.reset()
    self.right.position=0
    self.right.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.left.position=0
    self.left.setup_position_limited(position_sp=-int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.right.start()
    self.left.start()
    time.sleep(2)
    self.stop()
    after=self.gyro.readAngle()
    #print "After right turn: "+str(after)

    return after - before

# script used for testing
if __name__ == '__main__':
  run=1
  firstTime=1
  k = Driver()
  pre_mode = "w"
  try:
    mode=str(raw_input("command:"))
  except ValueError:
    print "Wrong key in"

  while (True):
      print "pre="+pre_mode+" mode="+mode+" firstTime="+str(firstTime)+" run="+str(run)
      if (firstTime == 1):
          if(mode == "w"):
              k.runForward()
              firstTime=0
          elif(mode == "s"):
              k.runBackward()
              firstTime=0
          elif(mode == "d"):
              k.stop()
              k.turnRightbyAngle(90)
              mode = pre_mode
          elif(mode == "a"):
              k.stop()
              k.turnLeftbyAngle(90)
              mode = pre_mode
          elif(mode == "z"):
              k.stop()
              break
              firstTime=0
          elif(mode == "x"):
              k.stop()
              firstTime=0
          elif(firstTime == 1):
              firstTime=0
              print "Wrong input"
      else:
          new_mode = str(raw_input())

          if(new_mode != mode):
              pre_mode = mode
              mode = new_mode
              firstTime=1
      print "Bye~"
