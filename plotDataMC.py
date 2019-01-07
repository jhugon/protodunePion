#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

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
  cutGoodBeamline = "(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1)"
  otherCuts = "*(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20))"

  deltaXTrackBICut = "*(isMC && ((PFBeamPrimXFrontTPC-xWC) > -10) && ((PFBeamPrimXFrontTPC-xWC) < 10)) || ((!isMC) && ((PFBeamPrimXFrontTPC-xWC) > 10) && ((PFBeamPrimXFrontTPC-xWC) < 30))"
  deltaYTrackBICut = "*(isMC && ((PFBeamPrimYFrontTPC-yWC) > -10) && ((PFBeamPrimYFrontTPC-yWC) < 10)) || ((!isMC) && ((PFBeamPrimYFrontTPC-yWC) > 7) && ((PFBeamPrimYFrontTPC-yWC) < 27))"
  primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimISTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ < 650.)"+deltaXTrackBICut+deltaYTrackBICut
  weightStr = "1"+otherCuts

  #nData = 224281.0
  logy = False

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    #{
    #  'fn': "piAbsSelector_run5145_v4.10.root",
    #  'name': "run5145",
    #  'title': "Run 5145: 7 GeV/c",
    #  'caption': "Run 5145: 7 GeV/c",
    #  'isData': True,
    #  'cuts': "*(CKov1Status == 1 && CKov0Status == 1)*"+cutGoodBeamline,
    #},
    #{
    #  'fn': "piAbsSelector_run5387_v4.10.root",
    #  'name': "run5387",
    #  'title': "Run 5387: 1 GeV/c",
    #  'caption': "Run 5387: 1 GeV/c",
    #  'isData': True,
    #  'cuts': "*"+cutGoodBeamline,
    #  'cuts': "*(CKov1Status == 0 && TOF < 170.)*"+cutGoodBeamline,
    #},
    {
      'fn': "piAbsSelector_run5432_1kevts_v4.10.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      #'cuts': "*"+cutGoodBeamline,
      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline, # for protons
    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.10.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 2 GeV/c FLF",
      'caption': "MCC11 2 GeV/c FLF",
      'color': root.kBlue-7,
      #'cuts': "",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 0.9732047159699893,
    },
    #{
    #  'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.4.root",
    #  'name': "mcc11_flf_7GeV",
    #  'title': "MCC11 7 GeV/c FLF",
    #  'caption': "MCC11 7 GeV/c FLF",
    #  'cuts': "",
    #  'color': root.kBlue-7,
    #  'scaleFactor': 1,
    #},
  ]

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
      'name': "pWC",
      'xtitle': "Momentum from BI [GeV/c]",
      'ytitle': "Events / bin",
      'binning': [100,0,10],
      'var': "pWC/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
      'printIntegral': True,
    },
    {
      'name': "PFBeamPrimKinInteract",
      'xtitle': "Primary PF Track Interaction Kinetic Energy [GeV]",
      'ytitle': "Events / bin",
      'binning': [50,0,10],
      'var': "PFBeamPrimKinInteract/1000.",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast3Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 3 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast3Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast5Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 5 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast5Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    {
      'name': "PFBeamPrimdEdxAverageLast7Hits",
      'xtitle': "Primary PF Track <dE/dx>_{Last 7 Hits} [MeV/cm]",
      'ytitle': "Events / bin",
      'binning': [100,0,30],
      'var': "PFBeamPrimdEdxAverageLast7Hits",
      'cuts': weightStr,
      #'normalize': True,
      'logy': logy,
    },
    #{
    #  'name': "PFNBeamSlices",
    #  'xtitle': "Number of Pandora Beam Slices",
    #  'ytitle': "Events / bin",
    #  'binning': [21,-0.5,20.5],
    #  'var': "PFNBeamSlices",
    #  'cuts': weightStr,
    #  'printIntegral': True,
    #},
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
      'binning': [200,-5,100],
      'var': "PFBeamPrimStartZ",
      'cuts': weightStr,
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
      'name': "PFBeamPrimTrkLen",
      'xtitle': "Pandora Beam Primary Track Length [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "PFBeamPrimTrkLen",
      'cuts': weightStr,
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
    #{
    #  'name': "DeltaPFBeamPrimEndXBeam",
    #  'xtitle': "Pandora Beam Primary Start - Beam Track X [cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [200,-50,50],
    #  'var': "PFBeamPrimStartX - beamTrackXFrontTPC",
    #  'cuts': weightStr,
    #},
    #{
    #  'name': "DeltaPFBeamPrimEndYBeam",
    #  'xtitle': "Pandora Beam Primary Start - Beam Track Y [cm]",
    #  'ytitle': "Events / bin",
    #  'binning': [120,-30,30],
    #  'var': "PFBeamPrimStartY - beamTrackYFrontTPC",
    #  'cuts': weightStr,
    #},
    {
      'name': "PFBeamPrimAngleToBeamTrk",
      'xtitle': "Angle Between BI & Primary PF Track [Deg]",
      'ytitle': "Events / bin",
      'binning': [80,0,40],
      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
    {
      'name': "PFBeamPrimAngleToBeamTrk_wide",
      'xtitle': "Angle Between BI & Primary PF Track [Deg]",
      'ytitle': "Events / bin",
      'binning': [180,0,180],
      'var': "PFBeamPrimAngleToBeamTrk*180/pi",
      'cuts': weightStr,
    },
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
      'binning': [200,-10,10],
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
      'binning': [200,-10,10],
      'var': "PFBeamPrimKins/1000.",
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
  ]

  #for i in reversed(range(len(histConfigs))):
  #  if histConfigs[i]['name'] != "pzWC":
  #  #if histConfigs[i]['name'] != "zWC4Hit":
  #    histConfigs.pop(i)

  if True:
    #plotManyFilesOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",nMax=NMAX)
    fileConfigMCs = copy.deepcopy(fileConfigs)
    fileConfigDatas = []
    for i in reversed(range(len(fileConfigMCs))):
      if 'isData' in fileConfigMCs[i] and fileConfigMCs[i]['isData']:
        fileConfigDatas.append(fileConfigMCs.pop(i))
    #dataMCStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",nMax=NMAX)
    print fileConfigDatas, fileConfigMCs
    dataMCCategoryStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="DataMC_",nMax=NMAX,
                  catConfigs=TRUECATEGORYFEWERCONFIGS
               )
    for histConfig in histConfigs:
      histConfig['logy'] = True
    dataMCCategoryStack(fileConfigDatas,fileConfigMCs,histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="DataMC_",nMax=NMAX,
                  outSuffix="_logyHist",
                  catConfigs=TRUECATEGORYFEWERCONFIGS
               )

  #######################################
  ############ 2D Plots #################
  #######################################

  histConfigs = [
    {
      'name': "PFBeamPrimdEdxVRange",
      'xtitle': "Primary Track Hit Residual Range [cm]",
      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
      'binning': [100,0,100,100,0,50],
      'var': "PFBeamPrimdEdxs:PFBeamPrimResRanges",
      'cuts': weightStr,
      #'normalize': True,
      #'logz': True,
    },
    {
      'name': "PFBeamPrimdEdxVRange_wide",
      'xtitle': "Primary Track Hit Residual Range [cm]",
      'ytitle': "Primary Track Hit dE/dx [MeV/cm]",
      'binning': [350,0,700,100,0,50],
      'var': "PFBeamPrimdEdxs:PFBeamPrimResRanges",
      'cuts': weightStr,
      #'normalize': True,
      #'logz': True,
    },
    {
      'name': "PFBeamPrimStartThetaVPhi_wide",
      'xtitle': "PF Primary Track Start #phi [deg]",
      'ytitle': "PF Primary Track Start #theta [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "PFBeamPrimStartTheta*180/pi:PFBeamPrimStartPhi*180/pi",
      'cuts': weightStr,
      #'normalize': True,
      #'logz': True,
    },
    {
      'name': "PFBeamPrimStartThetaVPhi_IsTruePrimary_wide",
      'xtitle': "PF Primary Track Start #phi [deg]",
      'ytitle': "PF Primary Track Start #theta [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "PFBeamPrimStartTheta*180/pi:PFBeamPrimStartPhi*180/pi",
      'cuts': weightStr+"*(abs(PFBeamPrimTrueTrackID) == trackTrueID)",
      'preliminaryString': "Matched to Truth"
      #'normalize': True,
      #'logz': True,
    },
    {
      'name': "trueStartThetaVPhi_wide",
      'xtitle': "True Primary Start #phi [deg]",
      'ytitle': "True Primary Start #theta [deg]",
      'binning': [90,-180,180,90,0,180],
      'var': "trueStartTheta*180/pi:trueStartPhi*180/pi",
      'cuts': weightStr,
      #'normalize': True,
      #'logz': True,
    },
    {
      'name': "nGoodFEMBsVAPA_wide",
      'xtitle': "APA Number",
      'ytitle': "N Good FEMBs",
      'binning': [6,-0.5,5.5,21,-0.5,20.5],
      'var': "nGoodFEMBs:Iteration$",
      'cuts': "1",
      #'normalize': True,
      #'logz': True,
    },
  ]

  plotOneHistOnePlot(fileConfigs,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataMC_",nMax=NMAX)

