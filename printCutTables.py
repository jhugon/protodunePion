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
    {"name": "Beam Trigger","cut": "triggerIsBeam == 1"},
    {"name": "nTracks","cut": "nTracks>3"},
    {"name": "nTracks","cut": "nTracks>80"},
  ]

  fileConfigsData = [
    {
      'fn': "PiAbsSelector.root",
      'name': "test",
    },
    {
      'fn': "piAbsSelector_run5141.root",
      'name': "run5141",
      'title': "Run 5141 7 GeV/c",
    },
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
  #fileConfigsData = [fileConfigsData[0]]

  PrintCutTable(fileConfigsData,cutConfigs,"PiAbsSelector/tree",nMax=NMAX)
