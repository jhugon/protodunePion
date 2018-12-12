#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  cuts = ""

  #cuts += "*( iBestMatch >= 0 && nMatchedTracks == 1)" # matching in analyzer

  # matching debug
  #cuts += "*(sqrt(pow(xWC-23.75,2)+pow(yWC-0.2,2)) < 11.93)" # wc track in flange
  #cuts += "*(trackXFrontTPC > -50. && trackXFrontTPC < -10. && trackYFrontTPC > 390. && trackYFrontTPC < 430.)" # TPC track in flange
  #cuts += "*(trackMatchLowestZ < 2.)" # matching
  #cuts += "*(fabs(trackMatchDeltaY) < 5.)" # matching
  #cuts += "*((!isMC && (trackMatchDeltaX < 6. && trackMatchDeltaX > -4.)) || (isMC && (fabs(trackMatchDeltaX) < 5.)))" # matching
  #cuts += "*(trackMatchDeltaAngle*180/pi < 10.)" # matching
  ###
  ###
  cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom > 0)"
  secTrkCuts = "*(trackStartDistToPrimTrkEnd < 2.)"
  #weightStr = "pzWeight"+cuts
  weightStr = "1"+cuts

  weightStrTrackMatch = "1"+cuts#+"*(trackMatchLowestZ < 2.)"

  #nData = 224281.0
  logy = False

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    #{
    #  'fn': "piAbsSelector_run5145_v3.root",
    #  'name': "run5145",
    #  'title': "Run 5145: 7 GeV/c",
    #  'caption': "Run 5145: 7 GeV/c",
    #  'cuts': "*(CKov1Status == 1 && CKov0Status == 1)*"+cutGoodBeamline,
    #},
    #{
    #  'fn': "piAbsSelector_run5387_v3.root",
    #  'name': "run5387",
    #  'title': "Run 5387: 1 GeV/c",
    #  'caption': "Run 5387: 1 GeV/c",
    #  'cuts': "*"+cutGoodBeamline,
    #  'cuts': "*(CKov1Status == 0 && TOF < 170.)*"+cutGoodBeamline,
    #},
#    {
#      'fn': "piAbsSelector_run5432_v3.root",
#      'name': "run5432",
#      'title': "Run 5432: 2 GeV/c",
#      'caption': "Run 5432: 2 GeV/c",
#      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline,
#    },
    {
      'fn': "piAbsSelector_mcc11_flf_2GeV.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 2 GeV/c FLF",
      'caption': "MCC11 2 GeV/c FLF",
      'cuts': "",
      'color': root.kBlue-7,
      'scaleFactor': 1,
    },
  ]

  histConfigs = [
    {
      'name': "nWC",
      'xtitle': "X Position of WC track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [50,-100,50],
      'var': "xWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "xWC",
      'xtitle': "X Position of WC track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [125,-75,50],
      'var': "xWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "yWC",
      'xtitle': "Y Position of WC track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [75,375,450],
      'var': "yWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "pWC",
      'xtitle': "Momentum from WC [GeV/c]",
      'ytitle': "Events / bin",
      'binning': [100,0,10],
      'var': "pWC/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimKins",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hit / bin",
      'binning': [100,0,10],
      'var': "PFBeamPrimKins/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimXs",
      'xtitle': "Primary PF Track Hit X-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,-100,100],
      'var': "PFBeamPrimXs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimYs",
      'xtitle': "Primary PF Track Hit Y-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,300,600],
      'var': "PFBeamPrimYs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimZs",
      'xtitle': "Primary PF Track Hit Z-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,0,400],
      'var': "PFBeamPrimZs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKinInteract",
      'xtitle': "Primary PF Track Interaction Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [100,0,10],
      'var': "PFBeamPrimKinInteract/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast3Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 3 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast3Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast5Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 5 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast5Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast7Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 7 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast7Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
  ]

  #for i in reversed(range(len(histConfigs))):
  #  if histConfigs[i]['name'] != "pzWC":
  #  #if histConfigs[i]['name'] != "zWC4Hit":
  #    histConfigs.pop(i)

  #plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",nMax=NMAX)
  fileConfigMCs = copy.deepcopy(fileConfigs)
  fileConfigDatas = []
  for i in reversed(range(len(fileConfigMCs))):
    if 'isData' in fileConfigMCs[i] and fileConfigMCs[i]['isData']:
      fileConfigDatas.append(fileConfigMCs.pop(i))
  #DataMCStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",nMax=NMAX)
  DataMCCategoryStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",
                outPrefix="DataMC_",nMax=NMAX,
                catConfigs=TRUECATEGORYFEWERCONFIGS
             )
