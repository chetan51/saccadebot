class Classifier(object):


  def __init__(self, sdrThreshold=15, durationThreshold=4):
    self.sdrThreshold = sdrThreshold
    self.durationThreshold = durationThreshold

    self.activeIndices = set()
    self.duration = 0
    self.classes = {}  # mapping from label => set


  def feed(self, sdr):
    if len(sdr & self.activeIndices) >= self.sdrThreshold:
      self.activeIndices = sdr & self.activeIndices
      self.duration += 1
    else:
      self.activeIndices = sdr
      self.duration = 0

    if self.duration >= self.durationThreshold:
      key = self.classify(sdr)

      if key is None:
        key = len(self.classes)
        self.classes[key] = set()

      value = self.classes[key]
      value.update(sdr)
      return key


  def classify(self, sdr):
    for key, value in self.classes.iteritems():
      if len(value & sdr) >= self.sdrThreshold:
        return key

    return None
