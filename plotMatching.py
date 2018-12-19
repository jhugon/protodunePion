#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import os.path

if __name__ == "__main__":

  cutConfigs = [
    {
      'name': "mcPartStartMom",
      'xtitle': "MCParticle Start Momentum [MeV/c]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [100,0,10000],
      #'binning': [100,0,100000],
      'var': "mcPartStartMom",
      'cut': "mcPartStartMom > 1000 && mcPartStartMom < 3000",
      #'cut': "mcPartStartMom > 500 && mcPartStartMom < 10000",
      #'cut': "1",
    },
    {
      'name': "mcPartXFrontTPC",
      'xtitle': "X of MCParticle Projected to Z=0 [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,-75,20],
      'binning': [50,-150,150],
      'var': "mcPartXFrontTPC",
      'cut': "mcPartXFrontTPC > -40 && mcPartXFrontTPC < 15",
      #'cut': "1",
    },
    {
      'name': "mcPartYFrontTPC",
      'xtitle': "Y of MCParticle Projected to Z=0 [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,375,475],
      'binning': [50,300,500],
      'var': "mcPartYFrontTPC",
      'cut': "mcPartYFrontTPC > 400 && mcPartYFrontTPC < 445",
      #'cut': "1",
    },
    {
      'name': "mcPartStartTheta",
      'xtitle': "#theta of MCParticle [deg]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [60,0,180],
      'var': "mcPartStartTheta*180/pi",
      #'cut': "mcPartStartTheta < 50*180/pi",
      'cut': "1",
    },
    {
      'name': "mcPartStartPhi",
      'xtitle': "#phi of MCParticle [deg]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [60,-180,180],
      'var': "mcPartStartPhi*180/pi",
      'cut': "1",
    },
    {
      'name': "mcPartIsBeamPrimary",
      'xtitle': "MCParticle is Beam + is Primary",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [4,0,4],
      'var': "mcPartIsBeam+mcPartIsPrimary",
      #'cut': "mcPartIsBeam*mcPartIsPrimary",
      'cut': "1",
    },
    {
      'name': "trackXFrontTPC",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,-400,400],
      'binning': [50,-100,50],
      'var': "trackXFrontTPC",
      'cut': "trackXFrontTPC > -50 && trackXFrontTPC < 0"
    },
    {
      'name': "trackYFrontTPC",
      'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,0,700],
      'binning': [50,300,600],
      'var': "trackYFrontTPC",
      'cut': "trackYFrontTPC > 400 && trackYFrontTPC < 470"
    },
    {
      'name': "trackStartZ",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [400,-5,800],
      'binning': [50,-5,25],
      'var': "trackStartZ",
      'cut': "trackStartZ<50",
    },
    {
      'name': "trackStartTheta",
      'xtitle': "TPC Track Start #theta [deg]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [60,0,180],
      'var': "trackStartTheta*180/pi",
      'cut': "1",
    },
    {
      'name': "trackStartPhi",
      'xtitle': "TPC Track Start #phi [deg]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [60,-180,180],
      'var': "trackStartPhi*180/pi",
      'cut': "1",
    },
    {
      'name': "trackLength",
      'xtitle': "TPC Track Length [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      'binning': [200,0,800],
      'var': "trackLength",
      'cut': "1",
    },
    {
      'name': "trackMCPartDeltaXFrontTPC",
      'xtitle': "#Delta X of MCPart & Track at TPC Front [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,-400,400],
      'binning': [50,-100,100],
      'var': "trackXFrontTPC-mcPartXFrontTPC",
      'cut': "1"
    },
    {
      'name': "trackMCPartDeltaYFrontTPC",
      'xtitle': "#Delta Y of MCPart & Track at TPC Front [cm]",
      'ytitle': "Particles #times Tracks / Bin",
      #'binning': [100,0,700],
      'binning': [50,-100,100],
      'var': "trackYFrontTPC-mcPartYFrontTPC",
      'cut': "1"
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_10evts.root"
  #caption = "MCC10, 2 GeV SCE"
  fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  caption = "MCC11"
  fileConfigsMC = [
    {
      'fn': fn,
      'title': "Beam Primaries Correctly Matched",
      'cuts': "*(!mcPartIsBeam)*(!mcPartIsPrimary)*(mcPartTrackID==trackTrueID || mcPartTrackID==trackTrueMotherID)",
      'color': root.kBlue-7,
    },
    {
      'fn': fn,
      'title': "Cosmic Primaries Correctly Matched",
      'cuts': "*(!mcPartIsBeam)*mcPartIsPrimary*(mcPartTrackID==trackTrueID)",
      'color': root.kGreen+3,
    },
    {
      'fn': fn,
      'title': "Beam Non-Primaries Incorrectly Matched",
      'cuts': "*mcPartIsBeam*(!mcPartIsPrimary)*(mcPartTrackID!=trackTrueID)",
      'color': root.kOrange-3,
    },
    {
      'fn': fn,
      'title': "Beam Primaries Incorrectly Matched",
      'cuts': "*mcPartIsBeam*mcPartIsPrimary*(mcPartTrackID!=trackTrueID)",
      'color': root.kAzure+10,
    },
  ]

  for cutConfig in cutConfigs:
    cutConfig["caption"] = "N-1 Cut, "+caption

  histConfigs = []
  for cutConfig in cutConfigs:
    config = copy.deepcopy(cutConfig)
    config["caption"] = caption
    del config["cut"]
    config["cuts"] = "1"
    histConfigs.append(config)

  NMinusOneDataMCStack([],fileConfigsMC,cutConfigs,c,"BeamMatchingAnalyzer/tree",outPrefix="Matching_",outSuffix="_NM1Hist",nMax=NMAX)
  DataMCStack([],fileConfigsMC,histConfigs,c,"BeamMatchingAnalyzer/tree",outPrefix="Matching_",outSuffix="Hist",nMax=NMAX)
  for cutConfig in cutConfigs:
    cutConfig['logy'] = True
  logHistConfigs = []
  for histConfig in histConfigs:
    histConfig['logy'] = True
  NMinusOneDataMCStack([],fileConfigsMC,cutConfigs,c,"BeamMatchingAnalyzer/tree",outPrefix="Matching_",outSuffix="_NM1_logyHist",nMax=NMAX)
  DataMCStack([],fileConfigsMC,histConfigs,c,"BeamMatchingAnalyzer/tree",outPrefix="Matching_",outSuffix="_logyHist",nMax=NMAX)

  fileConfigs = [
    {
      'fn': fn,
      'name': os.path.splitext(fn)[0],
      'title': caption,
      'caption': caption,
      'color': root.kBlack,
      'isData': False,
    },
  ]

  binning = [100,4e5,7e5,100,4e5,7e5]
  
  histConfigs = [
    {
      'name': "mcPartTrackIDVtrackTrueID",
      'xtitle': "Track Matched TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueID",
      'cuts': "1",
      #'normalize': True,
      'logz': True,
    },
    {
      'name': "mcPartTrackIDVtrackTrueID_mcPartIsPrimary",
      'xtitle': "Track Matched TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueID",
      'cuts': "(mcPartIsPrimary)",
      'captionright1': "MCParticle is Primary",
      #'normalize': True,
      'logz': True,
    },
    {
      'name': "mcPartTrackIDVtrackTrueID_trackTruthIsPrimary",
      'xtitle': "Track Matched TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueID",
      'cuts': "(trackTrueMotherID == 0)",
      'captionright1': "Track Matched Particle is Primary",
      #'normalize': True,
      'logz': True,
    },
    {
      'name': "mcPartTrackIDVtrackTrueID_cuts",
      'xtitle': "Track Matched TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueID",
      'cuts': "(mcPartStartMom > 1000 && mcPartStartMom < 3000)*(mcPartXFrontTPC > -40 && mcPartXFrontTPC < 15)*(mcPartYFrontTPC > 400 && mcPartYFrontTPC < 445)*(trackXFrontTPC > -50 && trackXFrontTPC < 0)*(trackYFrontTPC > 400 && trackYFrontTPC < 470)*(trackStartZ<50)",
      'captionright1': "Track & MCParticle Cuts",
      #'normalize': True,
      'logz': True,
    },
    {
      'name': "mcPartTrackIDVtrackTrueMotherID",
      'xtitle': "Track Matched Mother's TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueMotherID",
      'cuts': "1",
      #'normalize': True,
      'logz': True,
    },
    {
      'name': "mcPartTrackIDVtrackTrueMotherID_cuts",
      'xtitle': "Track Matched Mother's TrackID",
      'ytitle': "MCParticle TrackID",
      'binning': [100,0,1e6,100,0,1e6],
      'binning': binning,
      'var': "mcPartTrackID:trackTrueMotherID",
      'cuts': "(mcPartStartMom > 1000 && mcPartStartMom < 3000)*(mcPartXFrontTPC > -40 && mcPartXFrontTPC < 15)*(mcPartYFrontTPC > 400 && mcPartYFrontTPC < 445)*(trackXFrontTPC > -50 && trackXFrontTPC < 0)*(trackYFrontTPC > 400 && trackYFrontTPC < 470)*(trackStartZ<50)",
      'captionright1': "Track & MCParticle Cuts",
      #'normalize': True,
      'logz': True,
    },
  ]
  plotOneHistOnePlot(fileConfigs,histConfigs,c,"BeamMatchingAnalyzer/tree",outPrefix="Matching_",outSuffix="_Hist",nMax=NMAX)

