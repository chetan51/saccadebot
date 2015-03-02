import matplotlib.pyplot as plt
from matplotlib.pylab import ion, draw
import matplotlib.cm as cm
import numpy as np 



class Plot(object):


  def __init__(self,model):
    
    # TODO: Refactor columnDimensionsL4
    self.columnDimensionsL4 = (
      model.experimentRunner.tm.columnDimensions[0])
    self.columnDimensionsL3 = model.experimentRunner.tp._numColumns
    self.sensoryInputDim = model.sensorEncoder.n
    self.motorInputDim = model.motorEncoder.n
    self.sensoryInputNumActive = model.sensorEncoder.w

    self.l4Activity = np.zeros((self.columnDimensionsL4, 1))
    self.l3Activity = np.zeros((self.columnDimensionsL3, 1))

    self.numPredictedInput = [0]
    self.numExtraPredictedInput = [0]

    # establish an empty plot
    self.plot = plt.figure()
    plt.clf()
    plt.gca().invert_yaxis()
    ion() # interactive mode on
    plt.show()


  def update(self, model):
    """
    update figure 
    """
    # L4 and L3 activity
    L4_active = np.zeros((self.columnDimensionsL4, 1))
    L3_active = np.zeros((self.columnDimensionsL3, 1))
    if len(model.experimentRunner.tm.mmGetTraceActiveColumns().data)>0:
        L4_active[list(model.experimentRunner.tm.mmGetTraceActiveColumns().data[-1])] = 1

    self.l4Activity = np.concatenate((self.l4Activity, L4_active),1)

    if len(model.experimentRunner.tp.mmGetTraceActiveCells().data)>0:
        L3_active[list(model.experimentRunner.tp.mmGetTraceActiveCells().data[-1])] = 1
    self.l3Activity = np.concatenate((self.l3Activity, L3_active),1)

    # correctly predicted cells
    self.numPredictedInput.append( 
        len(model.experimentRunner.tm.mmGetTracePredictedActiveCells().data[-1]) )
    
    # extra predicted cells in L4
    self.numExtraPredictedInput.append(
        len(model.experimentRunner.tm.mmGetTracePredictedInactiveCells().data[-1]))
    
    self.display()


  def display(self):
    nrol = 3
    plt.subplot(nrol, 1, 1)
    plt.imshow(self.l3Activity, cmap = cm.Greys_r, \
                aspect="auto",interpolation="nearest")    
    plt.ylabel(' L3 Activity ')


    ax = plt.subplot(nrol, 1, 2)
    plt.imshow(self.l4Activity, cmap = cm.Greys_r, \
                aspect="auto",interpolation="nearest")
    plt.ylabel(' L4 Activity ')
    xmin, xmax = plt.xlim()

    ax = plt.subplot(nrol, 1, 3)
    numUnPredicted = self.sensoryInputNumActive - np.array(self.numPredictedInput)
    plt.plot(numUnPredicted,'b-',linewidth=4.0)    
    ax.set_ylim([-1, 22])
    plt.ylabel(' # Unpredicted ')
    plt.xlim(xmin, xmax)

    draw()
