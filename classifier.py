class Classifier(object):


  def __init__(self, sdrThreshold=12, durationThreshold=3):
    self.sdrThreshold = sdrThreshold
    self.durationThreshold = durationThreshold

    self.stableSdr = set()
    self.duration = 0
    self.classes = {}  # mapping from label => set


  def feed(self, sdr):
    if len(sdr & self.stableSdr) >= self.sdrThreshold:
      self.stableSdr = sdr & self.stableSdr
      self.duration += 1
    else:
      self.stableSdr = sdr
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
      # TODO: Return closest match, not first match
      if len(value & sdr) >= self.sdrThreshold:
        return key

    return None
