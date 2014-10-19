#!/usr/bin/env python
import csv
from itertools import count

from model import Model
from robot import Robot



OUTFILE_PATH = "output.csv"



def main():
  print "Initializing..."
  robot = Robot()
  # model = Model()

  with open(OUTFILE_PATH, "wb") as csvFile:
    csvWriter = csv.writer(csvFile)

    for i in count(1):
      behaviorType = raw_input("Enter behavior type: "
                               "Exhaustive (e), Random (r), "
                               "Sweep (s), User (u): ")
      assert behaviorType in ["e", "r", "s", "u"]

      targets = input("Enter targets (Python code returning a list): ")
      assert len(targets)

      def callback(sensorValue, current, target):
        print "Current: {0}\tSensor: {1}\tNext: {2}".format(current,
                                                            sensorValue,
                                                            target)
        row = [sensorValue, target - current, i]
        csvWriter.writerow(row)
        csvFile.flush()

      if behaviorType == "s":
        sweep(targets, robot, callback)

      robot.reset()



def sweep(targets, robot, callback):
  # Start from first target
  robot.move(targets[0])

  for target in targets[1:]:
    current = robot.actuator.current_position
    sensorValue = robot.sensor.center_ir_sensor_value

    callback(sensorValue, current, target)

    robot.move(target)



if __name__ == '__main__':
  main()
