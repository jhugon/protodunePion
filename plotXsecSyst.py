#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  c = root.TCanvas()
  hf = HistFile("XSHists.root")
  #root.gStyle.SetMarkerSize(0)
  print hf.keys()
  for energy in ["1GeV","2GeV","7GeV"]:
    hists = [
        hf["xsecPerBinBkgSubEff_mcc11_3ms_"+energy],
        hf["xsecPerBinBkgSubEff_mcc11_sce_"+energy],
        hf["xsecPerBinBkgSubEff_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    plotHistsSimple(hists,titles,"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_"+energy,drawOptions="E",xlim=[0,8],ylim=[0,8])
  
