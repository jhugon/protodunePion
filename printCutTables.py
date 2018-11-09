#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy

m2SF=1000.
tofOffset=61.4
tofDistance = 28.0
lightTime = tofDistance/2.99e8*1e9
momSF=1.0

if __name__ == "__main__":

  NMAX=10000000000
  #NMAX=10

  cutConfigs = [
    {"name": "All","cut": "1"},
    {"name": "CTB Beam Trigger","cut": "triggerIsBeam == 1"}, # CTB beam trigger
    {"name": "CTB BI Info Valid","cut": "BITrigger >= 0"}, # valid BI info in CTB
    {"name": "CTB TOF Coincidence","cut": "BITrigger > 0"}, # TOF coincidence according to CTB
    {"name": "CTB-BI Matched","cut": "BITriggerMatched > 0"}, # CTB event matched to BI event, TOF and fibers tracker info saved
    {"name": "> 0 Beam Momentum","cut": "nBeamMom > 0"},
    {"name": "> 0 Beam Track","cut": "nBeamTracks > 0"},
    #{"name": "CKov0 is 1","cut": "CKov0Status == 1"},
    #{"name": "CKov1 is 1","cut": "CKov1Status == 1"},
    #{"name": "TOF < 160 ns","cut": "TOF < 160."},
  ]

  fileConfigsData = [
    #{
    #  'fn': "PiAbsSelector.root",
    #  'name': "test",
    #},
    #{
    #  'fn': "piAbsSelector_run5141.root",
    #  'name': "run5141",
    #  'title': "Run 5141 7 GeV/c",
    #},
    {
      'fn': "piAbsSelector_run5145.root",
      'name': "run5145",
      'title': "Run 5145 7 GeV/c",
    },
#    {
#      'fn': "piAbsSelector_run5174.root",
#      'name': "run5174",
#      'title': "Run 5174 7 GeV/c",
#      'caption': "Run 5174 7 GeV/c",
#    },
    {
      'fn': "piAbsSelector_run5387.root",
      'name': "run5387",
      'title': "Run 5387 1 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5430.root",
      'name': "run5430",
      'title': "Run 5430 2 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5758.root",
      'name': "run5758",
      'title': "Run 5758 6 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5777.root",
      'name': "run5777",
      'title': "Run 5777 3 GeV/c",
    },
  ]

  PrintCutTable(fileConfigsData,cutConfigs,"PiAbsSelector/tree",nMax=NMAX)
  #fileConfigsData[0]['tree'].Print()
