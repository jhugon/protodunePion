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

#cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom  > 0)"
cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom  == 1)"

if __name__ == "__main__":

  cutConfigs = [
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimXFrontTPC",
            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [50,-100,100],
            'var': "PFBeamPrimXFrontTPC",
          },
          {
            'name': "PFBeamPrimXFrontTPC_wide",
            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [150,-600,600],
            'var': "PFBeamPrimXFrontTPC",
          },
       ],
      #'cut': "PFBeamPrimXFrontTPC > -40 && PFBeamPrimXFrontTPC < 20",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimYFrontTPC",
            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [50,300,600],
            'var': "PFBeamPrimYFrontTPC",
          },
          {
            'name': "PFBeamPrimYFrontTPC_wide",
            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [300,-500,1500],
            'var': "PFBeamPrimYFrontTPC",
          },
       ],
      #'cut': "PFBeamPrimYFrontTPC > 400 && PFBeamPrimYFrontTPC < 470"
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "DeltaXPFBeamPrimBI",
            'xtitle': "#Delta X PF Track & BI Track at TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [100,-100,100],
            'var': "PFBeamPrimXFrontTPC - xWC",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "DeltaYPFBeamPrimBI",
            'xtitle': "#Delta Y PF Track & BI Track at TPC Front [cm]",
            'ytitle': "Events / bin",
            'binning': [100,-100,100],
            'var': "PFBeamPrimYFrontTPC - yWC",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartX",
            'xtitle': "Track Start X Position [cm]",
            'ytitle': "Events / bin",
            'binning': [50,-100,100],
            'var': "PFBeamPrimStartX",
          },
          {
            'name': "PFBeamPrimStartX_wide",
            'xtitle': "Track Start X Position [cm]",
            'ytitle': "Events / bin",
            'binning': [150,-500,500],
            'var': "PFBeamPrimStartX",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartY",
            'xtitle': "Track Start Y Position [cm]",
            'ytitle': "Events / bin",
            'binning': [50,300,600],
            'var': "PFBeamPrimStartY",
          },
          {
            'name': "PFBeamPrimStartY_wide",
            'xtitle': "Track Start Y Position [cm]",
            'ytitle': "Events / bin",
            'binning': [315,-10,620],
            'var': "PFBeamPrimStartY",
          },
       ],
      'cut': "1"
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartZ",
            'xtitle': "TPC Track Start Z [cm]",
            'ytitle': "Events / bin",
            'binning': [100,-5,60],
            'var': "PFBeamPrimStartZ",
          },
          {
            'name': "PFBeamPrimStartZ_wide",
            'xtitle': "TPC Track Start Z [cm]",
            'ytitle': "Events / bin",
            'binning': [400,-10,705],
            'var': "PFBeamPrimStartZ",
          },
       ],
      #'cut': "PFBeamPrimStartZ<50",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimEndX",
            'xtitle': "Track End X Position [cm]",
            'ytitle': "Events / bin",
            'binning': [50,-100,100],
            'var': "PFBeamPrimEndX",
          },
          {
            'name': "PFBeamPrimEndX_wide",
            'xtitle': "Track End X Position [cm]",
            'ytitle': "Events / bin",
            'binning': [150,-500,500],
            'var': "PFBeamPrimEndX",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimEndY",
            'xtitle': "Track End Y Position [cm]",
            'ytitle': "Events / bin",
            'binning': [50,300,600],
            'var': "PFBeamPrimEndY",
          },
          {
            'name': "PFBeamPrimEndY_wide",
            'xtitle': "Track End Y Position [cm]",
            'ytitle': "Events / bin",
            'binning': [315,-10,620],
            'var': "PFBeamPrimEndY",
          },
       ],
      'cut': "1"
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimEndZ",
            'xtitle': "TPC Track End Z [cm]",
            'ytitle': "Events / bin",
            'binning': [200,-5,300],
            'var': "PFBeamPrimEndZ",
          },
          {
            'name': "PFBeamPrimEndZ_wide",
            'xtitle': "TPC Track End Z [cm]",
            'ytitle': "Events / bin",
            'binning': [400,-10,705],
            'var': "PFBeamPrimEndZ",
          },
       ],
      #'cut': "PFBeamPrimEndZ<50",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartTheta",
            'xtitle': "TPC Track Start #theta [deg]",
            'ytitle': "Events / bin",
            'binning': [50,0,50],
            'var': "PFBeamPrimStartTheta*180/pi",
          },
          {
            'name': "PFBeamPrimStartTheta_wide",
            'xtitle': "TPC Track Start #theta [deg]",
            'ytitle': "Events / bin",
            'binning': [180,0,180],
            'var': "PFBeamPrimStartTheta*180/pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartPhi",
            'xtitle': "TPC Track Start #phi [deg]",
            'ytitle': "Events / bin",
            'binning': [60,-160,-100],
            'var': "PFBeamPrimStartPhi*180/pi",
          },
          {
            'name': "PFBeamPrimStartPhi_wide",
            'xtitle': "TPC Track Start #phi [deg]",
            'ytitle': "Events / bin",
            'binning': [180,-180,180],
            'var': "PFBeamPrimStartPhi*180/pi",
            'printIntegral': True,
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartThetaY",
            'xtitle': "TPC Track #theta_{y} [deg]",
            'ytitle': "Events / bin",
            'binning': [180,0,180],
            'var': "acos(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartPhiZX",
            'xtitle': "TPC Track #phi_{zx} [deg]",
            'ytitle': "Events / bin",
            'binning': [180,-180,180],
            'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "PFBeamPrimStartThetaX",
            'xtitle': "TPC Track #theta_{x} [deg]",
            'ytitle': "Events / bin",
            'binning': [180,0,180],
            'var': "acos(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
              'name': "trackStartCosThetaX",
              'xtitle': "TPC Track cos(#theta_{x})",
              'ytitle': "Events / bin",
              'binning': [100,0,1],
              'var': "sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi)",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
              'name': "PFBeamPrimStartPhiZY",
              'xtitle': "TPC Track #phi_{zy} [deg]",
              'ytitle': "Events / bin",
              'binning': [180,-180,180],
              'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'name': "PFBeamPrimTrkLen",
      'xtitle': "TPC Track Length [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,800],
      'var': "PFBeamPrimTrkLen",
      'cut': "1",
    },
    {
      'name': "PFBeamPrimIsTracklike",
      'xtitle': "PF Beam Primary is Track-like",
      'ytitle': "Tracks / bin",
      'binning': [2,-0.5,1.5],
      'var': "PFBeamPrimIsTracklike",
      'cut': "PFBeamPrimIsTracklike == 1",
    },
    {
      'name': "PFNBeamSlices",
      'xtitle': "Number of PF Beam Slices",
      'ytitle': "Events / bin",
      'binning': [9,-0.5,8.5],
      'var': "PFNBeamSlices",
      'cut': "PFNBeamSlices == 1",
    },
    {
      'name': "PFBeamPrimNDaughters",
      'xtitle': "PF Beam Primary is Track-like",
      'ytitle': "Events / bin",
      'binning': [9,-0.5,8.5],
      'var': "PFBeamPrimNDaughters",
      'cut': "1",
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  #fn = "PiAbs_mcc11.root"
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "Beam Data, MCC10 2 & 7 GeV"
  mcfn = "piAbsSelector_mcc11_flf_2GeV.root"
  caption = "2 GeV/c Beam Data & MCC11 FLF"
  scaleFactor = 14.47

  fileConfigsData = [
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
    {
      'fn': "piAbsSelector_run5432_v3.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline,
    },
  ]
  fileConfigsMC = [
    {
      'fn': mcfn,
      'name': "mcc11",
      'title': "MCC11",
      'caption': "MCC11",
      'cuts': "",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
  ]

  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig["caption"] = "N-1 Cut, "+caption
    else: 
      cutConfig["caption"] = "N-1 Cut, "+caption

  histConfigs = []
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        config = copy.deepcopy(histConfig)
        config["caption"] = caption
        config["cuts"] = "1"
        histConfigs.append(config)
    else: 
      config = copy.deepcopy(cutConfig)
      config["caption"] = caption
      del config["cut"]
      config["cuts"] = "1"
      histConfigs.append(config)


  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_NM1Hist",nMax=NMAX,table=True)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="Hist",nMax=NMAX)
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig['logy'] = True
    else: 
      cutConfig['logy'] = True
  logHistConfigs = []
  for histConfig in histConfigs:
    histConfig['logy'] = True
  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_NM1_logyHist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_logyHist",nMax=NMAX)
