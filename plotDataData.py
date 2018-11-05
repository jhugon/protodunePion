#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy

m2SF= 1000.
lightTime = 155

if __name__ == "__main__":

  histConfigs = [
    {
      'name': "beamTrackXFrontTPC",
      'xtitle': "X of Beam Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [50,-100,50],
      'var': "beamTrackXFrontTPC",
      'cuts': "1",
    },
    {
      'name': "beamTrackXFrontTPC_wide",
      'xtitle': "X of Beam Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,-400,400],
      'var': "beamTrackXFrontTPC",
      'cuts': "1",
    },
    {
      'name': "beamTrackYFrontTPC",
      'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [50,300,600],
      'var': "beamTrackYFrontTPC",
      'cuts': "1",
    },
    {
      'name': "beamTrackYFrontTPC_wide",
      'xtitle': "Y of Beam Track Projection to TPC Front [cm]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,0,700],
      'var': "beamTrackYFrontTPC",
      'cuts': "1",
    },
    {
      'name': "beamTrackTheta",
      'xtitle': "Beam Track #theta [deg]",
      'ytitle': "Tracks / bin",
      'binning': [50,0,50],
      'var': "beamTrackTheta*180/pi",
      'cuts': "1",
    },
    {
      'name': "beamTrackTheta_wide",
      'xtitle': "Beam Track #theta [deg]",
      'ytitle': "Tracks / bin",
      'binning': [180,0,180],
      'var': "beamTrackTheta*180/pi",
      'cuts': "1",
    },
    {
      'name': "beamTrackPhi",
      'xtitle': "Beam Track #phi [deg]",
      'ytitle': "Tracks / bin",
      'binning': [60,-160,-100],
      'var': "beamTrackPhi*180/pi",
      'cuts': "1",
    },
    {
      'name': "beamTrackPhi_wide",
      'xtitle': "Beam Track #phi [deg]",
      'ytitle': "Tracks / bin",
      'binning': [180,-180,180],
      'var': "beamTrackPhi*180/pi",
      'printIntegral': True,
      'cuts': "1",
    },
    {
      'name': "nBeamTracks",
      'xtitle': "Number of Beam Tracks",
      'ytitle': "Events / bin",
      'binning': [21,-0.5,20.5],
      'var': "nBeamTracks",
      'cuts': "1",
    },
    {
      'name': "beamTrackMom",
      'xtitle': "Beam Track Momentum [GeV/c]",
      'ytitle': "Beam Tracks / bin",
      'binning': [100,0,10],
      'var': "beamTrackMom",
      'cuts': "1",
    },
    {
      'name': "TOFs",
      'xtitle': "Beam Time of Flight [ns]",
      'ytitle': "Events / bin",
      'binning': [1000,0.,300],
      'var': "TOFs",
      'cuts': "1",
    },
    {
      'name': "beamlineMassS1uared",
      'xtitle': "Beamline Mass Squared [{:.0f}#times (MeV/c^{{2}})^{{2}}]".format(m2SF),
      'ytitle': "Events / bin",
      'binning': [50,-3e5*1./m2SF,1e6*1./m2SF],
      'var': "beamTrackMom*beamTrackMom*1e6*(firstTOF*firstTOF/{}-1.)*".format(lightTime**2)+str(1./m2SF),
      'cuts': "1",
      'drawvlines':[105.65**2*1./m2SF,139.6**2*1./m2SF,493.677**2*1./m2SF,938.272046**2*1./m2SF],
    },
    {
      'name': "beamlineMass",
      'xtitle': "Beamline Mass[MeV/c^{2}]",
      'ytitle': "Events / bin",
      'binning': [100,0.,2000.],
      'var': "sqrt(beamTrackMom*beamTrackMom*1e6*(firstTOF*firstTOF/{}-1.))".format(lightTime**2),
      'cuts': "1",
      'drawvlines':[105.65,139.6,493.677,938.272046],
    },
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  fn = "PiAbs_mcc11.root"
  name = "mcc11"
  caption = "Beam Data & MCC11"
  scaleFactor= 2.651
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "MCC10 2 & 7 GeV 3m SCE"

  fileConfigsData = [
    #{
    #  'fn': "PiAbs_Run5287.root",
    #  'title': "Data Run 5287",
    #  'caption': "Data Run 5287",
    #  'color': root.kBlack,
    #},
    #{
    #  'fn': "PiAbs_PhysicsThrough5287.root",
    #  'title': "Data Runs 5000-5287",
    #  'caption': "Data Runs 5000-5287",
    #  'color': root.kBlack,
    #  #'cuts': "(triggerIsBeam)",
    #},
    #{
    #  'fn': "PiAbs_AllData.root",
    #  'name': "data",
    #  'title': "ProtoDUNE-SP Data",
    #  'caption': "ProtoDUNE-SP Data",
    #  'color': root.kBlack,
    #  'cuts': "*(triggerIsBeam)",
    #},
    {
      'fn': "piAbsSelector_run5141.root",
      'name': "run5141",
      'title': "Run 5141: 7 GeV/c",
      'caption': "Run 5141: 7 GeV/c",
      'color': root.kBlue-7,
      'cuts': "*(triggerIsBeam)",
      'isData': True,
    },
    {
      'fn': "piAbsSelector_run5387.root",
      'name': "run5387",
      'title': "Run 5387: 1 GeV/c",
      'caption': "Run 5387: 1 GeV/c",
      'color': root.kGreen+3,
      'cuts': "*(triggerIsBeam)",
      'isData': True,
    },
    {
      'fn': "piAbsSelector_run5430.root",
      'name': "run5430",
      'title': "Run 5430: 2 GeV/c",
      'caption': "Run 5430: 2 GeV/c",
      'color': root.kOrange-3,
      'cuts': "*(triggerIsBeam)",
      'isData': True,
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

  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
  plotManyFilesOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",outSuffix="_logyHist",nMax=NMAX)

  deuteronFunc = root.TF1("deuteron","{}*sqrt(1.8756*1.8756/x/x+1)".format(lightTime),0,10)
  deuteronFunc.SetLineColor(root.kGray+1)
  protonFunc = root.TF1("proton","{}*sqrt(0.9382720813*0.9382720813/x/x+1)".format(lightTime),0,10)
  protonFunc.SetLineColor(root.kBlack)
  kaonFunc = root.TF1("kaon","{}*sqrt(0.493677*0.493677/x/x+1)".format(lightTime),0,10)
  kaonFunc.SetLineColor(root.kOrange-3)
  pionFunc = root.TF1("pion","{}*sqrt(0.13957018*0.13957018/x/x+1)".format(lightTime),0,10)
  pionFunc.SetLineColor(root.kAzure+10)
  muonFunc = root.TF1("muon","{}*sqrt(0.1056583745*0.1056583745/x/x+1)".format(lightTime),0,10)
  muonFunc.SetLineColor(root.kRed+1)
  electronFunc = root.TF1("electron","{}".format(lightTime),0,10)
  electronFunc.SetLineColor(root.kGreen+1)
  histConfigs= [
    {
      'name': "TOFVMom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [100,0,10.,100,0,300.],
      'var': "firstTOF:beamTrackMom",
      'cuts': "1",
      'funcs': [deuteronFunc,protonFunc,kaonFunc,pionFunc,muonFunc,electronFunc],
    },
    {
      'name': "TOFVMom_zoom",
      'xtitle': "Beamline Momentum [GeV/c]",
      'ytitle': "Time of Flight [ns]",
      'binning': [60,0,3.,100,150,250.],
      'var': "firstTOF:beamTrackMom",
      'cuts': "1",
      'funcs': [deuteronFunc,protonFunc,kaonFunc,pionFunc,muonFunc,electronFunc],
    },
  ]
  plotOneHistOnePlot(fileConfigsData+fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="DataData_",nMax=NMAX)
