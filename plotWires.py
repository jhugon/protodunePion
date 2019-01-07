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
      'fn': "piAbsSelector_run5387_v4.10.root",
      'name': "run5387",
      'title': "Run 5387: 1 GeV/c",
      'caption': "Run 5387: 1 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 0 && TOF < 170.)*"+primaryTrackCutsData, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 170.)*"+primaryTrackCutsData, # for protons
    },
    {
      'fn': "piAbsSelector_run5432_1kevts_v4.10.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+primaryTrackCutsData, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+primaryTrackCutsData, # for protons
    },
    {
      'fn': "piAbsSelector_run5145_v4.10.root",
      'name': "run5145",
      'title': "Run 5145: 7 GeV/c",
      'caption': "Run 5145: 7 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    },
  ]
  for i, fileConfig in enumerate(fileConfigsData):
    fileConfig['color'] = COLORLIST[i]
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
    {
      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.10.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC 11 No SCE 2 GeV/c",
      'caption': "MCC11 No SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.10.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC 11 FLF SCE 2 GeV/c",
      'caption': "MCC11 FLF SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.10.root",
      'name': "mcc11_flf_7GeV",
      'title': "MCC 11 FLF SCE 7 GeV/c",
      'caption': "MCC11 FLF SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
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

  wireBinning = [480*3,0,480*3]
  #wireBinning = [100,0,100]

  histConfigs= [
    {
      'name': "dEdxVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dE/dx [MeV/cm]",
      'binning': wireBinning+[150,0,30],
      'var': "zWiredEdx:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "PitchVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Pitch [cm]",
      'binning': wireBinning+[100,0,5],
      'var': "zWirePitch:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "kinVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco Kinetic Energy [MeV]",
      'binning': wireBinning+[100,-1000,3000],
      'var': "zWirePartKin:Iteration$",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "energySum",
      'xtitle': "Primary Track Calorimetry Energy Sum [MeV]",
      'ytitle': "Events / Bin",
      'binning': [100,0,30000],
      'var': "zWireEnergySum",
      'cuts': "1",
      'logz': True,
      'printIntegral': True,
    },
  ]
  histFileName = "WireHists.root"
  hists = plotOneHistOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",nMax=NMAX,saveHistsRootName=histFileName)

  #### For MC truth stuff

  histConfigs= [
    {
      'name': "TrueEnergyVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "True Energy Deposit from Primary [MeV]",
      'binning': wireBinning+[100,0,20],
      'var': "zWireTrueEnergy:Iteration$",
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
  plotOneHistOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Wires_",nMax=NMAX)

  if False:
    histname = "dEdxVWireNum"
    mpvGraphs = []
    wGraphs = []
    labels = []
    names = []
    for samplename in sorted(hists[histname]):
      hist = hists[histname][samplename]
      mpvGraph, wGraph = fitSlicesLandaus(c,hist,samplename,fracMax=0.2,nJump=100,dumpFitPlots=True)
      mpvGraphs.append(mpvGraph)
      wGraphs.append(wGraph)
      label = samplename
      for fileConfig in fileConfigsData+fileConfigsMC:
        if fileConfig['name'] == samplename:
          label = fileConfig['title']
      labels.append(label)
      names.append(samplename)
      #fitSlicesLandauCore(c,hist,samplename)
    c.Clear()
    for i in range(len(mpvGraphs)):
        mpvGraphs[i].SetLineColor(COLORLIST[i])
        mpvGraphs[i].SetMarkerColor(COLORLIST[i])
    ax = drawGraphs(c,mpvGraphs,"Z Wire Number","Landau MPV [MeV/cm]",xlims=[0,480*3],ylims=[0,12],freeTopSpace=0.5,drawOptions=["pez"]*len(mpvGraphs),reverseDrawOrder=True)
    leg = drawNormalLegend(mpvGraphs,labels,["lep"]*len(mpvGraphs))
    drawStandardCaptions(c,"")

    c.SaveAs("Calibrate_mpvs.png")
    c.SaveAs("Calibrate_mpvs.pdf")

