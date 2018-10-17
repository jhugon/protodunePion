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
            'name': "beamTrackXFrontTPC",
            'xtitle': "X of Beam Track Projection to TPC Front [cm]",
            'ytitle': "Beam Tracks / bin",
            'binning': [50,-100,50],
            'var': "beamTrackXFrontTPC",
          },
          {
            'name': "beamTrackXFrontTPC_wide",
            'xtitle': "X of Beam Track Projection to TPC Front [cm]",
            'ytitle': "Beam Tracks / bin",
            'binning': [100,-400,400],
            'var': "beamTrackXFrontTPC",
          },
       ],
      'cut': "beamTrackXFrontTPC > -40 && beamTrackXFrontTPC < 20",
    },
    {
      'histConfigs':
        [
          {
            'name': "beamTrackYFrontTPC",
            'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
            'ytitle': "Beam Tracks / bin",
            'binning': [50,300,600],
            'var': "beamTrackYFrontTPC",
          },
          {
            'name': "beamTrackYFrontTPC_wide",
            'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
            'ytitle': "Beam Tracks / bin",
            'binning': [100,0,700],
            'var': "beamTrackYFrontTPC",
          },
       ],
      'cut': "beamTrackYFrontTPC > 400 && beamTrackYFrontTPC < 470"
    },
    {
      'histConfigs':
        [
          {
            'name': "beamTrackTheta",
            'xtitle': "Beam Track #theta [deg]",
            'ytitle': "Tracks / bin",
            'binning': [50,0,50],
            'var': "beamTrackTheta*180/pi",
          },
          {
            'name': "beamTrackTheta_wide",
            'xtitle': "Beam Track #theta [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,0,180],
            'var': "beamTrackTheta*180/pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "beamTrackPhi",
            'xtitle': "Beam Track #phi [deg]",
            'ytitle': "Tracks / bin",
            'binning': [60,-160,-100],
            'var': "beamTrackPhi*180/pi",
          },
          {
            'name': "beamTrackPhi_wide",
            'xtitle': "Beam Track #phi [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,-180,180],
            'var': "beamTrackPhi*180/pi",
            'printIntegral': True,
          },
       ],
      'cut': "1",
    },
    {
      'name': "nBeamTracks",
      'xtitle': "Number of Beam Tracks",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "nBeamTracks",
      'cut': "1",
    },
    {
      'name': "beamTrackMom",
      'xtitle': "Beam Track Momentum [GeV/c]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,0,10],
      'var': "beamTrackMom",
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
  scaleFactor= 8.2
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "MCC10 2 & 7 GeV 3m SCE"

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
      'title': "MC, 1 Beam Track",
      'cuts': "*(nBeamTracks==1)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'title': "MC, 2 Beam Track",
      'cuts': "*(nBeamTracks==2)",
      'color': root.kGreen+3,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'title': "MC, 3 Beam Track",
      'cuts': "*(nBeamTracks==3)",
      'color': root.kOrange-3,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'title': "MC, #geq 4 Beam Track",
      'cuts': "*(nBeamTracks>=4)",
      'color': root.kAzure+10,
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


  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="BeamTracks_",outSuffix="_NM1Hist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamTracks_",outSuffix="Hist",nMax=NMAX)
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig['logy'] = True
    else: 
      cutConfig['logy'] = True
  logHistConfigs = []
  for histConfig in histConfigs:
    histConfig['logy'] = True
  NMinusOnePlot(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="BeamTracks_",outSuffix="_NM1_logyHist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamTracks_",outSuffix="_logyHist",nMax=NMAX)

