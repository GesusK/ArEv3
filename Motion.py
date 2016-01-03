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
  Rrio=2.15 # R_robot/R_wheel: 60/28=2.14285
  Wper=175.93 # perimeter of the powering wheels: 175.92919 mm

  # Configs
  angle=240
  rmp_sp=200
  run_sp=500 # running speed
  t_sp=400 # turning speed

  t_accuracy=2 # turning accuracy for Gyro, in degree
  r_accuracy=5 # running accuracy for Motor position, in degree
  adjust_sp = [100, 50]

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

  def forwardbyDistance(self, dist): # distance must be in cm, and positive
    if (dist == 0):
        return
    angle = int(abs(dist*10)/self.Wper*360)
    self.forwardbyAngle(angle)

    #self.forwardbySecond()

  def forwardbyAngle(self, angle):
    angtruth = [0, 0]
    angtmp = [angle, angle]

    # moving and adjusting loop
    loop_counter = 0;
    while(abs(angtmp[0])>=self.r_accuracy and abs(angtmp[1]) >=self.r_accuracy):
      angtruth = self.oneAngleForward(angtmp[0], angtmp[1])
      angtmp[0]=angtmp[0]-angtruth[0]
      angtmp[1]=angtmp[1]-angtruth[1]
      print "fore New angtmp: "+ str(angtmp)

  def oneAngleForward(self, left_ang, right_ang):

    # run the main movement
    self.reset()
    self.left.setup_position_limited(position_sp=left_ang, speed_sp=self.run_sp,
                                     stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.right.setup_position_limited(position_sp=right_ang, speed_sp=self.run_sp,
                                      stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.left.start()
    self.right.start()
    time.sleep(10)  # need to figure out how much needed
    self.stop()

    # adjust using low speed mode
    for v_adj in self.adjust_sp:
        self.left.setup_position_limited(position_sp=left_ang, speed_sp=v_adj,
                                         stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
        self.right.setup_position_limited(position_sp=right_ang, speed_sp=v_adj,
                                          stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
        self.left.start()
        self.right.start()
        time.sleep(1)

    return [self.left.position, self.right.position]

  def forwardbySecond(self, sec):
    self.reset();
    self.left.setup_time_limited(time_sp=sec, speed_sp=self.run_sp, speed_regulation=True)
    self.right.setup_time_limited(time_sp=sec, speed_sp=self.run_sp, speed_regulation=True)
    self.left.start()
    self.right.start()
    time.sleep(sec)
    self.stop()

  def runBackward(self):
    self.reset()
    self.left.setup_forever(-self.run_sp,speed_regulation=True)
    self.right.setup_forever(-self.run_sp,speed_regulation=True)
    self.left.start()
    self.right.start()

  def backwardbyDistance(self, dist): # distance must be in cm, and positive
    if (dist == 0):
        return
    angle = -int(abs(dist*10)/self.Wper*360)
    self.backwardbyAngle(angle)

  def backwardbyAngle(self, angle):
    angtruth = [0, 0]
    angtmp = [angle, angle]

    # moving and adjusting loop
    while(abs(angtmp[0])>=self.r_accuracy and abs(angtmp[1]) >=self.r_accuracy):
      angtruth = self.oneAngleForward(angtmp[0], angtmp[1])
      angtmp[0] = angtmp[0]+angtruth[0]
      angtmp[1] = angtmp[1]+angtruth[1]
      print "back New angtmp: "+ str(angtmp)

  def oneAngleBackward(self, left_ang, right_ang):
    self.reset()
    self.left.setup_position_limited(position_sp=-left_ang, speed_sp=self.run_sp,
                                     stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.right.setup_position_limited(position_sp=-right_ang, speed_sp=self.run_sp,
                                      stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)

    self.left.start()
    self.right.start()
    time.sleep(10)
    self.stop()

    # adjust using low speed mode
    for v_adj in self.adjust_sp:
        self.left.setup_position_limited(position_sp=-left_ang, speed_sp=v_adj,
                                         stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
        self.right.setup_position_limited(position_sp=-right_ang, speed_sp=v_adj,
                                          stop_mode=Motor.STOP_MODE.HOLD, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
        self.left.start()
        self.right.start()
        time.sleep(1)
    return [self.left.position, self.right.position]

  def turnRightbyAngle(self, ang):
    angtruth = 0
    angtmp = ang
    # moving and adjusting loop
    while (abs(angtmp)>self.t_accuracy):
      angtruth=self.oneAngleTurnRight(angtmp)
      angtmp=angtmp-angtruth
      #print "Diff: "+str(angtmp)

  def oneAngleTurnRight(self, ang):
    before=self.gyro.readAngle()
    #print "Before right turn: "+str(before)
    self.reset()
    self.left.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                     stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
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
    # moving and adjusting loop
    while (abs(angtmp)>self.t_accuracy):
      angtruth=self.oneAngleTurnLeft(angtmp)
      angtmp=angtmp+angtruth
      print "Diff: "+str(angtmp)

  def oneAngleTurnLeft(self, ang):
    before=self.gyro.readAngle()
    #print "Before right turn: "+str(before)
    self.reset()
    self.right.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.left.setup_position_limited(position_sp=-int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp)
    self.right.start()
    self.left.start()
    time.sleep(2)
    self.stop()
    after=self.gyro.readAngle()
    #print "After right turn: "+str(after)

    return after - before


  def stop(self):
    self.left.stop()
    self.right.stop()

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
              #k.runForward()
              k.forwardbyDistance(10)
              firstTime=0
          elif(mode == "s"):
              #k.runBackward()
              k.backwardbyDistance(10)
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
