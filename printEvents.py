#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import os.path

if __name__ == "__main__":

  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status","BITrigger","BITriggerMatched","BIActiveTrigger","triggerIsBeam"]
  varNames = ["beamMom","TOF","CKov0Status","CKov1Status"]
  cuts = {
    #"triggerIsBeam": ["=",1],
    #"BITrigger": [">",0],
    "BITriggerMatched": ["==",1],
  }

  #print "Run 5145, 7 GeV/c"
  #printEvents("piAbsSelector_run5145.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  print "Run 5766, 6 GeV/c"
  printEvents("piAbsSelector_run5766.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  print "Run 5780, 3 GeV/c"
  printEvents("piAbsSelector_run5780.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)

