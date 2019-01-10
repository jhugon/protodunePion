#!/usr/bin/env python

from plotWires import *
import glob


class CaloCalibrationFactors(object):

  def __init__(self,fn,expectedMPV=1.74):
    self.fn = fn
    # wire, mpv, mpv err, nEvents
    self.entries = []
    with open(fn) as f:
      for row in f:
        row = row[:-1].split(",")
        entry = [int(row[0])]+ [float(i) for i in row[1:]]
        self.entries.append(entry)

    self.dataMPV = [expectedMPV]*3*480
    self.dataMPVErr = [expectedMPV]*3*480
    for entry in self.entries:
      self.dataMPV[entry[0]] = entry[1]
      self.dataMPVErr[entry[0]] = entry[2]
    self.sf = [expectedMPV/x for x in self.dataMPV]
    self.sfErr = [expectedMPV*(x/y/y) for x,y in zip(self.dataMPVErr,self.dataMPV)]

  def dump(self,outfilename):
    with open(outfilename,'w') as f:
      for sf in self.sf:
        f.write(str(sf)+'\n')

  def plot(self,fnPrefix="",fnPostfix=""):
    wireNums = numpy.arange(len(self.sf))
    mpv = numpy.array(self.dataMPV)
    mpvErr = numpy.array(self.dataMPVErr)
    sf = numpy.array(self.sf)
    sfErr = numpy.array(self.sfErr)

    fig, ax = mpl.subplots()
    ax.fill_between(wireNums,mpv-mpvErr,mpv+mpvErr,step='mid',facecolor='c',edgecolor='c')
    ax.plot(wireNums,mpv)
    ax.set_ylim(0,10)
    fig.savefig(fnPrefix+"MPV"+fnPostfix+".png")
    fig.savefig(fnPrefix+"MPV"+fnPostfix+".pdf")

    fig, ax = mpl.subplots()
    ax.fill_between(wireNums,sf-sfErr,sf+sfErr,step='mid',facecolor='c',edgecolor='c')
    ax.plot(wireNums,sf)
    ax.set_ylim(0,5)
    fig.savefig(fnPrefix+"sf"+fnPostfix+".png")
    fig.savefig(fnPrefix+"sf"+fnPostfix+".pdf")

if __name__ == "__main__":

  EXPECTEDMPV = 1.74

  caloCalib = CaloCalibrationFactors("Calibration_run5145.txt",EXPECTEDMPV)
  caloCalib.dump("CalibrationFactors_run5145.txt")
  try:
    import numpy
    import matplotlib.pyplot as mpl
  except:
    sys.exit(0)

  caloCalib.plot("CalibrationFactors_run5145_")

  
