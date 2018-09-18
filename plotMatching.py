#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  c = root.TCanvas()
  f = root.TFile("PiAbsSelector.root")
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamline"),None,None,c,"Matching_deltaXYTPCBeamline_wide",captionArgs=["MCC10, 2GeV SCE"],rebin=[50,50])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamline"),None,None,c,"Matching_deltaXYTPCBeamline",captionArgs=["MCC10, 2GeV SCE"],xlims=[-50,50],ylims=[-50,50],rebin=[5,5])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamlineOnlyBeamPrimaries"),None,None,c,"Matching_deltaXYTPCBeamlineOnlyBeamPrimaries_wide",captionArgs=["MCC10, 2GeV SCE"],rebin=[10,10])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamlineOnlyBeamPrimaries"),None,None,c,"Matching_deltaXYTPCBeamlineOnlyBeamPrimaries",captionArgs=["MCC10, 2GeV SCE"],xlims=[-50,50],ylims=[-50,50],rebin=[5,5])

  ###########################################################################

  cuts = ""

  #cuts += "*( iBestMatch >= 0 && nMatchedTracks == 1)" # matching in analyzer

  # matching debug
  #cuts += "*(sqrt(pow(xWC-23.75,2)+pow(yWC-0.2,2)) < 11.93)" # wc track in flange
  #cuts += "*(trackXFront > -50. && trackXFront < -10. && trackYFront > 390. && trackYFront < 430.)" # TPC track in flange
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

  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    {
      #'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_5evts.root",
      'fn': "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root",
      'name': "protodune_beam_p2GeV_cosmics_3ms_sce_mcc10",
      'title': "MCC10, 2 GeV SCE",
      'caption': "MCC10, 2 GeV SCE",
      'color': root.kBlack,
      'isData': False,
    },
  ]


  histConfigs = [
    {
      'name': "trackYFrontVtrackXFront",
      'xtitle': "X of TPC Track Projected to Z=0 [cm]",
      'ytitle': "Y of TPC Track Projected to Z=0 [cm]",
      'binning': [30,-60,0,30,300,500],
      'var': "trackYFront:trackXFront",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackYFrontVtrackXFront_beamMatched",
      'xtitle': "X of TPC Track Projected to Z=0 [cm]",
      'ytitle': "Y of TPC Track Projected to Z=0 [cm]",
      'binning': [30,-60,0,30,300,500],
      'var': "trackYFront:trackXFront",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackYFrontVtrackXFront_wide",
      'xtitle': "X of TPC Track Projected to Z=0 [cm]",
      'ytitle': "Y of TPC Track Projected to Z=0 [cm]",
      'binning': [100,-400,400,100,0,700],
      'var': "trackYFront:trackXFront",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackYFrontVtrackXFront_wide_beamMatched",
      'xtitle': "X of TPC Track Projected to Z=0 [cm]",
      'ytitle': "Y of TPC Track Projected to Z=0 [cm]",
      'binning': [100,-400,400,100,0,700],
      'var': "trackYFront:trackXFront",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartZVtrackStartX",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Z [cm]",
      'binning': [60,-400,400,60,-10,700],
      'var': "trackStartZ:trackStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartX",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [60,-400,400,60,0,600],
      'var': "trackStartY:trackStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartZ",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [60,-10,700,60,0,600],
      'var': "trackStartY:trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartZVtrackStartX_front",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Z [cm]",
      'binning': [30,-400,400,30,-10,30],
      'var': "trackStartZ:trackStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartX_zLt20cm",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [30,-400,400,30,0,600],
      'var': "trackStartY:trackStartX",
      'cuts': weightStr+"*(trackStartZ < 20.)",
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartX_zLt2cm",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [30,-400,400,30,0,600],
      'var': "trackStartY:trackStartX",
      'cuts': weightStr+"*(trackStartZ < 2.)",
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartZ_front",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [30,-10,30,30,0,600],
      'var': "trackStartY:trackStartZ",
      'cuts': weightStr,
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartZVtrackStartX_front_beamMatched",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "TPC Track Start Z [cm]",
      'binning': [30,-400,400,30,-10,30],
      'var': "trackStartZ:trackStartX",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'cuts': weightStr+"*(trackTrueIsBeam)",
      #'normalize': True,
      'logz': False,
    },
    {
      'name': "trackStartYVtrackStartZ_front_beamMatched",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "TPC Track Start Y [cm]",
      'binning': [30,-10,30,30,0,600],
      'var': "trackStartY:trackStartZ",
      'cuts': weightStr+"*(trackTrueIsBeam && trackTrueMotherID==0)",
      #'cuts': weightStr+"*(trackTrueIsBeam)",
      #'normalize': True,
      'logz': False,
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_",nMax=NMAX)


  ############################################################
  #################### Compare selectons #####################
  ############################################################
  fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  caption = "MCC10, 2 GeV SCE"

  fileConfigs = [
    {
      'fn': fn,
      'title': "No Cuts",
      'caption': caption,
      'cuts': "",
    },
    {
      'fn': fn,
      'title': "Is Beam",
      'cuts': "*(trackTrueIsBeam)",
    },
    {
      'fn': fn,
      'title': "Is Beam & Primary",
      'cuts': "*(trackTrueIsBeam && trackTrueMotherID==0)",
    },
  ]
  for i in range(len(fileConfigs)):
    fileConfigs[i]['color'] = COLORLIST[i]

  histConfigs = [
    {
      'name': "trackMatchDeltaX",
      'xtitle': "TPC / WC Track #Delta x at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [40,-10,10],
      #'var': "trackMatchDeltaX[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaX",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
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
    },
    {
      'name': "trackMatchDeltaY",
      'xtitle': "TPC / WC Track #Delta y at TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [40,-10,10],
      #'var': "trackMatchDeltaY[iBestMatch]",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaY",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
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
    },
    {
      'name': "trackMatchDeltaAngle",
      'xtitle': "TPC / WC Track #Delta #alpha [deg]",
      'ytitle': "TPC Tracks / bin",
      #'binning': [90,0,180],
      'binning': [40,0,20],
      #'var': "trackMatchDeltaAngle[iBestMatch]*180/pi",
      #'cuts': "(iBestMatch >= 0)*"+weightStr,
      'var': "trackMatchDeltaAngle*180/pi",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
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
    },
    {
      'name': "trackXFront",
      'xtitle': "X of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,-50,0],
      'var': "trackXFront",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trackYFront",
      'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [100,340,500],
      'var': "trackYFront",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trackMatchLowestZ",
      'xtitle': "TPC Track Start Z [cm]",
      'ytitle': "TPC Tracks / bin",
      'binning': [50,-5,20],
      'var': "trackMatchLowestZ",
      'cuts': weightStrTrackMatch,
      #'normalize': True,
      'logy': logy,
    },
#    {
#      'name': "nTOFs",
#      'xtitle': "Number of TOF Objects",
#      'ytitle': "Events / bin",
#      'binning': [11,0,10],
#      'var': "nTOFs",
#      'cuts': weightStr,
#      #'normalize': True,
#      'logy': logy,
#    },
#    {
#      'name': "TOFs",
#      'xtitle': "TOF [ns]",
#      'ytitle': "TOFs / bin",
#      'binning': [100,0,100],
#      'var': "TOFs",
#      'cuts': weightStr,
#      #'normalize': True,
#      'logy': logy,
#    },
#    {
#      'name': "firstTOF",
#      'xtitle': "TOF [ns]",
#      'ytitle': "Events / bin",
#      'binning': [100,0,100],
#      'var': "firstTOF",
#      'cuts': weightStr,
#      #'normalize': True,
#      'logy': logy,
#    },
    {
      'name': "trackStartX",
      'xtitle': "TPC Track Start X [cm]",
      'ytitle': "Tracks / bin",
      'binning': [200,-400,400],
      'var': "trackStartX",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
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
    },
  ]

  plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="Matching_",nMax=NMAX)
