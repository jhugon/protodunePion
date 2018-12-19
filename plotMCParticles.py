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
            'name': "mcPartStartMom",
            'xtitle': "MCParticle Start Momentum [MeV/c]",
            'ytitle': "Particles / bin",
            'binning': [100,0,10000],
            'var': "mcPartStartMom",
          },
          {
            'name': "mcPartStartMom_wide",
            'xtitle': "MCParticle Start Momentum [MeV/c]",
            'ytitle': "Particles / bin",
            'binning': [200,0,100000],
            'var': "mcPartStartMom",
          },
       ],
      #'cut': "mcPartStartMom > 1000 && mcPartStartMom < 3000",
      #'cut': "mcPartStartMom > 500 && mcPartStartMom < 10000",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "mcPartStartKin",
            'xtitle': "MCParticle Start Momentum [MeV/c]",
            'ytitle': "Particles / bin",
            'binning': [100,0,10000],
            'var': "mcPartStartMom",
          },
          {
            'name': "mcPartStartMom_wide",
            'xtitle': "MCParticle Start Momentum [MeV/c]",
            'ytitle': "Particles / bin",
            'binning': [200,0,100000],
            'var': "mcPartStartMom",
          },
       ],
      #'cut': "mcPartStartMom > 1000 && mcPartStartMom < 3000",
      #'cut': "mcPartStartMom > 500 && mcPartStartMom < 10000",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "mcPartXFrontTPC",
            'xtitle': "X of MCParticle Projected to Z=0 [cm]",
            'ytitle': "Particles / bin",
            'binning': [100,-75,20],
            'var': "mcPartXFrontTPC",
          },
          {
            'name': "mcPartXFrontTPC_wide",
            'xtitle': "X of MCParticle Projected to Z=0 [cm]",
            'ytitle': "Particles / bin",
            'binning': [200,-400,400],
            'var': "mcPartXFrontTPC",
          },
       ],
      #'cut': "mcPartXFrontTPC > -40 && mcPartXFrontTPC < 15",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "mcPartYFrontTPC",
            'xtitle': "Y of MCParticle Projected to Z=0 [cm]",
            'ytitle': "Particles / bin",
            'binning': [100,375,475],
            'var': "mcPartYFrontTPC",
          },
          {
            'name': "mcPartYFrontTPC_wide",
            'xtitle': "Y of MCParticle Projected to Z=0 [cm]",
            'ytitle': "Particles / bin",
            'binning': [200,0,800],
            'var': "mcPartYFrontTPC",
          },
       ],
      #'cut': "mcPartYFrontTPC > 400 && mcPartYFrontTPC < 445",
      'cut': "1",
    },
    {
      'name': "mcPartStartTheta",
      'xtitle': "#theta of MCParticle [deg]",
      'ytitle': "Particles / bin",
      'binning': [180,0,180],
      'var': "mcPartStartTheta*180/pi",
      #'cut': "mcPartStartTheta < 50*180/pi",
      'cut': "1",
    },
    {
      'name': "mcPartStartPhi",
      'xtitle': "#phi of MCParticle [deg]",
      'ytitle': "Particles / bin",
      'binning': [180,-180,180],
      'var': "mcPartStartPhi*180/pi",
      'cut': "1",
    },
    {
      'name': "mcPartIsBeamPrimary",
      'xtitle': "MCParticle is Beam + is Primary",
      'ytitle': "Particles / bin",
      'binning': [4,0,4],
      'var': "mcPartIsBeam+2*mcPartIsPrimary",
      #'cut': "mcPartIsBeam*mcPartIsPrimary",
      'cut': "1",
    },
    {
      'histConfigs':
        [
          {
            'name': "mcPartStartT",
            'xtitle': "MCParticle Start Time [ns]",
            'ytitle': "Particles / bin",
            'binning': [1000,-5e3,5e3],
            'var': "mcPartStartT",
          },
          {
            'name': "mcPartStartT_zoom",
            'xtitle': "MCParticle Start Time [ns]",
            'ytitle': "Particles / bin",
            'binning': [1000,-5e1,5e1],
            'var': "mcPartStartT",
          },
       ],
      'cut': "mcPartStartT==0.",
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  nData = 224281.0
  fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  caption = "MCC10, 2 GeV SCE"
  fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  caption = "MCC11"
  fileConfigsMC = [
    {
      'fn': fn,
      'title': "Cosmic Non-Primaries",
      'cuts': "*(!mcPartIsBeam)*(!mcPartIsPrimary)",
      'color': root.kBlue-7,
    },
    {
      'fn': fn,
      'title': "Cosmic Primaries",
      'cuts': "*(!mcPartIsBeam)*mcPartIsPrimary",
      'color': root.kGreen+3,
    },
    {
      'fn': fn,
      'title': "Beam Non-Primaries",
      'cuts': "*mcPartIsBeam*(!mcPartIsPrimary)",
      'color': root.kOrange-3,
    },
    {
      'fn': fn,
      'title': "Beam Primaries",
      'cuts': "*mcPartIsBeam*mcPartIsPrimary",
      'color': root.kAzure+10,
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

  dataMCStackNMinusOne([],fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="MCPart_",outSuffix="_NM1Hist",nMax=NMAX)
  dataMCStack([],fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="MCPart_",outSuffix="Hist",nMax=NMAX)
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig['logy'] = True
    else: 
      cutConfig['logy'] = True
  logHistConfigs = []
  for histConfig in histConfigs:
    histConfig['logy'] = True
  dataMCStackNMinusOne([],fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="MCPart_",outSuffix="_NM1_logyHist",nMax=NMAX)
  dataMCStack([],fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="MCPart_",outSuffix="_logyHist",nMax=NMAX)

