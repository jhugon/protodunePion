#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import multiprocessing
import copy

def doDataMCPlots(fileConfigs,catConfigs,weightStr,runSetName,NMAX):
  fileConfigs = copy.deepcopy(fileConfigs)
  catConfigs = copy.deepcopy(catConfigs)

  momentumBins = [160,0,8]
  #momentumBins = [50,0,2.5]
  #momentumBins = [40,0,2.]
  keBins = momentumBins
  keInteractBins = [160,0,8]
  #keInteractBins = [100,-2.5,2.5]

  c = root.TCanvas()

  histConfigs = [
    #{
    #  'name': "nGoodFEMBs_all",
    #  'xtitle': "N Good FEMBs for all APAs",
    #  'ytitle': "Events #times APAs / bin",
    #  'binning': [21,-0.5,20.5],
    #  'var': "nGoodFEMBs",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "nGoodFEMBs_beamSide",
    #  'xtitle': "N Good FEMBs for Beam Side",
    #  'ytitle': "Events #times APAs / bin",
    #  'binning': [21,-0.5,20.5],
    #  'var': "nGoodFEMBs",
    #  'cuts': weightStr+"*($Iteration == 0 || $Iteration == 2 || $Iteration == 4 )",
    #  #'normalize': True,
    #  'logy': logy,
    #},
    {
      'name': "TOF",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,0,300],
      'var': "TOF",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "xWC",
      'xtitle': "X Position of BI track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [125,-75,50],
      'var': "xWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "yWC",
      'xtitle': "Y Position of BI track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [75,375,450],
      'var': "yWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "xWCOld",
      'xtitle': "X Position of Old BI track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [125,-75,50],
      'var': "beamTrackXFrontTPCOld[0]",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "yWCOld",
      'xtitle': "Y Position of Old BI track projection to TPC [cm]",
      'ytitle': "Events / bin",
      'binning': [75,375,450],
      'var': "beamTrackYFrontTPCOld[0]",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "pWC",
      'xtitle': "Momentum from BI [GeV/c]",
      'ytitle': "Events / bin",
      'binning': momentumBins,
      'var': "pWC/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "kinWC",
      'xtitle': "KE from BI (Muon) [GeV]",
      'ytitle': "Events / bin",
      'binning': keBins,
      'var': "kinWC/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "kinWCProton",
      'xtitle': "KE from BI (Proton) [GeV]",
      'ytitle': "Events / bin",
      'binning': keBins,
      'var': "kinWCProton/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimEnergySumCSDAMu",
      'xtitle': "Primary KE from CSDA (Muon) [GeV]",
      'ytitle': "Events / bin",
      'binning': keBins,
      'var': "PFBeamPrimEnergySumCSDAMu/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimEnergySumCSDAProton",
      'xtitle': "Primary KE from CSDA (Proton) [GeV]",
      'ytitle': "Events / bin",
      'binning': keBins,
      'var': "PFBeamPrimEnergySumCSDAProton/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "zWireEnergySum_ajib",
      'xtitle': "Primary Calo Energy Sum [GeV]",
      'ytitle': "Events / bin",
      'binning': keBins,
      'var': "zWireEnergySum_ajib/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimGoodMatch",
      'xtitle': "Primary PF Track Matched to True Primary Particle",
      'ytitle': "Events / bin",
      'binning': [3,0,3],
      'var': "(PFBeamPrimTrueTrackID == truePrimaryTrackID) + 2*(PFBeamPrimTrueMotherTrackID == truePrimaryTrackID)",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'binLabels': ["Bad Match","Good Match"," Match to Mother"]
    },
    #{
    #  'name': "PFBeamPrimdEdxAverageLast3Hits",
    #  'xtitle': "Primary PF Track <dE/dx>_{Last 3 Hits} [MeV/cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [100,0,30],
    #  'var': "PFBeamPrimdEdxAverageLast3Hits",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "PFBeamPrimdEdxAverageLast5Hits",
    #  'xtitle': "Primary PF Track <dE/dx>_{Last 5 Hits} [MeV/cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [100,0,30],
    #  'var': "PFBeamPrimdEdxAverageLast5Hits",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    #{
    #  'name': "PFBeamPrimdEdxAverageLast7Hits",
    #  'xtitle': "Primary PF Track <dE/dx>_{Last 7 Hits} [MeV/cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [100,0,30],
    #  'var': "PFBeamPrimdEdxAverageLast7Hits",
    #  'cuts': weightStr,
    #  #'normalize': True,
    #  'logy': logy,
    #},
    {
      'name': "PFNBeamSlices",
      'xtitle': "Number of Pandora Beam Slices",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "PFNBeamSlices",
      'cuts': weightStr,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimNDaughters",
      'xtitle': "Number of Pandora Beam Secondaries",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "PFBeamPrimNDaughters",
      'cuts': weightStr,
    },
    #{
    #  'name': "PFBeamPrimIsTracklike",
    #  'xtitle': "Pandora Beam Primary is Tracklike",
    #  'ytitle': "Events / bin",
    #  'binning': [2,-0.5,1.5],
    #  'var': "PFBeamPrimIsTracklike",
    #  'cuts': weightStr,
    #  'printIntegral': True,
    #},
    {
      'name': "PFBeamPrimStartX",
      'xtitle': "Pandora Beam Primary Start X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-400,400],
      'var': "PFBeamPrimStartX",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimStartY",
      'xtitle': "Pandora Beam Primary Start Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-5,650],
      'var': "PFBeamPrimStartY",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimStartZ",
      'xtitle': "Pandora Beam Primary Start Z [cm]",
      'ytitle': "Events / bin",
      'binning': [95*2,-5,100],
      'var': "PFBeamPrimStartZ",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimStartZ_corr",
      'xtitle': "Pandora Beam Primary Start Z [cm]",
      'ytitle': "Events / bin",
      'binning': [250,-25,100],
      'var': "PFBeamPrimStartZ_corr",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimStartZ_corrFLF",
      'xtitle': "Pandora Beam Primary Start Z [cm]",
      'ytitle': "Events / bin",
      'binning': [250,-25,100],
      'var': "PFBeamPrimStartZ_corrFLF",
      'cuts': weightStr,
    },
    {
      'name': "zWireZFirstHitWire",
      'xtitle': "First Hit Wire Z [cm]",
      'ytitle': "Events / bin",
      'binning': [250,-25,100],
      'var': "zWireZ[zWireFirstHitWire]",
      'cuts': weightStr+"*(zWireFirstHitWire >= 0)",
    },
    {
      'name': "zWireZFirstHitWire_corr",
      'xtitle': "First Hit Wire Z (SCE Corrected) [cm]",
      'ytitle': "Events / bin",
      'binning': [250,-25,100],
      'var': "zWireZ_corr[zWireFirstHitWire]",
      'cuts': weightStr+"*(zWireFirstHitWire >= 0)",
    },
    {
      'name': "zWireZFirstHitWire_corrFLF",
      'xtitle': "First Hit Wire Z (SCE Corrected FLF) [cm]",
      'ytitle': "Events / bin",
      'binning': [250,-25,100],
      'var': "zWireZ_corrFLF[zWireFirstHitWire]",
      'cuts': weightStr+"*(zWireFirstHitWire >= 0)",
    },
    {
      'name': "PFBeamPrimEndX",
      'xtitle': "Pandora Beam Primary End X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-400,400],
      'var': "PFBeamPrimEndX",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndX_zoom0",
      'xtitle': "Pandora Beam Primary End X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-100,100],
      'var': "PFBeamPrimEndX",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndY",
      'xtitle': "Pandora Beam Primary End Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-5,650],
      'var': "PFBeamPrimEndY",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [141,-5,700],
      'var': "PFBeamPrimEndZ",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ_zoom225",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [50,200,250],
      'var': "PFBeamPrimEndZ",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ_zoom450",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [50,425,575],
      'var': "PFBeamPrimEndZ",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ_zoomBack",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [150,600,750],
      'var': "PFBeamPrimEndZ",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ_corr_zoomBack",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [150,600,750],
      'var': "PFBeamPrimEndZ_corr",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndZ_corrFLF_zoomBack",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [150,600,750],
      'var': "PFBeamPrimEndZ_corrFLF",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimTrkLen",
      'xtitle': "Pandora Beam Primary Track Length [cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,1000],
      'var': "PFBeamPrimTrkLen",
      'cuts': weightStr,
    },
    {
      'name': "deltaPFBeamPrimEndZTrueZ",
      'xtitle': "Reco Interaction Z-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-100,100],
      'var': "PFBeamPrimEndZ-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "deltaPFBeamPrimEndZTrueZ_wide",
      'xtitle': "Reco Interaction Z-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-500,500],
      'var': "PFBeamPrimEndZ-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "deltaPFBeamPrimEndZ_corrTrueZ",
      'xtitle': "Reco Interaction Z (SCE Corr.)-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-100,100],
      'var': "PFBeamPrimEndZ_corr-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "deltaPFBeamPrimEndZ_corrTrueZ_wide",
      'xtitle': "Reco Interaction Z (SCE Corr.)-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-500,500],
      'var': "PFBeamPrimEndZ_corr-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "deltaPFBeamPrimEndZ_corrFLFTrueZ",
      'xtitle': "Reco Interaction Z (FLF Corr.)-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-100,100],
      'var': "PFBeamPrimEndZ_corrFLF-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "deltaPFBeamPrimEndZ_corrFLFTrueZ_wide",
      'xtitle': "Reco Interaction Z (FLF Corr.)-True Interaction Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-500,500],
      'var': "PFBeamPrimEndZ_corrFLF-trueEndZ",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,100],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd_wide",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd_Zcorr",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,100],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ_corr-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd_Zcorr_wide",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ_corr-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd_ZcorrFLF",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,100],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ_corrFLF-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    {
      'name': "PFBeamPrimEndDistToTrueEnd_ZcorrFLF_wide",
      'xtitle': "Reco Distance to True Interaction Point [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ_corrFLF-trueEndZ,2))",
      'cuts': weightStr+"*isMC",
    },
    #{
    #  'name': "PFBeamPrimShwrLen",
    #  'xtitle': "Pandora Beam Primary Shower Length [cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [200,0,1000],
    #  'var': "PFBeamPrimShwrLen",
    #  'cuts': weightStr,
    #},
    #{
    #  'name': "PFBeamPrimShwrOpenAngle",
    #  'xtitle': "Pandora Beam Primary Shower Open Angle [deg]",
    #  'ytitle': "Events / bin",
    #  'binning': [30,0,90],
    #  'var': "PFBeamPrimShwrOpenAngle*180./pi",
    #  'cuts': weightStr,
    #},
    {
      'name': "PFBeamPrimStartTheta",
      'xtitle': "Pandora Beam Primary Start #theta [deg]",
      'ytitle': "Events / bin",
      'binning': [60,0,180],
      'var': "PFBeamPrimStartTheta*180./pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimStartPhi",
      'xtitle': "Pandora Beam Primary Start #phi [deg]",
      'ytitle': "Events / bin",
      'binning': [60,-180,180],
      'var': "PFBeamPrimStartPhi*180./pi",
      'cuts': weightStr,
    },
    {
      'name': "DeltaXPFBeamPrimStartBI",
      'xtitle': "Pandora Beam Primary Start - Beam Track X [cm]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartX - beamTrackXFrontTPC",
      'cuts': weightStr,
    },
    {
      'name': "DeltaYPFBeamPrimStartBI",
      'xtitle': "Pandora Beam Primary Start - Beam Track Y [cm]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "PFBeamPrimStartY - beamTrackYFrontTPC",
      'cuts': weightStr,
    },
    {
      'name': "DeltaXPFBeamPrimStartBIOld",
      'xtitle': "#Delta X PF Track Start & Old BI Track [cm]",
      'ytitle': "Events / bin",
      'binning': [150,-25,50],
      'var': "PFBeamPrimStartX - (beamTrackXFrontTPCOld[0]*(!isMC)+isMC*xWC)",
      'cuts': weightStr,
    },
    {
      'name': "DeltaYPFBeamPrimStartBIOld",
      'xtitle': "#Delta Y PF Track Start & Old BI Track [cm]",
      'ytitle': "Events / bin",
      'binning': [150,-25,50],
      'var': "PFBeamPrimStartY - (beamTrackYFrontTPCOld[0]*(!isMC)+isMC*yWC)",
      'cuts': weightStr,
    },
    {
      'name': "DeltaXBINewOld",
      'xtitle': "#Delta X New BI Track & Old BI Track [cm]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "xWC - beamTrackXFrontTPCOld[0]",
      'cuts': weightStr,
    },
    {
      'name': "DeltaYBINewOld",
      'xtitle': "#Delta Y New BI Track & Old BI Track [cm]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "yWC - beamTrackYFrontTPCOld[0]",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimAngleToBeamTrk",
      'xtitle': "Angle Between BI & Primary PF Track Start [Deg]",
      'ytitle': "Events / bin",
      'binning': [80,0,40],
      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimAngleToBeamTrk_wide",
      'xtitle': "Angle Between BI & Primary PF Track Start [Deg]",
      'ytitle': "Events / bin",
      'binning': [180,0,180],
      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimCosAngleToBeamTrk",
      'xtitle': "|cos(#theta)| of BI & Primary PF Track Start",
      'ytitle': "Events / bin",
      'binning': [100,0,1],
      'var': "fabs(cos(PFBeamPrimAngleToBeamTrk))",
      'cuts': weightStr+"*(PFBeamPrimAngleToBeamTrk > -100)",
    },
    {
      'name': "PFBeamPrimEndAngleToBeamTrk",
      'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
      'ytitle': "Events / bin",
      'binning': [80,0,40],
      'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndAngleToBeamTrk_wide",
      'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
      'ytitle': "Events / bin",
      'binning': [180,0,180],
      'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimEndCosAngleToBeamTrk",
      'xtitle': "|cos(#theta)| of BI & Primary PF Track End",
      'ytitle': "Events / bin",
      'binning': [100,0,1],
      'var': "fabs(cos(PFBeamPrimEndAngleToBeamTrk))",
      'cuts': weightStr+"*(PFBeamPrimEndAngleToBeamTrk > -100)",
    },
    {
      'name': "PFBeamPrimTrkStartEndDirAngle",
      'xtitle': "Angle Between PF Track Start & End [Deg]",
      'ytitle': "Events / bin",
      'binning': [80,0,40],
      'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimTrkStartEndDirAngle_wide",
      'xtitle': "Angle Between PF Track Start & End [Deg]",
      'ytitle': "Events / bin",
      'binning': [180,0,180],
      'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimTrkStartEndDirCosAngle",
      'xtitle': "|cos(#theta)| Primary PF Track Start & End",
      'ytitle': "Events / bin",
      'binning': [100,0,1],
      'var': "fabs(cos(PFBeamPrimTrkStartEndDirAngle))",
      'cuts': weightStr+"*(PFBeamPrimTrkStartEndDirAngle > -100)",
    },
    ######################################
    {
      'name': "PFBeamPrimStartThetaXZ",
      'xtitle': "TPC Track Start #theta_{xz} [deg]",
      'ytitle': "Events / bin",
      'binning': [50,-25,0],
      #'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
    },
    {
      'name': "PFBeamPrimStartThetaYZ",
      'xtitle': "TPC Track Start #theta_{yz} [deg]",
      'ytitle': "Events / bin",
      'binning': [80,-40,0],
      #'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100)",
    },
    {
      'name': "PFBeamPrimEndThetaXZ",
      'xtitle': "TPC Track End #theta_{xz} [deg]",
      'ytitle': "Events / bin",
      'binning': [50,-25,0],
      #'var': "atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "PFBeamPrimEndThetaYZ",
      'xtitle': "TPC Track End #theta_{yz} [deg]",
      'ytitle': "Events / bin",
      'binning': [80,-40,0],
      #'var': "atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi",
      'var': "atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "thetaWCXZ",
      'xtitle': "BI Track #theta_{xz} [deg]",
      'ytitle': "Events / bin",
      'binning': [50,-25,0],
      #'var': "atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi",
      'var': "atan(tan(thetaWC)*cos(phiWC))*180/pi",
      'cuts': weightStr+"*(thetaWC > -100)",
    },
    {
      'name': "thetaWCYZ",
      'xtitle': "BI Track #theta_{yz} [deg]",
      'ytitle': "Events / bin",
      'binning': [80,-40,0],
      #'var': "atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi",
      'var': "atan(tan(thetaWC)*sin(phiWC))*180/pi",
      'cuts': weightStr+"*(thetaWC > -100)",
      'printIntegral': True,
    },
    ######################################
    {
      'name': "PFBeamPrimAngleStartEndXZ",
      'xtitle': "TPC Track Start-End Angle in XZ-Plane [deg]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi-atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartEndYZ",
      'xtitle': "TPC Track Start-End Angle in YZ-Plane [deg]",
      'ytitle': "Events / bin",
      'binning': [50,-50,50],
      'var': "atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi-atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && PFBeamPrimEndTheta > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartBIXZ",
      'xtitle': "TPC Track Start-BI Angle in XZ-Plane [deg]",
      'ytitle': "Events / bin",
      'binning': [30,-30,30],
      'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && thetaWC > -100)",
    },
    {
      'name': "PFBeamPrimAngleStartBIYZ",
      'xtitle': "TPC Track Start-BI Angle in YZ-Plane [deg]",
      'ytitle': "Events / bin",
      'binning': [30,-30,30],
      'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi-atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi",
      'cuts': weightStr+"*(PFBeamPrimStartTheta > -100 && thetaWC > -100)",
    },
    ######################################
    {
      'name': "PFBeamPrimBeamCosmicScore",
      'xtitle': "Pandora Beam / Cosmic BDT Score",
      'ytitle': "Events / bin",
      'binning': [100,-0.5,0.5],
      'var': "PFBeamPrimBeamCosmicScore",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimKinInteract",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "PFBeamPrimKinInteract/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKinInteract_lt2p5",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [50,-2.5,2.5],
      'var': "PFBeamPrimKinInteract/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKinInteract_corr",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "PFBeamPrimKinInteract_corr/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKinInteract_corr_lt2p5",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [50,-2.5,2.5],
      'var': "PFBeamPrimKinInteract_corr/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKinInteractGeq0",
      'xtitle': "Primary PF Track End Kinetic Energy #geq 0",
      'ytitle': "Events / bin",
      'binning': [2,-0.5,1.5],
      'var': "PFBeamPrimKinInteract >= 0",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteract",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKin[zWireLastHitWire]/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractProton",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKinProton[zWireLastHitWire]/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteract_corr",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKin_corr[zWireLastHitWire]/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractProton_corr",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKinProton_corr[zWireLastHitWire]/1000.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteract_ajib",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKin_ajib[zWireLastHitWire]/1000.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractProton_ajib",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "zWirePartKinProton_ajib[zWireLastHitWire]/1000.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractLt2p5",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [50,-2.5,2.5],
      'var': "zWirePartKin[zWireLastHitWire]/1000.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractLt2p5_corr",
      'xtitle': "Primary PF Track End Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [50,-2.5,2.5],
      'var': "zWirePartKin_corr[zWireLastHitWire]/1000.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "zWirePartKinInteractGeq0",
      'xtitle': "Primary PF Track End Kinetic Energy #geq 0",
      'ytitle': "Events / bin",
      'binning': [2,-0.5,1.5],
      'var': "zWirePartKin[zWireLastHitWire]/1000. >= 0.",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinInteractGeq0_corr",
      'xtitle': "Primary PF Track End Kinetic Energy #geq 0",
      'ytitle': "Events / bin",
      'binning': [2,-0.5,1.5],
      'var': "zWirePartKin_corr[zWireLastHitWire] >= 0",
      'cuts': "zWireLastHitWire >= 0 && "+weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueSecondToEndKin",
      'xtitle': "True End KE [GeV]",
      'ytitle': "Events / bin",
      'binning': keInteractBins,
      'var': "trueSecondToEndKin/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "deltazWireTruePartKintrueSecondToEndKin",
      'xtitle': "zWireTruePartKin-True End KE [GeV]",
      'ytitle': "Events / bin",
      'binning': [60,-3.0,3.0],
      'var': "zWireTruePartKin[zWireLastHitWire]/1000.-trueSecondToEndKin/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "deltazWireTrueTrajKintrueSecondToEndKin",
      'xtitle': "zWireTrueTrajKin-True End KE [GeV]",
      'ytitle': "Events / bin",
      'binning': [60,-3.0,3.0],
      'var': "zWireTrueTrajKin[zWireLastHitWire]/1000.-trueSecondToEndKin/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "deltazWirePartKintrueSecondToEndKin",
      'xtitle': "zWirePartKin-True End KE [GeV]",
      'ytitle': "Events / bin",
      'binning': [60,-3.0,3.0],
      'var': "zWirePartKin[zWireLastHitWire]/1000.-trueSecondToEndKin/1000.",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "RatioPFBeamPrimEnergySumCSDAAndKinWCMu",
      'xtitle': "KE^{range} / KE^{beam} (Assuming Muons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "PFBeamPrimEnergySumCSDAMu/kinWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "RatioPFBeamPrimEnergySumCSDAAndKinWCProton",
      'xtitle': "KE^{range} / KE^{beam} (Assuming Protons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "PFBeamPrimEnergySumCSDAProton/kinWCProton",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "RatiozWireEnergySum_ajibAndKinWCMu",
      'xtitle': "KE^{calo} / KE^{beam} (Assuming Muons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "zWireEnergySum_ajib/kinWC",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "RatiozWireEnergySumAndKinWCProton",
      'xtitle': "KE^{calo} / KE^{beam} (Assuming Protons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "zWireEnergySum/kinWCProton",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      #'printIntegral': True,
    },
    {
      'name': "RatiozWireEnergySum_ajibAndKinWCProton",
      'xtitle': "KE^{calo} / KE^{beam} (Assuming Protons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "zWireEnergySum_ajib/kinWCProton",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      #'fitFunc': "gaus",
      #'fitFunc': "[0]*exp(-0.5*pow((x-[1])/[2],2))",
      #'fitDefParams': [250,0.9,0.005],
      #'fitOnlyFWHM': 0.4,
      'printIntegral': True,
    },
    {
      'name': "RatioPFBeamPrimEnergySumCSDAMuAndzWireEnergySum_ajib",
      'xtitle': "KE^{range} / KE^{calo} (Assuming Muons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "PFBeamPrimEnergySumCSDAMu/zWireEnergySum_ajib",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "RatioPFBeamPrimEnergySumCSDAProtonAndzWireEnergySum_ajib",
      'xtitle': "KE^{range} / KE^{calo} (Assuming Protons)",
      'ytitle': "Events / bin",
      'binning': [100,0,2],
      'var': "PFBeamPrimEnergySumCSDAProton/zWireEnergySum_ajib",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "trueCategory",
      'xtitle': "True Category",
      'ytitle': "Events / bin",
      'binning': [18,0,18],
      'var': "trueCategory",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "lastHitWire",
      'xtitle': "Last Hit Z Wire Number",
      'ytitle': "Events / bin",
      'binning': [24*3,0,480*3],
      'var': "zWireLastHitWire",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "lastHitWireMod480",
      'xtitle': "Last Hit Z Wire Number Mod 480",
      'ytitle': "Events / bin",
      'binning': [96,0,480],
      'var': "zWireLastHitWire % 480",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "lastHitWireMod480Minus480",
      'xtitle': "Last Hit Z Wire Number Mod 480 - 480",
      'ytitle': "Events / bin",
      'binning': [30,-15,15],
      'var': "((zWireLastHitWire % 480) - 480)*((zWireLastHitWire % 480) >= 240) + ((zWireLastHitWire % 480))*((zWireLastHitWire % 480) < 240)",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "lastHitWireMod480Minus480_wide",
      'xtitle': "Last Hit Z Wire Number Mod 480 - 480",
      'ytitle': "Events / bin",
      'binning': [96,-240,240],
      'var': "((zWireLastHitWire % 480) - 480)*((zWireLastHitWire % 480) >= 240) + ((zWireLastHitWire % 480))*((zWireLastHitWire % 480) < 240)",
      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
      #'normalize': True,
      'logy': logy,
    },
    ##############################################
    ################  Per Hit  ###################
    ##############################################
    {
      'name': "PFBeamPrimdEdxs",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [100,0,20],
      'var': "PFBeamPrimdEdxs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxs_zoom",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [200,0,10],
      'var': "PFBeamPrimdEdxs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxs_corr_zoom",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [200,0,10],
      'var': "PFBeamPrimdEdxs_corr",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxs_wide",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [250,0,500],
      'var': "PFBeamPrimdEdxs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxPitches",
      'xtitle': "Primary PF Track Hit dE/dx #times Pitch [MeV]",
      'ytitle': "Hit / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxs*PFBeamPrimPitches",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxPitches_zoom",
      'xtitle': "Primary PF Track Hit dE/dx #times Pitch [MeV]",
      'ytitle': "Hit / bin",
      'binning': [200,0,10],
      'var': "PFBeamPrimdEdxs*PFBeamPrimPitches",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxPitches_wide",
      'xtitle': "Primary PF Track Hit dE/dx #times Pitch [MeV]",
      'ytitle': "Hit / bin",
      'binning': [250,0,500],
      'var': "PFBeamPrimdEdxs*PFBeamPrimPitches",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimResRanges",
      'xtitle': "Primary PF Track Hit Residual Range [cm]",
      'ytitle': "Hit / bin",
      'binning': [350,0,700],
      'var': "PFBeamPrimResRanges",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimPitches",
      'xtitle': "Primary PF Track Hit Pitch [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,0,10],
      'var': "PFBeamPrimPitches",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimPitches_zoom",
      'xtitle': "Primary PF Track Hit Pitch [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,0,1],
      'var': "PFBeamPrimPitches",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKins_lt2p5",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hit / bin",
      'binning': [50,-2.5,2.5],
      'var': "PFBeamPrimKins/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKins",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hit / bin",
      'binning': keInteractBins,
      'var': "PFBeamPrimKins/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimKins_corr",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hit / bin",
      'binning': keInteractBins,
      'var': "PFBeamPrimKins_corr/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimXs",
      'xtitle': "Primary PF Track Hit X-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,-100,100],
      'var': "PFBeamPrimXs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimYs",
      'xtitle': "Primary PF Track Hit Y-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,300,600],
      'var': "PFBeamPrimYs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimZs",
      'xtitle': "Primary PF Track Hit Z-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [700,0,700],
      'var': "PFBeamPrimZs",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimXsKEProtonLt0",
      'xtitle': "Primary PF Track Hit X-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,-100,100],
      'var': "PFBeamPrimXs",
      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimYsKEProtonLt0",
      'xtitle': "Primary PF Track Hit Y-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,300,600],
      'var': "PFBeamPrimYs",
      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimZsKEProtonLt0",
      'xtitle': "Primary PF Track Hit Z-positions [cm]",
      'ytitle': "Hit / bin",
      'binning': [700,0,700],
      'var': "PFBeamPrimZs",
      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWiredEdx_zoom",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [200,0,10],
      'var': "zWiredEdx",
      'cuts': weightStr+"*(zWireZ<600.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWiredEdx_ajib",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [300,0,30],
      'var': "zWiredEdx_ajib",
      'cuts': weightStr+"*(zWireZ<600.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWiredEdx_ajib_zoom",
      'xtitle': "Primary PF Track Hit dE/dx [MeV/cm]",
      'ytitle': "Hit / bin",
      'binning': [200,0,10],
      'var': "zWiredEdx_ajib",
      'cuts': weightStr+"*(zWireZ<600.)",
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePitch",
      'xtitle': "Primary PF Track Hit Pitch [cm]",
      'ytitle': "Hit / bin",
      'binning': [100,0,10],
      'var': "zWirePitch",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePitch_zoom",
      'xtitle': "Primary PF Track Hit Pitch [cm]",
      'ytitle': "Hit / bin",
      'binning': [50,0.4,0.65],
      'var': "zWirePitch",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKin",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hits / bin",
      'binning': keInteractBins,
      'var': "zWirePartKin/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKin_corr",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hits / bin",
      'binning': keInteractBins,
      'var': "zWirePartKin_corr/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinLt2p5",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hits / bin",
      'binning': [50,-2.5,2.5],
      'var': "zWirePartKin/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "zWirePartKinLt2p5_corr",
      'xtitle': "Primary PF Track Hit Kinetic Energy [GeV]",
      'ytitle': "Hits / bin",
      'binning': [50,-2.5,2.5],
      'var': "zWirePartKin_corr/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
  ]

  for fc in fileConfigs:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]

  for i in reversed(range(len(histConfigs))):
    #if (not ("XZ" in histConfigs[i]['name'])) and (not ("YZ" in histConfigs[i]['name'])) \
    #    and (not ("DeltaX" in histConfigs[i]['name'])) and (not ("DeltaY" in histConfigs[i]['name'])) \
    #    and histConfigs[i]['name'] != "PFBeamPrimStartX" \
    #    and histConfigs[i]['name'] != "PFBeamPrimStartY" \
    #    and (not ("xWC" in histConfigs[i]['name'])) and (not ("yWC" in histConfigs[i]['name'])):
    #if (not ("Angle" in histConfigs[i]['name'])):
    #if histConfigs[i]['name'] != "PFNBeamSlices":
    #if (histConfigs[i]['name'] != "zWirePitch") and (histConfigs[i]['name'] != "zWirePitch_zoom") and (histConfigs[i]['name'] != "zWiredEdx_zoom"):
    #if (histConfigs[i]['name'] != "zWirePitch_zoom"):
    #if histConfigs[i]['name'] != "pWC":
    #if histConfigs[i]['name'] != "zWirePartKinInteractProton":
    #if histConfigs[i]['name'] != "zWirePartKinInteractProton_corr":
    #if histConfigs[i]['name'] != "RatiozWireEnergySum_ajibAndKinWCProton":
    if (not ("Ratio" in histConfigs[i]['name'])) \
        and (histConfigs[i]['name'] != "pWC") \
        and (not ("kinWC" in histConfigs[i]['name'])) \
        and (not ("EnergySum" in histConfigs[i]['name'])) \
        and (not ("AngleToBeamTrk" in histConfigs[i]['name'])) \
        and (histConfigs[i]['name'] != "PFBeamPrimTrkLen") \
        and histConfigs[i]['name'] != "zWiredEdx_ajib" \
        and histConfigs[i]['name'] != "zWiredEdx" \
        and histConfigs[i]['name'] != "zWiredEdx_ajib_zoom" \
        and histConfigs[i]['name'] != "zWiredEdx_zoom" \
        and histConfigs[i]['name'] != "zWirePartKinInteract_ajib" \
        and histConfigs[i]['name'] != "zWirePartKinInteract" \
        and histConfigs[i]['name'] != "zWirePartKin_ajib" \
        and histConfigs[i]['name'] != "zWirePartKin":
        #and histConfigs[i]['name'] != "zWirePartKinInteract"
        #and histConfigs[i]['name'] != "zWirePartKinInteract_corr"
        #and (histConfigs[i]['name'] != "PFBeamPrimXs") \
        #and (histConfigs[i]['name'] != "PFBeamPrimYs") \
        #and (histConfigs[i]['name'] != "PFBeamPrimZs") \
        #and (histConfigs[i]['name'] != "PFBeamPrimXsKEProtonLt0") \
        #and (histConfigs[i]['name'] != "PFBeamPrimYsKEProtonLt0") \
        #and (histConfigs[i]['name'] != "PFBeamPrimZsKEProtonLt0"):
    #if (not ("lastHitWire" in histConfigs[i]['name'])):
    #if (not ("zWirePartKin" in histConfigs[i]['name'])) or histConfigs[i]["name"] == "zWirePartKin":
    #if not ("PFBeamPrimKinInteract" in histConfigs[i]['name']) and not ("zWirePartKin" in histConfigs[i]['name']):
    #if (not ("Ratio" in histConfigs[i]['name'])) and histConfigs[i]['name'] != "pWC":
    #if histConfigs[i]['name'] != "kinWCProton":
      histConfigs.pop(i)

  if True:
    #plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",outSuffix="_"+runSetName,nMax=NMAX)
    fileConfigMCs = copy.deepcopy(fileConfigs)
    fileConfigDatas = []
    for histConfig in histConfigs:
      histConfig['logy'] = False
      #histConfig['normalize'] = True
    for i in reversed(range(len(fileConfigMCs))):
      if 'isData' in fileConfigMCs[i] and fileConfigMCs[i]['isData']:
        fileConfigDatas.append(fileConfigMCs.pop(i))
    #dataMCStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",outSuffix="_"+runSetName,nMax=NMAX)
    dataMCCategoryStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="DataMC_",outSuffix="_"+runSetName,nMax=NMAX,
                  catConfigs=catConfigs
               )
    for histConfig in histConfigs:
      histConfig['logy'] = True
      histConfig['normalize'] = False
    dataMCCategoryStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="DataMC_",outSuffix="_logy_"+runSetName,nMax=NMAX,
                  catConfigs=catConfigs
               )

  #######################################
  ############ 2D Plots #################
  #######################################

  histConfigs = [
#    {
#      'name': "PFBeamPrimdEdxVRange",
#      'xtitle': "Primary Track Hit Residual Range [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [100,0,50,100,0,50],
#      'var': "PFBeamPrimdEdxs:PFBeamPrimResRanges",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimdEdxVRange_wide",
#      'xtitle': "Primary Track Hit Residual Range [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [350,0,700,100,0,50],
#      'var': "PFBeamPrimdEdxs:PFBeamPrimResRanges",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimdEdx_corrVRange",
#      'xtitle': "Primary Track Hit Residual Range [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [200,0,50,100,0,50],
#      'var': "PFBeamPrimdEdxs_corr:PFBeamPrimResRanges",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimdEdx_corrVRange_goodZWire",
#      'xtitle': "Primary Track Hit Residual Range [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [200,0,50,100,0,50],
#      'var': "PFBeamPrimdEdxs_corr:PFBeamPrimResRanges",
#      'cuts': weightStr+"*(PFBeamPrimZWires)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimStartThetaVPhi",
#      'xtitle': "PF Primary Track Start #phi [deg]",
#      'ytitle': "PF Primary Track Start #theta [deg]",
#      'binning': [90,-180,180,90,0,180],
#      'var': "PFBeamPrimStartTheta*180/pi:PFBeamPrimStartPhi*180/pi",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimStartThetaVPhi_IsTruePrimary_wide",
#      'xtitle': "PF Primary Track Start #phi [deg]",
#      'ytitle': "PF Primary Track Start #theta [deg]",
#      'binning': [90,-180,180,90,0,180],
#      'var': "PFBeamPrimStartTheta*180/pi:PFBeamPrimStartPhi*180/pi",
#      'cuts': weightStr+"*(abs(PFBeamPrimTrueTrackID) == trackTrueID)",
#      'preliminaryString': "Matched to Truth"
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "trueStartThetaVPhi_wide",
#      'xtitle': "True Primary Start #phi [deg]",
#      'ytitle': "True Primary Start #theta [deg]",
#      'binning': [90,-180,180,90,0,180],
#      'var': "trueStartTheta*180/pi:trueStartPhi*180/pi",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "nGoodFEMBsVAPA_wide",
#      'xtitle': "APA Number",
#      'ytitle': "N Good FEMBs",
#      'binning': [6,-0.5,5.5,21,-0.5,20.5],
#      'var': "nGoodFEMBs:Iteration$",
#      'cuts': "1",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWiredEdxVzToEnd",
#      'xtitle': "Primary Track Hit Residual Z [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [280,-20,50,100,0,50],
#      'var': "zWiredEdx:zWireZ[zWireLastHitWire]-zWireZ",
#      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWiredEdx_corrVzToEnd",
#      'xtitle': "Primary Track Hit Residual Z [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [280,-20,50,100,0,50],
#      'var': "zWiredEdx_corr:zWireZ[zWireLastHitWire]-zWireZ",
#      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWiredEdx_corrVzToEnd_corr",
#      'xtitle': "Primary Track Hit Residual Z [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [280,-20,50,100,0,50],
#      'var': "zWiredEdx_corr:zWireZ_corr[zWireLastHitWire]-zWireZ_corr",
#      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWiredEdx_corrVzToEnd_corrFLF",
#      'xtitle': "Primary Track Hit Residual Z [cm]",
#      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
#      'binning': [280,-20,50,100,0,50],
#      'var': "zWiredEdx_corr:zWireZ_corrFLF[zWireLastHitWire]-zWireZ_corrFLF",
#      'cuts': weightStr+"*(zWireLastHitWire >= 0)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWirePartKinVzWireWireZ",
#      'xtitle': "Reco Hit Position [cm]",
#      'ytitle': "Reco Hit Kinetric Energy [GeV]",
#      'binning': [72,-10,710,100,-10,10],
#      'var': "zWirePartKin*1e-3:zWireWireZ",
#      'cuts': "zWireFirstHitWire>=0 && "+weightStr+"*(zWirePartKin[zWireLastHitWire]>0)",
#      #'normalize': True,
#      'logz': True,
#    },
#    {
#      'name': "zWirePartKinInteractVzWireWireZ",
#      'xtitle': "Reco Interaction Position [cm]",
#      'ytitle': "Reco Interaction Kinetric Energy [GeV]",
#      'binning': [72,-10,710,100,-10,10],
#      'var': "zWirePartKin[zWireLastHitWire]*1e-3:zWireWireZ[zWireLastHitWire]",
#      'cuts': "zWireLastHitWire>=0 && zWireFirstHitWire>=0 && "+weightStr+"*(zWirePartKin[zWireLastHitWire]>0)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "zWireZVzWireTrueZ",
#      'xtitle': "Hit True Z [cm]",
#      'ytitle': "Hit Z [cm]",
#      'binning': [100,-20,50,100,-20,50],
#      'var': "zWireZ:zWireTrueZ",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "pWCCSDARangeMuVpWC",
#      'xtitle': "Beam Instrumentation Momentum [GeV/c]",
#      'ytitle': "CSDA Muon Expected Range [cm]",
#      'binning': [500,0,3,500,0,1000],
#      'var': "pWCCSDARangeMu:pWC/1000.",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "pWCCSDARangeProtonVpWC",
#      'xtitle': "Beam Instrumentation Momentum [GeV/c]",
#      'ytitle': "CSDA Proton Expected Range [cm]",
#      'binning': [500,0,3,500,0,1000],
#      'var': "pWCCSDARangeProton:pWC/1000.",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimEnergySumCSDAMuVPFBeamPrimTrkLen",
#      'xtitle': "Reconstructed Primary Track Length [cm]",
#      'ytitle': "CSDA Muon Kinetic Energy [MeV]",
#      'binning': [500,0,800,500,0,8000],
#      'var': "PFBeamPrimEnergySumCSDAMu:PFBeamPrimTrkLen",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimEnergySumCSDAProtonVPFBeamPrimTrkLen",
#      'xtitle': "Reconstructed Primary Track Length [cm]",
#      'ytitle': "CSDA Proton Kinetic Energy [MeV]",
#      'binning': [500,0,800,500,0,8000],
#      'var': "PFBeamPrimEnergySumCSDAProton:PFBeamPrimTrkLen",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimXsVPFBeamPrimZs",
#      'xtitle': "Primary Track Hit Z [cm]",
#      'ytitle': "Primary Track Hit X [cm]",
#      'binning': [100,0,200,100,-150,150],
#      'var': "PFBeamPrimXs:PFBeamPrimZs",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimYsVPFBeamPrimZs",
#      'xtitle': "Primary Track Hit Z [cm]",
#      'ytitle': "Primary Track Hit Y [cm]",
#      'binning': [100,0,200,100,350,450],
#      'var': "PFBeamPrimYs:PFBeamPrimZs",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimYsVPFBeamPrimXs",
#      'xtitle': "Primary Track Hit X [cm]",
#      'ytitle': "Primary Track Hit Y [cm]",
#      'binning': [100,-150,150,100,350,450],
#      'var': "PFBeamPrimYs:PFBeamPrimXs",
#      'cuts': weightStr,
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimXsVPFBeamPrimZsKEProtonLt0",
#      'xtitle': "Primary Track Hit Z [cm]",
#      'ytitle': "Primary Track Hit X [cm]",
#      'binning': [100,0,200,100,-150,150],
#      'var': "PFBeamPrimXs:PFBeamPrimZs",
#      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimYsVPFBeamPrimZsKEProtonLt0",
#      'xtitle': "Primary Track Hit Z [cm]",
#      'ytitle': "Primary Track Hit Y [cm]",
#      'binning': [100,0,200,100,350,450],
#      'var': "PFBeamPrimYs:PFBeamPrimZs",
#      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
#      #'normalize': True,
#      #'logz': True,
#    },
#    {
#      'name': "PFBeamPrimYsVPFBeamPrimXsKEProtonLt0",
#      'xtitle': "Primary Track Hit X [cm]",
#      'ytitle': "Primary Track Hit Y [cm]",
#      'binning': [100,-150,150,100,350,450],
#      'var': "PFBeamPrimYs:PFBeamPrimXs",
#      'cuts': "(zWireLastHitWire >= 0) && "+weightStr+"*(zWirePartKinProton_ajib[zWireLastHitWire] < 0.)",
#      #'normalize': True,
#      #'logz': True,
#    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC2D_",outSuffix="_"+runSetName,nMax=NMAX)

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

  deltaThetaXZTrackBICut = "*(isMC && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) > -5) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) < 3)) || ((!isMC) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) > -10) && ((atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*cos(phiWC))*180/pi) < 0))"
  deltaThetaYZTrackBICut = "*(isMC && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) > -8) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) < 2)) || ((!isMC) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) > -20) && ((atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi-atan(tan(thetaWC)*sin(phiWC))*180/pi) < -5))"
  rejectThroughgoingCut = "*(PFBeamPrimEndZ < 650.)"
  primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50.)"+deltaXTrackBICut+deltaYTrackBICut+deltaThetaXZTrackBICut+deltaThetaYZTrackBICut+rejectThroughgoingCut
  stoppingProtonCut = "*(PFBeamPrimEnergySumCSDAProton/kinWCProton > 0.8 && PFBeamPrimEnergySumCSDAProton/kinWCProton < 1.)"
  stoppingMuonCut = "*(PFBeamPrimEnergySumCSDAMu/kinWC > 0.8 && PFBeamPrimEnergySumCSDAMu/kinWC < 1.)"
  weightStr = "1"+primaryTrackCuts#+stoppingProtonCut

  #nData = 224281.0
  logy = False

  #catConfigs=TRUECATEGORYFEWERCONFIGS
  catConfigs=TRUECATEGORYPOORMATCHCONFIGS
  #catConfigs=TRUECATEGORYPROTONCONFIGS

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
      'scaleFactor': 0.18142931664058426, # for pions
    }],
    "run5387_1GeV",
  ))

  sillies.append((
    [{
      'fn': "piAbsSelector_run5432_v8.1_da81b52a.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      'cuts': "*(BIPion2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
      #'cuts': "*(BIProton2GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
    },
    {
      'fn': "piAbsSelector_mcc11_sce_2GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 2 GeV/c SCE",
      'caption': "MCC11 2 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 12.180555555555555,
    }],
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
      'scaleFactor': 30.827235772357724,
    }],
    "run5786_3GeV",
  ))

  sillies.append((
    [{
      'fn': "piAbsSelector_run5770_v8.1_da81b52a.root",
      'name': "run5770",
      'title': "Run 5770: 6 GeV/c",
      'caption': "Run 5770: 6 GeV/c",
      'isData': True,
      'cuts': "*(BIPion6GeV)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
    },
    {
      'fn': "piAbsSelector_mcc11_sce_6GeV_v7a1_55712adf.root",
      'name': "mcc11_sce_6GeV",
      'title': "MCC11 6 GeV/c SCE",
      'caption': "MCC11 6 GeV/c SCE",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13 || truePrimaryPDG == -11)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 12.046087888531618,
    }],
    "run5770_6GeV",
  ))

  #sillies.append((
  # [{
  #    'fn': "piAbsSelector_run5145_v7_55712ad_local.root",
  #    'name': "run5145",
  #    'title': "Run 5145: 7 GeV/c",
  #    'caption': "Run 5145: 7 GeV/c",
  #    'isData': True,
  #    'cuts': "*(BIPion7GeV)*"+cutGoodBeamline+cutGoodFEMBs,
  #  },
  #  {
  #    'fn': "piAbsSelector_mcc11_sce_7p0GeV_v7.0_55712adf_local.root",
  #    'name': "mcc11_sce_7GeV",
  #    'title': "MCC11 7 GeV/c SCE",
  #    'caption': "MCC11 7 GeV/c SCE",
  #    'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13 || truePrimaryPDG == -11)",
  #    'scaleFactor': 1,
  #  }],
  #  "run5145_7GeV",
  #))

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
      'scaleFactor': 37.68827160493827,
    }],
    "run5204_7GeV",
  ))

  doMP = False
  pool = None
  if doMP:
    pool = multiprocessing.Pool()
  for silly in sillies:
    if doMP:
      pool.apply_async(doDataMCPlots,(silly[0],catConfigs,weightStr,silly[1],NMAX))
    else:
      doDataMCPlots(silly[0],catConfigs,weightStr,silly[1],NMAX)
  if doMP:
    pool.close()
    pool.join()
