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
            'binning': [50,-100,100],
            'var': "trackXFrontTPC",
          },
          {
            'name': "trackXFrontTPC_wide",
            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [150,-600,600],
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
            'binning': [300,-500,1500],
            'var': "trackYFrontTPC",
          },
       ],
      'cut': "trackYFrontTPC > 400 && trackYFrontTPC < 470"
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartX",
            'xtitle': "Track Start X Position [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [50,-100,100],
            'var': "trackStartX",
          },
          {
            'name': "trackStartX_wide",
            'xtitle': "Track Start X Position [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [150,-500,500],
            'var': "trackStartX",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartY",
            'xtitle': "Track Start Y Position [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [50,300,600],
            'var': "trackStartY",
          },
          {
            'name': "trackStartY_wide",
            'xtitle': "Track Start Y Position [cm]",
            'ytitle': "TPC Tracks / bin",
            'binning': [315,-10,620],
            'var': "trackStartY",
          },
       ],
      'cut': "1"
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
      'histConfigs':
        [
          {
            'name': "trackStartThetaY",
            'xtitle': "TPC Track #theta_{y} [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,0,180],
            'var': "acos(sin(trackStartTheta)*sin(trackStartPhi))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartPhiZX",
            'xtitle': "TPC Track #phi_{zx} [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,-180,180],
            'var': "atan2(sin(trackStartTheta)*cos(trackStartPhi),cos(trackStartTheta))*180./pi",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "trackStartThetaX",
            'xtitle': "TPC Track #theta_{x} [deg]",
            'ytitle': "Tracks / bin",
            'binning': [180,0,180],
            'var': "acos(sin(trackStartTheta)*cos(trackStartPhi))*180./pi",
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
              'ytitle': "Tracks / bin",
              'binning': [100,0,1],
              'var': "sin(trackStartTheta)*cos(trackStartPhi)",
          },
       ],
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
              'name': "trackStartPhiZY",
              'xtitle': "TPC Track #phi_{zy} [deg]",
              'ytitle': "Tracks / bin",
              'binning': [180,-180,180],
              'var': "atan2(sin(trackStartTheta)*sin(trackStartPhi),cos(trackStartTheta))*180./pi",
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
  #fn = "PiAbs_mcc11.root"
  fn = "piAbsSelector_mcc11_protoDUNE_reco_hadd.root"
  caption = "Beam Data & MCC11"
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "Beam Data, MCC10 2 & 7 GeV"
  scaleFactor= 7.95

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
      'name': "data",
      'title': "ProtoDUNE-SP Data",
      'caption': "ProtoDUNE-SP Data",
      'color': root.kBlack,
      'cuts': "*(triggerIsBeam)",
    },
  ]
  fileConfigsMC = [
    {
      'fn': fn,
      'name': "mcc11_cosmics",
      'title': "MCC11 Cosmics",
      'caption': "MCC11 Cosmics",
      'cuts': "*(!trackTrueIsBeam)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'name': "mcc11_beam_nonTrigger",
      'title': "MCC11 Beam Non-Trigger",
      'caption': "MCC11 Beam Non-Trigger",
      'cuts': "*trackTrueIsBeam*((trackTrueMotherID!=0) || (fabs(trackTrueStartT) >= 1e-6))",
      'color': root.kGreen+3,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'name': "mcc11_beamline_trigger",
      'title': "MCC11 Beamline Trigger",
      'caption': "MCC11 Beamline Trigger",
      'cuts': "*trackTrueIsBeam*(trackTrueMotherID==0) && (fabs(trackTrueStartT) < 1e-6)",
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


  NMinusOneDataMCStack(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_NM1Hist",nMax=NMAX,table=True)
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
  NMinusOneDataMCStack(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_NM1_logyHist",nMax=NMAX)
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",outSuffix="_logyHist",nMax=NMAX)

  fileConfigsMC += [
    {
      'fn': fn,
      'name': "mcc11_no_cuts",
      'title': "MCC11 No Cuts",
      'caption': "MCC11 No Cuts",
      'scaleFactor': scaleFactor,
    },
    {
      'fn': fn,
      'name': "mcc11_no_cuts_scale_beam",
      'title': "MCC11 No Cuts, Scale Beam #times 10",
      'caption': "MCC11 No Cuts, Scale Beam #times 10",
      'scaleFactor': scaleFactor,
      'cuts': "*(trackTrueIsBeam*10+(!trackTrueIsBeam))",
    },
  ]

  logz = True
  histConfigs= [
    {
      'name': "trackStartThetaVPhi",
      'xtitle': "TPC Track #phi [deg]",
      'ytitle': "TPC Track #theta [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "trackStartTheta*180/pi:trackStartPhi*180/pi",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackStartThetaYVtrackStartPhiZX",
      'xtitle': "TPC Track #phi_{zx} [deg]",
      'ytitle': "TPC Track #theta_{y} [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "acos(sin(trackStartTheta)*sin(trackStartPhi))*180/pi:atan2(sin(trackStartTheta)*cos(trackStartPhi),cos(trackStartTheta))*180/pi",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackStartThetaXVtrackStartPhiZY",
      'xtitle': "TPC Track #phi_{zy} [deg]",
      'ytitle': "TPC Track #theta_{x} [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "acos(sin(trackStartTheta)*cos(trackStartPhi))*180/pi:atan2(sin(trackStartTheta)*sin(trackStartPhi),cos(trackStartTheta))*180/pi",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackStartThetaVtrackStartZ",
      'xtitle': "TPC Track Start Z Position [cm]",
      'ytitle': "TPC Track #theta [deg]",
      'binning': [100,-50,700,30,0,180],
      'var': "trackStartTheta*180/pi:trackStartZ",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackStartThetaVtrackLength",
      'xtitle': "TPC Track Length [cm]",
      'ytitle': "TPC Track #theta [deg]",
      'binning': [100,-50,700,30,0,180],
      'var': "trackStartTheta*180/pi:trackLength",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackYFrontTPCVtrackXFrontTPC",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "Y of TPC Track Projection to TPC Front [cm]",
      'binning': [100,-560,560,50,-200,800],
      'var': "trackYFrontTPC:trackXFrontTPC",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackYFrontTPCVtrackXFrontTPC_trackStartThetaLt30",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "Y of TPC Track Projection to TPC Front [cm]",
      'binning': [100,-560,560,50,-200,800],
      'var': "trackYFrontTPC:trackXFrontTPC",
      'cuts': "(trackStartTheta < 30*pi/180.)",
      'logz': logz,
    },
    {
      'name': "trackYFrontTPCVtrackXFrontTPC_trackStartZLt50",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "Y of TPC Track Projection to TPC Front [cm]",
      'binning': [100,-560,560,50,-200,800],
      'var': "trackYFrontTPC:trackXFrontTPC",
      'cuts': "(trackStartZ < 50)",
      'logz': logz,
    },
    {
      'name': "trackStartYVtrackStartX",
      'xtitle': "Track Start X Position [cm]",
      'ytitle': "Track Start Y Position [cm]",
      'binning': [100,-450,450,100,-50,650],
      'var': "trackStartY:trackStartX",
      'cuts': "1",
      'logz': logz,
    },
    {
      'name': "trackStartYVtrackStartX_trackStartThetaLt30",
      'xtitle': "Track Start X Position [cm]",
      'ytitle': "Track Start Y Position [cm]",
      'binning': [100,-450,450,100,-50,650],
      'var': "trackStartY:trackStartX",
      'cuts': "(trackStartTheta < 30*pi/180.)",
      'logz': logz,
    },
    {
      'name': "trackStartYVtrackStartX_trackStartZLt50",
      'xtitle': "Track Start X Position [cm]",
      'ytitle': "Track Start Y Position [cm]",
      'binning': [100,-450,450,100,-50,650],
      'var': "trackStartY:trackStartX",
      'cuts': "(trackStartZ < 50)",
      'logz': logz,
    },
  ]
  plotOneHistOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Tracks_",nMax=NMAX)
