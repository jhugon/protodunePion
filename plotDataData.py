#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy

m2SF=1000.
tofOffset=59.6
tofDistance = 28.6
lightTime = tofDistance/2.99e8*1e9
momSF=1.0

if __name__ == "__main__":

  histConfigs = [
#    {
#      'name': "beamTrackXFrontTPC",
#      'xtitle': "X of Beam Track Projection to TPC Front [cm]",
#      'ytitle': "Beam Tracks / bin",
#      'binning': [50,-100,50],
#      'var': "beamTrackXFrontTPC",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackXFrontTPC_wide",
#      'xtitle': "X of Beam Track Projection to TPC Front [cm]",
#      'ytitle': "Beam Tracks / bin",
#      'binning': [100,-400,400],
#      'var': "beamTrackXFrontTPC",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackYFrontTPC",
#      'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
#      'ytitle': "Beam Tracks / bin",
#      'binning': [50,300,600],
#      'var': "beamTrackYFrontTPC",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackYFrontTPC_wide",
#      'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
#      'ytitle': "Beam Tracks / bin",
#      'binning': [100,0,700],
#      'var': "beamTrackYFrontTPC",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackTheta",
#      'xtitle': "Beam Track #theta [deg]",
#      'ytitle': "Tracks / bin",
#      'binning': [50,0,50],
#      'var': "beamTrackTheta*180/pi",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackTheta_wide",
#      'xtitle': "Beam Track #theta [deg]",
#      'ytitle': "Tracks / bin",
#      'binning': [180,0,180],
#      'var': "beamTrackTheta*180/pi",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackPhi",
#      'xtitle': "Beam Track #phi [deg]",
#      'ytitle': "Tracks / bin",
#      'binning': [60,-160,-100],
#      'var': "beamTrackPhi*180/pi",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackPhi_wide",
#      'xtitle': "Beam Track #phi [deg]",
#      'ytitle': "Tracks / bin",
#      'binning': [180,-180,180],
#      'var': "beamTrackPhi*180/pi",
#      'printIntegral': True,
#      'cuts': "1",
#    },
    {
      'name': "nBeamTracks",
      'xtitle': "Number of Beam Tracks",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "nBeamTracks",
      'cuts': "1",
    },
#    {
#      'name': "nBeamMom",
#      'xtitle': "Number of Beam Momenta",
#      'ytitle': "Events / bin",
#      'binning': [21,-0.5,20.5],
#      'var': "nBeamMom",
#      'cuts': "1",
#    },
#    {
#      'name': "nBeamEvents",
#      'xtitle': "Number of Beam Events",
#      'ytitle': "Events / bin",
#      'binning': [21,-0.5,20.5],
#      'var': "nBeamEvents",
#      'cuts': "1",
#    },
#    {
#      'name': "beamTrackMom",
#      'xtitle': "Beam Track Matched Momentum [GeV/c]",
#      'ytitle': "Beam Tracks / bin",
#      'binning': [100,0,10],
#      'var': "beamTrackMom",
#      'cuts': "1",
#    },
#    {
#      'name': "beamMom",
#      'xtitle': "Beam Momentum [GeV/c]",
#      'ytitle': "Beam Momenta / bin",
#      'binning': [120,0,12],
#      'var': "beamMom*{}".format(momSF),
#      'preliminaryString': "Momentum Scaled by {:.2f}".format(momSF),
#      'cuts': "1",
#    },
    {
      'name': "TOF",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,0,300],
      'var': "TOF",
      'cuts': "1",
    },
    {
      'name': "TOF_zoom",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,150,250],
      'var': "TOF",
      'cuts': "1",
    },
    {
      'name': "TOF_zoom_zoom",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [60,140,170],
      'var': "TOF",
      'cuts': "1",
    },
    {
      'name': "TOF_CKov0_zoom_zoom",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [80,145,165],
      'var': "TOF",
      'cuts': "(CKov0Status == 1)",
      'caption': "Cherenkov 0 Fired",
    },
    {
      'name': "TOF_Corrected_zoom_zoom",
      'xtitle': "Raw Beamline TOF - {} ns [ns]".format(tofOffset),
      'ytitle': "Events / bin",
      'binning': [60,140,170],
      'var': "TOF - {}".format(tofOffset),
      'cuts': "1",
    },
    {
      'name': "TOFChan",
      'xtitle': "TOF Channel",
      'ytitle': "Events / bin",
      'binning': [6,-1.5,4.5],
      'var': "TOFChan",
      'cuts': "1",
    },
    {
      'name': "CKov0Status",
      'xtitle': "Cherenkov 0 Status",
      'ytitle': "Events / bin",
      #'binning': [3,-1.5,1.5],
      'binning': [2,-0.5,1.5],
      'var': "CKov0Status",
      'cuts': "1",
    },
    {
      'name': "CKov1Status",
      'xtitle': "Cherenkov 1 Status",
      'ytitle': "Events / bin",
      #'binning': [3,-1.5,1.5],
      'binning': [2,-0.5,1.5],
      'var': "CKov1Status",
      'cuts': "1",
    },
    {
      'name': "CKov0Pressure",
      'xtitle': "Cherenkov 0 Pressure",
      'ytitle': "Events / bin",
      'binning': [100,0.,1.2],
      'var': "CKov0Pressure",
      'cuts': "(CKov0Status > -1)",
    },
    {
      'name': "CKov1Pressure",
      'xtitle': "Cherenkov 1 Pressure",
      'ytitle': "Events / bin",
      'binning': [100,0.,1.2],
      'var': "CKov1Pressure",
      'cuts': "(CKov1Status > -1)",
    },
    {
      'name': "beamlineMassSquared",
      'xtitle': "Beamline Mass Squared [{:.0f}#times (MeV/c^{{2}})^{{2}}]".format(m2SF),
      'ytitle': "Events / bin",
      'binning': [100,-2e5/m2SF,15e5/m2SF],
      'var': "beamMom*beamMom*{}*1e6*(pow(TOF-{},2)/{}-1.)*{}".format(momSF**2,tofOffset,lightTime**2,1./m2SF),
      'cuts': "(!isMC)",
      #'normalize': True,
      'logy': False,
      'drawvlines':[0.511**2/m2SF,105.65**2/m2SF,139.6**2/m2SF,493.677**2/m2SF,938.272046**2/m2SF,1875.6**2/m2SF],
      #'preliminaryString': "Assuming d/c = {:.1f} ns, Momentum Scaled by {:.2f}".format(lightTime,momSF)
      'preliminaryString': "Assuming d = {:.1f} m, TOF = Raw TOF - {:.1f} ns".format(tofDistance,tofOffset)
    },
    {
      'name': "beamlineMassSquared_zoom0_onlyCKov0",
      'xtitle': "Beamline Mass Squared [{:.0f}#times (MeV/c^{{2}})^{{2}}]".format(m2SF),
      'ytitle': "Events / bin",
      'binning': [50,-2e5/m2SF,2e5/m2SF],
      'var': "beamMom*beamMom*{}*1e6*(pow(TOF-{},2)/{}-1.)*{}".format(momSF**2,tofOffset,lightTime**2,1./m2SF),
      'cuts': "(CKov0Status == 1 && CKov1Status == 0)",
      'caption': "Only Cherenkov 0 Fired",
      #'normalize': True,
      'logy': False,
      'drawvlines':[0.511**2/m2SF,105.65**2/m2SF,139.6**2/m2SF,493.677**2/m2SF,938.272046**2/m2SF,1875.6**2/m2SF],
      #'preliminaryString': "Assuming d/c = {:.1f} ns, Momentum Scaled by {:.2f}".format(lightTime,momSF)
      'preliminaryString': "Assuming d = {:.1f} m, TOF = Raw TOF - {:.1f} ns".format(tofDistance,tofOffset)
    },
    {
      'name': "beamlineMassSquared_zoom0",
      'xtitle': "Beamline Mass Squared [{:.0f}#times (MeV/c^{{2}})^{{2}}]".format(m2SF),
      'ytitle': "Events / bin",
      'binning': [50,-2e5/m2SF,2e5/m2SF],
      'var': "beamMom*beamMom*{}*1e6*(pow(TOF-{},2)/{}-1.)*{}".format(momSF**2,tofOffset,lightTime**2,1./m2SF),
      'cuts': "(!isMC)",
      #'normalize': True,
      'logy': False,
      'drawvlines':[0.511**2/m2SF,105.65**2/m2SF,139.6**2/m2SF,493.677**2/m2SF,938.272046**2/m2SF,1875.6**2/m2SF],
      #'preliminaryString': "Assuming d/c = {:.1f} ns, Momentum Scaled by {:.2f}".format(lightTime,momSF)
      'preliminaryString': "Assuming d = {:.1f} m, TOF = Raw TOF - {:.1f} ns".format(tofDistance,tofOffset)
    },
    {
      'name': "beamlineMass",
      'xtitle': "Beamline Mass [MeV/c^{2}]",
      'ytitle': "Events / bin",
      'binning': [100,0,2000],
      'var': "sqrt(beamMom*beamMom*{}*1e6*(pow(TOF-{},2)/{}-1.))".format(momSF**2,tofOffset,lightTime**2),
      'cuts': "(!isMC)"+"*(beamMom*beamMom*{}*1e6*(pow(TOF-{},2)/{}-1.)>0.)".format(momSF**2,tofOffset,lightTime**2),
      #'normalize': True,
      'logy': False,
      'drawvlines':[0.511,105.65,139.6,493.677,938.272046,1875.6],
      #'preliminaryString': "Assuming d/c = {:.1f} ns, Momentum Scaled by {:.2f}".format(lightTime,momSF)
      'preliminaryString': "Assuming d = {:.1f} m, TOF = Raw TOF - {:.1f} ns".format(tofDistance,tofOffset)
    },
    {
      'name': "PFNBeamSlices",
      'xtitle': "Number of Pandora Beam Slices",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "PFNBeamSlices",
      'cuts': "1",
    },
    {
      'name': "PFBeamPrimNDaughters",
      'xtitle': "Number of Pandora Beam Secondaries",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "PFBeamPrimNDaughters[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimIsTracklike",
      'xtitle': "Pandora Beam Primary is Tracklike",
      'ytitle': "Events / bin",
      'binning': [2,-0.5,1.5],
      'var': "PFBeamPrimIsTracklike[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimStartX",
      'xtitle': "Pandora Beam Primary Start X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-400,400],
      'var': "PFBeamPrimStartX[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimStartY",
      'xtitle': "Pandora Beam Primary Start Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-5,650],
      'var': "PFBeamPrimStartY[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimStartZ",
      'xtitle': "Pandora Beam Primary Start Z [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-5,100],
      'var': "PFBeamPrimStartZ[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimEndX",
      'xtitle': "Pandora Beam Primary End X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-400,400],
      'var': "PFBeamPrimEndX[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimEndY",
      'xtitle': "Pandora Beam Primary End Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-5,650],
      'var': "PFBeamPrimEndY[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimEndZ",
      'xtitle': "Pandora Beam Primary End Z [cm]",
      'ytitle': "Events / bin",
      'binning': [35,-5,700],
      'var': "PFBeamPrimEndZ[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimTrkLen",
      'xtitle': "Pandora Beam Primary Track Length [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "PFBeamPrimTrkLen[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimShwrLen",
      'xtitle': "Pandora Beam Primary Shower Length [cm]",
      'ytitle': "Events / bin",
      'binning': [200,0,1000],
      'var': "PFBeamPrimShwrLen[0]",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimShwrOpenAngle",
      'xtitle': "Pandora Beam Primary Shower Open Angle [deg]",
      'ytitle': "Events / bin",
      'binning': [30,0,90],
      'var': "PFBeamPrimShwrOpenAngle[0]*180./pi",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimStartTheta",
      'xtitle': "Pandora Beam Primary Shower Open Angle [deg]",
      'ytitle': "Events / bin",
      'binning': [60,0,180],
      'var': "PFBeamPrimStartTheta[0]*180./pi",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "PFBeamPrimStartPhi",
      'xtitle': "Pandora Beam Primary Shower Open Angle [deg]",
      'ytitle': "Events / bin",
      'binning': [60,-180,180],
      'var': "PFBeamPrimStartPhi[0]*180./pi",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "DeltaPFBeamPrimEndXBeam",
      'xtitle': "Pandora Beam Primary Start - Beam Track X [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-200,200],
      'var': "PFBeamPrimStartX[0] - beamTrackXFrontTPC",
      'cuts': "(PFNBeamSlices > 0)",
    },
    {
      'name': "DeltaPFBeamPrimEndYBeam",
      'xtitle': "Pandora Beam Primary Start - Beam Track Y [cm]",
      'ytitle': "Events / bin",
      'binning': [200,-200,200],
      'var': "PFBeamPrimStartY[0] - beamTrackYFrontTPC",
      'cuts': "(PFNBeamSlices > 0)",
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  #fn = "PiAbs_mcc11.root"
  fn = "piAbsSelector_mcc11_protoDUNE_reco_hadd.root"
  name = "mcc11"
  #caption = "ProtoDUNE-SP Internal"# & MCC11"
  caption = ""
  scaleFactor= 2.651
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "MCC10 2 & 7 GeV 3m SCE"

  fileConfigsData = [
    #{
    #  'fn': "piAbsSelector_run5141.root",
    #  'name': "run5141",
    #  'title': "Run 5141: 7 GeV/c",
    #  'caption': "Run 5141: 7 GeV/c",
    #  'color': root.kBlack,
    #  'cuts': "*(triggerIsBeam)",
    #},
    #{
    #  'fn': "piAbsSelector_run5145.root",
    #  'name': "run5145",
    #  'title': "Run 5145: 7 GeV/c",
    #  'caption': "Run 5145: 7 GeV/c",
    #  'color': root.kOrange-3,
    #  'cuts': "*(triggerIsBeam)",
    #},
#    {
#      'fn': "piAbsSelector_run5174.root",
#      'name': "run5174",
#      'title': "Run 5174: 7 GeV/c",
#      'caption': "Run 5174: 7 GeV/c",
#      'color': root.kOrange-3,
#      'cuts': "*(triggerIsBeam)",
#    },
#    {
#      'fn': "piAbsSelector_run5387.root",
#      'name': "run5387",
#      'title': "Run 5387: 1 GeV/c",
#      'caption': "Run 5387: 1 GeV/c",
#      'color': root.kBlue-7,
#      'cuts': "*(triggerIsBeam)",
#    },
#    {
#      'fn': "piAbsSelector_run5430.root",
#      'name': "run5430",
#      'title': "Run 5430: 2 GeV/c",
#      'caption': "Run 5430: 2 GeV/c",
#      'color': root.kGreen+3,
#      'cuts': "*(triggerIsBeam)",
#    },
#    #{
#    #  'fn': "piAbsSelector_run5758.root",
#    #  'name': "run5758",
#    #  'title': "Run 5758: 6 GeV/c",
#    #  'caption': "Run 5758: 6 GeV/c",
#    #  'color': root.kBlue-7,
#    #  'cuts': "*(triggerIsBeam)",
#    #},
#    #{
#    #  'fn': "piAbsSelector_run5777.root",
#    #  'name': "run5777",
#    #  'title': "Run 5777: 3 GeV/c",
#    #  'caption': "Run 5777: 3 GeV/c",
#    #  'color': root.kBlue-7,
#    #  'cuts': "*(triggerIsBeam)",
#    #},
#    {
#      'fn': "piAbsSelector_run5826.root",
#      'name': "run5826",
#      'title': "Run 5826: 0.5 GeV/c",
#      'caption': "Run 5826: 0.5 GeV/c",
#      'color': root.kBlue-7,
#      'cuts': "*(triggerIsBeam)",
#    },
#    {
#      'fn': "piAbsSelector_run5834.root",
#      'name': "run5834",
#      'title': "Run 5834: 0.3 GeV/c",
#      'caption': "Run 5834: 0.3 GeV/c",
#      'color': root.kBlue-7,
#      'cuts': "*(triggerIsBeam)",
#    },
    {
      'fn': "PiAbs_redoBeamEvent_run5387.root",
      'name': "run5387_redo",
      'title': "Run 5387: 1 GeV/c Redo Beam Reco",
      'caption': "Run 5387: 1 GeV/c Redo Beam Reco",
      'color': root.kBlue-7,
      'cuts': "*(triggerIsBeam)",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5430.root",
      'name': "run5430_redo",
      'title': "Run 5430: 2 GeV/c Redo Beam Reco",
      'caption': "Run 5430: 2 GeV/c Redo Beam Reco",
      'color': root.kGreen+3,
      'cuts': "*(triggerIsBeam)",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5826.root",
      'name': "run5826_redo",
      'title': "Run 5826: 0.5 GeV/c Redo Beam Reco",
      'caption': "Run 5826: 0.5 GeV/c Redo Beam Reco",
      'color': root.kBlue-7,
      'cuts': "*(triggerIsBeam)",
    },
    {
      'fn': "PiAbs_redoBeamEvent_run5834.root",
      'name': "run5834_redo",
      'title': "Run 5834: 0.3 GeV/c Redo Beam Reco",
      'caption': "Run 5834: 0.3 GeV/c Redo Beam Reco",
      'color': root.kBlue-7,
      'cuts': "*(triggerIsBeam)",
    },
  ]
  for i, fileConfig in enumerate(fileConfigsData):
    fileConfig['color'] = COLORLIST[i]
  fileConfigsAllData = [
    {
      'fn': [
                "piAbsSelector_run5145.root",
                "piAbsSelector_run5387.root",
                "piAbsSelector_run5430.root",
                "piAbsSelector_run5758.root",
                "piAbsSelector_run5777.root",
                "piAbsSelector_run5826.root",
                "piAbsSelector_run5834.root",
            ],
      'name': "runMany",
      #'title': "Runs 5387, 5430",
      #'caption': "Runs 5387, 5430",
      'color': root.kBlack,
      'cuts': "*(triggerIsBeam)",
    },
  ]
  fileConfigsMC = [
    #{
    #  'fn': fn,
    #  'title': "MCC 11",
    #  'color': root.kBlue-7,
    #  'scaleFactor': scaleFactor,
    #},
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

  for histConfig in histConfigs:
    histConfig["caption"] = caption
    histConfig["normalize"] = True
    histConfig["ytitle"] = "Normalized Events / Bin"

  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
    histConfig["normalize"] = False
    histConfig["ytitle"] = "Events / Bin"
  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",outSuffix="_logyHist",nMax=NMAX)

  functions = [root.TF1("proton","{}*sqrt({}/x/x+1.)".format(lightTime,(i*1e-3)**2),0.01,15) for i in [0.511,105.65,139.6,493.677,938.272046,1875.6]]
  for i in range(len(functions)):
    functions[i].SetLineColor(COLORLIST[len(functions)-i-1])
  histConfigs= [
    {
      'name': "TOFVMom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [150,0,10,100,0,300-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "1",
      'funcs': functions,
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,8,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "1",
      'funcs': functions,
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_zoom_uncorrected",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Uncorrected Time of Flight [ns]",
      'binning': [100,0,8,100,150,210],
      'var': "TOF:beamMom",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "TOFVMom_zoom_uncorrected_CKov1StatusIs0",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Uncorrected Time of Flight [ns]",
      'binning': [100,0,8,100,150,210],
      'var': "TOF:beamMom",
      'cuts': "(CKov1Status == 0)",
      'logz': True,
      'caption': "Cherenkov Electron Veto",
    },
    {
      'name': "TOFVMom_bothCKov_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,8,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 1 && CKov1Status == 1)",
      'funcs': functions,
      'caption': "Both Cherenkov Detectors Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_noCKov_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [150,0,10,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 0 && CKov1Status == 0)",
      'funcs': functions,
      'caption': "Neither Cherenkov Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_zoom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,4,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "1",
      'funcs': functions,
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_bothCKov_zoom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,4,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 1 && CKov1Status == 1)",
      'funcs': functions,
      'caption': "Both Cherenkov Detectors Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_onlyCKov0_zoom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,4,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 1 && CKov1Status == 0)",
      'funcs': functions,
      'caption': "Only Cherenkov 0 Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_onlyCKov1_zoom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,4,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 0 && CKov1Status == 1)",
      'funcs': functions,
      'caption': "Only Cherenkov 1 Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_noCKov_zoom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,4,100,150-tofOffset,210-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "(CKov0Status == 0 && CKov1Status == 0)",
      'funcs': functions,
      'caption': "Neither Cherenkov Fired",
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
    {
      'name': "TOFVMom_protons",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [200,0.5,1.5,100,150-tofOffset,250-tofOffset],
      'var': "TOF-{}:beamMom*{}".format(tofOffset,momSF),
      'cuts': "1",
      #'funcs': functions,
      'captionright1': "Lines Assume d = {:.1f} m".format(tofDistance),
      'captionright2': "Momentum Scaled by {:.2f}".format(momSF),
      'captionright3': "TOF = Raw TOF - {:.2f} ns".format(tofOffset),
      'logz': True,
    },
  ]
  plotOneHistOnePlot(fileConfigsAllData,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",nMax=NMAX)

  histConfigs= [
    {
      'title': "CKov0 & CKov1",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,150,250],
      'var': "TOF",
      'cuts': "CKov0Status == 1 && CKov1Status == 1",
    },
    {
      'title': "CKov0",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,150,250],
      'var': "TOF",
      'cuts': "CKov0Status == 1 && CKov1Status == 0",
    },
    {
      'title': "CKov 1",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,150,250],
      'var': "TOF",
      'cuts': "CKov0Status == 0 && CKov1Status == 1",
    },
    {
      'title': "No CKov",
      'xtitle': "Beamline Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [100,150,250],
      'var': "TOF",
      'cuts': "CKov0Status == 0 && CKov1Status == 0",
    },
    #{
    #  'title': "Invalid CKov",
    #  'xtitle': "Beamline Time of Flight [ns]",
    #  'ytitle': "Events / bin",
    #  'binning': [100,150,250],
    #  'var': "TOF",
    #  'cuts': "CKov0Status == -1 && CKov1Status == -1",
    #},
  ]
  for i, histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[i]
  plotManyHistsOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_TOF_KCovCuts_",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
  plotManyHistsOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_TOF_KCovCuts_",outSuffix="_logyHist",nMax=NMAX)

  histConfigs= [
    {
      'title': "CKov0 & CKov1",
      'xtitle': "Beam Momentum [GeV/c]",
      'ytitle': "Beam Momenta / bin",
      'binning': [100,0,10],
      'var': "beamMom",
      'cuts': "CKov0Status == 1 && CKov1Status == 1",
    },
    {
      'title': "CKov0",
      'xtitle': "Beam Momentum [GeV/c]",
      'ytitle': "Beam Momenta / bin",
      'binning': [100,0,10],
      'var': "beamMom",
      'cuts': "CKov0Status == 1 && CKov1Status == 0",
    },
    {
      'title': "CKov 1",
      'xtitle': "Beam Momentum [GeV/c]",
      'ytitle': "Beam Momenta / bin",
      'binning': [100,0,10],
      'var': "beamMom",
      'cuts': "CKov0Status == 0 && CKov1Status == 1",
    },
    {
      'title': "No CKov",
      'xtitle': "Beam Momentum [GeV/c]",
      'ytitle': "Beam Momenta / bin",
      'binning': [100,0,10],
      'var': "beamMom",
      'cuts': "CKov0Status == 0 && CKov1Status == 0",
    },
    {
      'title': "Invalid CKov",
      'xtitle': "Beam Momentum [GeV/c]",
      'ytitle': "Beam Momenta / bin",
      'binning': [100,0,10],
      'var': "beamMom",
      'cuts': "CKov0Status == -1 && CKov1Status == -1",
    },
  ]
  for i, histConfig in enumerate(histConfigs):
    histConfig['color'] = COLORLIST[i]
  plotManyHistsOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_beamMom_KCovCuts_",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
  plotManyHistsOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_beamMom_KCovCuts_",outSuffix="_logyHist",nMax=NMAX)
