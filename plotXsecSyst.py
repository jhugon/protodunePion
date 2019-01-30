#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)

if __name__ == "__main__":

  c = root.TCanvas()
  hf = HistFile("XSHists.root")
  #root.gStyle.SetMarkerSize(0)
  print hf.keys()
  print hf.keysStartsWith("xsecPerBinBkgSubEff")
  if True:
    energy = "2GeV"
    hists = [
        hf["xsecPerKE_mcc11_3ms_2GeV"],
        hf["xsecPerKE_mcc11_3ms_2GeV_beamScaleUp"],
        hf["xsecPerKE_mcc11_3ms_2GeV_beamScaleDown"],
        hf["xsecPerKE_mcc11_3ms_2GeV_caloScaleUp"],
        hf["xsecPerKE_mcc11_3ms_2GeV_caloScaleDown"],
        hf["xsecPerKE_mcc11_sce_2GeV"],
        hf["xsecPerKE_mcc11_flf_2GeV"],
    ]
    titles = [
        "Nominal",
        "Beam Momentum Scale +10%",
        "Beam Momentum Scale -10%",
        "Calo Energy Scale +10%",
        "Calo Energy Scale -10%",
        "SCE",
        "SCE Fluid-flow",
    ]
    colors = COLORLIST[:len(titles)]
    caption="MCC11 {} GeV/c, No Bkg. Sub. or Eff. Corr.".format(energy[0])
    captionright1="No Bkg. Sub. or Eff. Corr."
    captionright1=""
    plotHistsSimple(hists,titles,"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_NoBkgEff_"+energy,drawOptions=["E"]+["hist"]*(len(hists)-1),captionArgs=[caption],captionKArgs={'captionright1':captionright1},colors=colors,logy=False)

    def threeHistsToErrors(nom,up,down):
      result = root.TGraphAsymmErrors()
      for iBin in range(1,nom.GetNbinsX()):
        x = nom.GetBinCenter(iBin)
        y = nom.GetBinContent(iBin)
        result.SetPoint(iBin-1,x,y)
        result.SetPoint(iBin-1,x,y)
        result.SetPointEXhigh(iBin-1,nom.GetXaxis().GetBinUpEdge(iBin)-x)
        result.SetPointEXlow(iBin-1,x-nom.GetXaxis().GetBinLowEdge(iBin))
        if up and down:
          yup = up.GetBinContent(iBin)
          ydown = down.GetBinContent(iBin)
          ymax = max([yup,ydown,y])
          ymin = min([yup,ydown,y])
          result.SetPointEYhigh(iBin-1,ymax-y)
          result.SetPointEYlow(iBin-1,y-ymin)
        else:
          yerr = nom.GetBinError(iBin)
          result.SetPointEYhigh(iBin-1,yerr)
          result.SetPointEYlow(iBin-1,yerr)
      return result

    statError = threeHistsToErrors(hists[0],None,None)
    beamScaleError = threeHistsToErrors(hists[0],hists[1],hists[2])
    caloScaleError = threeHistsToErrors(hists[0],hists[3],hists[4])
    statError.SetMarkerColor(colors[0])
    statError.SetLineColor(colors[0])
    beamScaleError.SetFillColor(COLORLIST[1])
    caloScaleError.SetFillColor(COLORLIST[2])
    beamScaleError.SetLineColor(COLORLIST[1])
    caloScaleError.SetLineColor(COLORLIST[2])
    axisHist = drawGraphs(c,[caloScaleError,beamScaleError,statError],"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",freeTopSpace=0.5,drawOptions=["5","5","PEZ"])
    leg = drawNormalLegend([statError,beamScaleError,caloScaleError],["Nominal #pm Stat.","Beam Energy Scale","Calo Energy Scale"],["lep","f","f"],wide=True)
#    axisHist = drawGraphs(c,[caloScaleError,statError],"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",freeTopSpace=0.5,drawOptions=["5","PEZ"])
#    leg = drawNormalLegend([statError,beamScaleError,caloScaleError],["Nominal #pm Stat.","Beam Energy Scale","Calo Energy Scale"],["lep","f","f"],wide=True)
    c.SaveAs("XSSyst_xsPerGeV_graphs_NoBkgEff_"+energy+".png")
    c.SaveAs("XSSyst_xsPerGeV_graphs_NoBkgEff_"+energy+".pdf")

    #c.SetLogy(True)
    for i in reversed(range(0,len(hists))):
      #if i==0: continue
      hists[i].Divide(hists[0])
    #hists.pop(0)
    #titles.pop(0)
    #colors.pop(0)
    plotHistsSimple(hists,titles,"Kinetic Energy [GeV]","Cross-section Ratio to Nominal, No-SCE",c,"XSSyst_xsPerGeV_Ratio_NoBkgEff_"+energy,drawOptions=["LEP"]+["hist"]*(len(hists)-1),captionArgs=[caption],captionKArgs={'captionright1':captionright1},colors=colors,logy=False)
    #c.SetLogy(False)

 #   hists = [
 #       hf["incidEff_mcc11_3ms_"+energy],
 #       hf["incidEff_mcc11_sce_"+energy],
 #       hf["incidEff_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE",
 #       "SCE",
 #       "Fluid-flow SCE",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Efficiency",c,"XSSyst_incidEff_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   hists = [
 #       hf["interEff_mcc11_3ms_"+energy],
 #       hf["interEff_mcc11_sce_"+energy],
 #       hf["interEff_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE",
 #       "SCE",
 #       "Fluid-flow SCE",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Efficiency",c,"XSSyst_interEff_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   hists = [
 #       hf["incidPurity_mcc11_3ms_"+energy],
 #       hf["incidPurity_mcc11_sce_"+energy],
 #       hf["incidPurity_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE",
 #       "SCE",
 #       "Fluid-flow SCE",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Purity (Signal / All)",c,"XSSyst_incidPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   hists = [
 #       hf["interPurity_mcc11_3ms_"+energy],
 #       hf["interPurity_mcc11_sce_"+energy],
 #       hf["interPurity_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE",
 #       "SCE",
 #       "Fluid-flow SCE",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Purity (Signal / All)",c,"XSSyst_interPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   hists = [
 #       hf["incidEff_mcc11_3ms_"+energy],
 #       hf["incidEff_mcc11_sce_"+energy],
 #       hf["incidEff_mcc11_flf_"+energy],
 #       hf["incidPurity_mcc11_3ms_"+energy],
 #       hf["incidPurity_mcc11_sce_"+energy],
 #       hf["incidPurity_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE Efficiency",
 #       "SCE Efficiency",
 #       "Fluid-flow SCE Efficiency",
 #       "No SCE Purity",
 #       "SCE Purity",
 #       "Fluid-flow SCE Purity",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Incident Kinetic Energy [GeV]","Efficiency or Purity",c,"XSSyst_incidEffPurity_"+energy,drawOptions="PEZ0",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   hists = [
 #       hf["interEff_mcc11_3ms_"+energy],
 #       hf["interEff_mcc11_sce_"+energy],
 #       hf["interEff_mcc11_flf_"+energy],
 #       hf["interPurity_mcc11_3ms_"+energy],
 #       hf["interPurity_mcc11_sce_"+energy],
 #       hf["interPurity_mcc11_flf_"+energy],
 #   ]
 #   titles = [
 #       "No SCE Efficiency",
 #       "SCE Efficiency",
 #       "Fluid-flow SCE Efficiency",
 #       "No SCE Purity",
 #       "SCE Purity",
 #       "Fluid-flow SCE Purity",
 #   ]
 #   caption="MCC11 {} GeV/c".format(energy[0])
 #   captionright1=""
 #   plotHistsSimple(hists,titles,"Interaction Kinetic Energy [GeV]","Efficiency or Purity",c,"XSSyst_interEffPurity_"+energy,drawOptions="PEZ",xlim=[0,8],captionArgs=[caption],captionKArgs={'captionright1':captionright1})

 #   ################################################

    incidEff3ms = hf["incidEff_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)
    interEff3ms = hf["interEff_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)
    incidBkg3ms = hf["incidRecoBkg_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)
    interBkg3ms = hf["interRecoBkg_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)
    incidReco3ms = hf["incidReco_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)
    interReco3ms = hf["interReco_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex)

    systs = [
        "",
        "_beamScaleUp",
        "_beamScaleDown",
        "_caloScaleUp",
        "_caloScaleDown",
    ]
    titles = [
        "Nominal",
        "Beam Momentum Scale +10%",
        "Beam Momentum Scale -10%",
        "Calo Energy Scale +10%",
        "Calo Energy Scale -10%",
    ]
    histsXsecBkgSubEff = []
    histsXsecRaw = []
    histsIncidRecoBkgSub = []
    histsInterRecoBkgSub = []
    histsIncidReco = []
    histsIncidBkg3msScaled = []
    histsIncidBkg = []
    histsInterBkg = []
    histsIncidEff = []
    histsInterEff = []
    for syst in systs:
      sample = "3ms"
      incidReco = hf["incidReco_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex)
      interReco = hf["interReco_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex)
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
      xsecBkgSubEff = getXsec(incidRecoBkgSubEff,interRecoBkgSubEff,sliceThickness=0.5)
      xsecRaw = getXsec(incidReco,interReco,sliceThickness=0.5)
      normToBinWidth(xsecBkgSubEff)
      normToBinWidth(xsecRaw)
      histsXsecBkgSubEff.append(xsecBkgSubEff)
      histsXsecRaw.append(xsecRaw)
      histsIncidRecoBkgSub.append(incidRecoBkgSub)
      histsInterRecoBkgSub.append(interRecoBkgSub)
      histsIncidReco.append(incidReco)
      histsIncidBkg3msScaled.append(incidBkg3msScaled)
      histsIncidBkg.append(hf["incidRecoBkg_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex))
      histsInterBkg.append(hf["interRecoBkg_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex))
      histsIncidEff.append(hf["incidEff_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex))
      histsInterEff.append(hf["interEff_mcc11_{}_{}{}".format(sample,energy,syst)].Clone(uuid.uuid1().hex))
    histsIncidEff.append(hf["incidEff_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex))
    histsInterEff.append(hf["interEff_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex))
    histsXsecBkgSubEff.append(hf["xsecPerBinBkgSubEff_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex))
    histsXsecRaw.append(hf["xsecPerBin_mcc11_3ms_"+energy].Clone(uuid.uuid1().hex))

    captionright1="Uncorrected"
    plotHistsSimple(histsIncidReco,titles,"Kinetic Energy [GeV]","Incident Hits / bin",c,"XSSyst_incidReco_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1=""
    plotHistsSimple(histsIncidBkg+histsIncidBkg3msScaled,[t+" Own" for t in titles]+[t+" Scaled 3ms" for t in titles],"Kinetic Energy [GeV]","Incident Hits Background Estimate / bin",c,"XSSyst_incidBkg_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1="Using 3ms Bkg., No Eff. Corr."
    plotHistsSimple(histsIncidRecoBkgSub,titles,"Kinetic Energy [GeV]","Incident Hits / bin",c,"XSSyst_incidReco_3msBkg_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    titles.append("From plotXsec.py")

    captionright1=""
    plotHistsSimple(histsIncidEff,titles,"Kinetic Energy [GeV]","Incident Efficiency",c,"XSSyst_incidEff_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})
    plotHistsSimple(histsInterEff,titles,"Kinetic Energy [GeV]","Interaction Efficiency",c,"XSSyst_interEff_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1="Raw Reco"
    plotHistsSimple(histsXsecRaw,titles,"Kinetic Energy [GeV]","Raw Reco d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_Raw_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    captionright1="Using 3ms Bkg. & Eff."
    plotHistsSimple(histsXsecBkgSubEff,titles,"Kinetic Energy [GeV]","d#sigma / dE [barn / GeV]",c,"XSSyst_xsPerGeV_3msBkgEff_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1})

    for i in reversed(range(0,len(histsXsecBkgSubEff))):
      histsXsecBkgSubEff[i].Divide(histsXsecBkgSubEff[0])
    c.SetLogy(True)
    plotHistsSimple(histsXsecBkgSubEff,titles,"Kinetic Energy [GeV]","Cross-section Ratio to Nominal",c,"XSSyst_xsPerGeV_3msBkgEff_Ratio_"+energy,drawOptions="E",captionArgs=[caption],captionKArgs={'captionright1':captionright1},logy=True,ylim=[0,2.5])
    c.SetLogy(False)
  
