#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  cuts = ""

  weightStr = "1"+cuts

  logy = False

  c = root.TCanvas()
  f = root.TFile("PiAbsSelector.root")
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamline"),None,None,c,"Matching_deltaXYTPCBeamline_wide",captionArgs=["MCC10, 2GeV SCE"],rebin=[50,50])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamline"),None,None,c,"Matching_deltaXYTPCBeamline",captionArgs=["MCC10, 2GeV SCE"],xlims=[-50,50],ylims=[-50,50],rebin=[5,5])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamlineOnlyBeamPrimaries"),None,None,c,"Matching_deltaXYTPCBeamlineOnlyBeamPrimaries_wide",captionArgs=["MCC10, 2GeV SCE"],rebin=[10,10])
  plotHist2DSimple(f.Get("PiAbsSelector/deltaXYTPCBeamlineOnlyBeamPrimaries"),None,None,c,"Matching_deltaXYTPCBeamlineOnlyBeamPrimaries",captionArgs=["MCC10, 2GeV SCE"],xlims=[-50,50],ylims=[-50,50],rebin=[5,5])
