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
    for entry in self.entries:
      self.dataMPV[entry[0]] = entry[1]
    self.sf = [expectedMPV/x for x in self.dataMPV]

  def dump(self,outfilename):
    with open(outfilename,'w') as f:
      for sf in self.sf:
        f.write(str(sf)+'\n')

if __name__ == "__main__":

  EXPECTEDMPV = 1.74

  caloCalib = CaloCalibrationFactors("Calibration_run5145.txt",EXPECTEDMPV)
  caloCalib.dump("CalibrationFactors_run5145.txt")

