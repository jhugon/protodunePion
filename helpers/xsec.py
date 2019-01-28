#!/usr/bin/env python

from misc import *
from plotters import plotOneHistOnePlot

def getIncidentInteractingHists(fileConfig,
                    incidentCuts="",interactingCuts="",
                    incidentVar="PFBeamPrimKins*1e-3",interactingVar="PFBeamPrimKinInteract*1e-3",
                treeName="PiAbsSelector/tree",
                binning=[1500,0.,7.5],
                nMax=sys.maxint,
                printIntegral=False
                ):
  if type(fileConfig) != dict:
    raise Exception("fileConfig must be dict, not list or something. Is: ",type(fileConfig))
  c1 = root.TCanvas(uuid.uuid1().hex)
  histConfigs = [
    {
      'name': "Incident",
      'title': "Incident",
      'xtitle': "Reco Kinetic Energy [MeV]",
      'ytitle': "Track Hits / MeV",
      'binning': binning,
      'var': incidentVar,
      'cuts': incidentCuts,
      'printIntegral': printIntegral,
    },
    {
      'name': "Interacting",
      'title': "Interacting",
      'xtitle': "Reco Kinetic Energy [MeV]",
      'ytitle': "Track Interactions / MeV",
      'binning': binning,
      'var': interactingVar,
      'cuts': interactingCuts,
      'printIntegral': printIntegral,
    },
  ]
  #print "incid histCuts: ", histConfigs[0]['cuts']
  #print "inter histCuts: ", histConfigs[1]['cuts']
  kinHists = plotOneHistOnePlot([fileConfig],histConfigs,c1,treeName,nMax=nMax,writeImages=False)
  incidentHist = kinHists["Incident"][fileConfig["name"]]
  interactingHist = kinHists["Interacting"][fileConfig["name"]]
  #print fileConfig["name"]
  #fileConfig["tree"].Print()
  return incidentHist,interactingHist

def getXsec(incident,interacting,
        sliceThickness = 0.5, # cm
        rebin = 1,
        ardensity = 1.3954 # g / cm3
    ):

  interacting.Rebin(rebin)
  incident.Rebin(rebin)
  xsec = interacting.Clone(interacting.GetName()+"xsec")
  xsec.Divide(incident)
  #
  molardensity = 39.948 #g / mol
  avagadro = 6.022140857e23
  numberdensity = ardensity * avagadro / molardensity # particles / cm3
  scaleFactorcm = 1./(numberdensity*sliceThickness) # cm2 / particles
  scaleFactorBarn = 1e24 * scaleFactorcm # barn / particles
  #
  xsec.Scale(scaleFactorBarn)
  return xsec

def applyBkgSub(reco,bkg):
  assert(reco.GetNbinsX() == bkg.GetNbinsX())
  result = reco.Clone(reco.GetName()+"_BkgSub")
  for iBin in range(1,reco.GetNbinsX()+1):
    recoVal = reco.GetBinContent(iBin)
    recoErr = reco.GetBinError(iBin)
    bkgSubVal = recoVal - bkg.GetBinContent(iBin)
    bkgSubErr = recoErr
    result.SetBinContent(iBin,bkgSubVal)
    result.SetBinError(iBin,bkgSubErr)
  return result

def applyEfficiencyCorr(reco,eff,defaultErr=10.):
  assert(reco.GetNbinsX() == eff.GetTotalHistogram().GetNbinsX())
  result = reco.Clone(reco.GetName()+"_EffCorr")
  for iBin in range(1,reco.GetNbinsX()+1):
    recoVal = reco.GetBinContent(iBin)
    recoErr = reco.GetBinError(iBin)
    effVal = eff.GetEfficiency(iBin)
    recoEffCorVal = 0.
    if effVal > 0.:
      recoEffCorVal = recoVal/effVal
    recoEffCorErr = defaultErr
    if effVal > 0.:
      recoEffCorVal = recoErr/effVal
    result.SetBinContent(iBin,recoEffCorVal)
    result.SetBinError(iBin,recoEffCorErr)
  return result
