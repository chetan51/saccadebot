#!/usr/bin/env python
import csv
from itertools import count
import random

from nupic.research.monitor_mixin.monitor_mixin_base import MonitorMixinBase

from model import Model
from robot import Robot



OUTFILE_PATH = "output.csv"



def main():
  print "Initializing..."
  robot = Robot()
  model = Model()

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
        motorValue = target - current
        row = [sensorValue, motorValue, i]
        csvWriter.writerow(row)
        csvFile.flush()

        model.feed(sensorValue, motorValue, sequenceLabel=i)
        print sorted(model.experimentRunner.tp.mmGetTraceActiveCells().data[-1])

      if behaviorType == "s":
        sweep(targets, robot, callback)
      elif behaviorType == "e":
        exhaustive(targets, robot, callback)
      elif behaviorType == "r":
        randomly(targets, robot, callback)

      print MonitorMixinBase.mmPrettyPrintTraces(
        model.experimentRunner.tm.mmGetDefaultTraces(verbosity=2) +
        model.experimentRunner.tp.mmGetDefaultTraces(verbosity=2))

      print MonitorMixinBase.mmPrettyPrintMetrics(
        model.experimentRunner.tm.mmGetDefaultMetrics() +
        model.experimentRunner.tp.mmGetDefaultMetrics())

      robot.reset()
      model.feed(None, None, sequenceLabel=i)  # Reset

      model.experimentRunner.tm.mmClearHistory()
      model.experimentRunner.tp.mmClearHistory()



def sweep(targets, robot, callback):
  # Start from first target
  robot.move(targets[0])

  for target in targets[1:]:
    current = robot.actuator.current_position
    sensorValue = robot.sensor.center_ir_sensor_value

    callback(sensorValue, current, target)

    robot.move(target)



def exhaustive(targets, robot, callback):
  moves = []
  currentPosition = targets[0]
  homePositions = list(targets)
  awayPositions = []

  while len(homePositions):
    if not len(awayPositions):
      newHomePosition = homePositions.pop(0)
      moves.append(newHomePosition)
      currentPosition = newHomePosition
      awayPositions = list(homePositions)

    while len(awayPositions):
      awayPosition = awayPositions.pop(0)
      moves.append(awayPosition)
      moves.append(currentPosition)

  moves.append(targets[0])  # Finish at start position

  sweep(moves, robot, callback)



def randomly(targets, robot, callback):
  num = input("Enter number of movements: ")
  target = None
  for _ in range(num):
    validTargets = list(set(targets) - set([target]))  # Don't allow repeats
    target = random.choice(validTargets)
    current = robot.actuator.current_position
    sensorValue = robot.sensor.center_ir_sensor_value

    callback(sensorValue, current, target)

    robot.move(target)



if __name__ == '__main__':
  main()
