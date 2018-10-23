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
  name = "mcc11"
  caption = "Beam Data & MCC11"
  scaleFactor= 2.651
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
      'name': "data",
      'title': "Data",
      'caption': "Data",
      'color': root.kBlack,
      'cuts': "*(triggerIsBeam)",
    },
  ]
  fileConfigsMC = [
    {
      'fn': fn,
      'title': "MCC 11",
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

  histConfigs= [
    {
      'name': "beamTrackPhi",
      'xtitle': "Beam or TPC Track #phi [deg]",
      'ytitle': "Tracks / bin",
      'binning': [120,-160,-100],
      'var': "beamTrackPhi*180/pi",
      'cuts': "1",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "beamTrackTheta",
      'xtitle': "Beam or TPC Track #theta [deg]",
      'ytitle': "Tracks / bin",
      'binning': [100,0,50],
      'var': "beamTrackTheta*180/pi",
      'cuts': "1",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "beamTrackXFrontTPC",
      'xtitle': "X of Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,-100,50],
      'var': "beamTrackXFrontTPC",
      'cuts': "1",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "beamTrackYFrontTPC",
      'xtitle': "Y of Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,300,600],
      'var': "beamTrackYFrontTPC",
      'cuts': "1",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "trackStartPhi",
      'xtitle': "Beam or TPC Track #phi [deg]",
      'ytitle': "Tracks / bin",
      'binning': [120,-160,-100],
      'var': "trackStartPhi*180/pi",
      'cuts': "trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "trackStartTheta",
      'xtitle': "Beam or TPC Track #theta [deg]",
      'ytitle': "Tracks / bin",
      'binning': [100,0,50],
      'var': "trackStartTheta*180/pi",
      'cuts': "trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "trackXFrontTPC",
      'xtitle': "X of Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,-100,50],
      'var': "trackXFrontTPC",
      'cuts': "trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
      'normalize': True,
      'writeImage': False,
    },
    {
      'name': "trackYFrontTPC",
      'xtitle': "Y of Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,300,600],
      'var': "trackYFrontTPC",
      'cuts': "trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackStartZ<50",
      'normalize': True,
      'writeImage': False,
    },
  ]

  fileConfigs = fileConfigsData + [
    {
      'fn': fn,
      'name': name,
      'title': name.upper(),
      'caption': name.upper(),
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
  ]

  hists = plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamAndTPCTracks_",nMax=NMAX)
  print hists
  for histName in ["Phi","Theta","XFrontTPC","YFrontTPC"]:
    names = []
    thesehists = []
    for hn in hists:
      if histName in hn:
        ns = hists[hn].keys()
        ns.sort()
        names += [hn+" "+i for i in ns]
        thesehists += [hists[hn][n] for n in ns]
    print histName, names, thesehists
    plotHistsSimple(thesehists,names,None,"Tracks / bin",c,"BeamAndTPCTracks_"+histName)

  histConfigs= [
    {
      'name': "deltaXFrontTPC",
      'xtitle': "#Delta X of Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,-25,75],
      'var': "trackXFrontTPC - beamTrackXFrontTPC[0]",
      'cuts': "nBeamTracks == 1 && beamTrackMom > 0. && trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
    },
    {
      'name': "deltaYFrontTPC",
      'xtitle': "#Delta Y of Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,-50,50],
      'var': "trackYFrontTPC - beamTrackYFrontTPC[0]",
      'cuts': "nBeamTracks == 1 && beamTrackMom > 0. && trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
    },
  ]
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamAndTPCTracks_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
  DataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamAndTPCTracks_",outSuffix="_logyHist",nMax=NMAX)

  histConfigs= [
    {
      'name': "deltaYFrontTPCVDeltaXFrontTPC",
      'xtitle': "#Delta X of Track Projection to TPC Front [cm]",
      'ytitle': "#Delta Y of Track Projection to TPC Front [cm]",
      'binning': [50,-25,75,50,-50,50],
      'var': "trackYFrontTPC - beamTrackYFrontTPC[0]:trackXFrontTPC - beamTrackXFrontTPC[0]",
      'cuts': "nBeamTracks == 1 && beamTrackMom > 0. && trackXFrontTPC > -40 && trackXFrontTPC < 20 && trackYFrontTPC > 400 && trackYFrontTPC < 470 && trackStartZ<50",
    },
  ]
  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="BeamAndTPCTracks_",nMax=NMAX)
