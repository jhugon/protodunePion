#!/usr/bin/env python

from misc import *
from plotters import plotOneHistOnePlot

def getIncidentInteractingHists(fileConfig,
                    incidentCuts="",interactingCuts="",
                    incidentVar="PFBeamPrimKins*1e-3",interactingVar="PFBeamPrimKinInteract*1e-3",
                treeName="PiAbsSelector/tree",
                binning=[1500,0.,7.5],
                nMax=sys.maxint):
  if type(fileConfig) != dict:
    raise Exception("fileConfig must be dict, not list or something. Is: ",type(fileConfig))
  c1 = root.TCanvas(uuid.uuid1().hex)
  plotOneHistOnePlot
  histConfigs = [
    {
      'name': "Incident",
      'title': "Incident",
      'xtitle': "Reco Kinetic Energy [MeV]",
      'ytitle': "Track Hits / MeV",
      'binning': binning,
      'var': incidentVar,
      'cuts': incidentCuts,
    },
    {
      'name': "Interacting",
      'title': "Interacting",
      'xtitle': "Reco Kinetic Energy [MeV]",
      'ytitle': "Track Interactions / MeV",
      'binning': binning,
      'var': interactingVar,
      'cuts': interactingCuts,
    },
  ]
  kinHists = plotOneHistOnePlot([fileConfig],histConfigs,c1,treeName,nMax=nMax,writeImages=False)
  incidentHist = kinHists["Incident"][fileConfig["name"]]
  interactingHist = kinHists["Interacting"][fileConfig["name"]]
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

