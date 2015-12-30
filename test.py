#!/home/arthur/.virtualenvs/ev3py27/bin/python
# a test script for basic motion model
from ev3.ev3dev import Motor
from ev3.lego import GyroSensor
import unittest
import time

class Mover():

  # Moving motors
  left=None;
  right=None;
  
  # Sensors
  gyro=None;

  # Paras
  Rrio=2.15; # 60/28=2.14285
  # Configs
  angle=240;
  rmp_sp=200;
  run_sp=500; # running speed
  t_sp=400; # turning speed
  def __init__(self):
	self.left=Motor(port=Motor.PORT.B);
	self.right=Motor(port=Motor.PORT.C);
	self.left.reset();
	self.right.reset();
        self.gyro=GyroSensor();

  def readAngle(self,RESET=0):
    if(RESET==1):
      self.gyro.rate;
    return self.gyro.ang;

  def reset(self):
	self.left.reset();
	self.right.reset();

  def runForward(self):
        self.reset();
	self.left.setup_forever(self.run_sp,speed_regulation = True);
	self.right.setup_forever(self.run_sp,speed_regulation = True);
	self.left.start();
	self.right.start();

  def runBackward(self):
        self.reset();
	self.left.setup_forever(-self.run_sp,speed_regulation = True);
	self.right.setup_forever(-self.run_sp,speed_regulation = True);
	self.left.start();
	self.right.start();

  def stop(self):
	self.left.stop();
	self.right.stop();

  def turnRightbyAngle(self, ang):
    angtruth = 0;
    angtmp = ang;
    # adjust loop
    while (abs(angtmp)>3):
      angtruth=self.oneAngleTurnRight(angtmp);
      angtmp=angtmp-angtruth;
      #print "Diff: "+str(angtmp);

  def oneAngleTurnRight(self, ang):
    before=self.readAngle(RESET=1);
    #print "Before right turn: "+str(before);
    self.reset();
    self.left.position=0;
    self.left.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp);
    self.right.position=0;
    self.right.setup_position_limited(position_sp=-int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp);
    self.left.start();
    self.right.start();
    time.sleep(2);
    self.stop();
    after=self.readAngle();
    #print "After right turn: "+str(after);

    return after - before;

  def turnLeftbyAngle(self, ang):
    angtruth = 0;
    angtmp = ang;
    # adjust loop
    while (abs(angtmp)>3):
      angtruth=self.oneAngleTurnLeft(angtmp);
      angtmp=angtmp+angtruth;
      print "Diff: "+str(angtmp);

  def oneAngleTurnLeft(self, ang):
    before=self.readAngle(RESET=1);
    print "Before right turn: "+str(before);
    self.reset();
    self.right.position=0;
    self.right.setup_position_limited(position_sp=int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp);
    self.left.position=0;
    self.left.setup_position_limited(position_sp=-int(ang*self.Rrio), speed_sp=self.t_sp,
                                   stop_mode=Motor.STOP_MODE.BRAKE, ramp_up_sp=self.rmp_sp, ramp_down_sp=self.rmp_sp);
    self.right.start();
    self.left.start();
    time.sleep(2);
    self.stop();
    after=self.readAngle();
    print "After right turn: "+str(after);

    return after - before;
    

if __name__ == '__main__':
  run=1;
  firstTime=1;
  k = Mover();
  pre_mode = "w";
  try:
    mode=str(raw_input("command:"));
  except ValueError:
    print "Wrong key in";

  while (run == 1):
    print "pre="+pre_mode+" mode="+mode+" firstTime="+str(firstTime)+" run="+str(run);
    if(firstTime==1 and mode == "w"):
      k.runForward();
      firstTime=0;  
    elif(firstTime == 1 and mode == "s"):
      k.runBackward();
      firstTime=0;
    elif(firstTime == 1 and mode == "d"):
      k.stop();
      k.turnRightbyAngle(90);
      mode = pre_mode;
    elif(firstTime == 1 and mode == "a"):
      k.stop();
      k.turnLeftbyAngle(90);
      mode = pre_mode;
    elif(firstTime == 1 and mode == "z"):
      k.stop();
      break;
      firstTime=0;
    elif(firstTime == 1 and mode == "p"):
      k.stop();
      firstTime=0;
    elif(firstTime == 1):
      firstTime=0;
      print "Wrong input"
    
    if (firstTime != 1):
      new_mode = str(raw_input());

      if(new_mode != mode):
        pre_mode = mode;
        mode = new_mode;
        firstTime=1;

print "Bye~"
