from sensorimotor.sensorimotor_experiment_runner import SensorimotorExperimentRunner
from nupic.encoders import ScalarEncoder



class Model(object):


  def __init__(self):
    self.sensorEncoder = ScalarEncoder(n=100, w=21, minval=8.9, maxval=40,
                                       clipInput=True, forced=True)
    self.motorEncoder = ScalarEncoder(n=100, w=21, minval=-400, maxval=400,
                                      clipInput=True, forced=True)

    self.experimentRunner = SensorimotorExperimentRunner(
      tmOverrides={
        "columnDimensions": [100],
        "maxNewSynapseCount": 21*2,
        "minThreshold": 16*2,
        "activationThreshold": 16*2
      },
      tpOverrides={
        "columnDimensions": [100],
        "numActiveColumnsPerInhArea": 20,
      }
    )


  def feed(self, sensorValue, motorValue, sequenceLabel=None):    
    sensorSDR = set(self.sensorEncoder.encode(sensorValue).nonzero()[0].tolist())
    motorSDR = set((self.motorEncoder.encode(motorValue).nonzero()[0] +
                    self.sensorEncoder.n).tolist())
    sensorimotorSDR = sensorSDR.union(motorSDR)

    self.experimentRunner.feedTransition(sensorSDR, sensorimotorSDR,
                                         tmLearn=True, tpLearn=True,
                                         sequenceLabel=sequenceLabel)
