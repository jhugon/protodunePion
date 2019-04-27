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

  c = root.TCanvas()

  NMAX=10000000000
  #NMAX=100

  cutConfigsGoodBeamline = [
    #{"name": "All","cut": "1"},
    {"name": "Timing Beam Trigger","cut": "triggerIsBeam == 1"},
    {"name": "Matched Beam Trigger to Timing Trigger","cut": "BITriggerMatched > 0"}, # CTB event matched to BI event, TOF and fibers tracker info saved
    {"name": "CTB BI Info Valid","cut": "BITrigger >= 0"}, # valid BI info in CTB
    {"name": "TOF Info Valid","cut": "BITrigger > 0"}, # TOF coincidence according to CTB
    {"name": "> 0 Beam Tracks","cut": "nBeamTracks > 0"},
    {"name": "> 0 Beam Momenta","cut": "nBeamMom > 0"},
    {"name": "Exactly 1 Beam Tracks","cut": "nBeamTracks == 1"},
    {"name": "Exactly 1 Beam Momenta","cut": "nBeamMom == 1"},
  ]

  cutConfigsGoodBeamlineOld = [
    #{"name": "All","cut": "1"},
    {"name": "Timing Beam Trigger","cut": "isMC || triggerIsBeam == 1"},
    {"name": "Matched Beam Trigger to Timing Trigger","cut": "isMC || BITriggerMatchedOld > 0"}, # CTB event matched to BI event, TOF and fibers tracker info saved
    {"name": "CTB BI Info Valid","cut": "isMC || BITriggerOld >= 0"}, # valid BI info in CTB
    {"name": "TOF Info Valid","cut": "isMC || BITriggerOld > 0"}, # TOF coincidence according to CTB
    {"name": "> 0 Beam Tracks","cut": "isMC || nBeamTracksOld > 0"},
    {"name": "> 0 Beam Momenta","cut": "isMC || nBeamMomOld > 0"},
    {"name": "Exactly 1 Beam Tracks","cut": "isMC || nBeamTracksOld == 1"},
    {"name": "Exactly 1 Beam Momenta","cut": "isMC || nBeamMomOld == 1"},
  ]

  cutConfigsGoodBeamlineNew = [
    #{"name": "All","cut": "1"},
    {"name": "Timing Beam Trigger","cut": "isMC || triggerIsBeam == 1"},
    {"name": "Matched Beam Trigger to Timing Trigger","cut": "isMC || BITriggerMatched > 0"}, # CTB event matched to BI event, TOF and fibers tracker info saved
    {"name": "> 0 Beam Tracks","cut": "isMC || nBeamTracks > 0"},
    {"name": "> 0 Beam Momenta","cut": "isMC || nBeamMom > 0"},
    {"name": "Exactly 1 Beam Tracks","cut": "isMC || nBeamTracks == 1"},
    {"name": "Exactly 1 Beam Momenta","cut": "isMC || nBeamMom == 1"},
  ]

  cutGoodBeamlineOld = "(isMC || (triggerIsBeam == 1 && BITriggerMatchedOld > 0 && BITriggerOld > 0 && nBeamTracksOld == 1 && nBeamMomOld == 1))"
  cutGoodBeamlineNew = "(isMC || (triggerIsBeam == 1 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1))"

  cutGoodBeamline = {"name":"Silver Beamline Event", "cut":"(isMC || (triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom > 0))"}
  cutGoodBeamline = {"name":"Golden Beamline Event", "cut":"(isMC || (triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1))"}

  fileConfigsMC = [
    {
      'fn': "piAbsSelector_mcc11_sce_1GeV_histats_partAll_v7a1_55712adf.root",
      'name': "mcc11_sce_1p0GeV",
      'title': "MCC 11 1 GeV/c SCE",
    },
    {
      'fn': "piAbsSelector_mcc11_sce_2GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_2p0GeV",
      'title': "MCC 11 2 GeV/c SCE",
    },
    {
      'fn': "piAbsSelector_mcc11_sce_3GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_3p0GeV",
      'title': "MCC 11 3 GeV/c SCE",
    },
    {
      'fn': "piAbsSelector_mcc11_sce_6GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_6p0GeV",
      'title': "MCC 11 6 GeV/c SCE",
    },
    {
      'fn': "piAbsSelector_mcc11_sce_7GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_7p0GeV",
      'title': "MCC 11 7 GeV/c SCE",
    },
  ]

  fileConfigsData = [
    {
      'fn': "piAbsSelector_run5387_v8.1_da81b52a.root",
      'name': "run5387",
      'title': "Run 5387 1 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5432_v8.1_da81b52a.root",
      'name': "run5432",
      'title': "Run 5432 2 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5786_v8.1_da81b52a.root",
      'name': "run5786",
      'title': "Run 5786 3 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5770_v8.1_da81b52a.root",
      'name': "run5770",
      'title': "Run 5770 6 GeV/c",
    },
    {
      'fn': "piAbsSelector_run5204_v8.1_da81b52a.root",
      'name': "run5204",
      'title': "Run 5204 7 GeV/c",
    },
    #{
    #  #'fn': "piAbsSelector_run5145_d9d59922.root", # old BI
    #  #'fn': "piAbsSelector_run5145_e453e2e5.root", # new BI
    #  'fn': "piAbsSelector_data_run5145_v6_b49a88cb.root",
    #  'name': "run5145",
    #  'title': "Run 5145 7 GeV/c",
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
  ]
  for iFC, fc in enumerate(fileConfigsData):
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
  for iFC, fc in enumerate(fileConfigsMC):
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]

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
        "k": "0", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "1": {
        "p": "CKov1Status == 0",
        "k": "0", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "0.5": {
        "p": "CKov1Status == 0",
        "k": "0", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
    "0.3": {
        "p": "CKov1Status == 0",
        "k": "0", # no setup for this
        "pi": "CKov1Status == 0",
        "e": "CKov1Status == 1",
    },
  }

  bigCuts = {
    "7": {
        "p": "BIProton7GeV",
        "pi": "BIPion7GeV",
        "e": "BIElectron7GeV",
        "k": "BIKaon7GeV",
    },
    "6": {
        "p": "BIProton6GeV",
        "pi": "BIPion6GeV",
        "e": "BIElectron6GeV",
        "k": "BIKaon6GeV",
    },
    "3": {
        "p": "BIProton3GeV",
        "pi": "BIPion3GeV",
        "e": "BIElectron3GeV",
        "k": "BIKaon3GeV",
    },
    "2": {
        "p": "BIProton2GeV",
        "pi": "BIPion2GeV",
        "e": "BIElectron2GeV",
        "k": "BIKaon2GeV",
    },
    "1": {
        "p": "BIProton1GeV",
        "pi": "BIPion1GeV",
        "e": "BIElectron1GeV",
        "k": "BIKaon1GeV",
    },
    "0.5": {
        "p": "BIProton0p5GeV",
        "pi": "BIPion0p5GeV",
        "e": "BIElectron0p5GeV",
        "k": "BIKaon0p5GeV",
    },
    "0.3": {
        "p": "BIProton0p3GeV",
        "pi": "BIPion0p3GeV",
        "e": "BIElectron0p3GeV",
        "k": "BIKaon0p3GeV",
    },
  }

  def getCutForAllRuns(fileConfigs,cutDict,particle,appendOld=False):
    result = "( isMC"
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
      if appendOld:
        thisCut += "Old"
      thisCut = "(runNumber == {} && {})".format(runStr,thisCut)
      result += " || ("+thisCut+")"
    result += ")"
    return result

#  print "\n\n"
#  print "Good Beamline:"
#  PrintCutTable(fileConfigsData,cutConfigsGoodBeamline,"PiAbsSelector/tree",nMax=NMAX,errors=True)

#  print "\n\n"
#  print "Pion Selection:"
#  cutConfigsPion = [
#    #{"name": "All","cut": "1"},
#    cutGoodBeamline,
#    {"name": "All Beam-side APAs Good","cut": "(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20))"},
##    {"name": "All APAs Good","cut": "(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20 && nGoodFEMBs[1]==20 && nGoodFEMBs[3]==20 && nGoodFEMBs[5]==20))"},
#    {"name": "Cherenkov Pion","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'pi')},
#    {"name": "TOF Pion","cut": getCutForAllRuns(fileConfigsData,tofCuts,'pi')},
#    {"name": "MC Truth Pion or Muon","cut": "(!isMC || abs(truePrimaryPDG) == 13 || truePrimaryPDG == 211)"},
#    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices == 1"},
#    {"name": "PF Primary is Tracklike","cut": "PFBeamPrimIsTracklike"},
#    {"name": "PF Primary Start Z < 50 cm","cut": "PFBeamPrimStartZ < 50."},
#    {"name": "PF Primary End Z < 650 cm","cut": "PFBeamPrimEndZ < 650."},
#    {"name": "Delta X PF Track & BI Track TPC Front","cut": "(isMC && ((PFBeamPrimStartX-xWC) > -10) && ((PFBeamPrimStartX-xWC) < 10)) || ((!isMC) && ((PFBeamPrimStartX-xWC) > 10) && ((PFBeamPrimStartX-xWC) < 30))"},
#    {"name": "Delta Y PF Track & BI Track TPC Front","cut": "(isMC && ((PFBeamPrimStartY-yWC) > -10) && ((PFBeamPrimStartY-yWC) < 10)) || ((!isMC) && ((PFBeamPrimStartY-yWC) > 7) && ((PFBeamPrimStartY-yWC) < 27))"},
#  ]
#  PrintCutTable(fileConfigsData+fileConfigsMC,cutConfigsPion,"PiAbsSelector/tree",nMax=NMAX,errors=True)

#  print "\n\n"
#  print "Electron Selection:"
#  cutConfigsElectron = [
#    {"name": "All","cut": "1"},
#    cutGoodBeamline,
#    {"name": "TOF Electron","cut": getCutForAllRuns(fileConfigsData,tofCuts,'e')},
#    {"name": "Cherenkov Electron","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'e')},
#    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
#    {"name": "Pandora Showerlike","cut": "PFBeamPrimIsShowerlike[0]"},
#  ]
#  PrintCutTable(fileConfigsData,cutConfigsElectron,"PiAbsSelector/tree",nMax=NMAX)
#
#  print "\n\n"
#  print "Proton Selection:"
#  cutConfigsProton = [
#    {"name": "All","cut": "1"},
#    cutGoodBeamline,
#    {"name": "TOF Proton","cut": getCutForAllRuns(fileConfigsData,tofCuts,'p')},
#    {"name": "Cherenkov Proton","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'p')},
#    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
#    {"name": "Pandora Tracklike","cut": "PFBeamPrimIsTracklike[0]"},
#  ]
#  PrintCutTable(fileConfigsData,cutConfigsProton,"PiAbsSelector/tree",nMax=NMAX)
#
#  print "\n\n"
#  print "Kaon Selection:"
#  cutConfigsKaon = [
#    {"name": "All","cut": "1"},
#    cutGoodBeamline,
#    {"name": "TOF Kaon","cut": getCutForAllRuns(fileConfigsData,tofCuts,'k')},
#    {"name": "Cherenkov Kaon","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'k')},
#    {"name": "Pandora Beam Slice","cut": "PFNBeamSlices > 0"},
#    {"name": "Pandora Tracklike","cut": "PFBeamPrimIsTracklike[0]"},
#  ]
#  PrintCutTable(fileConfigsData,cutConfigsKaon,"PiAbsSelector/tree",nMax=NMAX)
#
#  cutConfigsBeamElectron = [{"name": "All","cut": "1"}]+cutConfigsGoodBeamline+[
#    {"name": "Official BI Electron","cut": getCutForAllRuns(fileConfigsData,bigCuts,'e')},
#    #{"name": "TOF Electron","cut": getCutForAllRuns(fileConfigsData,tofCuts,'e')},
#    #{"name": "Cherenkov Electron","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'e')},
#  ]
#
#  cutConfigsBeamPion = [{"name": "All","cut": "1"}]+cutConfigsGoodBeamline+[
#    {"name": "Official BI Pion/Muon","cut": getCutForAllRuns(fileConfigsData,bigCuts,'pi')},
#    #{"name": "TOF Pion/Muon","cut": getCutForAllRuns(fileConfigsData,tofCuts,'pi')},
#    #{"name": "Cherenkov Pion/Muon","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'pi')},
#  ]
#
#  cutConfigsBeamKaon = [{"name": "All","cut": "1"}]+cutConfigsGoodBeamline+[
#    {"name": "Official BI Kaon","cut": getCutForAllRuns(fileConfigsData,bigCuts,'k')},
#    #{"name": "TOF Kaon","cut": getCutForAllRuns(fileConfigsData,tofCuts,'k')},
#    #{"name": "Cherenkov Kaon","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'k')},
#  ]
#
#  cutConfigsBeamProton = [{"name": "All","cut": "1"}]+cutConfigsGoodBeamline+[
#    {"name": "Official BI Proton","cut": getCutForAllRuns(fileConfigsData,bigCuts,'p')},
#    #{"name": "TOF Proton","cut": getCutForAllRuns(fileConfigsData,tofCuts,'p')},
#    #{"name": "Cherenkov Proton","cut": getCutForAllRuns(fileConfigsData,cherenkovCuts,'p')},
#  ]
#
#  print "\n\n"
#  print "New Beamline Electron Selection:"
#  PrintCutTable(fileConfigsData,cutConfigsBeamElectron,"PiAbsSelector/tree",nMax=NMAX)
#
#  print "\n\n"
#  print "New Beamline Pion/Muon Selection:"
#  PrintCutTable(fileConfigsData,cutConfigsBeamPion,"PiAbsSelector/tree",nMax=NMAX)
#
#  print "\n\n"
#  print "New Beamline Kaon Selection:"
#  PrintCutTable(fileConfigsData,cutConfigsBeamKaon,"PiAbsSelector/tree",nMax=NMAX)
#
#  print "\n\n"
#  print "New Beamline Proton Selection:"
#  PrintCutTable(fileConfigsData,cutConfigsBeamProton,"PiAbsSelector/tree",nMax=NMAX)

  ###########################################################################################
  ###########################################################################################
  ###########################################################################################

  #print "\n\n"
  #print "Old Beamline Selection:"
  #PrintCutTable(fileConfigsData,cutConfigsGoodBeamlineOld,"PiAbsSelector/tree",nMax=NMAX)

  #print "\n\n"
  #print "New Beamline Selection:"
  #PrintCutTable(fileConfigsData,cutConfigsGoodBeamlineNew,"PiAbsSelector/tree",nMax=NMAX)

  ###########################################################################################
  ###########################################################################################
  ###########################################################################################

  catConfigsSpeciesOld = [
    {"name": "Good BI Event","cut": cutGoodBeamlineOld},
    {"name": "BI Electron","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'e',appendOld=True)+" && "+cutGoodBeamlineOld+")"},
    {"name": "BI Pion","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'pi',appendOld=True)+" && "+cutGoodBeamlineOld+")"},
    {"name": "BI Kaon","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'k',appendOld=True)+" && "+cutGoodBeamlineOld+")"},
    {"name": "BI Proton","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'p',appendOld=True)+" && "+cutGoodBeamlineOld+")"},
  ]

  catConfigsSpeciesNew = [
    {"name": "Good BI Event","cut": cutGoodBeamlineNew},
    {"name": "BI Electron","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'e')+" && "+cutGoodBeamlineNew+")"},
    {"name": "BI Pion","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'pi')+" && "+cutGoodBeamlineNew+")"},
    {"name": "BI Kaon","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'k')+" && "+cutGoodBeamlineNew+")"},
    {"name": "BI Proton","cut": "("+getCutForAllRuns(fileConfigsData,bigCuts,'p')+" && "+cutGoodBeamlineNew+")"},
  ]

  #print "\n\n"
  #print "Old Beamline Categories:"
  #PrintPercentTable(fileConfigsData,catConfigsSpeciesOld,"PiAbsSelector/tree",nMax=NMAX)

  #print "\n\n"
  #print "New Beamline Categories:"
  #PrintPercentTable(fileConfigsData,catConfigsSpeciesNew,"PiAbsSelector/tree",nMax=NMAX)

  ###########################################################################################
  ###########################################################################################
  ###########################################################################################


  cutConfigsBeamPionNew = [{"name": "All","cut": "1"}]+cutConfigsGoodBeamlineNew+[
    {"name": "Official BI Pion/Muon","cut": getCutForAllRuns(fileConfigsData,bigCuts,'pi')},
    {"name": "All Beam-side APAs Good","cut": "(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20))"},
#    {"name": "All APAs Good","cut": "(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20 && nGoodFEMBs[1]==20 && nGoodFEMBs[3]==20 && nGoodFEMBs[5]==20))"},
    #{"name": "MC Truth Pion or Muon","cut": "(!isMC || abs(truePrimaryPDG) == 13 || truePrimaryPDG == 211)"},
    {"name": "MC Truth Pion or Muon (or Electron)","cut": "(!isMC || abs(truePrimaryPDG) == 13 || abs(truePrimaryPDG) == 211 || (abs(truePrimaryPDG)==11 && trueStartMom > 4.5))"},
    {"name": "1 Pandora Beam Slice","cut": "PFNBeamSlices == 1"},
    {"name": "PF Primary is Tracklike","cut": "PFBeamPrimIsTracklike"},
    {"name": "PF Primary Start Z < 50 cm","cut": "PFBeamPrimStartZ < 50."},
    #{"name": "PF Primary End Z < 650 cm","cut": "PFBeamPrimEndZ < 650."},
    {"name": "Delta X PF Track & BI Track","cut": "(isMC && ((PFBeamPrimStartX-xWC) > -2) && ((PFBeamPrimStartX-xWC) < 3)) || ((!isMC) && ((PFBeamPrimStartX-xWC) > 8) && ((PFBeamPrimStartX-xWC) < 15))"},
    {"name": "Delta Y PF Track & BI Track","cut": "(isMC && ((PFBeamPrimStartY-yWC) > -3) && ((PFBeamPrimStartY-yWC) < 3)) || ((!isMC) && ((PFBeamPrimStartY-yWC) > -2) && ((PFBeamPrimStartY-yWC) < 7))"},
    {"name": "Delta Theta XZ PF Track & BI Track",'cut': "(isMC && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) > -5) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) < 3)) || ((!isMC) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) > -10) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) < 0))"},
    {"name": "Delta Theta YZ PF Track & BI Track","cut": "(isMC && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) > -8) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) < 2)) || ((!isMC) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) > -20) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) < -5))"},
    #{"name": "PF Primary Doesn't End Last 4 Wires of APA","cut": "(zWireLastHitWire % 480) <= 485"},
  ]

  cutConfigsBeamPionOld = copy.deepcopy(cutConfigsBeamPionNew)
  for i in reversed(range(1,1+len(cutConfigsGoodBeamlineNew))):
    cutConfigsBeamPionOld.pop(i)
  cutConfigsBeamPionOld.pop(1)

  cutConfigsBeamPionOld.insert(1,{"name": "Official BI Pion/Muon","cut": getCutForAllRuns(fileConfigsData,bigCuts,'pi',appendOld=True)})
  for x in reversed(cutConfigsGoodBeamlineOld):
    cutConfigsBeamPionOld.insert(1,x)

  #print "\n\n"
  #print "Pion Selection (Old BI):"
  #PrintCutTable(fileConfigsData+fileConfigsMC,cutConfigsBeamPionOld,"PiAbsSelector/tree",nMax=NMAX)

  print "\n\n"
  print "Pion Selection (New BI):"
  PrintCutTable(fileConfigsData+fileConfigsMC,cutConfigsBeamPionNew,"PiAbsSelector/tree",nMax=NMAX)
