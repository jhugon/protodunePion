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
  primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ < 650. && PFBeamPrimStartZ > 25.)"+deltaXTrackBICut+deltaYTrackBICut
  incidHitCut = "*(zWireZ > 15. && zWireZ < 600.)"
  interHitCut = "*(zWireLastHitWire >= 0)*(zWireZ > 15. && zWireZ < 600.)"
  weightStr = "1"+otherCuts+primaryTrackCuts

  trueFiducialCut = "(trueCategory>=1 && trueCategory <=4)*(trueEndZ > 25.)"#"*(trueEndZ > 650 || (trueEndX < -15 && trueEndX > -300 && trueEndY < 500 && trueEndY > 200))"
  trueFiducialIncidHitCut = "*(zWireTrueZ > 15. && zWireTrueZ < 600.)"
  trueFiducialInterHitCut = "*(zWireTrueZ > 15. && zWireTrueZ < 600.)"
  trueGoodReco = "*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)"

  #nData = 224281.0
  logy = False

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    {
      'fn': "piAbsSelector_run5432_v4.10.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      #'cuts': "*"+cutGoodBeamline,
      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline, # for protons
    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 2 GeV/c FLF",
      'caption': "MCC11 2 GeV/c FLF",
      'color': root.kBlue-7,
      #'cuts': "",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 1.,
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 2 GeV/c No SCE",
      'caption': "MCC11 2 GeV/c No SCE",
      'color': root.kBlue-7,
      #'cuts': "",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 1.,
    },
  ]
  for fc in fileConfigs:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]

  binning = [30,-5,2.5]
  for fileConfig in fileConfigs:
    legEntries = []
    incidHists = []
    interHists = []
    xsecPerBinHists = []
    xsecPerKEHists = []
    #incid, inter = getIncidentInteractingHists(fileConfig,
    #                                            incidentCuts=weightStr,
    #                                            interactingCuts=weightStr,
    #                                            incidentVar="PFBeamPrimKins*1e-3",
    #                                            interactingVar="PFBeamPrimKinInteract*1e-3",
    #                                            nMax=NMAX,binning=binning)
    #xsecPerBin = getXsec(incid,inter,sliceThickness=0.5)
    #xsecPerKE = normToBinWidth(xsecPerBin.Clone(xsecPerBin.GetName()+"_perKE"))
    #incidHists.append(incid)
    #interHists.append(inter)
    #xsecPerBinHists.append(xsecPerBin)
    #xsecPerKEHists.append(xsecPerKE)
    #legEntries.append("PFBeamPrimKins")
    incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
                                                incidentCuts=weightStr,
                                                interactingCuts="(zWireLastHitWire >= 0)*"+weightStr,
                                                incidentVar="zWirePartKin*1e-3",
                                                interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                nMax=NMAX,binning=binning)
    xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
    xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
    incidHists.append(incidZWire)
    interHists.append(interZWire)
    xsecPerBinHists.append(xsecPerBinZWire)
    xsecPerKEHists.append(xsecPerKEZWire)
    legEntries.append("zWirePartKin")

    if not ("isData" in fileConfig) or (not fileConfig["isData"]):
      incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=weightStr,
                                                  #interactingCuts=weightStr+"*(zWireLastHitWire >= 0)",
                                                  interactingCuts="(zWireLastHitWire >= 0)*"+weightStr,
                                                  incidentVar="zWireTruePartKin*1e-3",
                                                  interactingVar="zWireTruePartKin[zWireLastHitWireTrue]*1e-3",
                                                  nMax=NMAX,binning=binning)
      xsecPerBinTrue = getXsec(incidZWireTrue,interZWireTrue,sliceThickness=0.5)
      xsecPerKETrue = normToBinWidth(xsecPerBinTrue.Clone(xsecPerBinTrue.GetName()+"_perKE"))
      incidHists.append(incidZWireTrue)
      interHists.append(interZWireTrue)
      xsecPerBinHists.append(xsecPerBinTrue)
      xsecPerKEHists.append(xsecPerKETrue)
      legEntries.append("zWireTruePartKin")
      incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=weightStr,
                                                  #interactingCuts=weightStr+"*(zWireLastHitWire >= 0)",
                                                  interactingCuts="(zWireLastHitWire >= 0)*"+weightStr,
                                                  incidentVar="zWireTrueTrajKin*1e-3",
                                                  interactingVar="zWireTrueTrajKin[zWireLastHitWireTrue]*1e-3",
                                                  nMax=NMAX,binning=binning)
      xsecPerBinTrue = getXsec(incidZWireTrue,interZWireTrue,sliceThickness=0.5)
      xsecPerKETrue = normToBinWidth(xsecPerBinTrue.Clone(xsecPerBinTrue.GetName()+"_perKE"))
      incidHists.append(incidZWireTrue)
      interHists.append(interZWireTrue)
      xsecPerBinHists.append(xsecPerBinTrue)
      xsecPerKEHists.append(xsecPerKETrue)
      legEntries.append("zWireTrueTrajKin")

      ### Now cuts
      #incid, inter = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts="1"+trueGoodReco,
      #                                            interactingCuts="1"+trueGoodReco,
      #                                            incidentVar="PFBeamPrimKins*1e-3",
      #                                            interactingVar="PFBeamPrimKinInteract*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBin = getXsec(incid,inter,sliceThickness=0.5)
      #xsecPerKE = normToBinWidth(xsecPerBin.Clone(xsecPerBin.GetName()+"_perKE"))
      #incidHists.append(incid)
      #interHists.append(inter)
      #xsecPerBinHists.append(xsecPerBin)
      #xsecPerKEHists.append(xsecPerKE)
      #legEntries.append("PFBeamPrimKins Good Reco")
      incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts="1"+trueGoodReco,
                                                  interactingCuts="(zWireLastHitWire >= 0)"+trueGoodReco,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
      xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
      incidHists.append(incidZWire)
      interHists.append(interZWire)
      xsecPerBinHists.append(xsecPerBinZWire)
      xsecPerKEHists.append(xsecPerKEZWire)
      legEntries.append("zWirePartKin Good Reco")

      ## Now efficiency/background stuff
      incidZWireTrueFidCut, interZWireTrueFidCut = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=trueFiducialCut+trueFiducialIncidHitCut+trueGoodReco,
                                                  interactingCuts="(zWireLastHitWire>=0)*"+trueFiducialCut+trueFiducialInterHitCut+trueGoodReco,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      incidZWireNotTrueFidCut, interZWireNotTrueFidCut = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts="(!("+trueFiducialCut+trueFiducialIncidHitCut+trueGoodReco+"))",
                                                  interactingCuts="(zWireLastHitWire>=0)*"+"(!("+trueFiducialCut+trueFiducialInterHitCut+trueGoodReco+"))",
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)

    plotHistsSimple(incidHists,legEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_incident",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(interHists,legEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_interacting",captionArgs=[fileConfig["caption"]])
    c.SetLogy(True)
    plotHistsSimple(incidHists,legEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_incident_logy",logy=True,captionArgs=[fileConfig["caption"]])
    plotHistsSimple(interHists,legEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_interacting_logy",logy=True,captionArgs=[fileConfig["caption"]])
    c.SetLogy(False)

    plotHistsSimple(xsecPerBinHists,legEntries,"Reco Kinetic Energy [GeV]","Cross-section / bin [barns]",c,"XS_"+fileConfig["name"]+"_xsPerBin",drawOptions="E",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(xsecPerKEHists,legEntries,"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,"XS_"+fileConfig["name"]+"_xsPerGeV_wide",drawOptions="E",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(xsecPerKEHists,legEntries,"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,"XS_"+fileConfig["name"]+"_xsPerGeV",drawOptions="E",xlim=[0,3.],ylim=[0,20],captionArgs=[fileConfig["caption"]])

