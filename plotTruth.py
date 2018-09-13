#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  cuts = ""

  secTrkCuts = "*(trackStartDistToPrimTrkEnd < 2.)"
  #weightStr = "pzWeight"+cuts
  weightStr = "1"+cuts

  logy = False

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    {
      'fn': "PiAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10.root",
      'name': "protodune_beam_p2GeV_cosmics_3ms_sce_mcc10",
      'title': "MCC10, 2 GeV SCE",
      'caption': "MCC10, 2 GeV SCE",
      'color': root.kBlack,
      'isData': False,
    },
  ]

  histConfigs = [
    {
      'name': "trueStartMom",
      'xtitle': "True Primary Start Momentum [MeV/c]",
      'ytitle': "Events / bin",
      'binning': [500,0,10000],
      'var': "trueStartMom",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueStartKin",
      'xtitle': "True Primary Start KE [MeV]",
      'ytitle': "Events / bin",
      'binning': [500,0,10000],
      'var': "trueStartKin",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueCategory",
      'xtitle': "Truth Category",
      'ytitle': "Events / bin",
      'binning': [20,0,20],
      'var': "trueCategory",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueEndProcess",
      'xtitle': "trueEndProcess",
      'ytitle': "Events / bin",
      'binning': [17,0,17],
      'var': "trueEndProcess",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "truePrimaryPDG",
      'xtitle': "True Primary PDG",
      'ytitle': "Events / bin",
      'binning': [3000,0,3000],
      'var': "abs(truePrimaryPDG)",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueStartX",
      'xtitle': "True Primary Starting X [cm]",
      'ytitle': "Events / bin",
      'binning': [100,-100,100],
      'var': "trueStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueStartY",
      'xtitle': "True Primary Starting Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,350,550],
      'var': "trueStartY",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueStartZ",
      'xtitle': "True Primary Starting Z [cm]",
      'ytitle': "Events / bin",
      'binning': [100,-300,100],
      'var': "trueStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueEndX",
      'xtitle': "True Primary Ending X [cm]",
      'ytitle': "Events / bin",
      'binning': [500,-500,500],
      'var': "trueEndX",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueEndY",
      'xtitle': "True Primary Ending Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,600],
      'var': "trueEndY",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueEndZ",
      'xtitle': "True Primary Ending Z [cm]",
      'ytitle': "Events / bin",
      'binning': [500,-200,5000],
      'var': "trueEndZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    #{
    #  'name': "trueStartTheta",
    #  'xtitle': "True Start #theta [deg]",
    #  'binning': [90,0,180],
    #  'var': "trueStartTheta*180/pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #},
    #{
    #  'name': "trueStartPhi",
    #  'xtitle': "True Start #phi",
    #  'binning': [90,-180,180],
    #  'var': "trueStartPhi*180/pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #},
    #{
    #  'name': "trueStartThetaY",
    #  'xtitle': "True Start #theta_{y} [deg]",
    #  'ytitle': "Events / bin",
    #  'binning': [180,0,180],
    #  'var': "acos(sin(trueStartTheta)*sin(trueStartPhi))*180./pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "trueStartPhiZX",
    #  'xtitle': "True Start #theta_{zx} [deg]",
    #  'ytitle': "Events / bin",
    #  'binning': [180,-180,180],
    #  'var': "atan2(sin(trueStartTheta)*cos(trueStartPhi),cos(trueStartTheta))*180./pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "trueStartThetaX",
    #  'xtitle': "True Start #theta_{x} [deg]",
    #  'ytitle': "Events / bin",
    #  'binning': [180,0,180],
    #  'var': "acos(sin(trueStartTheta)*cos(trueStartPhi))*180./pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "trueStartPhiZY",
    #  'xtitle': "True Start #theta_{zy} [deg]",
    #  'ytitle': "Events / bin",
    #  'binning': [180,-180,180],
    #  'var': "atan2(sin(trueStartTheta)*sin(trueStartPhi),cos(trueStartTheta))*180./pi",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
  ]

  plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="TruthInfo_",nMax=NMAX)

  histConfigs = [
    {
      'name': "trueStartThetaVtrueStartPhi",
      'xtitle': "True Start #phi [deg]",
      'ytitle': "True Start #theta [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "trueStartTheta*180/pi:trueStartPhi*180/pi",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trueStartThetaYVtrueStartPhiZX",
      'xtitle': "True Start #phi_{zx} [deg]",
      'ytitle': "True Start #theta_{y} [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "acos(sin(trueStartTheta)*sin(trueStartPhi))*180/pi:atan2(sin(trueStartTheta)*cos(trueStartPhi),cos(trueStartTheta))*180./pi",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trueStartThetaXVtrueStartPhiZY",
      'xtitle': "True Start #phi_{zy} [deg]",
      'ytitle': "True Start #theta_{x} [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "acos(sin(trueStartTheta)*cos(trueStartPhi))*180/pi:atan2(sin(trueStartTheta)*sin(trueStartPhi),cos(trueStartTheta))*180./pi",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trueStartYVtrueStartX",
      'xtitle': "True Start X [cm]",
      'ytitle': "True Start Y [cm]",
      'binning': [100,-1000,1000,100,-2000,200],
      'var': "trueStartY:trueStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trueYFrontTPCVtrueXFrontTPC",
      'xtitle': "True Start X Projected to Z=0 [cm]",
      'ytitle': "True Start Y Projected to Z=0 [cm]",
      'binning': [100,-1000,1000,100,-2000,200],
      'var': "trueYFrontTPC:trueXFrontTPC",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="TruthInfo_",nMax=NMAX)

