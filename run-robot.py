#!/usr/bin/env python
import csv
from itertools import count
import random
import numpy as np
from nupic.research.monitor_mixin.monitor_mixin_base import MonitorMixinBase

from classifier import Classifier
from model import Model
from plot import Plot
from robot import Robot


OUTFILE_PATH = "output.csv"



def main():
  print "Initializing robot..."
  robot = Robot()
  print "Initializing model..."
  model = Model()
  print "Initializing plot..."
  plot = Plot()
  print "Initializing classifier..."
  classifier = Classifier()

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
        tpActiveCells = model.experimentRunner.tp.mmGetTraceActiveCells().data[-1]
        classification = classifier.feed(tpActiveCells)
        print "Classification: {0}".format(classification)
        print sorted(tpActiveCells)

        if classification is not None:
          robot.playTune(classification)

        plot.update(model)


      if behaviorType == "s":
        sweep(targets, robot, callback)
      elif behaviorType == "e":
        exhaustive(targets, robot, callback)
      elif behaviorType == "r":
        randomlyExplore(targets, robot, callback)

      print MonitorMixinBase.mmPrettyPrintTraces(
        model.experimentRunner.tm.mmGetDefaultTraces(verbosity=2) +
        model.experimentRunner.tp.mmGetDefaultTraces(verbosity=2),
        breakOnResets=model.experimentRunner.tm.mmGetTraceResets())

      print MonitorMixinBase.mmPrettyPrintMetrics(
        model.experimentRunner.tm.mmGetDefaultMetrics() +
        model.experimentRunner.tp.mmGetDefaultMetrics())

      robot.reset()

      doReset = raw_input("Reset (y/n)? ")
      if doReset == "y":
        model.experimentRunner.tm.reset()
        model.experimentRunner.tp.reset()

      model.experimentRunner.tm.mmClearHistory()
      model.experimentRunner.tp.mmClearHistory()



def sweep(targets, robot, callback):
  # Start from first target
  robot.move(targets[0])

  for target in targets[1:]:
    current = robot.actuator.current_position  
    sensorValue = robot.getSensorValue()
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
    sensorValue = robot.getSensorValue()

    callback(sensorValue, current, target)

    robot.move(target)



def randomlyExplore(targets, robot, callback):
  num = input("Enter number of movements: ")
  target = None
  
  past_path = []
  for _ in range(num):
    current_position = robot.actuator.current_position    
    validTargets = list(set(targets) - set([target]))  # Don't allow repeats
    frequency_count = [0] * len(validTargets)

    for target in range(len(validTargets)):
      for i in range(len(past_path)):
        if (past_path[i][0] == current_position and 
          past_path[i][1] == validTargets[target]):
            frequency_count[target] += 1
    
    # randomly pick one that has the minimum frequency count
    frequency_count = np.array(frequency_count)
    validTargets = np.array(validTargets)
    print frequency_count
    target = random.choice(
      [validTargets[np.where(frequency_count==min(frequency_count))[0]]][0])
    
    current = robot.actuator.current_position
    sensorValue = robot.getSensorValue()

    
    callback(sensorValue, current, target)

    robot.move(target)
    past_path.append([current_position, target])



if __name__ == '__main__':
  main()
