#!/usr/bin/env python

import ROOT as root
from helpers import *
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

if __name__ == "__main__":

  makeHists=False

  histConfigs = [
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100

  fileConfigsMC = [
    {
      'fn': "piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 No SCE 1 GeV/c",
      'caption': "MCC11 No SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_1p0GeV_v4.11.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 SCE 1 GeV/c",
      'caption': "MCC11 SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_1p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 FLF SCE 1 GeV/c",
      'caption': "MCC11 FLF SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 No SCE 2 GeV/c",
      'caption': "MCC11 No SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_2p0GeV_v4.11.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 SCE 2 GeV/c",
      'caption': "MCC11 SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 FLF SCE 2 GeV/c",
      'caption': "MCC11 FLF SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root",
      'name': "mcc11_3ms_7GeV",
      'title': "MCC11 No SCE SCE 7 GeV/c",
      'caption': "MCC11 No SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_7p0GeV_v4.11.root",
      'name': "mcc11_sce_7GeV",
      'title': "MCC11 SCE 7 GeV/c",
      'caption': "MCC11 SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.11.root",
      'name': "mcc11_flf_7GeV",
      'title': "MCC11 FLF SCE 7 GeV/c",
      'caption': "MCC11 FLF SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
  ]

  if makeHists:
    for histConfig in histConfigs:
      histConfig["caption"] = caption
      histConfig["normalize"] = True
      histConfig["ytitle"] = "Normalized Events / Bin"

    plotManyFilesOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",outSuffix="Hist",nMax=NMAX)
    for histConfig in histConfigs:
      histConfig['logy'] = True
      histConfig["normalize"] = False
      histConfig["ytitle"] = "Events / Bin"
    plotManyFilesOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",outSuffix="_logyHist",nMax=NMAX)

  wireBinning = [480*3,0,480*3]
  #wireBinning = [100,0,100]

  histConfigs= [
    {
      'name': "zWireZVzWireWireZ",
      'xtitle': "Z Wire Z-Position [cm]",
      'ytitle': "Reco Hit Z-Position [cm]",
      'binning': 2*[710,-5.,705.],
      'var': "zWireZ:zWireWireZ",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "zWireZVzWireWireZ",
      'xtitle': "Z Wire Z-Position [cm]",
      'ytitle': "True Hit Z-Position [cm]",
      'binning': 2*[710,-5.,705.],
      'var': "zWireTrueZ:zWireWireZ",
      'cuts': "1",
      'logz': True,
    },
    #{
    #  'name': "deltaRecoWireZVWireNum",
    #  'xtitle': "Z Wire Number",
    #  'ytitle': "Reco Hit-Wire Z-Position [cm]",
    #  'binning': wireBinning+[300,-30,30],
    #  'var': "zWireZ-zWireWireZ:Iteration$",
    #  'cuts': "1",
    #  'logz': True,
    #},
    {
      'name': "deltaWireTrueZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Wire-True Hit Z-Position [cm]",
      'binning': wireBinning+[300,-20,20],
      'var': "zWireWireZ-zWireTrueZ:Iteration$",
      'cuts': "1",
      'logz': True,
      'profileXtoo': True,
    },
    {
      'name': "deltaRecoTrueZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco-True Hit Z-Position [cm]",
      'binning': wireBinning+[300,-20,20],
      'var': "zWireZ-zWireTrueZ:Iteration$",
      'cuts': "1",
      'logz': True,
      'profileXtoo': True,
    },
    {
      'name': "deltaPitchTrueHitSpacingVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco Pitch-True Hit Spacing [cm]",
      'binning': wireBinning+[200,-5,5],
      'var': "zWirePitch-zWireTruedR:Iteration$",
      'cuts': "1",
      'logz': True,
    },
  ]
  if makeHists:
    plotOneHistOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",nMax=NMAX,saveHistsRootName="WireHistsSCE.root")

  histFileName = "WireHistsSCE.root"
  histname = "dEdxVWireNum"
  hf = HistFile(histFileName)
  root.gStyle.SetMarkerSize(0)
  for histConfig in histConfigs:
    histName = histConfig['name']
    if "PitchTrueHitSpacing" in histName:
      continue
    profs = []
    labels = []
    derivs = []
    for iFileConfig,fileConfig in enumerate(fileConfigsMC):
      fileName = fileConfig['name']
      if "3ms" in fileName:
        continue
      name = histName+"_"+fileName
      hist = hf[name]
      prof = hist.ProfileX(hist.GetName()+"_pfxAgain")
      prof.SetMarkerSize(0)
      profs.append(prof)
      labels.append(fileConfig['title'])
    plotHistsSimple(profs,labels,histConfig['xtitle'],"Profile of "+histConfig['ytitle'],c,"WireZ_prof_"+histName,drawOptions="",ylim=[-10,25])
