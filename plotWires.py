#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys

m2SF=1000.
tofOffset=59.6
tofDistance = 28.6
lightTime = tofDistance/2.99e8*1e9
momSF=1.0

cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom > 0)"

if __name__ == "__main__":

  histConfigs = [
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  #fn = "PiAbs_mcc11.root"
  fn = "PiAbsSelector.root"
  name = "mcc11"
  #caption = "ProtoDUNE-SP Internal"# & MCC11"
  caption = ""
  scaleFactor= 1.
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "MCC10 2 & 7 GeV 3m SCE"

  fileConfigsData = [
    {
      'fn': "piAbsSelector_run5387_6_dl6.root",
      'name': "run5387",
      'title': "Run 5387: 1 GeV/c",
      'caption': "Run 5387: 1 GeV/c",
      'isData': True,
      #'cuts': "*"+cutGoodBeamline,
      #'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline, # for protons
    },
    {
      'fn': "piAbsSelector_run5432_6_dl6.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      #'cuts': "*"+cutGoodBeamline,
      #'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline, # for protons
    },
    {
      'fn': "piAbsSelector_run5142_6_dl6.root",
      'name': "run5142",
      'title': "Run 5142: 7 GeV/c",
      'caption': "Run 5142: 7 GeV/c",
      'isData': True,
      #'cuts': "*"+cutGoodBeamline,
      #'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline, # for protons
    },
  ]
  for i, fileConfig in enumerate(fileConfigsData):
    fileConfig['color'] = COLORLIST[i]
  fileConfigsAllData = [
    {
      'fn': [
                "piAbsSelector_run5142_6_dl6.root",
                #"piAbsSelector_run5387.root",
                #"piAbsSelector_run5430.root",
                #"piAbsSelector_run5758.root",
                #"piAbsSelector_run5777.root",
                #"piAbsSelector_run5826.root",
                #"piAbsSelector_run5834.root",
                #"piAbsSelector_run5145_v3.root",
                #"piAbsSelector_run5387_v3.root",
                #"piAbsSelector_run5432_v3.root",
            ],
      'name': "runMany",
      'title': "Runs 5145, 5387, 5432",
      'caption': "Runs 5145, 5387, 5432",
      'color': root.kBlack,
      #'cuts': "*"+cutGoodBeamline,
    },
  ]
  fileConfigsMC = [
    {
      'fn': fn,
      'title': "MCC 11",
      'name': name,
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    #{
    #  'fn': fn,
    #  'title': "MC, 1 Beam Track",
    #  'cuts': "*(nBeamTracks==1)",
    #  'color': root.kBlue-7,
    #  'scaleFactor': scaleFactor,
    #},
    #{
    #  'fn': fn,
    #  'title': "MC, 2 Beam Track",
    #  'cuts': "*(nBeamTracks==2)",
    #  'color': root.kGreen+3,
    #  'scaleFactor': scaleFactor,
    #},
    #{
    #  'fn': fn,
    #  'title': "MC, 3 Beam Track",
    #  'cuts': "*(nBeamTracks==3)",
    #  'color': root.kOrange-3,
    #  'scaleFactor': scaleFactor,
    #},
    #{
    #  'fn': fn,
    #  'title': "MC, #geq 4 Beam Track",
    #  'cuts': "*(nBeamTracks>=4)",
    #  'color': root.kAzure+10,
    #  'scaleFactor': scaleFactor,
    #},
  ]

  for histConfig in histConfigs:
    histConfig["caption"] = caption
    histConfig["normalize"] = True
    histConfig["ytitle"] = "Normalized Events / Bin"

  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
    histConfig["normalize"] = False
    histConfig["ytitle"] = "Events / Bin"
  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",outSuffix="_logyHist",nMax=NMAX)

  histConfigs= [
    {
      'name': "dEdxVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dE/dx [MeV/cm]",
      'binning': [480*3,0,480*3,100,0,20],
      'var': "zWiredEdx:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "PitchVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Pitch [cm]",
      'binning': [480*3,0,480*3,100,0,5],
      'var': "zWirePitch:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "kinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco Kinetic Energy [MeV]",
      'binning': [480*3,0,480*3,100,-1000,3000],
      'var': "zWirePartKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TrueEnergyVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Energy Deposit from Primary [MeV]",
      'binning': [480*3,0,480*3,100,0,20],
      'var': "zWireTrueEnergy:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruedZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True #Delta Z [cm]",
      'binning': [480*3,0,480*3,200,-1,1],
      'var': "zWireTruedZ:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruedRVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True #Delta R [cm]",
      'binning': [480*3,0,480*3,200,-1,1],
      'var': "zWireTruedR:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruePartKinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Particle Kinetic Energy [MeV]",
      'binning': [480*3,0,480*3,100,-1000,3000],
      'var': "zWireTruePartKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TrueTrajKinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Particle Traj Kinetic Energy [MeV]",
      'binning': [480*3,0,480*3,100,-1000,3000],
      'var': "zWireTrueTrajKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
  ]
  plotOneHistOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",nMax=NMAX)
