#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy

if __name__ == "__main__":

  cutConfigs = [
    {
      'histConfigs':
        [
          {
            'name': "trackXFrontTPC",
            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [50,-100,50],
            'var': "trackXFrontTPC",
          },
          {
            'name': "trackXFrontTPC_wide",
            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [100,-400,400],
            'var': "trackXFrontTPC",
          },
       ],
      'cut': "trackXFrontTPC > -40 && trackXFrontTPC < 20",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackYFrontTPC",
            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [50,300,600],
            'var': "trackYFrontTPC",
          },
          {
            'name': "trackYFrontTPC_wide",
            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [100,0,700],
            'var': "trackYFrontTPC",
          },
       ],
      'cut': "trackYFrontTPC > 400 && trackYFrontTPC < 470"
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartZ",
            'xtitle': "TPC Track Start Z [cm]",
            'ytitle': "Tracks / bin",
            'binning': [100,-5,60],
            'var': "trackStartZ",
          },
          {
            'name': "trackStartZ_wide",
            'xtitle': "TPC Track Start Z [cm]",
            'ytitle': "Tracks / bin",
            'binning': [400,-10,705],
            'var': "trackStartZ",
          },
       ],
      'cut': "trackStartZ<50",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartTheta",
            'xtitle': "TPC Track Start #theta [deg]",
            'ytitle': "Tracks / bin",
            'binning': [50,0,50],
            'var': "trackStartTheta*180/pi",
          },
          {
            'name': "trackStartTheta_wide",
            'xtitle': "TPC Track Start #theta [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,0,180],
            'var': "trackStartTheta*180/pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartPhi",
            'xtitle': "TPC Track Start #phi [deg]",
            'ytitle': "Tracks / bin",
            'binning': [60,-160,-100],
            'var': "trackStartPhi*180/pi",
          },
          {
            'name': "trackStartPhi_wide",
            'xtitle': "TPC Track Start #phi [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,-180,180],
            'var': "trackStartPhi*180/pi",
            'printIntegral': True,
          },
       ],
      'cut': "1",
    },
    {
      'name': "trackLength",
      'xtitle': "TPC Track Length [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,0,800],
      'var': "trackLength",
      'cut': "1",
    },
    {
      'name': "trackTrueStartT",
      'xtitle': "Track Truth Match Start Time [ns]",
      'ytitle': "Tracks / bin",
      'binning': [1000,-100,100],
      'var': "trackTrueStartT",
      'cut': "1",
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  fn = "PiAbs_mcc11.root"
  caption = "MCC11"
  #fn = "PiAbs_mcc10_2andGeV_3ms_sce.root"
  #caption = "Beam Data, MCC10 2 & 7 GeV"
  scaleFactor= 16.33

  fileConfigsData = [
    #{
    #  'fn': "PiAbs_Run5287.root",
    #  'title': "Data Run 5287",
    #  'caption': "Data Run 5287",
    #  'color': root.kBlack,
    #},
    #{
    #  'fn': "PiAbs_PhysicsThrough5287.root",
    #  'title': "Data Runs 5000-5287",
    #  'caption': "Data Runs 5000-5287",
    #  'color': root.kBlack,
    #  #'cuts': "(triggerIsBeam)",
    #},
    {
      'fn': "PiAbs_AllData.root",
      'title': "Data",
      'caption': "Data",
      'color': root.kBlack,
      'cuts': "*(triggerIsBeam)",
    },
  ]
  fileConfigsMC = [
    {
      'fn': fn,
      'title': "Cosmics",
      'cuts': "*(!trackTrueIsBeam)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'title': "Beam Non-Beamline",
      'cuts': "*trackTrueIsBeam*(!(trackTrueMotherID==0)*(fabs(trackTrueStartT) < 50))",
      'color': root.kGreen+3,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'title': "Beamline",
      'cuts': "*trackTrueIsBeam*(trackTrueMotherID==0)*(fabs(trackTrueStartT) < 50)",
      'color': root.kOrange-3,
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


  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_NM1Hist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="Hist",nMax=NMAX)
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig['logy'] = True
    else: 
      cutConfig['logy'] = True
  logHistConfigs = []
  for histConfig in histConfigs:
    histConfig['logy'] = True
  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_NM1_logyHist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_logyHist",nMax=NMAX)

