#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import multiprocessing
import copy

def compareTrackAngles(fileConfigs,weightStr,runSetName,NMAX):
  fileConfigs = copy.deepcopy(fileConfigs)
  for iFC, fc in enumerate(fileConfigs):
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
    fc["color"] = COLORLIST[iFC]

  c = root.TCanvas()

  histConfigs = [
    {
      'name': "PFBeamPrimAngleStartEndXZ",
      'xtitle': "#Delta #theta_{xz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartEndYZ",
      'xtitle': "#Delta #theta_{yz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    },
  ]
  plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_CompareSCE_",outSuffix="_"+runSetName,nMax=NMAX)

  del c

def compareMomSpread(fileConfigs,weightStr,runSetName,NMAX):
  fileConfigs = copy.deepcopy(fileConfigs)
  for fc in fileConfigs:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
  c = root.TCanvas()
  allhists = []
  alltitles = []
  for fileConfig in fileConfigs:
    if "3ms" in fileConfig["name"] or "flf" in fileConfig["name"]:
      continue
    match = re.search(r"\s+(\d+)\s+GeV",fileConfig['title'])
    if match:
      nomEnergy = match.group(1)
      histConfigs = [{
          'name': "Pspread",
          'xtitle': "BI #Delta p / p",
          'ytitle': "Area Normalized",
          'binning': [100,0,2],
          'var': "pWC/1000./{}".format(nomEnergy),
          'normalize': True,
          'cuts': weightStr+"*(pWC > -100)",
      }]
      hists = plotOneHistOnePlot([fileConfig],histConfigs,c,"PiAbsSelector/tree",nMax=NMAX,writeImages=False)
      for histname in hists:
        for samplename in hists[histname]:
          allhists.append(hists[histname][samplename])
      alltitles.append(fileConfig["title"])
      histConfigs = [
        {
          'name': "thetaWCXZvPspread",
          'ytitle': "BI #theta_{xz} [deg]",
          'xtitle': "BI #Delta p / p",
          'binning': [100,0,2,40,-12,-10],
          'var': "atan(tan(thetaWC)*cos(phiWC))*180/pi:pWC/1000./{}".format(nomEnergy),
          'cuts': weightStr+"*(thetaWC > -100 && pWC > -100)",
          'logz': False,
        },
        {
          'name': "thetaWCYZvPspread",
          'ytitle': "BI #theta_{yz} [deg]",
          'xtitle': "BI #Delta p / p",
          'binning': [100,0,2,30,-13,-10],
          'var': "atan(tan(thetaWC)*sin(phiWC))*180/pi:pWC/1000./{}".format(nomEnergy),
          'cuts': weightStr+"*(thetaWC > -100 && pWC > -100)",
          'logz': False,
        },
        {
          'name': "xWCXZvPspread",
          'ytitle': "BI X at TPC Front [cm]",
          'xtitle': "BI #Delta p / p",
          'binning': [100,0,2,50,-50,0],
          'var': "xWC:pWC/1000./{}".format(nomEnergy),
          'cuts': weightStr+"*(xWC > -100 && pWC > -100)",
          'logz': False,
        },
        {
          'name': "yWCXZvPspread",
          'ytitle': "BI Y at TPC Front [cm]",
          'xtitle': "BI #Delta p / p",
          'binning': [100,0,2,40,400,440],
          'var': "yWC:pWC/1000./{}".format(nomEnergy),
          'cuts': weightStr+"*(yWC > -100 && pWC > -100)",
          'logz': False,
        },
      ]
      hists = plotOneHistOnePlot([fileConfig],histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching2D_",outSuffix="",nMax=NMAX)
  plotHistsSimple(allhists,alltitles,"BI #Delta p / p","Area Normalized",c,"Matching_ComparePspread")
  del c

def doPlotsVersusMomentum(fileConfigs,weightStr,runSetName,NMAX):
  fileConfigsAll = copy.deepcopy(fileConfigs)
  for fc in fileConfigsAll:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
  fileConfigs = [fileConfig for fileConfig in fileConfigsAll if not ("SCE" in fileConfig["title"])]
  c = root.TCanvas()

  histConfigs = [
    {
      'name': "thetaWCXZvP",
      'ytitle': "BI #theta_{xz} [deg]",
      'xtitle': "BI Momentum [GeV/c]",
      'binning': [85,0,8.5,40,-12,-10],
      'var': "atan(tan(thetaWC)*cos(phiWC))*180/pi:pWC/1000.",
      'cuts': weightStr+"*(thetaWC > -100 && pWC > -100)",
      'logz': False,
    },
    {
      'name': "thetaWCYZvP",
      'ytitle': "BI #theta_{yz} [deg]",
      'xtitle': "BI Momentum [GeV/c]",
      'binning': [85,0,8.5,30,-13,-10],
      'var': "atan(tan(thetaWC)*sin(phiWC))*180/pi:pWC/1000.",
      'cuts': weightStr+"*(thetaWC > -100 && pWC > -100)",
      'logz': False,
    },
    {
      'name': "xWCXZvP",
      'ytitle': "BI X at TPC Front [cm]",
      'xtitle': "BI Momentum [GeV/c]",
      'binning': [85,0,8.5,50,-50,0],
      'var': "xWC:pWC/1000.",
      'cuts': weightStr+"*(xWC > -100 && pWC > -100)",
      'logz': False,
    },
    {
      'name': "yWCXZvP",
      'ytitle': "BI Y at TPC Front [cm]",
      'xtitle': "BI Momentum [GeV/c]",
      'binning': [85,0,8.5,40,400,440],
      'var': "yWC:pWC/1000.",
      'cuts': weightStr+"*(yWC > -100 && pWC > -100)",
      'logz': False,
    },
  ]
  for histConfig in histConfigs:
    histConfig["normalize"] = True
  hists = plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",nMax=NMAX,writeImages=False)
  print hists
  for histname in hists:
    sumHist = None
    for fn in hists[histname]:
      hist = hists[histname][fn]
      try:
        sumHist.Add(hist)
      except AttributeError:
        sumHist = hist
    plotHist2DSimple(sumHist,sumHist.GetXaxis().GetTitle(),sumHist.GetYaxis().GetTitle(),c,"Matching_"+histname)

def doMatchingPlots(fileConfigs,weightStr,runSetName,NMAX):
  fileConfigsAll = copy.deepcopy(fileConfigs)
  for fc in fileConfigsAll:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
  fileConfigs = [fileConfig for fileConfig in fileConfigsAll if not ("SCE" in fileConfig["title"])]

  c = root.TCanvas()

  histConfigs = [
    {
      'name': "xWC",
      'title': "New BI track projection to TPC",
      #'xtitle': "X Position of BI track projection to TPC [cm]",
      'xtitle': "X [cm]",
      'ytitle': "Area Normalized",
      'binning': [125,-75,50],
      'var': "xWC",
      'cuts': weightStr,
      'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "xWCOld",
      'title': "Old BI track projection to TPC",
      'binning': [125,-75,50],
      'var': "beamTrackXFrontTPCOld[0]",
      'cuts': weightStr,
      'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimStartX",
      'title': "PF Track Start",
      'binning': [125,-75,50],
      'normalize': True,
      'var': "PFBeamPrimStartX",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndX",
      'title': "PF Track End",
      'binning': [125,-75,50],
      'normalize': True,
      'var': "PFBeamPrimEndX",
      'cuts': weightStr,
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_X_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "yWC",
      #'xtitle': "Y Position of BI track projection to TPC [cm]",
      'xtitle': "Y [cm]",
      'title': "New BI track projection to TPC",
      'ytitle': "Area Normalized",
      'binning': [75,375,450],
      'var': "yWC",
      'cuts': weightStr,
      'normalize': True,
      'logy': logy,
    },
    {
      'name': "yWCOld",
      'title': "Old BI track projection to TPC",
      'binning': [75,375,450],
      'var': "beamTrackYFrontTPCOld[0]",
      'cuts': weightStr,
      'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimStartY",
      'title': "PF Track Start",
      'binning': [75,375,450],
      'var': "PFBeamPrimStartY",
      'normalize': True,
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndY",
      'title': "PF Track End",
      'binning': [75,375,450],
      'var': "PFBeamPrimEndY",
      'normalize': True,
      'cuts': weightStr,
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_Y_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "DeltaXPFBeamPrimStartBI",
      #'xtitle': "Pandora Beam Primary Start - Beam Track X [cm]",
      'xtitle': "#Delta X [cm]",
      'title': "PF Track Start - New Beam Track",
      'ytitle': "Area Normalized",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartX - beamTrackXFrontTPC",
      'normalize': True,
      'cuts': weightStr,
    },
    {
      'name': "DeltaXPFBeamPrimStartBIOld",
      'title': "PF Track Start - Old BI Track",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartX - beamTrackXFrontTPCOld[0]",
      'normalize': True,
      'cuts': weightStr,
    },
    {
      'name': "DeltaXBINewOld",
      'title': "New BI Track - Old BI Track",
      'binning': [50,-50,50],
      'var': "xWC - beamTrackXFrontTPCOld[0]",
      'normalize': True,
      'cuts': weightStr,
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_DeltaX_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "DeltaYPFBeamPrimStartBI",
      #'xtitle': "Pandora Beam Primary Start - Beam Track Y [cm]",
      'title': "PF Track Start - New Beam Track",
      'xtitle': "#Delta Y [cm]",
      'ytitle': "Area Normalized",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartY - beamTrackYFrontTPC",
      'normalize': True,
      'cuts': weightStr,
    },
    {
      'name': "DeltaYPFBeamPrimStartBIOld",
      'title': "PF Track Start - Old BI Track",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartY - beamTrackYFrontTPCOld[0]",
      'normalize': True,
      'cuts': weightStr,
    },
    {
      'name': "DeltaYBINewOld",
      'title': "New BI Track - Old BI Track",
      'binning': [50,-50,50],
      'var': "yWC - beamTrackYFrontTPCOld[0]",
      'normalize': True,
      'cuts': weightStr,
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_DeltaY_",outSuffix="",nMax=NMAX)
#  histConfigs = [
#    {
#      'name': "PFBeamPrimAngleToBeamTrk",
#      'xtitle': "Angle Between BI & Primary PF Track Start [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [80,0,40],
#      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
#      'cuts': weightStr,
#    },
#    {
#      'name': "PFBeamPrimAngleToBeamTrk_wide",
#      'xtitle': "Angle Between BI & Primary PF Track Start [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [180,0,180],
#      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
#      'cuts': weightStr,
#    },
#    #{
#    #  'name': "PFBeamPrimCosAngleToBeamTrk",
#    #  'xtitle': "|cos(#theta)| of BI & Primary PF Track Start",
#    #  'ytitle': "Events / bin",
#    #  'binning': [100,0,1],
#    #  'var': "fabs(cos(PFBeamPrimAngleToBeamTrk))",
#    #  'cuts': weightStr+"*(PFBeamPrimAngleToBeamTrk > -100)",
#    #},
#    {
#      'name': "PFBeamPrimEndAngleToBeamTrk",
#      'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [80,0,40],
#      'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
#      'cuts': weightStr,
#    },
#    {
#      'name': "PFBeamPrimEndAngleToBeamTrk_wide",
#      'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [180,0,180],
#      'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
#      'cuts': weightStr,
#    },
#    #{
#    #  'name': "PFBeamPrimEndCosAngleToBeamTrk",
#    #  'xtitle': "|cos(#theta)| of BI & Primary PF Track End",
#    #  'ytitle': "Events / bin",
#    #  'binning': [100,0,1],
#    #  'var': "fabs(cos(PFBeamPrimEndAngleToBeamTrk))",
#    #  'cuts': weightStr+"*(PFBeamPrimEndAngleToBeamTrk > -100)",
#    #},
#    {
#      'name': "PFBeamPrimTrkStartEndDirAngle",
#      'xtitle': "Angle Between PF Track Start & End [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [80,0,40],
#      'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
#      'cuts': weightStr,
#    },
#    {
#      'name': "PFBeamPrimTrkStartEndDirAngle_wide",
#      'xtitle': "Angle Between PF Track Start & End [Deg]",
#      'ytitle': "Events / bin",
#      'binning': [180,0,180],
#      'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
#      'cuts': weightStr,
#    },
#    #{
#    #  'name': "PFBeamPrimTrkStartEndDirCosAngle",
#    #  'xtitle': "|cos(#theta)| Primary PF Track Start & End",
#    #  'ytitle': "Events / bin",
#    #  'binning': [100,0,1],
#    #  'var': "fabs(cos(PFBeamPrimTrkStartEndDirAngle))",
#    #  'cuts': weightStr+"*(PFBeamPrimTrkStartEndDirAngle > -100)",
#    #},
#    ######################################
  histConfigs = [
    {
      'name': "PFBeamPrimStartThetaXZ",
      #'xtitle': "TPC Track Start #theta_{xz} [deg]",
      'title': "TPC Track Start",
      'xtitle': "#theta_{xz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [50,-25,0],
      #'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
    },
    {
      'name': "PFBeamPrimEndThetaXZ",
      'title': "TPC Track End",
      'binning': [50,-25,0],
      #'var': "atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "thetaWCXZ",
      'title': "New BI Track",
      'binning': [50,-25,0],
      #'var': "atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi",
      'var': "atan(tan(thetaWC)*cos(phiWC))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(thetaWC > -100)",
    },
    {
      'name': "thetaWCXZOld",
      'title': "Old BI Track",
      'binning': [50,-25,0],
      #'var': "atan2(sin(beamTrackThetaOld[0])*cos(beamTrackPhiOld[0]),cos(beamTrackThetaOld[0]))*180/pi",
      'var': "atan(tan(beamTrackThetaOld[0])*cos(beamTrackPhiOld[0]))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(nBeamTracksOld > 0 && beamTrackThetaOld > -100.)",
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_ThetaXZ_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "PFBeamPrimStartThetaYZ",
      #'xtitle': "TPC Track Start #theta_{yz} [deg]",
      'title': "TPC Track Start",
      'xtitle': "#theta_{yz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [80,-40,0],
      #'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
    },
    {
      'name': "PFBeamPrimEndThetaYZ",
      'title': "TPC Track End",
      'binning': [80,-40,0],
      #'var': "atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "thetaWCYZ",
      'title': "New BI Track",
      'binning': [80,-40,0],
      #'var': "atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi",
      'var': "atan(tan(thetaWC)*sin(phiWC))*180/pi",
      'cuts': weightStr+"*(thetaWC > -100)",
      'normalize': True,
      'printIntegral': True,
    },
    {
      'name': "thetaWCYZOld",
      'title': "Old BI Track",
      'binning': [80,-40,0],
      #'var': "atan2(sin(beamTrackThetaOld[0])*sin(beamTrackPhiOld[0]),cos(beamTrackThetaOld[0]))*180/pi",
      'var': "atan(tan(beamTrackThetaOld[0])*sin(beamTrackPhiOld[0]))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(nBeamTracksOld > 0 && beamTrackThetaOld > -100.)",
    },
  ]
  ######################################
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_ThetaYZ_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "PFBeamPrimAngleStartBIXZ",
      #'xtitle': "TPC Track Start-BI Angle in XZ-Plane [deg]",
      'title': "TPC Track Start-New BI Track",
      'xtitle': "#Delta #theta_{xz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && thetaWC > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartBIOldXZ",
      'title': "TPC Track Start-Old BI Track",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(beamTrackThetaOld[0])*cos(beamTrackPhiOld[0]),cos(beamTrackThetaOld[0]))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && nBeamTracksOld > 0 && beamTrackThetaOld[0] > -100)",
    },
    #{
    #  'name': "PFBeamPrimAngleStartEndXZ",
    #  'title': "TPC Track Start-End",
    #  'binning': [100,-50,50],
    #  'var': "atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi-atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
    #  'normalize': True,
    #  'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    #},
    {
      'name': "PFBeamPrimAngleStartBINewOldXZ",
      'title': "New BI Track - Old BI Track",
      'binning': [100,-50,50],
      'var': "atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi-atan2(sin(beamTrackThetaOld[0])*cos(beamTrackPhiOld[0]),cos(beamTrackThetaOld[0]))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(thetaWC > -100 && nBeamTracksOld > 0 && beamTrackThetaOld[0] > -100)",
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_DeltaThetaXZ_",outSuffix="",nMax=NMAX)
  histConfigs = [
    {
      'name': "PFBeamPrimAngleStartBIYZ",
      #'xtitle': "TPC Track Start-BI Angle in YZ-Plane [deg]",
      'title': "TPC Track Start-New BI Track",
      'xtitle': "#Delta #theta_{yz} [deg]",
      'ytitle': "Area Normalized",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && thetaWC > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartBIYZ",
      'title': "TPC Track Start-Old BI Track",
      'binning': [100,-50,50],
      'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(thetaWC)*sin(beamTrackPhiOld[0]),cos(thetaWC))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && nBeamTracksOld > 0 && beamTrackThetaOld[0] > -100)",
    },
    #{
    #  'name': "PFBeamPrimAngleStartEndYZ",
    #  'title': "TPC Track Start-End",
    #  'binning': [100,-50,50],
    #  'var': "atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi-atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
    #  'normalize': True,
    #  'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    #},
    {
      'name': "PFBeamPrimAngleStartBINewOldYZ",
      'title': "New BI Track - Old BI Track",
      'binning': [100,-50,50],
      'var': "atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi-atan2(sin(beamTrackThetaOld[0])*sin(beamTrackPhiOld[0]),cos(beamTrackThetaOld[0]))*180/pi",
      'normalize': True,
      'cuts': weightStr+"*(thetaWC > -100 && nBeamTracksOld > 0 && beamTrackThetaOld[0] > -100)",
    },
  ]
  for iHistConfig,histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[iHistConfig]
  plotManyHistsOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_DeltaThetaYZ_",outSuffix="",nMax=NMAX)

  histConfigs = [
    {
      'name': "xWCNewVOld",
      'xtitle': "Old BI Track X [cm]",
      'ytitle': "New BI Track X [cm]",
      'binning': [125,-75,50,125,-75,50],
      'var': "xWC:beamTrackXFrontTPCOld[0]",
      'cuts': weightStr,
      'logz': False,
    },
    {
      'name': "yWCNewVOld",
      'xtitle': "Old BI Track Y [cm]",
      'ytitle': "New BI Track Y [cm]",
      'binning': [75,375,450,75,375,450],
      'var': "yWC:beamTrackYFrontTPCOld[0]",
      'cuts': weightStr,
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartXVxWCNew",
      'xtitle': "New BI Track X [cm]",
      'ytitle': "PF Track Start X [cm]",
      'binning': [75,375,450,75,375,450],
      'var': "PFBeamPrimStartX:xWC",
      'cuts': weightStr,
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartXVxWCOld",
      'xtitle': "Old BI Track X [cm]",
      'ytitle': "PF Track Start X [cm]",
      'binning': [75,375,450,75,375,450],
      'var': "PFBeamPrimStartX:beamTrackXFrontTPCOld[0]",
      'cuts': weightStr,
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartYVyWCNew",
      'xtitle': "New BI Track Y [cm]",
      'ytitle': "PF Track Start Y [cm]",
      'binning': [75,375,450,75,375,450],
      'var': "PFBeamPrimStartY:yWC",
      'cuts': weightStr,
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartYVyWCOld",
      'xtitle': "Old BI Track Y [cm]",
      'ytitle': "PF Track Start Y [cm]",
      'binning': [75,375,450,75,375,450],
      'var': "PFBeamPrimStartY:beamTrackYFrontTPCOld[0]",
      'cuts': weightStr,
      'logz': False,
    },
  ]
  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching2D_",outSuffix="",nMax=NMAX)
    ##########################
    #### Tom Junk's Plots ####
    ##########################
  histConfigs = [
    {
      'name': "PFBeamPrimStartThetaYZVXZ",
      'ytitle': "PF Track Start #theta_{yz} [deg]",
      'xtitle': "PF Track Start #theta_{xz} [deg]",
      'binning': [50,-25,0,80,-40,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi:atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimEndThetaYZVXZ",
      'ytitle': "PF Track End #theta_{yz} [deg]",
      'xtitle': "PF Track End #theta_{xz} [deg]",
      'binning': [50,-25,0,80,-40,0],
      'var': "atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi:atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimEndTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartVEndThetaXZ",
      'ytitle': "PF Track Start #theta_{xz} [deg]",
      'xtitle': "PF Track End #theta_{xz} [deg]",
      'binning': [50,-25,0,50,-25,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi:atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartVEndThetaYZ",
      'ytitle': "PF Track Start #theta_{yz} [deg]",
      'xtitle': "PF Track End #theta_{yz} [deg]",
      'binning': [80,-40,0,80,-40,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi:atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
      'logz': False,
    },
    ############################
    {
      'name': "PFBeamPrimStartThetaXZVStartX",
      'ytitle': "PF Track start #theta_{xz} [deg]",
      'xtitle': "PF Track Start X [cm]",
      'binning': [50,-75,25,50,-25,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartX",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartThetaYZVStartX",
      'ytitle': "PF Track start #theta_{yz} [deg]",
      'xtitle': "PF Track Start X [cm]",
      'binning': [50,-75,25,80,-40,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartX",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartThetaXZVStartY",
      'ytitle': "PF Track start #theta_{xz} [deg]",
      'xtitle': "PF Track Start Y [cm]",
      'binning': [75,375,450,50,-25,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartY",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartThetaYZVStartY",
      'ytitle': "PF Track start #theta_{yz} [deg]",
      'xtitle': "PF Track Start Y [cm]",
      'binning': [75,375,450,80,-40,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartY",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartThetaXZVStartZ",
      'ytitle': "PF Track start #theta_{xz} [deg]",
      'xtitle': "PF Track Start Z [cm]",
      'binning': [55,-5,105,50,-25,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartZ",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartThetaYZVStartZ",
      'ytitle': "PF Track start #theta_{yz} [deg]",
      'xtitle': "PF Track Start Z [cm]",
      'binning': [55,-5,105,80,-40,0],
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi:PFBeamPrimStartZ",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
      'logz': False,
    },
    ###########################################
    ################ For Martin ###############
    ###########################################
    {
      'name': "PFBeamPrimStartXVStartZ",
      'ytitle': "PF Track Start X [cm]",
      'xtitle': "PF Track Start Z [cm]",
      'binning': [55,-5,105,50,-50,0],
      'var': "PFBeamPrimStartX:PFBeamPrimStartZ",
      'cuts': weightStr+"*(PFBeamPrimStartX > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartYVStartZ",
      'ytitle': "PF Track Start Y [cm]",
      'xtitle': "PF Track Start Z [cm]",
      'binning': [55,-5,105,40,400,440],
      'var': "PFBeamPrimStartY:PFBeamPrimStartZ",
      'cuts': weightStr+"*(PFBeamPrimStartX > -100)",
      'logz': False,
    },
    {
      'name': "PFBeamPrimStartYVStartX",
      'ytitle': "PF Track Start Y [cm]",
      'xtitle': "PF Track Start X [cm]",
      'binning': [50,-50,0,40,400,440],
      'var': "PFBeamPrimStartY:PFBeamPrimStartX",
      'cuts': weightStr+"*(PFBeamPrimStartX > -100)",
      'logz': False,
    },
  ]
  plotOneHistOnePlot(fileConfigsAll,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching2D_",outSuffix="",nMax=NMAX)

  del c

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
  #cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom > 0)"
  cutGoodBeamline = "(triggerIsBeam == 1 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1)"
  cutGoodFEMBs = "*(nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20)"

  deltaXTrackBICut = "*((isMC && ((PFBeamPrimStartX-xWC) > -5) && ((PFBeamPrimStartX-xWC) < 5)) || ((!isMC) && ((PFBeamPrimStartX-xWC) > 0) && ((PFBeamPrimStartX-xWC) < 20)))"
  deltaYTrackBICut = "*((isMC && ((PFBeamPrimStartY-yWC) > 0) && ((PFBeamPrimStartY-yWC) < 10)) || ((!isMC) && ((PFBeamPrimStartY-yWC) > 10) && ((PFBeamPrimStartY-yWC) < 30)))"
  rejectThroughgoingCut = "*(PFBeamPrimEndZ < 650.)"
  #primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50.)"+deltaXTrackBICut+deltaYTrackBICut+rejectThroughgoingCut
  primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50.)"
  stoppingProtonCut = "*(PFBeamPrimEnergySumCSDAProton/kinWCProton > 0.8 && PFBeamPrimEnergySumCSDAProton/kinWCProton < 1.)"
  stoppingMuonCut = "*(PFBeamPrimEnergySumCSDAMu/kinWC > 0.8 && PFBeamPrimEnergySumCSDAMu/kinWC < 1.)"
  weightStr = "1"+primaryTrackCuts#+stoppingProtonCut

  #nData = 224281.0
  logy = False

  NMAX=10000000000
  #NMAX=100
  sillies = []

  sillies.append((
    [{
      'fn': "piAbsSelector_run5387_v8.1_da81b52a.root",
      'name': "run5387",
      'title': "Run 5387: 1 GeV/c",
      'caption': "Run 5387: 1 GeV/c ",
      'isData': True,
      'cuts': "*(BIPion1GeV)*"+cutGoodBeamline+cutGoodFEMBs,
      #'cuts': "*(BIProton1GeV)*"+cutGoodBeamline+cutGoodFEMBs,
    },
    {
      'fn': "piAbsSelector_mcc11_sce_1GeV_histats_partAll_v7a1_55712adf.root",
      'name': "mcc11_sce_1GeV",
      'title': "MCC11 1 GeV/c SCE",
      'caption': "MCC11 1 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 0.39676616915422885, # for pions
      #'scaleFactor': 1, # for protons stopping cut
    }],
    "run5387_1GeV",
  ))

  sillies.append((
    [
    {
      'fn': "piAbsSelector_run5432_v8.1_da81b52a.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      'cuts': "*(BIPion2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
      #'cuts': "*(BIProton2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
    },
    #{
    #  'fn': "piAbsSelector_run5432_oldCalo_oldBIPos_v7.4_5a76d2fe.root",
    #  'name': "run5432_oldBIPos",
    #  'title': "Run 5432: 2 GeV/c Old BI Positions",
    #  'caption': "Run 5432: 2 GeV/c Old BI Positions",
    #  'isData': True,
    #  'cuts': "*(BIPion2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
    #  #'cuts': "*(BIProton2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
    #},
    #{
    #  'fn': "piAbsSelector_run5432_v8.0_64cf7360_local.root",
    #  'name': "run5432_fix",
    #  'title': "Run 5432: 2 GeV/c Jake's Fix",
    #  'caption': "Run 5432: 2 GeV/c Jake's Fix",
    #  'isData': True,
    #  'cuts': "*(BIPion2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
    #  #'cuts': "*(BIProton2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
    #},
    {
      'fn': "piAbsSelector_mcc11_sce_2GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 2 GeV/c SCE",
      'caption': "MCC11 2 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 5.451612903225806*1.62515262515,
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_2GeV_v7a1_55712adf.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 2 GeV/c No SCE",
      'caption': "MCC11 2 GeV/c No SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 1.,
    }
    ],
    "run5432_2GeV",
  ))

  sillies.append((
    [{
      'fn': "piAbsSelector_run5786_v8.1_da81b52a.root",
      'name': "run5786",
      'title': "Run 5786: 3 GeV/c",
      'caption': "Run 5786: 3 GeV/c",
      'isData': True,
      'cuts': "*(BIPion3GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
    },
    {
      'fn': "piAbsSelector_mcc11_sce_3GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_3GeV",
      'title': "MCC11 3 GeV/c SCE",
      'caption': "MCC11 3 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      #'scaleFactor': 1,
    }],
    "run5786_3GeV",
  ))

  sillies.append((
   [
    {
      'fn': "piAbsSelector_run5204_v8.1_da81b52a.root",
      'name': "run5204",
      'title': "Run 5204: 7 GeV/c",
      'caption': "Run 5204: 7 GeV/c",
      'isData': True,
      'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
    },
    {
      'fn': "piAbsSelector_mcc11_sce_7p0GeV_v7.0_55712adf_local.root",
      'name': "mcc11_sce_7GeV",
      'title': "MCC11 7 GeV/c SCE",
      'caption': "MCC11 7 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13 || truePrimaryPDG == -11)",
      'scaleFactor': 1,
    }],
    "run5204_7GeV",
  ))

  #sillies.append((
  # [
  # {
  #    'fn': "piAbsSelector_run5145_v7_55712ad_local.root",
  #    'name': "run5145",
  #    'title': "Run 5145: 7 GeV/c",
  #    'caption': "Run 5145: 7 GeV/c",
  #    'isData': True,
  #    'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
  #  },
  # # {
  # #   'fn': "PiAbsSelector_run5145_50evt_v7.4_5a76d2fe.root",
  # #   'name': "run5145_new",
  # #   'title': "Run 5145: 7 GeV/c New Run",
  # #   'caption': "Run 5145: 7 GeV/c New Run",
  # #   'isData': True,
  # #   'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
  # # },
  # # {
  # #   'fn': "piAbs_noRedoCalo_run5145_n100_64cf7360.root",
  # #   'name': "run5145_fix",
  # #   'title': "Run 5145: 7 GeV/c Jake's Fix",
  # #   'caption': "Run 5145: 7 GeV/c Jake's Fix",
  # #   'isData': True,
  # #   'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
  # # },
  # # {
  # #   'fn': "PiAbsSelector_run5145_50evt_oldPos_v7.4_5a76d2fe.root",
  # #   'name': "run5145_oldPos",
  # #   'title': "Run 5145: 7 GeV/c Old Pos",
  # #   'caption': "Run 5145: 7 GeV/c Old Pos",
  # #   'isData': True,
  # #   'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
  # # },
  #  {
  #    'fn': "piAbsSelector_mcc11_sce_7p0GeV_v7.0_55712adf_local.root",
  #    'name': "mcc11_sce_7GeV",
  #    'title': "MCC11 7 GeV/c SCE",
  #    'caption': "MCC11 7 GeV/c SCE",
  #    'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)",
  #    'scaleFactor': 1,
  #  }],
  #  "run5145_7GeV",
  #))

  doMP = True
  pool = None
  if doMP:
    pool = multiprocessing.Pool()
  for silly in sillies:
    if doMP:
      pool.apply_async(doMatchingPlots,(silly[0],weightStr,silly[1],NMAX))
    else:
      doMatchingPlots(silly[0],weightStr,silly[1],NMAX)
  for silly in sillies:
    if doMP:
      pool.apply_async(compareTrackAngles,(silly[0],weightStr,silly[1],NMAX))
    else:
      compareTrackAngles(silly[0],weightStr,silly[1],NMAX)
  if doMP:
    pool.apply_async(compareMomSpread,([fileConfig for silly in sillies  for fileConfig in silly[0]],weightStr,None,NMAX))
  else:
    compareMomSpread([fileConfig for silly in sillies for fileConfig in silly[0]],weightStr,None,NMAX)
  if doMP:
    pool.apply_async(doPlotsVersusMomentum,([fileConfig for silly in sillies  for fileConfig in silly[0]],weightStr,None,NMAX))
  else:
    doPlotsVersusMomentum([fileConfig for silly in sillies for fileConfig in silly[0]],weightStr,None,NMAX)
  if doMP:
    pool.close()
    pool.join()
