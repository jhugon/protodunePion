#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import os.path

if __name__ == "__main__":

  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status","BITrigger","BITriggerMatched","BIActiveTrigger","triggerIsBeam"]
  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status"]
  varNames = [#"beamMom",
                "TOF",
                #"primTrkStartX","primTrkStartY","primTrkStartZ","primTrkLength",
                #"PFBeamPrimStartX","PFBeamPrimStartY","PFBeamPrimStartZ","PFBeamPrimTrkLen",
                #"PFBeamPrimIsTracklike"
            ]
  cuts = {
    "triggerIsBeam": ["=",1],
    "BITrigger": [">",0],
    "BITriggerMatched": [">",0],
    #"CKov1Status":["=",0],
    #"CKov0Status":["=",1],
    "TOF":[">",180.], # should be ~191 raw TOF for Deuterons at 2 GeV, 172 at 3GeV so maybe cut 168 at 2 GeV
  }

  #print "Run 5145, 7 GeV/c"
  #printEvents("piAbsSelector_run5145_v4.4.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=1000,printFileBasename=True)
  print "Run 5432, 2 GeV/c @ LSU, Deuteron Cut"
  printEvents("piAbsSelector_run5432_v4.4.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100,printFileBasename=True)
  print "Run 5432, 2 GeV/c @ Fermilab, Deuteron Cut"
  printEvents("piAbsSelector_run5432_v3.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  #print "Run 5758, 6 GeV/c"
  #printEvents("piAbsSelector_run5758.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  #print "Run 5780, 3 GeV/c"
  #printEvents("piAbsSelector_run5780.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)

  #print "MCC11 FLF 2 GeV v4.4"
  #varNames = ["trueCategory","trueEndProcess","trueEndProcess","trueStartMom","trueEndX","trueEndY","trueEndZ"]
  #cuts = {
  #  "truePrimaryPDG": ["==",211],
  #}
  #printEvents("piAbsSelector_mcc11_flf_2p0GeV_v4.4.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
