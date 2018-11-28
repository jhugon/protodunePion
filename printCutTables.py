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

  cutConfigsGoodBeamline = [
    {"name": "All","cut": "1"},
    {"name": "CTB Beam Trigger","cut": "triggerIsBeam == 1"}, # CTB beam trigger
    {"name": "CTB BI Info Valid","cut": "BITrigger >= 0"}, # valid BI info in CTB
    {"name": "CTB TOF Coincidence","cut": "BITrigger > 0"}, # TOF coincidence according to CTB
    {"name": "CTB-BI Matched","cut": "BITriggerMatched > 0"}, # CTB event matched to BI event, TOF and fibers tracker info saved
    {"name": "> 0 Beam Tracks","cut": "nBeamTracks > 0"},
    {"name": "> 0 Beam Momenta","cut": "nBeamMom > 0"},
  ]

  cutGoodBeamline = {"name":"Good Beamline Event", "cut":"triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom > 0"}

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
    #{
    #  'fn': "piAbsSelector_run5145.root",
    #  'name': "run5145",
    #  'title': "Run 5145 7 GeV/c",
    #},
#    {
#      'fn': "piAbsSelector_run5174.root",
#      'name': "run5174",
#      'title': "Run 5174 7 GeV/c",
#      'caption': "Run 5174 7 GeV/c",
#    },
    #{
    #  'fn': "piAbsSelector_run5387.root",
    #  'name': "run5387",
    #  'title': "Run 5387 1 GeV/c",
    #},
    #{
    #  'fn': "piAbsSelector_run5430.root",
    #  'name': "run5430",
    #  'title': "Run 5430 2 GeV/c",
    #},
    #{
    #  'fn': "piAbsSelector_run5758.root",
    #  'name': "run5758",
    #  'title': "Run 5758 6 GeV/c",
    #},
    #{
    #  'fn': "piAbsSelector_run5777.root",
    #  'name': "run5777",
    #  'title': "Run 5777 3 GeV/c",
    #},
    #{
    #  'fn': "piAbsSelector_run5826.root",
    #  'name': "run5826",
    #  'title': "Run 5826 0.5 GeV/c",
    #},
    #{
    #  'fn': "piAbsSelector_run5834.root",
    #  'name': "run5834",
    #  'title': "Run 5834 0.3 GeV/c",
    #},
    {
      'fn': "PiAbs_redoBeamEvent_run5387.root",
      'name': "run5387_redo",
      'title': "Run 5387: 1 GeV/c Redo Beam Reco",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5430.root",
      'name': "run5430_redo",
      'title': "Run 5430: 2 GeV/c Redo Beam Reco",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5826.root",
      'name': "run5826_redo",
      'title': "Run 5826: 0.5 GeV/c Redo Beam Reco",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5834.root",
      'name': "run5834_redo",
      'title': "Run 5834: 0.3 GeV/c Redo Beam Reco",
    },
  ]

  #PrintCutTable(fileConfigsData,cutConfigs,"PiAbsSelector/tree",nMax=NMAX)
  #fileConfigsData[0]['tree'].Print()

  tofCuts = {
    "7": {
        "p": "1",
        "pi": "1",
        "e": "1",
        "k": "1",
    },
    "6": {
        "p": "1",
        "pi": "1",
        "e": "1",
        "k": "1",
    },
    "5": {
        "p": "1",
        "pi": "1",
        "e": "1",
        "k": "1",
    },
    "4": {
        "p": "1",
        "pi": "1",
        "e": "1",
        "k": "1",
    },
    "3": {
        "p": "1",
        "pi": "1",
        "e": "1",
        "k": "1",
    },
    "2": {
        "p": "TOF > 160.",
        "pi": "TOF < 160.",
        "e": "1",
        "k": "1",
    },
    "1": {
        "p": "TOF > 170.",
        "pi": "TOF < 170.",
        "e": "1",
        "k": "1",
    },
    "0.5": {
        "p": "TOF > 170.",
        "pi": "TOF < 170.",
        "e": "1",
        "k": "1",
    },
    "0.3": {
        "p": "TOF > 170.",
        "pi": "TOF < 170.",
        "e": "1",
        "k": "1",
    },
  }


  cherenkovCuts = {
    "7": {
        "p": "CKov0Status == 0 && CKov1Status == 0",
        "pi": "CKov0Status == 1 && CKov1Status == 1",
        "e": "CKov0Status == 1 && CKov1Status == 1",
        "k": "CKov0Status == 0 && CKov1Status == 1",
    },
    "6": {
        "p": "CKov0Status == 0 && CKov1Status == 0",
        "pi": "CKov0Status == 1 && CKov1Status == 1",
        "e": "CKov0Status == 1 && CKov1Status == 1",
        "k": "CKov0Status == 0 && CKov1Status == 1",
    },
    "5": {
        "p": "CKov0Status == 0 && CKov1Status == 0",
        "k": "CKov0Status == 0 && CKov1Status == 0",
        "pi": "CKov0Status == 0 && CKov1Status == 1",
        "e": "CKov0Status == 1 && CKov1Status == 1",
    },
    "4": {
        "p": "CKov0Status == 0 && CKov1Status == 0",
        "k": "CKov0Status == 0 && CKov1Status == 0",
        "pi": "CKov0Status == 0 && CKov1Status == 1",
        "e": "CKov0Status == 1 && CKov1Status == 1",
    },
    "3": {
        "p": "CKov0Status == 0 && CKov1Status == 0",
        "k": "CKov0Status == 0 && CKov1Status == 0",
        "pi": "CKov0Status == 0 && CKov1Status == 1",
        "e": "CKov0Status == 1 && CKov1Status == 1",
    },
    "2": {
        "p": "CKov1Status == 0",
        "k": "1", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "1": {
        "p": "CKov1Status == 0",
        "k": "1", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "0.5": {
        "p": "CKov1Status == 0",
        "k": "1", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "0.3": {
        "p": "CKov1Status == 0",
        "k": "1", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
  }

  def getCutForAllRuns(fileConfigs,cutDict,particle):
    result = "("
    for iFile, fileConfig in enumerate(fileConfigs):
      momStr = ""
      match = re.search(r" ([0-9.]+) GeV/c",fileConfig['title'])
      if match:
        momStr = match.group(1)
      else:
        raise Exception("Couldn't find momentum in title string: "+fileConfig['title'])
      runStr = ""
      match = re.search(r"Run ([0-9.]+)",fileConfig['title'])
      if match:
        runStr = match.group(1)
      else:
        raise Exception("Couldn't find run number in title string: "+fileConfig['title'])
      thisCut = cutDict[momStr][particle]
      thisCut = "(runNumber == {} && {})".format(runStr,thisCut)
      if iFile == 0:
        result += thisCut
      else:
        result += " || ("+thisCut+")"
    result += ")"
    return result

  print "\n\n"
  print "Good Beamline:"
  PrintCutTable(fileConfigsData,cutConfigsGoodBeamline,"PiAbsSelector/tree",nMax=NMAX)

  print "\n\n"
  print "Pion Selection:"
  cutConfigsPion = [
    {"name": "All","cut": "1"},
    cutGoodBeamline,
    {"name": "TOF Pion","cut": getCutForAllRuns(fileConfigsData,tofCuts,'pi')},
    {"name": "Cherenkov Pion","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'pi')},
    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
    {"name": "Pandora Tracklike","cut": "PFBeamPrimIsTracklike[0]"},
  ]
  PrintCutTable(fileConfigsData,cutConfigsPion,"PiAbsSelector/tree",nMax=NMAX)

  print "\n\n"
  print "Electron Selection:"
  cutConfigsElectron = [
    {"name": "All","cut": "1"},
    cutGoodBeamline,
    {"name": "TOF Electron","cut": getCutForAllRuns(fileConfigsData,tofCuts,'e')},
    {"name": "Cherenkov Electron","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'e')},
    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
    {"name": "Pandora Showerlike","cut": "PFBeamPrimIsShowerlike[0]"},
  ]
  PrintCutTable(fileConfigsData,cutConfigsElectron,"PiAbsSelector/tree",nMax=NMAX)

  print "\n\n"
  print "Proton Selection:"
  cutConfigsProton = [
    {"name": "All","cut": "1"},
    cutGoodBeamline,
    {"name": "TOF Proton","cut": getCutForAllRuns(fileConfigsData,tofCuts,'p')},
    {"name": "Cherenkov Proton","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'p')},
    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
    {"name": "Pandora Tracklike","cut": "PFBeamPrimIsTracklike[0]"},
  ]
  PrintCutTable(fileConfigsData,cutConfigsProton,"PiAbsSelector/tree",nMax=NMAX)

  print "\n\n"
  print "Kaon Selection:"
  cutConfigsKaon = [
    {"name": "All","cut": "1"},
    cutGoodBeamline,
    {"name": "TOF Kaon","cut": getCutForAllRuns(fileConfigsData,tofCuts,'k')},
    {"name": "Cherenkov Kaon","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'k')},
    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
    {"name": "Pandora Tracklike","cut": "PFBeamPrimIsTracklike[0]"},
  ]
  PrintCutTable(fileConfigsData,cutConfigsKaon,"PiAbsSelector/tree",nMax=NMAX)
