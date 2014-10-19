import dynamixel
import time

PORT = "/dev/tty.usbserial-A501ELE8"
BAUD = 1000000


class Robot(object):


  def __init__(self):
    # Establish a serial connection to the dynamixel network.
    # This usually requires a USB2Dynamixel
    serial = dynamixel.SerialStream(port=PORT, baudrate=BAUD, timeout=1)
    net = dynamixel.DynamixelNetwork(serial)
    self.net = net

    # Create our sensor object. Sensor is assumed to be at id 100
    self.sensor = dynamixel.SensorModule(100, net)

    # Populate our network with dynamixel objects
    servoId = 1
    newDynamixel = dynamixel.Dynamixel(servoId, net)
    net._dynamixel_map[servoId] = newDynamixel

    # Set up the servos
    actuator = self.net.get_dynamixels()[0]
    self.actuator = actuator

    self.reset()


  def reset(self):
    actuator = self.actuator
    actuator.torque_enable = True
    actuator.torque_limit = 800
    actuator.max_torque = 800
    actuator.moving_speed = 1023

    self.move(512)

  def move(self, target):
    self.actuator.goal_position = target
    self.net.synchronize()
    time.sleep(1.25)

  def getSensorValue(self):
    sensorValue = self.linearizeInput(
                  self.sensor.center_ir_sensor_value)
    return sensorValue
    
  @staticmethod
  def linearizeInput(sensorValue):
    import math
    if sensorValue < 13.0655:
      dist = 40
    else:
      dist = - (math.log((sensorValue-13.0655)/52.4871) - 3.0533) / 0.1708
    return dist
