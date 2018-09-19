#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  cuts = ""

  #cuts += "*( iBestMatch >= 0 && nMatchedTracks == 1)" # matching in analyzer

  # matching debug
  #cuts += "*(sqrt(pow(xWC-23.75,2)+pow(yWC-0.2,2)) < 11.93)" # wc track in flange
  #cuts += "*(trackXFront > -50. && trackXFront < -10. && trackYFrontTPC > 390. && trackYFrontTPC < 430.)" # TPC track in flange
  #cuts += "*(trackMatchLowestZ < 2.)" # matching
  #cuts += "*(fabs(trackMatchDeltaY) < 5.)" # matching
  #cuts += "*((!isMC && (trackMatchDeltaX < 6. && trackMatchDeltaX > -4.)) || (isMC && (fabs(trackMatchDeltaX) < 5.)))" # matching
  #cuts += "*(trackMatchDeltaAngle*180/pi < 10.)" # matching
  ###
  ###
  secTrkCuts = "*(trackStartDistToPrimTrkEnd < 2.)"
  #weightStr = "pzWeight"+cuts
  weightStr = "1"+cuts

  weightStrTrackMatch = "1"+cuts#+"*(trackMatchLowestZ < 2.)"

  #nData = 224281.0
  logy = False

  c = root.TCanvas("c")

  NMAX=10000000000
  caption = "MCC10, 2 GeV SCE"

  fileConfigs = [
    {
      'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_mcc10_100evts.root",
      'title': "SCE Off",
      'caption': caption,
    },
    {
      'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root",
      'title': "SCE On",
      'caption': caption,
    },
  ]
  for i in range(len(fileConfigs)):
    fileConfigs[i]['color'] = COLORLIST[i]

  histConfigs = [
    {
      'name': "trackMatchDeltaX",
      'xtitle': "TPC / WC Track #Delta x at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [40,-50,50],
      #'var': "trackMatchDeltaX[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaX",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackMatchDeltaX_wide",
      'xtitle': "TPC / WC Track #Delta x at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,-500,500],
      #'var': "trackMatchDeltaX[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaX",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackMatchDeltaY",
      'xtitle': "TPC / WC Track #Delta y at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [40,-50,50],
      #'var': "trackMatchDeltaY[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaY",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackMatchDeltaY_wide",
      'xtitle': "TPC / WC Track #Delta y at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,-500,500],
      #'var': "trackMatchDeltaY[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaY",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackMatchDeltaAngle",
      'xtitle': "TPC / WC Track #Delta #alpha [deg]",
      'ytitle': "TPC Tracks / bin",
      #'binning': [90,0,180],
      'binning': [30,0,30],
      #'var': "trackMatchDeltaAngle[iBestMatch]*180/pi",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaAngle*180/pi",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackMatchDeltaAngle_wide",
      'xtitle': "TPC / WC Track #Delta #alpha [deg]",
      'ytitle': "TPC Tracks / bin",
      'binning': [90,0,180],
      #'binning': [20,0,20],
      #'var': "trackMatchDeltaAngle[iBestMatch]*180/pi",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaAngle*180/pi",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackXFrontTPC",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [50,-100,100],
      'var': "trackXFrontTPC",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackYFrontTPC",
      'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [50,340,500],
      'var': "trackYFrontTPC",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackXFrontTPC_beamMatched",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [50,-100,100],
      'var': "trackXFrontTPC",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logy': logy,
      'caption': "Truth Beam Matched, "+caption,
    },
    {
      'name': "trackYFrontTPC_beamMatched",
      'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [50,340,500],
      'var': "trackYFrontTPC",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logy': logy,
      'caption': "Truth Beam Matched, "+caption,
    },
    {
      'name': "trackStartX",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-400,400],
      'var': "trackStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackStartY",
      'xtitle': "TPC Track Start Y [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-5,650],
      'var': "trackStartY",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'caption': caption,
    },
    {
      'name': "trackStartZ",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-5,25],
      'var': "trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': False,
      'caption': caption,
    },
    {
      'name': "trackStartZ_Logy",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-5,25],
      'var': "trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
      'caption': caption,
    },
    {
      'name': "trackStartZ_wide",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-25,725],
      'var': "trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': False,
      'caption': caption,
    },
    {
      'name': "trackStartZ_wide_Logy",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-25,725],
      'var': "trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logy': True,
      'caption': caption,
    },
    {
      'name': "trackStartZ_beamMatched",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-5,25],
      'var': "trackStartZ",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logy': False,
      'caption': caption,
      'caption': "Truth Beam Matched, "+caption,
    },
    {
      'name': "trackStartZ_beamMatched_Logy",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-5,25],
      'var': "trackStartZ",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logy': True,
      'caption': "Truth Beam Matched, "+caption,
    },
  ]

  plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="CompareSCE_",nMax=NMAX)
