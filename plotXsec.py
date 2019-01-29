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
  interHitCut = "&& (zWireLastHitWire >= 0) && zWireZ[zWireLastHitWire] > 5. && zWireZ[zWireLastHitWire] < 600."
  weightStr = "1"+primaryTrackCuts

  trueFiducialCut = "((trueCategory>=1 && trueCategory <=4) || trueCategory==8 || trueCategory==6) && (trueEndZ > 5.)"
  trueFiducialCutGoodReco = "((trueCategory>=1 && trueCategory <=4 && (sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)) || trueCategory==8 || trueCategory==6) && (PFBeamPrimTrueTrackID == truePrimaryTrackID) && (trueEndZ > 5.)"
  trueFiducialIncidHitCut = "&& (zWireTrueZ < 600.)"
  trueFiducialInterHitCut = "&& (zWireLastHitWireTrue >=0) && (zWireTrueZ[zWireLastHitWireTrue] > 5. && zWireTrueZ[zWireLastHitWireTrue] < 600.)"
  trueGoodReco = "&& (PFBeamPrimTrueTrackID == truePrimaryTrackID) && (sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)"

  denomCut="((trueCategory>=1 && trueCategory <=4) || trueCategory==6 || trueCategory==8)"
  incidHitCutDenom=denomCut+trueFiducialIncidHitCut
  interHitCutDenom="(zWireLastHitWire >= 0) && "+denomCut+trueFiducialInterHitCut
  incidHitCutNumer=incidHitCutDenom+" && "+trueFiducialCutGoodReco+primaryTrackCuts+incidHitCut
  interHitCutNumer=interHitCutDenom+" && "+trueFiducialCutGoodReco+primaryTrackCuts+interHitCut

  #incidRecoCutsBkg="(!("+trueFiducialCutGoodReco+"|| (1"+trueFiducialIncidHitCut+")))"+primaryTrackCuts+incidHitCut
  #interRecoCutsBkg="(!("+trueFiducialCutGoodReco+"|| (1"+trueFiducialInterHitCut+")))"+primaryTrackCuts+interHitCut
  incidRecoCutsSig=trueFiducialCutGoodReco+primaryTrackCuts+trueFiducialIncidHitCut+incidHitCut
  interRecoCutsSig=trueFiducialCutGoodReco+primaryTrackCuts+trueFiducialInterHitCut+interHitCut

  #nData = 224281.0
  logy = False

  outrootfile = root.TFile("XSHists.root","recreate")

  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100
  fileConfigs = [
    #{
    #  'fn': "piAbsSelector_run5432_v4.10.root",
    #  'name': "run5432",
    #  'title': "Run 5432: 2 GeV/c",
    #  'caption': "Run 5432: 2 GeV/c",
    #  'isData': True,
    #  #'cuts': "*"+cutGoodBeamline+cutGoodFEMBs,
    #  'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+cutGoodBeamline+cutGoodFEMBs, # for pions
    #  #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+cutGoodBeamline+cutGoodFEMBs, # for protons
    #},
#    {
#      'fn': "piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",
#      'name': "mcc11_3ms_1GeV",
#      'title': "MCC11 1 GeV/c No SCE",
#      'caption': "MCC11 1 GeV/c No SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
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
#    {
#      'fn': "piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root",
#      'name': "mcc11_3ms_7GeV",
#      'title': "MCC11 7 GeV/c No SCE",
#      'caption': "MCC11 7 GeV/c No SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
#    {
#      'fn': "piAbsSelector_mcc11_sce_1p0GeV_v4.11.root",
#      'name': "mcc11_sce_1GeV",
#      'title': "MCC11 1 GeV/c SCE",
#      'caption': "MCC11 1 GeV/c SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
    {
      'fn': "piAbsSelector_mcc11_sce_2p0GeV_v4.11.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 2 GeV/c SCE",
      'caption': "MCC11 2 GeV/c SCE",
      'color': root.kBlue-7,
      #'cuts': "",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 1.,
    },
#    {
#      'fn': "piAbsSelector_mcc11_sce_7p0GeV_v4.11.root",
#      'name': "mcc11_sce_7GeV",
#      'title': "MCC11 7 GeV/c SCE",
#      'caption': "MCC11 7 GeV/c SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_1p0GeV_v4.11.root",
#      'name': "mcc11_flf_1GeV",
#      'title': "MCC11 1 GeV/c FLF SCE",
#      'caption': "MCC11 1 GeV/c FLF SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 2 GeV/c FLF SCE",
      'caption': "MCC11 2 GeV/c FLF SCE",
      'color': root.kBlue-7,
      #'cuts': "",
      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
      'scaleFactor': 1.,
    },
#    {
#      'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.11.root",
#      'name': "mcc11_flf_7GeV",
#      'title': "MCC11 7 GeV/c FLF SCE",
#      'caption': "MCC11 7 GeV/c FLF SCE",
#      'color': root.kBlue-7,
#      #'cuts': "",
#      'cuts': "*(truePrimaryPDG == 211 || truePrimaryPDG == -13)", # for pions
#      #'cuts': "*(truePrimaryPDG == 2212)", # for protons
#      'scaleFactor': 1.,
#    },
  ]
  for fc in fileConfigs:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]

  systConfigs=[
    {"name":""},
    {"name":"caloScaleUp",
        "zWirePartKin":"zWirePartKin_caloScaleUp",
        "zWireEnergySum":"zWireEnergySum_caloScaleUp",
        "zWiredEdx":"zWiredEdx_caloScaleUp",
    },
    {"name":"caloScaleDown",
        "zWirePartKin":"zWirePartKin_caloScaleDown",
        "zWireEnergySum":"zWireEnergySum_caloScaleDown",
        "zWiredEdx":"zWiredEdx_caloScaleDown",
    },
    {"name":"beamScaleUp",
        "zWirePartKin":"zWirePartKin_beamScaleUp",
    },
    {"name":"beamScaleDown",
        "zWirePartKin":"zWirePartKin_beamScaleDown",
    },
  ]
  class ModifyStringSyst(object): 
    def __init__(self,cfg,fileConfig):
      self.cfg = cfg
      self.fileConfig = fileConfig
    
    def __call__(self,s):
      result = copy.deepcopy(s)
      for key in self.cfg:
        if key != "name":
          result = result.replace(key,self.cfg[key])
      return result

    def makeName(self,prefix,suffix=""):
      if self.cfg['name'] == "":
        return "{0}_{1}{2}".format(prefix,self.fileConfig["name"],suffix)
      else:
        return "{0}_{1}_{2}{3}".format(prefix,self.fileConfig["name"],self.cfg['name'],suffix)

  #binning = [30,-5,2.5]
  #binning = [10,0.2,2.2]
  #binning = [20,0,8]
  binning = [5,0.,2.5]
  xsecHistos=[]
  for fileConfig in fileConfigs:
    for systConfig in systConfigs:
      modStrSyst = ModifyStringSyst(systConfig,fileConfig)

      legEntries = []
      incidHists = []
      interHists = []
      extraLegEntries = []
      extraIncidHists = []
      extraInterHists = []
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
      #                                            incidentCuts=modStrSyst(weightStr),
      #                                            interactingCuts=modStrSyst(weightStr),
      #                                            incidentVar=modStrSyst("PFBeamPrimKins*1e-3"),
      #                                            interactingVar=modStrSyst("PFBeamPrimKinInteract*1e-3"),
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBin = getXsec(incid,inter,sliceThickness=0.5)
      #xsecPerKE = normToBinWidth(xsecPerBin.Clone(xsecPerBin.GetName()+"_perKE"))
      #incidHists.append(incid)
      #interHists.append(inter)
      #xsecPerBinHists.append(xsecPerBin)
      #xsecPerKEHists.append(xsecPerKE)
      #legEntries.append("PFBeamPrimKins")
      #incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
      #                                            incidentCuts=modStrSyst(weightStr,#+incidHitCut),
      #                                            interactingCuts=modStrSyst("(zWireLastHitWire >= 0)*"+weightStr,#+interHitCut),
      #                                            incidentVar=modStrSyst("zWirePartKin*1e-3"),
      #                                            interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
      #                                            nMax=NMAX,binning=binning)
      #xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
      #xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
      #incidHists.append(incidZWire)
      #interHists.append(interZWire)
      #xsecPerBinHists.append(xsecPerBinZWire)
      #xsecPerKEHists.append(xsecPerKEZWire)
      #legEntries.append("zWirePartKin")

      incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
                                                  incidentCuts=modStrSyst(weightStr+incidHitCut),
                                                  interactingCuts=modStrSyst("zWireLastHitWire >= 0 && "+weightStr+interHitCut),
                                                  incidentVar=modStrSyst("zWirePartKin*1e-3"),
                                                  interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
                                                  nMax=NMAX,binning=binning,printIntegral=True)
      xsecPerBinZWire = getXsec(incidZWire,interZWire,sliceThickness=0.5)
      xsecPerKEZWire = normToBinWidth(xsecPerBinZWire.Clone(xsecPerBinZWire.GetName()+"_perKE"))
      incidHists.append(incidZWire)
      interHists.append(interZWire)
      xsecPerBinHists.append(xsecPerBinZWire)
      xsecPerKEHists.append(xsecPerKEZWire)
      legEntries.append("Reco")
      incidReco=incidZWire
      interReco=interZWire
      xsecPerBin=xsecPerBinZWire
      xsecPerKE=xsecPerKEZWire

      outrootfile.cd()
      incidReco.SetName(modStrSyst.makeName("incidReco"))
      incidReco.Write()
      interReco.SetName(modStrSyst.makeName("interReco"))
      interReco.Write()
      xsecPerBin.SetName(modStrSyst.makeName("xsecPerBin"))
      xsecPerBin.Write()
      xsecPerKE.SetName(modStrSyst.makeName("xsecPerKE"))
      xsecPerKE.Write()

      if not ("isData" in fileConfig) or (not fileConfig["isData"]):
        #incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
        #                                            incidentCuts=modStrSyst(weightStr),
        #                                            interactingCuts=modStrSyst("(zWireLastHitWireTrue >= 0)*"+weightStr),
        #                                            incidentVar=modStrSyst("zWireTruePartKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWireTruePartKin[zWireLastHitWireTrue]*1e-3"),
        #                                            nMax=NMAX,binning=binning)
        #xsecPerBinTrue = getXsec(incidZWireTrue,interZWireTrue,sliceThickness=0.5)
        #xsecPerKETrue = normToBinWidth(xsecPerBinTrue.Clone(xsecPerBinTrue.GetName()+"_perKE"))
        #incidHists.append(incidZWireTrue)
        #interHists.append(interZWireTrue)
        #xsecPerBinHists.append(xsecPerBinTrue)
        #xsecPerKEHists.append(xsecPerKETrue)
        #legEntries.append("zWireTruePartKin")
        #incidZWireTrue, interZWireTrue = getIncidentInteractingHists(fileConfig,
        #                                            incidentCuts=modStrSyst(weightStr),
        #                                            #interactingCuts=modStrSyst(weightStr+"*(zWireLastHitWire >= 0)"),
        #                                            interactingCuts=modStrSyst("(zWireLastHitWire >= 0)*"+weightStr),
        #                                            incidentVar=modStrSyst("zWireTrueTrajKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWireTrueTrajKin[zWireLastHitWireTrue]*1e-3"),
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
        #                                            incidentCuts=modStrSyst("1"+trueGoodReco),
        #                                            interactingCuts=modStrSyst("1"+trueGoodReco),
        #                                            incidentVar=modStrSyst("PFBeamPrimKins*1e-3"),
        #                                            interactingVar=modStrSyst("PFBeamPrimKinInteract*1e-3"),
        #                                            nMax=NMAX,binning=binning)
        #xsecPerBin = getXsec(incid,inter,sliceThickness=0.5)
        #xsecPerKE = normToBinWidth(xsecPerBin.Clone(xsecPerBin.GetName()+"_perKE"))
        #incidHists.append(incid)
        #interHists.append(inter)
        #xsecPerBinHists.append(xsecPerBin)
        #xsecPerKEHists.append(xsecPerKE)
        #legEntries.append("PFBeamPrimKins Good Reco")
        #incidZWire, interZWire = getIncidentInteractingHists(fileConfig,
        #                                            incidentCuts=modStrSyst("1"+trueGoodReco),
        #                                            interactingCuts=modStrSyst("(zWireLastHitWire >= 0)"+trueGoodReco),
        #                                            incidentVar=modStrSyst("zWirePartKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
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
        #                                            incidentCuts=modStrSyst(trueFiducialCut+trueFiducialIncidHitCut),
        #                                            interactingCuts=modStrSyst("(zWireLastHitWire>=0)*"+trueFiducialCut+trueFiducialInterHitCut),
        #                                            incidentVar=modStrSyst("zWirePartKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
        #                                            nMax=NMAX,binning=binning)
        #extraIncidHists.append(incidZWireTrueFidCut)
        #extraInterHists.append(interZWireTrueFidCut)
        #extraLegEntries.append("zWirePartKin in Fid")
        #incidZWireNotTrueFidCut, interZWireNotTrueFidCut = getIncidentInteractingHists(fileConfig,
        #                                            incidentCuts=modStrSyst("(!("+trueFiducialCut+trueFiducialIncidHitCut+"))"),
        #                                            interactingCuts=modStrSyst("(zWireLastHitWire>=0)*"+"(!("+trueFiducialCut+trueFiducialInterHitCut+"))"),
        #                                            incidentVar=modStrSyst("zWirePartKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
        #                                            nMax=NMAX,binning=binning)
        #extraIncidHists.append(incidZWireNotTrueFidCut)
        #extraInterHists.append(interZWireNotTrueFidCut)
        #extraLegEntries.append("zWirePartKin Not in Fid")

        incidRecoSig, interRecoSig = getIncidentInteractingHists(fileConfig,
                                                    incidentCuts=modStrSyst(incidRecoCutsSig),
                                                    interactingCuts=modStrSyst(interRecoCutsSig),
                                                    incidentVar=modStrSyst("zWirePartKin*1e-3"),
                                                    interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
                                                    nMax=NMAX,binning=binning)
        extraIncidHists.append(incidRecoSig)
        extraInterHists.append(interRecoSig)
        extraLegEntries.append("Reco Signal")
        outrootfile.cd()
        incidRecoSig.SetName(modStrSyst.makeName("incidRecoSig"))
        incidRecoSig.Write()
        interRecoSig.SetName(modStrSyst.makeName("interRecoSig"))
        interRecoSig.Write()



        #incidRecoBkg, interRecoBkg = getIncidentInteractingHists(fileConfig,
        #                                            incidentCuts=modStrSyst(incidRecoCutsBkg),
        #                                            interactingCuts=modStrSyst(interRecoCutsBkg),
        #                                            incidentVar=modStrSyst("zWirePartKin*1e-3"),
        #                                            interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
        #                                            nMax=NMAX,binning=binning)
        incidRecoBkg = incidReco.Clone(incidReco.GetName()+"_Bkg")
        interRecoBkg = interReco.Clone(interReco.GetName()+"_Bkg")
        incidRecoBkg.Add(incidRecoSig,-1.)
        interRecoBkg.Add(interRecoSig,-1.)
        extraIncidHists.append(incidRecoBkg)
        extraInterHists.append(interRecoBkg)
        extraLegEntries.append("Reco Background")
        outrootfile.cd()
        incidRecoBkg.SetName(modStrSyst.makeName("incidRecoBkg"))
        incidRecoBkg.Write()
        interRecoBkg.SetName(modStrSyst.makeName("interRecoBkg"))
        interRecoBkg.Write()

        incidPurity = root.TEfficiency(incidRecoSig,incidReco)
        interPurity = root.TEfficiency(interRecoSig,interReco)
        plotHistsSimple([incidPurity,interPurity],["Incident","Interacting"],"Reco Hit Kinetic Energy [GeV]","Purity (Reco Signal / All Reco)",c,modStrSyst.makeName("XS","_Purity"),captionArgs=[fileConfig["caption"]],drawOptions="PEZ0")
        outrootfile.cd()
        incidPurity.SetName(modStrSyst.makeName("incidPurity"))
        incidPurity.Write()
        interPurity.SetName(modStrSyst.makeName("interPurity"))
        interPurity.Write()

        incidDenom, interDenom = getIncidentInteractingHists(fileConfig,
                                                    incidentCuts=modStrSyst(incidHitCutDenom),
                                                    interactingCuts=modStrSyst(interHitCutDenom),
                                                    incidentVar=modStrSyst("zWirePartKin*1e-3"),
                                                    interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
                                                    nMax=NMAX,binning=binning)
        extraIncidHists.append(incidDenom)
        extraInterHists.append(interDenom)
        extraLegEntries.append("Efficiency Denominator")
        outrootfile.cd()
        incidDenom.SetName(modStrSyst.makeName("incidDenom"))
        incidDenom.Write()
        interDenom.SetName(modStrSyst.makeName("interDenom"))
        interDenom.Write()
        incidNumer, interNumer = getIncidentInteractingHists(fileConfig,
                                                    incidentCuts=modStrSyst(incidHitCutNumer),
                                                    interactingCuts=modStrSyst(interHitCutNumer),
                                                    incidentVar=modStrSyst("zWirePartKin*1e-3"),
                                                    interactingVar=modStrSyst("zWirePartKin[zWireLastHitWire]*1e-3"),
                                                    nMax=NMAX,binning=binning)
        extraIncidHists.append(incidNumer)
        extraInterHists.append(interNumer)
        extraLegEntries.append("Efficiency Numerator")
        outrootfile.cd()
        incidNumer.SetName(modStrSyst.makeName("incidNumer"))
        incidNumer.Write()
        interNumer.SetName(modStrSyst.makeName("interNumer"))
        interNumer.Write()

        incidEff = root.TEfficiency(incidNumer,incidDenom)
        interEff = root.TEfficiency(interNumer,interDenom)
        outrootfile.cd()
        incidEff.SetName(modStrSyst.makeName("incidEff"))
        incidEff.Write()
        interEff.SetName(modStrSyst.makeName("interEff"))
        interEff.Write()

        plotHistsSimple([incidEff,interEff],["Incident","Interacting"],"Reco Hit Kinetic Energy [GeV]","Efficiency",c,modStrSyst.makeName("XS","_Eff"),captionArgs=[fileConfig["caption"]],drawOptions="PEZ0")
        plotHistsSimple([incidEff],None,"Incident Reco Hit Kinetic Energy [GeV]","Efficiency",c,modStrSyst.makeName("XS","_incidentEff"),captionArgs=[fileConfig["caption"]],drawOptions="PEZ0")
        plotHistsSimple([interEff],None,"Reco Interacting Kinetic Energy [GeV]","Efficiency",c,modStrSyst.makeName("XS","_interactingEff"),captionArgs=[fileConfig["caption"]],drawOptions="PEZ0")

        incidRecoBkgSub = applyBkgSub(incidReco,incidRecoBkg)
        interRecoBkgSub = applyBkgSub(interReco,interRecoBkg)
        incidRecoBkgSubEff = applyEfficiencyCorr(incidRecoBkgSub,incidEff)
        interRecoBkgSubEff = applyEfficiencyCorr(interRecoBkgSub,interEff)

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
        if systConfig["name"] == "":
          xsecHistos.append(xsecPerKEBkgSubEff)

        legEntries.append("Reco Bkg Sub'd")
        legEntries.append("Reco Bkg Sub'd & Eff. Corr.")

        outrootfile.cd()

        incidRecoBkgSub.SetName(modStrSyst.makeName("incidRecoBkgSub"))
        incidRecoBkgSub.Write()
        interRecoBkgSub.SetName(modStrSyst.makeName("interRecoBkgSub"))
        interRecoBkgSub.Write()

        incidRecoBkgSubEff.SetName(modStrSyst.makeName("incidRecoBkgSubEff"))
        incidRecoBkgSubEff.Write()
        interRecoBkgSubEff.SetName(modStrSyst.makeName("interRecoBkgSubEff"))
        interRecoBkgSubEff.Write()

        xsecPerBinBkgSub.SetName(modStrSyst.makeName("xsecPerBinBkgSub"))
        xsecPerBinBkgSub.Write()

        xsecPerBinBkgSubEff.SetName(modStrSyst.makeName("xsecPerBinBkgSubEff"))
        xsecPerBinBkgSubEff.Write()

        xsecPerKEBkgSub.SetName(modStrSyst.makeName("xsecPerKEBkgSub"))
        xsecPerKEBkgSub.Write()

      plotHistsSimple(incidHists+extraIncidHists,legEntries+extraLegEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,modStrSyst.makeName("XS","_incident"),captionArgs=[fileConfig["caption"]])
      plotHistsSimple(interHists+extraInterHists,legEntries+extraLegEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,modStrSyst.makeName("XS","_interacting"),captionArgs=[fileConfig["caption"]])
      c.SetLogy(True)
      plotHistsSimple(incidHists+extraIncidHists,legEntries+extraLegEntries,"Reco Hit Kinetic Energy [GeV]","Hits / bin",c,modStrSyst.makeName("XS","_incident_logy"),logy=True,captionArgs=[fileConfig["caption"]])
      plotHistsSimple(interHists+extraInterHists,legEntries+extraLegEntries,"Reco Interaction Kinetic Energy [GeV]","Hits / bin",c,modStrSyst.makeName("XS","_interacting_logy"),logy=True,captionArgs=[fileConfig["caption"]])
      c.SetLogy(False)

      plotHistsSimple(xsecPerBinHists,legEntries,"Reco Kinetic Energy [GeV]","Cross-section / bin [barns]",c,modStrSyst.makeName("XS","_xsPerBin"),drawOptions="E",captionArgs=[fileConfig["caption"]])
      plotHistsSimple(xsecPerKEHists,legEntries,"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,modStrSyst.makeName("XS","_xsPerGeV_wide"),drawOptions="E",captionArgs=[fileConfig["caption"]])
      plotHistsSimple(list(reversed(xsecPerKEHists)),list(reversed(legEntries)),"Reco Kinetic Energy [GeV]","d#sigma / dE_{reco} [barns / GeV]",c,modStrSyst.makeName("XS","_xsPerGeV"),drawOptions="E",ylim=[0,12],captionArgs=[fileConfig["caption"]])

      if systConfig["name"] == "":
        catConfigs=[
           {
             'title': "#pi Inelastic--good",
             'cuts':"(trueCategory>=1 && trueCategory <=4)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(trueEndZ >5.)",
             'sillyTag': True,
           },
           {
             'title': "#pi Inelastic--hit outside fiducial",
             'cuts':"(trueCategory>=1 && trueCategory <=4)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(trueEndZ >5.)",
             'sillyTag': False,
           },
           {
             'title': "#pi Inelastic--bad reco",
             'cuts':"(trueCategory>=1 && trueCategory <=4) && ((sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))>=20) || (PFBeamPrimTrueTrackID != truePrimaryTrackID))*(trueEndZ >5.)",
           },
           {
             'title': "#pi Inelastic--Interaction Outside Fiducial",
             'cuts':"(trueCategory>=1 && trueCategory <=4)*(trueEndZ <=5.)",
           },
           {
             'title': "#pi Through-going",
             'cuts':"(trueCategory==6 || trueCategory==8)",
           },
           {
             'title': "#pi Interacted Before TPC",
             'cuts':"trueCategory==7",
           },
           {
             'title': "#pi Decay",
             'cuts':"trueCategory==9 || trueCategory==10",
           },
           {
             'title': "Non-#pi Primary",
             'cuts':"trueCategory>=11 && trueCategory<=14",
           },
           {
             'title': "Unknown",
             'cuts':"trueCategory==0 || trueCategory==16 || trueCategory == 15",
           },
        ]
        # less cateogries
        catConfigs=[
           {
             'title': "#pi Inelastic--good",
             'cuts':"(trueCategory>=1 && trueCategory <=4)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(trueEndZ >5.)",
           },
           {
             'title': "#pi Inelastic--bad reco",
             'cuts':"(trueCategory>=1 && trueCategory <=4) && ((sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))>=20) || (PFBeamPrimTrueTrackID != truePrimaryTrackID))*(trueEndZ >5.)",
           },
           {
             'title': "#pi Inelastic--Interaction Outside Fiducial",
             'cuts':"(trueCategory>=1 && trueCategory <=4)*(trueEndZ <=5.)",
           },
           #{
           #  'title': "#pi Through-going",
           #  'cuts':"(trueCategory==6 || trueCategory==8)",
           #},
           {
             'title': "#pi Interacted Before TPC",
             'cuts':"trueCategory==7",
           },
           {
             'title': "#pi Decay",
             'cuts':"trueCategory==9 || trueCategory==10",
           },
           {
             'title': "Non-#pi Primary",
             'cuts':"trueCategory>=11 && trueCategory<=14",
           },
           {
             'title': "Unknown",
             'cuts':"trueCategory==0 || trueCategory==16 || trueCategory == 15",
           },
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
        catConfigsIncid = []
        catConfigsInter = []
        for iCat in range(len(catConfigs)):
            config = catConfigs[iCat]
            configIncid = copy.deepcopy(config)
            configInter = copy.deepcopy(config)
            if "sillyTag" in config:
              if config["sillyTag"]:
                configIncid['cuts'] += "*("+configIncid['cuts']+")*(zWireTrueZ < 600.)"
                configInter['cuts'] += "*("+configInter['cuts']+")*(zWireLastHitWireTrue>=0)*(zWireTrueZ[zWireLastHitWireTrue]>5.)*(zWireTrueZ[zWireLastHitWireTrue]<600.)"
              else:
                configIncid['cuts'] += "*("+configIncid['cuts']+")*(!(zWireTrueZ < 600.))"
                configInter['cuts'] += "*("+configInter['cuts']+")*(!(zWireLastHitWireTrue>=0 && zWireTrueZ[zWireLastHitWireTrue]>5. && zWireTrueZ[zWireLastHitWireTrue]<600.))"
            catConfigsIncid.append(configIncid)
            catConfigsInter.append(configInter)
        dataMCCategoryStack([],[fileConfig],histConfigs,c,"PiAbsSelector/tree",
                      outPrefix="XS_"+fileConfig["name"]+"_Stack_",nMax=NMAX,
                      #catConfigs=TRUECATEGORYFEWERCONFIGS
                      catConfigs=catConfigsIncid
                   )
        #for iCat in range(len(catConfigs)):
        #    catConfigs[iCat]['cuts'] = catConfigs[iCat]['cuts'].replace("zWireTrueZ","zWireTrueZ[zWireLastHitWireTrue]")
        histConfigs = [
          {
            'name': "Interacting",
            'title': "Interacting",
            'xtitle': "Reco Interaction Kinetic Energy [GeV]",
            'ytitle': "Track Interactions / Bin",
            'binning': binning,
            'var': "zWirePartKin[zWireLastHitWire]*1e-3",
            'cuts': "(zWireLastHitWire >= 0)*"+weightStr+interHitCut,
            'printIntegral': True,
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
            'printIntegral': True,
          },
        ]
        dataMCCategoryStack([],[fileConfig],histConfigs,c,"PiAbsSelector/tree",
                      outPrefix="XS_"+fileConfig["name"]+"_Stack_",nMax=NMAX,
                      #catConfigs=TRUECATEGORYFEWERCONFIGS
                      catConfigs=catConfigsInter
                   )

  for fileConfig, xsecHisto in zip(fileConfig,xsecHistos):
    plotHistsSimple(xsecHistos,[x["title"] for x in fileConfigs],None,None,c,"XS_All_xsPerGeV",drawOptions="E",ylim=[0,12])
  outrootfile.Close()
  print "Done."
