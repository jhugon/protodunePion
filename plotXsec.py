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
  cutGoodFEMBs = " && (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20)"

  deltaXTrackBICut = "&& ((isMC && ((PFBeamPrimXFrontTPC-xWC) > -10) && ((PFBeamPrimXFrontTPC-xWC) < 10)) || ((!isMC) && ((PFBeamPrimXFrontTPC-xWC) > 10) && ((PFBeamPrimXFrontTPC-xWC) < 30)))"
  deltaYTrackBICut = "&& ((isMC && ((PFBeamPrimYFrontTPC-yWC) > -10) && ((PFBeamPrimYFrontTPC-yWC) < 10)) || ((!isMC) && ((PFBeamPrimYFrontTPC-yWC) > 7) && ((PFBeamPrimYFrontTPC-yWC) < 27)))"
  primaryTrackCuts = "&& zWireLastHitWire >= 0 && (PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ < 650. && PFBeamPrimEndZ > 5.)"+deltaXTrackBICut+deltaYTrackBICut+" && zWirePartKin[zWireLastHitWire] >= 0."
  incidHitCut = "&& (zWireZ < 600.)"
  interHitCut = "&& (zWireLastHitWire >= 0) && (zWireZ[zWireLastHitWire] > 5. && zWireZ[zWireLastHitWire] < 600.)"
  weightStr = "1"+primaryTrackCuts

  trueFiducialCut = "((trueCategory>=1 && trueCategory <=4) || trueCategory==8 || trueCategory==6) && (trueEndZ > 5.)"
  trueFiducialCutGoodReco = "((trueCategory>=1 && trueCategory <=4 && (sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)) || trueCategory==8 || trueCategory==6) && (PFBeamPrimTrueTrackID == truePrimaryTrackID) && (trueEndZ > 5.)"
  trueFiducialIncidHitCut = "&& (zWireTrueZ < 600.)"
  trueFiducialInterHitCut = "&& (zWireLastHitWireTrue >=0) && (zWireTrueZ[zWireLastHitWireTrue] > 5. && zWireTrueZ[zWireLastHitWireTrue] < 600.)"
  trueGoodReco = "&& (PFBeamPrimTrueTrackID == truePrimaryTrackID) && (sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)"

  denomCut="((trueCategory>=1 && trueCategory <=4) || trueCategory==6 || trueCategory==8)"
  incidHitCutDenom=denomCut+trueFiducialIncidHitCut
  interHitCutDenom="(zWireLastHitWire >= 0)*"+denomCut+trueFiducialInterHitCut
  incidHitCutNumer=incidHitCutDenom+" && "+trueFiducialCutGoodReco+primaryTrackCuts+incidHitCut
  interHitCutNumer=interHitCutDenom+" && "+trueFiducialCutGoodReco+primaryTrackCuts+interHitCut

  incidRecoCutsBkg="(!("+trueFiducialCutGoodReco+"))"+primaryTrackCuts+"(!("+trueFiducialIncidHitCut+"))"+incidHitCut
  interRecoCutsBkg="(!("+trueFiducialCutGoodReco+"))"+primaryTrackCuts+"(!("+trueFiducialInterHitCut+"))"+interHitCut
  incidRecoCutsSig=trueFiducialCutGoodReco+primaryTrackCuts+trueFiducialIncidHitCut+incidHitCut
  interRecoCutsSig=trueFiducialCutGoodReco+primaryTrackCuts+trueFiducialInterHitCut+interHitCut

  #nData = 224281.0
  logy = False

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
#    {
#      'fn': "piAbsSelector_run5432_v4.10.root",
#      'name': "run5432",
#      'title': "Run 5432: 2 GeV/c",
#      'caption': "Run 5432: 2 GeV/c",
#      'isData': True,
#      #'cuts': "*"+cutGoodBeamline+cutGoodFEMBs,
#      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
#      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
#    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
#      'name': "mcc11_flf_2GeV",
#      'title': "MCC11 2 GeV/c FLF",
#      'caption': "MCC11 2 GeV/c FLF",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
    {
      'fn': "piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",
      'name': "mcc11_3ms_1GeV",
      'title': "MCC11 1 GeV/c No SCE",
      'caption': "MCC11 1 GeV/c No SCE",
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

  #binning = [30,-5,2.5]
  #binning = [10,0.2,2.2]
  binning = [12,0,2.4]
  xsecHistos=[]
  for fileConfig in fileConfigs:
    legEntries = []
    extraLegEntries = []
    incidHists = []
    interHists = []
    xsecPerBinHists = []
    xsecPerKEHists = []

    ## The reco'd Nevts in data andn MC w.r.t. reco KE
    incidReco = None
    interReco = None
    ## Like above but evt and hits pass trueFidCuts
    incidRecoSig = None
    interRecoSig = None
    ## Like above but not pass evt or hit trueFidCuts
    incidRecoBkg = None
    interRecoBkg = None
    ##
    incidDenom=None
    interDenom=None
    ##
    incidNumer=None
    interNumer=None

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
    #incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
    #                                            incidentCuts=weightStr,#+incidHitCut,
    #                                            interactingCuts="(zWireLastHitWire >= 0)*"+weightStr,#+interHitCut,
    #                                            incidentVar="zWirePartKin*1e-3",
    #                                            interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
    #                                            nMax=NMAX,binning=binning)
    #xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
    #xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
    #incidHists.append(incidZWire)
    #interHists.append(interZWire)
    #xsecPerBinHists.append(xsecPerBinZWire)
    #xsecPerKEHists.append(xsecPerKEZWire)
    #legEntries.append("zWirePartKin")

    incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
                                                incidentCuts=weightStr+incidHitCut,
                                                interactingCuts="(zWireLastHitWire >= 0)*"+weightStr+interHitCut,
                                                incidentVar="zWirePartKin*1e-3",
                                                interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                nMax=NMAX,binning=binning)
    xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
    xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
    incidHists.append(incidZWire)
    interHists.append(interZWire)
    xsecPerBinHists.append(xsecPerBinZWire)
    xsecPerKEHists.append(xsecPerKEZWire)
    legEntries.append("zWirePartKin+HitCuts")
    incidReco=incidZWire
    interReco=interZWire

    if not ("isData" in fileConfig) or (not fileConfig["isData"]):
      #incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts=weightStr,
      #                                            interactingCuts="(zWireLastHitWireTrue >= 0)*"+weightStr,
      #                                            incidentVar="zWireTruePartKin*1e-3",
      #                                            interactingVar="zWireTruePartKin[zWireLastHitWireTrue]*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBinTrue = getXsec(incidZWireTrue,interZWireTrue,sliceThickness=0.5)
      #xsecPerKETrue = normToBinWidth(xsecPerBinTrue.Clone(xsecPerBinTrue.GetName()+"_perKE"))
      #incidHists.append(incidZWireTrue)
      #interHists.append(interZWireTrue)
      #xsecPerBinHists.append(xsecPerBinTrue)
      #xsecPerKEHists.append(xsecPerKETrue)
      #legEntries.append("zWireTruePartKin")
      #incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts=weightStr,
      #                                            #interactingCuts=weightStr+"*(zWireLastHitWire >= 0)",
      #                                            interactingCuts="(zWireLastHitWire >= 0)*"+weightStr,
      #                                            incidentVar="zWireTrueTrajKin*1e-3",
      #                                            interactingVar="zWireTrueTrajKin[zWireLastHitWireTrue]*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBinTrue = getXsec(incidZWireTrue,interZWireTrue,sliceThickness=0.5)
      #xsecPerKETrue = normToBinWidth(xsecPerBinTrue.Clone(xsecPerBinTrue.GetName()+"_perKE"))
      #incidHists.append(incidZWireTrue)
      #interHists.append(interZWireTrue)
      #xsecPerBinHists.append(xsecPerBinTrue)
      #xsecPerKEHists.append(xsecPerKETrue)
      #legEntries.append("zWireTrueTrajKin")

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
      #incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts="1"+trueGoodReco,
      #                                            interactingCuts="(zWireLastHitWire >= 0)"+trueGoodReco,
      #                                            incidentVar="zWirePartKin*1e-3",
      #                                            interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
      #xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
      #incidHists.append(incidZWire)
      #interHists.append(interZWire)
      #xsecPerBinHists.append(xsecPerBinZWire)
      #xsecPerKEHists.append(xsecPerKEZWire)
      #legEntries.append("zWirePartKin Good Reco")

      ### Now efficiency/background stuff
      #incidZWireTrueFidCut, interZWireTrueFidCut = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts=trueFiducialCut+trueFiducialIncidHitCut,
      #                                            interactingCuts="(zWireLastHitWire>=0)*"+trueFiducialCut+trueFiducialInterHitCut,
      #                                            incidentVar="zWirePartKin*1e-3",
      #                                            interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #incidHists.append(incidZWireTrueFidCut)
      #interHists.append(interZWireTrueFidCut)
      #extraLegEntries.append("zWirePartKin in Fid")
      #incidZWireNotTrueFidCut, interZWireNotTrueFidCut = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts="(!("+trueFiducialCut+trueFiducialIncidHitCut+"))",
      #                                            interactingCuts="(zWireLastHitWire>=0)*"+"(!("+trueFiducialCut+trueFiducialInterHitCut+"))",
      #                                            incidentVar="zWirePartKin*1e-3",
      #                                            interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
      #                                            nMax=NMAX,binning=binning)
      #incidHists.append(incidZWireNotTrueFidCut)
      #interHists.append(interZWireNotTrueFidCut)
      #extraLegEntries.append("zWirePartKin Not in Fid")

      incidRecoBkg, interRecoBkg = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=incidRecoCutsBkg,
                                                  interactingCuts=interRecoCutsBkg,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      incidHists.append(incidRecoBkg)
      interHists.append(interRecoBkg)
      extraLegEntries.append("zWirePartKin 'Bkg'")
      incidRecoSig, interRecoSig = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=incidRecoCutsSig,
                                                  interactingCuts=interRecoCutsSig,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      #incidHists.append(incidRecoSig)
      #interHists.append(interRecoSig)
      #extraLegEntries.append("zWirePartKin 'Sig'")

      incidDenom, interDenom = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=incidHitCutDenom,
                                                  interactingCuts=interHitCutDenom,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      #incidHists.append(incidDenom)
      #interHists.append(interDenom)
      #extraLegEntries.append("zWirePartKin 'Denom'")
      incidNumer, interNumer = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=incidHitCutNumer,
                                                  interactingCuts=interHitCutNumer,
                                                  incidentVar="zWirePartKin*1e-3",
                                                  interactingVar="zWirePartKin[zWireLastHitWire]*1e-3",
                                                  nMax=NMAX,binning=binning)
      #incidHists.append(incidNumer)
      #interHists.append(interNumer)
      #extraLegEntries.append("zWirePartKin 'Numer'")

      incidEff = root.TEfficiency(incidNumer,incidDenom)
      interEff = root.TEfficiency(interNumer,interDenom)

      plotHistsSimple([incidEff,interEff],["Incident","Interacting"],"Reco Hit Kinetic Energy [GeV]","Efficiency",c,"XS_"+fileConfig["name"]+"_Eff",captionArgs=[fileConfig["caption"]],drawOptions="PEZ0",xlim=[0,3.])
      plotHistsSimple([incidEff],None,"Incident Reco Hit Kinetic Energy [GeV]","Efficiency",c,"XS_"+fileConfig["name"]+"_incidentEff",captionArgs=[fileConfig["caption"]],drawOptions="PEZ0",xlim=[0,3.])
      plotHistsSimple([interEff],None,"Reco Interacting Kinetic Energy [GeV]","Efficiency",c,"XS_"+fileConfig["name"]+"_interactingEff",captionArgs=[fileConfig["caption"]],drawOptions="PEZ0",xlim=[0,3.])

      incidRecoBkgSub = incidReco.Clone(incidReco.GetName()+"_bkgSub")
      incidRecoBkgSubEff = incidReco.Clone(incidReco.GetName()+"_bkgSubEff")
      for iBin in range(1,incidReco.GetNbinsX()+1):
        recoVal = incidReco.GetBinContent(iBin)
        bkgSubVal = recoVal - incidRecoBkg.GetBinContent(iBin)
        effVal = incidEff.GetEfficiency(iBin)
        bkgSubEffVal = 0.
        if effVal > 0.:
          bkgSubEffVal = bkgSubVal/effVal
        recoErr = incidReco.GetBinError(iBin)
        bkgSubErr = recoErr
        bkgSubEffErr = 10.
        if effVal > 0.:
          bkgSubEffErr = bkgSubErr/effVal
        incidRecoBkgSub.SetBinContent(iBin,bkgSubVal)
        incidRecoBkgSubEff.SetBinContent(iBin,bkgSubEffVal)
        incidRecoBkgSub.SetBinError(iBin,bkgSubErr)
        incidRecoBkgSubEff.SetBinError(iBin,bkgSubEffErr)

      interRecoBkgSub = interReco.Clone(interReco.GetName()+"_bkgSub")
      interRecoBkgSubEff = interReco.Clone(interReco.GetName()+"_bkgSubEff")
      for iBin in range(1,interReco.GetNbinsX()+1):
        recoVal = interReco.GetBinContent(iBin)
        bkgSubVal = recoVal - interRecoBkg.GetBinContent(iBin)
        effVal = interEff.GetEfficiency(iBin)
        bkgSubEffVal = 0.
        if effVal > 0.:
          bkgSubEffVal = bkgSubVal/effVal
        recoErr = interReco.GetBinError(iBin)
        bkgSubErr = recoErr
        bkgSubEffErr = 10000.
        if effVal > 0.:
          bkgSubEffErr = bkgSubErr/effVal
        interRecoBkgSub.SetBinContent(iBin,bkgSubVal)
        interRecoBkgSubEff.SetBinContent(iBin,bkgSubEffVal)
        interRecoBkgSub.SetBinError(iBin,bkgSubErr)
        interRecoBkgSubEff.SetBinError(iBin,bkgSubEffErr)
      incidHists.append(incidRecoBkgSub)
      incidHists.append(incidRecoBkgSubEff)
      interHists.append(interRecoBkgSub)
      interHists.append(interRecoBkgSubEff)
      xsecPerBinBkgSub = getXsec(incidRecoBkgSub,interRecoBkgSub,sliceThickness=0.5)
      xsecPerKEBkgSub = normToBinWidth(xsecPerBinBkgSub.Clone(xsecPerBinBkgSub.GetName()+"_perKE"))
      xsecPerBinBkgSubEff = getXsec(incidRecoBkgSubEff,interRecoBkgSubEff,sliceThickness=0.5)
      xsecPerKEBkgSubEff = normToBinWidth(xsecPerBinBkgSubEff.Clone(xsecPerBinBkgSubEff.GetName()+"_perKE"))
      xsecPerBinHists.append(xsecPerBinBkgSub)
      xsecPerKEHists.append(xsecPerKEBkgSub)
      xsecPerBinHists.append(xsecPerBinBkgSubEff)
      xsecPerKEHists.append(xsecPerKEBkgSubEff)
      xsecHistos.append(xsecPerKEBkgSubEff)

      legEntries.append("Reco Bkg Sub'd")
      legEntries.append("Reco Bkg Sub'd & Eff. Corr.")

    plotHistsSimple(incidHists,legEntries+extraLegEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_incident",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(interHists,legEntries+extraLegEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_interacting",captionArgs=[fileConfig["caption"]])
    c.SetLogy(True)
    plotHistsSimple(incidHists,legEntries+extraLegEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_incident_logy",logy=True,captionArgs=[fileConfig["caption"]])
    plotHistsSimple(interHists,legEntries+extraLegEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,"XS_"+fileConfig["name"]+"_interacting_logy",logy=True,captionArgs=[fileConfig["caption"]])
    c.SetLogy(False)

    plotHistsSimple(xsecPerBinHists,legEntries,"Reco Kinetic Energy [GeV]","Cross-section / bin [barns]",c,"XS_"+fileConfig["name"]+"_xsPerBin",drawOptions="E",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(xsecPerKEHists,legEntries,"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,"XS_"+fileConfig["name"]+"_xsPerGeV_wide",drawOptions="E",captionArgs=[fileConfig["caption"]])
    plotHistsSimple(xsecPerKEHists,legEntries,"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,"XS_"+fileConfig["name"]+"_xsPerGeV",drawOptions="E",xlim=[0,3.],ylim=[0,12],captionArgs=[fileConfig["caption"]])

    catConfigs=[
       {
         'title': "#pi Inelastic--Good",
         'cuts':"(trueCategory>=1 && trueCategory <=4)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)*(zWireTrueZ < 600.)*(trueEndZ > 5.)",
       },
       {
         'title': "#pi Through-going--Good",
         'cuts':"(trueCategory==6 || trueCategory==8)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(zWireTrueZ < 600.)*(trueEndZ > 5.)",
       },
       {
         'title': "#pi Inelastic--Bad Reco/True Interaction Match",
         'cuts':"(trueCategory>=1 && trueCategory <=4)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))>=20)*(zWireTrueZ < 600.)*(trueEndZ > 5.)",
       },
       {
         'title': "#pi Inelastic or Through-going--Bad Track/True Primary Match",
         'cuts':"((trueCategory>=1 && trueCategory <=4) || trueCategory==6 || trueCategory==8)*(PFBeamPrimTrueTrackID != truePrimaryTrackID)",
       },
       #{
       #  'title': "#pi Inelastic--Wire Outside Fiducial",
       #  'cuts':"(trueCategory>=1 && trueCategory <=4)*(!(zWireTrueZ < 600.))*(trueEndZ > 5.)",
       #},
       {
         'title': "#pi Interacted Outside Fiducial",
         'cuts':"(trueCategory>=1 && trueCategory <=4)*(!(trueEndZ > 5.)) || trueCategory==7",
       },
       #{
       #  'title': "#pi Interacted Outside Fiducial",
       #  'cuts':"(trueCategory>=1 && trueCategory <=4)*(!(trueEndZ > 5.))",
       #},
       {
         'title': "#pi Decay",
         'cuts':"trueCategory==9 || trueCategory==10",
       },
       #{
       #  'title': "#pi Interacted Before TPC",
       #  'cuts':"trueCategory==7",
       #},
       {
         'title': "Non-#pi Primary",
         'cuts':"trueCategory>=11 && trueCategory<=14",
       },
       #{
       #  'title': "Unknown",
       #  'cuts':"trueCategory==0 || trueCategory==16 || trueCategory == 15",
       #},
    ]
    histConfigs = [
      {
        'name': "Incident",
        'title': "Incident",
        'xtitle': "Reco Incident Hit Kinetic Energy [GeV]",
        'ytitle': "Hits / Bin",
        'binning': binning,
        'var': "zWirePartKin*1e-3",
        'cuts': weightStr+incidHitCut,
      },
      {
        'name': "IncidentFrac",
        'title': "Incident",
        'xtitle': "Reco Incident Hit Kinetic Energy [GeV]",
        'ytitle': "Fraction of Reco Selected Hits",
        'binning': binning,
        'var': "zWirePartKin*1e-3",
        'cuts': weightStr+incidHitCut,
        'efficiencyDenomCuts': weightStr+incidHitCut+fileConfig['cuts'],
      },
    ]
    for iCat in range(len(catConfigs)):
        catConfigs[iCat]['color'] = COLORLIST[iCat]
    dataMCCategoryStack([],[fileConfig],histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="XS_"+fileConfig["name"]+"_Stack_",nMax=NMAX,
                  #catConfigs=TRUECATEGORYFEWERCONFIGS
                  catConfigs=catConfigs
               )
    for iCat in range(len(catConfigs)):
        catConfigs[iCat]['cuts'] = catConfigs[iCat]['cuts'].replace("zWireTrueZ","zWireTrueZ[zWireLastHitWireTrue]")
    histConfigs = [
      {
        'name': "Interacting",
        'title': "Interacting",
        'xtitle': "Reco Interaction Kinetic Energy [GeV]",
        'ytitle': "Track Interactions / Bin",
        'binning': binning,
        'var': "zWirePartKin[zWireLastHitWire]*1e-3",
        'cuts': "(zWireLastHitWire >= 0)*"+weightStr+interHitCut,
      },
      {
        'name': "InteractingFrac",
        'title': "Interacting",
        'xtitle': "Reco Interaction Kinetic Energy [GeV]",
        'ytitle': "Fraction of Reco Selected Events",
        'binning': binning,
        'var': "zWirePartKin[zWireLastHitWire]*1e-3",
        'cuts': "(zWireLastHitWire >= 0)*"+weightStr+interHitCut,
        'efficiencyDenomCuts': "(zWireLastHitWire >= 0)*"+weightStr+interHitCut+fileConfig['cuts'],
      },
    ]
    dataMCCategoryStack([],[fileConfig],histConfigs,c,"PiAbsSelector/tree",
                  outPrefix="XS_"+fileConfig["name"]+"_Stack_",nMax=NMAX,
                  #catConfigs=TRUECATEGORYFEWERCONFIGS
                  catConfigs=catConfigs
               )

  for fileConfig, xsecHisto in zip(fileConfig,xsecHistos):
    plotHistsSimple(xsecHistos,[x["title"] for x in fileConfigs],None,None,c,"XS_All_xsPerGeV",drawOptions="E",xlim=[0,3.],ylim=[0,12])
