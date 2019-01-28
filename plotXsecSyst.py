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
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1="Using Own Bkg. & Eff."
    plotHistsSimple(hists,titles,"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_OwnBkgEff_"+energy,drawOptions="E",xlim=[0,8],ylim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["incidEff_mcc11_3ms_"+energy],
        hf["incidEff_mcc11_sce_"+energy],
        hf["incidEff_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Efficiency",c,"XSSyst_incidEff_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["interEff_mcc11_3ms_"+energy],
        hf["interEff_mcc11_sce_"+energy],
        hf["interEff_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Efficiency",c,"XSSyst_interEff_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["incidPurity_mcc11_3ms_"+energy],
        hf["incidPurity_mcc11_sce_"+energy],
        hf["incidPurity_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Purity (Signal / All)",c,"XSSyst_incidPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["interPurity_mcc11_3ms_"+energy],
        hf["interPurity_mcc11_sce_"+energy],
        hf["interPurity_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Purity (Signal / All)",c,"XSSyst_interPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["incidEff_mcc11_3ms_"+energy],
        hf["incidEff_mcc11_sce_"+energy],
        hf["incidEff_mcc11_flf_"+energy],
        hf["incidPurity_mcc11_3ms_"+energy],
        hf["incidPurity_mcc11_sce_"+energy],
        hf["incidPurity_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE Efficiency",
        "SCE Efficiency",
        "Fluid-flow SCE Efficiency",
        "No SCE Purity",
        "SCE Purity",
        "Fluid-flow SCE Purity",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Efficiency or Purity",c,"XSSyst_incidEffPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    hists = [
        hf["interEff_mcc11_3ms_"+energy],
        hf["interEff_mcc11_sce_"+energy],
        hf["interEff_mcc11_flf_"+energy],
        hf["interPurity_mcc11_3ms_"+energy],
        hf["interPurity_mcc11_sce_"+energy],
        hf["interPurity_mcc11_flf_"+energy],
    ]
    titles = [
        "No SCE Efficiency",
        "SCE Efficiency",
        "Fluid-flow SCE Efficiency",
        "No SCE Purity",
        "SCE Purity",
        "Fluid-flow SCE Purity",
    ]
    caption="MCC11 {} GeV/c".format(energy[0])
    captionright1=""
    plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Efficiency or Purity",c,"XSSyst_interEffPurity_"+energy,drawOptions="PEZ",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    ################################################

    incidEff3ms = hf["incidEff_mcc11_3ms_"+energy]
    interEff3ms = hf["interEff_mcc11_3ms_"+energy]
    incidBkg3ms = hf["incidRecoBkg_mcc11_3ms_"+energy]
    interBkg3ms = hf["interRecoBkg_mcc11_3ms_"+energy]
    incidReco3ms = hf["incidReco_mcc11_3ms_"+energy]
    interReco3ms = hf["interReco_mcc11_3ms_"+energy]

    titles = [
        "No SCE",
        "SCE",
        "Fluid-flow SCE",
    ]
    histsXsecBkgSubEff = []
    histsIncidRecoBkgSub = []
    histsInterRecoBkgSub = []
    histsIncidReco = []
    histsIncidBkg3msScaled = []
    histsIncidBkg = []
    for sample in ["3ms","sce","flf"]:
      incidReco = hf["incidReco_mcc11_{}_{}".format(sample,energy)]
      interReco = hf["incidReco_mcc11_{}_{}".format(sample,energy)]
      incidBkg3msScaled = incidBkg3ms.Clone(incidBkg3ms.GetName()+"_scaled_"+sample)
      incidBkg3msScaled.Multiply(incidReco)
      incidBkg3msScaled.Divide(incidReco3ms)
      interBkg3msScaled = interBkg3ms.Clone(interBkg3ms.GetName()+"_scaled_"+sample)
      interBkg3msScaled.Multiply(interReco)
      interBkg3msScaled.Divide(interReco3ms)
      incidRecoBkgSub = applyBkgSub(incidReco,incidBkg3msScaled)
      interRecoBkgSub = applyBkgSub(interReco,interBkg3msScaled)
      incidRecoBkgSubEff = applyEfficiencyCorr(incidRecoBkgSub,incidEff3ms)
      interRecoBkgSubEff = applyEfficiencyCorr(interRecoBkgSub,interEff3ms)
      xsec = getXsec(incidRecoBkgSubEff,interRecoBkgSubEff)
      normToBinWidth(xsec)
      histsXsecBkgSubEff.append(xsec)
      histsIncidRecoBkgSub.append(incidRecoBkgSub)
      histsInterRecoBkgSub.append(interRecoBkgSub)
      histsIncidReco.append(incidReco)
      histsIncidBkg3msScaled.append(incidBkg3msScaled)
      histsIncidBkg.append(hf["incidRecoBkg_mcc11_{}_{}".format(sample,energy)])
    histsXsecBkgSubEff.append(hf["xsecPerBinBkgSubEff_mcc11_3ms_"+energy])

    captionright1="Uncorrected"
    plotHistsSimple(histsIncidReco,titles,"Kinetic Energy [GeV]","Incident Hits / bin",c,"XSSyst_incidReco_"+energy,drawOptions="E",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1=""
    plotHistsSimple(histsIncidBkg+histsIncidBkg3msScaled,[t+" Own" for t in titles]+[t+" Scaled 3ms" for t in titles],"Kinetic Energy [GeV]","Incident Hits Background Estimate / bin",c,"XSSyst_incidBkg_"+energy,drawOptions="E",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1="Using 3ms Bkg., No Eff. Corr."
    plotHistsSimple(histsIncidRecoBkgSub,titles,"Kinetic Energy [GeV]","Incident Hits / bin",c,"XSSyst_incidReco_3msBkg_"+energy,drawOptions="E",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    titles.append("From plotXsec.py")
    captionright1="Using 3ms Bkg. & Eff."
    plotHistsSimple(histsXsecBkgSubEff,titles,"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_3msBkgEff_"+energy,drawOptions="E",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})
  
