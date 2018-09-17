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
      #'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_5evts.root",
      'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_10evts.root",
      #'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root",
      'name': "protodune_beam_p2GeV_cosmics_3ms_sce_mcc10",
      'title': "MCC10, 2 GeV SCE",
      'caption': "MCC10, 2 GeV SCE",
      'color': root.kBlack,
      'isData': False,
    },
  ]

  mcPartCases = [
    {
      'title': "Cosmic Non-Primaries",
      'cuts': "(!mcPartIsBeam)*(!mcPartProcess)",
      'color': root.kBlue-7,
    },
    {
      'title': "Cosmic Primaries",
      'cuts': "(!mcPartIsBeam)*mcPartProcess",
      'color': root.kGreen+3,
    },
    {
      'title': "Beam Non-Primaries",
      'cuts': "mcPartIsBeam*(!mcPartProcess)",
      'color': root.kOrange-3,
    },
    {
      'title': "Beam Primaries",
      'cuts': "mcPartIsBeam*mcPartProcess",
      'color': root.kAzure+10,
    },
  ]
  for i in range(len(mcPartCases)):
    mcPartCases[i]['color'] = TRUECATEGORYFEWERCONFIGS[i]['color']

  mcPartSpeciesCases = [
    #{
    #  'title': "Cosmic #mu^{#pm}",
    #  'cuts': "(!mcPartIsBeam)*(abs(mcPartPrimaryPDG) == 13)",
    #  'color': root.kRed-4,
    #},
    {
      'title': "Beam #mu^{#pm}",
      'cuts': "mcPartIsBeam*(abs(mcPartPrimaryPDG) == 13)",
     'color': root.kBlue-7,
    },
    {
      'title': "Beam #pmp",
      'cuts': "mcPartIsBeam*(abs(mcPartPrimaryPDG) == 2212)",
     'color': root.kGreen+3,
    },
    {
      'title': "Beam e^{#pm}",
      'cuts': "mcPartIsBeam*(abs(mcPartPrimaryPDG) == 11)",
     'color': root.kOrange-3,
    },
    {
      'title': "Beam #pm#pi",
      'cuts': "mcPartIsBeam*(abs(mcPartPrimaryPDG) == 211)",
     'color': root.kAzure+10,
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

  #plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="TruthInfo_",nMax=NMAX)

  histConfigs = [
    {
      'name': "mcPartStartMom",
      'xtitle': "MCParticle Start Momentum [MeV/c]",
      'ytitle': "Events / bin",
      'binning': [100,0,4],
      'var': "mcPartStartMom",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
    {
      'name': "mcPartStartMom_logx",
      'xtitle': "MCParticle Start Momentum [MeV/c]",
      'ytitle': "Events / bin",
      'binning': getLogBins(100,0.01,100),
      'var': "mcPartStartMom",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
      'logx': True,
    },
    {
      'name': "mcPartStartX",
      'xtitle': "MCParticle Start X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-500,500],
      'var': "mcPartStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
    {
      'name': "mcPartStartY",
      'xtitle': "MCParticle Start Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-100,1500],
      'var': "mcPartStartY",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
    {
      'name': "mcPartStartZ",
      'xtitle': "MCParticle Start Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-300,1000],
      'var': "mcPartStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
    {
      'name': "mcPartXFrontTPC",
      'xtitle': "X of MCParticle Projected to Z=0 [cm]",
      'ytitle': "Events / bin",
      'binning': [100,-1000,1000],
      'var': "mcPartXFrontTPC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
    {
      'name': "mcPartYFrontTPC",
      'xtitle': "Y of MCParticle Projected to Z=0 [cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,1500],
      'var': "mcPartYFrontTPC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
    },
  ]

  DataMCCategoryStack([],fileConfigs,histConfigs,c,"PiAbsSelector/tree",
                outPrefix="TruthInfo_",nMax=NMAX,
                catConfigs=mcPartCases
             )

  DataMCCategoryStack([],fileConfigs,histConfigs,c,"PiAbsSelector/tree",
                outPrefix="TruthInfo_Species_",nMax=NMAX,
                catConfigs=mcPartSpeciesCases
             )

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
      'binning': [100,-50,50,100,400,500],
      'var': "trueStartY:trueStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trueYFrontTPCVtrueXFrontTPC",
      'xtitle': "X of True Particle Projected to Z=0 [cm]",
      'ytitle': "Y of True Particle Projected to Z=0 [cm]",
      'binning': [30,-60,0,30,300,500],
      'var': "trueYFrontTPC:trueXFrontTPC",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="TruthInfo_",nMax=NMAX)

