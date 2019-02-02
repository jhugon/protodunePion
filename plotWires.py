#!/usr/bin/env python

import ROOT as root
from helpers import *
from helpers.dEdxCalibration import fitSlicesLandauCore, fitSlicesLandaus
root.gROOT.SetBatch(True)
import copy
import sys

cutGoodBeamline = "*(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1)"
cutGoodFEMBs = "*(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20))"

deltaXTrackBICut = "*(isMC && ((PFBeamPrimXFrontTPC-xWC) > -10) && ((PFBeamPrimXFrontTPC-xWC) < 10)) || ((!isMC) && ((PFBeamPrimXFrontTPC-xWC) > 10) && ((PFBeamPrimXFrontTPC-xWC) < 30))"
deltaYTrackBICut = "*(isMC && ((PFBeamPrimYFrontTPC-yWC) > -10) && ((PFBeamPrimYFrontTPC-yWC) < 10)) || ((!isMC) && ((PFBeamPrimYFrontTPC-yWC) > 7) && ((PFBeamPrimYFrontTPC-yWC) < 27))"
primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ < 650.)"+deltaXTrackBICut+deltaYTrackBICut
primaryTrackCutsMu = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ > 650.)"+deltaXTrackBICut+deltaYTrackBICut

primaryTrackCutsData = cutGoodFEMBs+cutGoodBeamline+primaryTrackCutsMu
cutsMC = "(truePrimaryPDG == 211 || truePrimaryPDG == -13)"+primaryTrackCutsMu

SLABTHICKNESS = 0.5

if __name__ == "__main__":

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
    #{
    #  'fn': "piAbsSelector_run5387_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5387_v4.10.root"],
    #  'name': "run5387",
    #  'title': "Run 5387: 1 GeV/c",
    #  'caption': "Run 5387: 1 GeV/c",
    #  'isData': True,
    #  'cuts': "*(CKov1Status == 0 && TOF < 170.)*"+primaryTrackCutsData, # for pions
    #  #'cuts': "*(CKov1Status == 0 && TOF > 170.)*"+primaryTrackCutsData, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5432_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5432_v4.10.root"],
    #  'name': "run5432",
    #  'title': "Run 5432: 2 GeV/c",
    #  'caption': "Run 5432: 2 GeV/c",
    #  'isData': True,
    #  'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+primaryTrackCutsData, # for pions
    #  #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+primaryTrackCutsData, # for protons
    #},
    {
      'fn': "test5145.root",
      'addFriend': ["friend","friendTree_test5145.root"],
      'name': "run5145",
      'title': "Run 5145: 7 GeV/c",
      'caption': "Run 5145: 7 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    },
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5145_v4.10.root"],
    #  'name': "run5145_evtLt15000",
    #  'title': "Run 5145: 7 GeV/c, Event < 15000",
    #  'caption': "Run 5145: 7 GeV/c, Event < 15000",
    #  'isData': True,
    #  'cuts': "*(eventNumber < 15000)*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5145_v4.10.root"],
    #  'name': "run5145_evtGeq15000",
    #  'title': "Run 5145: 7 GeV/c, Event #geq 15000",
    #  'caption': "Run 5145: 7 GeV/c, Event #geq 15000",
    #  'isData': True,
    #  'cuts': "*(eventNumber >= 15000)*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5145_v4.10.root"],
    #  'name': "run5145_evtLt2000",
    #  'title': "Run 5145: 7 GeV/c, Event < 2000",
    #  'caption': "Run 5145: 7 GeV/c, Event < 2000",
    #  'isData': True,
    #  'cuts': "*(eventNumber < 2000)*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5145_v4.10.root"],
    #  'name': "run5145_evtGeq37000",
    #  'title': "Run 5145: 7 GeV/c, Event #geq 37000",
    #  'caption': "Run 5145: 7 GeV/c, Event #geq 37000",
    #  'isData': True,
    #  'cuts': "*(eventNumber >= 37000)*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
    #  #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'addFriend': ["friend","friendTree_piAbsSelector_run5145_v4.10.root"],
    #  'name': "run5145_noCuts",
    #  'title': "Run 5145: 7 GeV/c, No Cuts",
    #  'caption': "Run 5145: 7 GeV/c, No Cuts",
    #  'isData': True,
    #},
  ]
  fileConfigsAllData = [
    {
      'fn': [
                "piAbsSelector_run5145_v4.10.root",
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
#    {
#      'fn': "piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",
#      'name': "mcc11_3ms_2GeV",
#      'title': "MCC11 No SCE 1 GeV/c",
#      'caption': "MCC11 No SCE 1 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_sce_1p0GeV_v4.11.root",
#      'name': "mcc11_sce_2GeV",
#      'title': "MCC11 SCE 1 GeV/c",
#      'caption': "MCC11 SCE 1 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_1p0GeV_v4.11.root",
#      'name': "mcc11_flf_2GeV",
#      'title': "MCC11 FLF SCE 1 GeV/c",
#      'caption': "MCC11 FLF SCE 1 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root",
#      'name': "mcc11_3ms_2GeV",
#      'title': "MCC11 No SCE 2 GeV/c",
#      'caption': "MCC11 No SCE 2 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_sce_2p0GeV_v4.11.root",
#      'name': "mcc11_sce_2GeV",
#      'title': "MCC11 SCE 2 GeV/c",
#      'caption': "MCC11 SCE 2 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
#      'name': "mcc11_flf_2GeV",
#      'title': "MCC11 FLF SCE 2 GeV/c",
#      'caption': "MCC11 FLF SCE 2 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root",
#      'name': "mcc11_3ms_7GeV",
#      'title': "MCC11 No SCE SCE 7 GeV/c",
#      'caption': "MCC11 No SCE 7 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_sce_7p0GeV_v4.11.root",
#      'name': "mcc11_sce_7GeV",
#      'title': "MCC11 SCE 7 GeV/c",
#      'caption': "MCC11 SCE 7 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.11.root",
#      'name': "mcc11_flf_7GeV",
#      'title': "MCC11 FLF SCE 7 GeV/c",
#      'caption': "MCC11 FLF SCE 7 GeV/c",
#      'isData': False,
#      "cuts": "*"+cutsMC
#    },
  ]

  for fileConfig in fileConfigsMC:
    fileConfig['addFriend'] = ["friend","friendTree_"+fileConfig["fn"]]

  fileConfigs = fileConfigsData + fileConfigsMC
  for i, fileConfig in enumerate(fileConfigs):
    fileConfig['color'] = COLORLIST[i]

  histConfigs = [
    {
      'name': "firstHitWire",
      'xtitle': "First Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [480*3,0,480*3],
      'var': "zWireFirstHitWire",
      'cuts': "1",
    },
    {
      'name': "lastHitWire",
      'xtitle': "Last Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [480*3,0,480*3],
      'var': "zWireLastHitWire",
      'cuts': "1",
    },
    {
      'name': "lastContigHitWire",
      'xtitle': "Last Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [480*3,0,480*3],
      'var': "zWireLastContigHitWire",
      'cuts': "1",
    },
    {
      'name': "firstHitWire_zoom",
      'xtitle': "First Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [150,0,150],
      'var': "zWireFirstHitWire",
      'cuts': "1",
    },
    {
      'name': "firstHitWire_zoom2",
      'xtitle': "First Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [40,50,90],
      'var': "zWireFirstHitWire",
      'cuts': "1",
    },
    {
      'name': "firstHitWireZ_zoom",
      'xtitle': "First Hit Wire Z [cm]",
      'ytitle': "Events / bin",
      'binning': [160,0,80],
      'var': "zWireWireZ[zWireFirstHitWire]",
      'cuts': "1",
    },
    {
      'name': "firstHitWireZ_zoom2",
      'xtitle': "First Hit Wire Z [cm]",
      'ytitle': "Events / bin",
      'binning': [80,10,50],
      'var': "zWireWireZ[zWireFirstHitWire]",
      'cuts': "1",
    },
    {
      'name': "lastHitWire_zoom",
      'xtitle': "Last Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [480*3-1300,1300,480*3],
      'var': "zWireLastHitWire",
      'cuts': "1",
    },
    {
      'name': "lastHitWire_zoom2",
      'xtitle': "Last Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [480*3-1350,1350,480*3],
      'var': "zWireLastHitWire",
      'cuts': "1",
    },
    {
      'name': "lastHitWireZ_zoom",
      'xtitle': "Last Hit Wire Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,600,700],
      'var': "zWireWireZ[zWireLastHitWire]",
      'cuts': "1",
    },
    {
      'name': "lastHitWireZ_zoom2",
      'xtitle': "Last Hit Wire Z [cm]",
      'ytitle': "Events / bin",
      'binning': [100,650,700],
      'var': "zWireWireZ[zWireLastHitWire]",
      'cuts': "1",
    },
    #{
    #  'name': "lastContigHitWire_zoom",
    #  'xtitle': "Last Hit Z Wire Number",
    #  'ytitle': "Events / bin",
    #  'binning': [480*3-1300,1300,480*3],
    #  'var': "zWireLastContigHitWire",
    #  'cuts': "1",
    #},
    {
      'name': "SillyTest",
      'xtitle': "dE/dx of Wire 105",
      'ytitle': "Events / bin",
      'binning': [100,0,10],
      'var': "zWiredEdx[105]",
      'cuts': "1",
    },
    {
      'name': "SillyTest2",
      'xtitle': "dE/dx of Wire 224",
      'ytitle': "Events / bin",
      'binning': [100,0,10],
      'var': "zWiredEdx[224]",
      'cuts': "1",
    },
    {
      'name': "SillyTest3",
      'xtitle': "dQ/dx",
      'ytitle': "Events / bin",
      'binning': [300,0,1500],
      'var': "zWiredQdx",
      'cuts': "1",
    },
  ]

  for histConfig in histConfigs:
    histConfig["caption"] = caption
    histConfig["normalize"] = True
    histConfig["ytitle"] = "Normalized Events / Bin"

  plotManyFilesOnePlot([x for x in fileConfigs if (not ("1p0GeV" in x["fn"])) and (not ("3ms" in x["fn"]))],histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
    histConfig["normalize"] = False
    histConfig["ytitle"] = "Events / Bin"
  plotManyFilesOnePlot([x for x in fileConfigs if (not ("1p0GeV" in x["fn"])) and (not ("3ms" in x["fn"]))],histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",outSuffix="_logyHist",nMax=NMAX)

  wireBinning = [480*3,0,480*3]
  #wireBinning = [100,0,100]

  histConfigs= [
    {
      'name': "dEdxVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dE/dx [MeV/cm]",
      'binning': wireBinning+[600,0,30],
      'var': "zWiredEdx:Iteration$",
      'cuts': "1",
      'logz': True,
      'captionright1': "Uncalibrated dE/dx"
    },
    {
      'name': "dEdxCorrVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Corrected dE/dx [MeV/cm]",
      'binning': wireBinning+[600,0,30],
      'var': "zWiredEdx_corr:Iteration$",
      'cuts': "1",
      'logz': True,
      'captionright1': "Calibrated dE/dx"
    },
    {
      'name': "dEdxAjibVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Corrected dE/dx [MeV/cm]",
      'binning': wireBinning+[600,0,30],
      'var': "zWiredEdx_ajib:Iteration$",
      'cuts': "1",
      'logz': True,
      'captionright1': "Ajib Calibrated dE/dx"
    },
    {
      'name': "dQdxVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dQ/dx [ADC #times tick/cm]",
      'binning': wireBinning+[600,0,1000],
      'var': "zWiredQdx:Iteration$",
      'cuts': "1",
      'logz': True,
      'captionright1': "Uncalibrated dQ/dx"
    },
    {
      'name': "dQdxAjibVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dQ/dx [ADC #times tick/cm]",
      'binning': wireBinning+[600,0,1000],
      'var': "zWiredQdx_ajib:Iteration$",
      'cuts': "1",
      'logz': True,
      'captionright1': "Ajib Calibrated dQ/dx"
    },
    #{
    #  'name': "PitchVWireNum",
    #  'xtitle': "Z Wire Number",
    #  'ytitle': "Pitch [cm]",
    #  'binning': wireBinning+[100,0,5],
    #  'var': "zWirePitch:Iteration$",
    #  'cuts': "1",
    #  'logz': True,
    #},
    #{
    #  'name': "kinVWireNum",
    #  'xtitle': "Z Wire Number",
    #  'ytitle': "Reco Kinetic Energy [MeV]",
    #  'binning': wireBinning+[100,-1000,3000],
    #  'var': "zWirePartKin:Iteration$",
    #  'cuts': "1",
    #  'logz': True,
    #},
    #{
    #  'name': "energySum",
    #  'xtitle': "Primary Track Calorimetry Energy Sum [MeV]",
    #  'ytitle': "Events / Bin",
    #  'binning': [100,0,30000],
    #  'var': "zWireEnergySum",
    #  'cuts': "1",
    #  'logz': True,
    #  'printIntegral': True,
    #},
  ]
  histFileName = "WireHists.root"
  hists = plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",nMax=NMAX,saveHistsRootName=histFileName)

  #### For MC truth stuff

  histConfigs= [
    {
      'name': "TrueEnergyVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Energy Deposit from Primary [MeV]",
      'binning': wireBinning+[300,0,20],
      'var': "zWireTrueEnergy:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TrueEnergyOverTrajPitchVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True dE/dx (Trajectory Pitch) [MeV/cm]",
      'binning': wireBinning+[500,0,50],
      'var': "zWireTrueEnergy/zWireTrueTrajPitch:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TrueEnergyOverdRVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True dE/dx (IDE Average Distance) [MeV/cm]",
      'binning': wireBinning+[500,0,50],
      'var': "zWireTrueEnergy/zWireTruedR:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruedZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True #Delta Z [cm]",
      'binning': wireBinning+[200,-1,1],
      'var': "zWireTruedZ:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruedRVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True #Delta R [cm]",
      'binning': wireBinning+[200,-1,1],
      'var': "zWireTruedR:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TruePartKinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Particle Kinetic Energy [MeV]",
      'binning': wireBinning+[100,-1000,3000],
      'var': "zWireTruePartKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TrueTrajKinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Particle Traj Kinetic Energy [MeV]",
      'binning': wireBinning+[100,-1000,3000],
      'var': "zWireTrueTrajKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
  ]
  plotOneHistOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",nMax=NMAX,saveHistsRootName="WireHistsTrue.root")
  histConfigs = [
    {
      'name': "dEdxVWireNum",
      'title': "Uncalibrated dE/dx",
      'ytitle': "Hits / Bin",
      'xtitle': "dE/dx [MeV/cm]",
      'binning': [600,0,30],
      'var': "zWiredEdx",
      'cuts': "1",
      'color' : COLORLIST[0],
    },
    {
      'name': "dEdxCorrVWireNum",
      'title': "Hugon Calibrated dE/dx",
      'ytitle': "Hits / Bin",
      'xtitle': "dE/dx [MeV/cm]",
      'binning': [600,0,30],
      'var': "zWiredEdx_corr",
      'cuts': "1",
      'color' : COLORLIST[1],
    },
    {
      'name': "dEdxCorrVWireNum",
      'title': "Ajib Calibrated dE/dx",
      'ytitle': "Hits / Bin",
      'xtitle': "dE/dx [MeV/cm]",
      'binning': [600,0,30],
      'var': "zWiredEdx_ajib",
      'cuts': "1",
      'color' : COLORLIST[2],
    },
  ]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareCalib_dEdx",nMax=NMAX)
  for i in range(len(histConfigs)):
    histConfigs[i]['logy'] = True
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareCalib_dEdx",outSuffix="_logy_Hist",nMax=NMAX)

  histConfigs = [
    {
      'name': "dQdxVWireNum",
      'title': "Uncalibrated dQ/dx",
      'ytitle': "Hits / Bin",
      'xtitle': "dQ/dx [ADC #times tick / cm]",
      'binning': [200,0,1000],
      'var': "zWiredQdx",
      'cuts': "1",
      'color' : COLORLIST[0],
    },
    {
      'name': "dQdxCorrVWireNum",
      'title': "Ajib Calibrated dQ/dx",
      'ytitle': "Hits / Bin",
      'xtitle': "dQ/dx [ADC #times tick / cm]",
      'binning': [200,0,1000],
      'var': "zWiredQdx_ajib",
      'cuts': "1",
      'color' : COLORLIST[2],
    },
  ]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareCalib_dQdx",outSuffix="zoom_Hist",nMax=NMAX)
  for i in range(len(histConfigs)):
    histConfigs[i]['logy'] = True
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareCalib_dQdx",outSuffix="zoom_logy_Hist",nMax=NMAX)

  #histConfigs = [
  #  {
  #    'title': "Event Number < 15000",
  #    'ytitle': "Hits / Bin",
  #    'xtitle': "Uncalibrated dE/dx [MeV/cm]",
  #    'binning': [200,0,10],
  #    'var': "zWiredEdx",
  #    'cuts': "eventNumber < 15000",
  #    'color' : COLORLIST[0],
  #  },
  #  {
  #    'title': "Event Number #geq 15000",
  #    'ytitle': "Hits / Bin",
  #    'xtitle': "Uncalibrated dE/dx [MeV/cm]",
  #    'binning': [200,0,10],
  #    'var': "zWiredEdx",
  #    'cuts': "eventNumber >=15000",
  #    'color' : COLORLIST[1],
  #  },
  #]
  #plotManyHistsOnePlot([x for x in fileConfigsData if "5145" in x["name"]],histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareParts_dEdx_",outSuffix="zoom_Hist",nMax=NMAX)

  #histConfigs = [
  #  {
  #    'title': "Event Number < 15000",
  #    'ytitle': "Hits / Bin",
  #    'xtitle': "Calibrated dE/dx [MeV/cm]",
  #    'binning': [200,0,10],
  #    'var': "zWiredEdx_corr",
  #    'cuts': "eventNumber < 15000",
  #    'color' : COLORLIST[0],
  #  },
  #  {
  #    'title': "Event Number #geq 15000",
  #    'ytitle': "Hits / Bin",
  #    'xtitle': "Calibrated dE/dx [MeV/cm]",
  #    'binning': [200,0,10],
  #    'var': "zWiredEdx_corr",
  #    'cuts': "eventNumber >=15000",
  #    'color' : COLORLIST[1],
  #  },
  #]
  #plotManyHistsOnePlot([x for x in fileConfigsData if "5145" in x["name"]],histConfigs,c,"PiAbsSelector/tree",outPrefix="WiresCompareParts_dEdxCorr_",outSuffix="zoom_Hist",nMax=NMAX)
