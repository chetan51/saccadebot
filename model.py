from sensorimotor.sensorimotor_experiment_runner import SensorimotorExperimentRunner
from nupic.encoders import ScalarEncoder



class Model(object):


  def __init__(self):
    self.sensorEncoder = ScalarEncoder(n=100, w=11, minval=20, maxval=40,
                                       clipInput=True, forced=True)
    self.motorEncoder = ScalarEncoder(n=100, w=11, minval=-400, maxval=400,
                                      clipInput=True, forced=True)

    self.experimentRunner = SensorimotorExperimentRunner(
      tmOverrides={
        "columnDimensions": [512],
        "minThreshold": 11*2,
        "maxNewSynapseCount": 11*2,
        "activationThreshold": 11*2
      },
      tpOverrides={
        "columnDimensions": [512],
        "numActiveColumnsPerInhArea": 20,
      }
    )


  def feed(self, sensorValue, motorValue, sequenceLabel=None):
    sensorSDR = set(self.sensorEncoder.encode(sensorValue).nonzero()[0].tolist())
    motorSDR = set(self.motorEncoder.encode(motorValue).nonzero()[0].tolist())
    sensorimotorSDR = sensorSDR.union(motorSDR)

    self.experimentRunner.feedLayers([[sensorSDR],
                                      [motorSDR],
                                      [sensorimotorSDR],
                                      [sequenceLabel]],
                                     tmLearn=True, tpLearn=True)
