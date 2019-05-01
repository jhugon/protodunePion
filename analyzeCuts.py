#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys
import signal
import multiprocessing
import time

def getNDecPlacesStr(parError):
  if parError >= 10:
    return '0'
  sfs = -math.log10(parError)
  sfs = abs(math.ceil(sfs))
  return "{:.0f}".format(sfs)

def makeFRDict(fitresult):
  frDict = {}
  frDict["chi2"] = "{:.2f}".format(fitresult.Chi2()/fitresult.Ndf())
  nDigits = getNDecPlacesStr(fitresult.ParError(1))
  frDict["mu"] = ("{:."+nDigits+"f}").format(fitresult.Value(1))
  frDict["muErr"] = ("{:."+nDigits+"f}").format(fitresult.ParError(1))
  nDigits = getNDecPlacesStr(fitresult.ParError(2))
  frDict["sigma"] = ("{:."+nDigits+"f}").format(fitresult.Value(2))
  frDict["sigmaErr"] = ("{:."+nDigits+"f}").format(fitresult.ParError(2))
  return frDict

def getAvgMuSigma(frs):
  n = len(frs)
  mus = [fr.Value(1) for fr in frs]
  muErrs = [fr.ParError(1) for fr in frs]
  sigs = [fr.Value(2) for fr in frs]
  sigErrs = [fr.ParError(2) for fr in frs]
  muVars = [x**2 for x in muErrs]
  sigVars = [x**2 for x in sigErrs]
  muWeights = [1./x for x in muVars]
  sigWeights = [1./x for x in sigVars]
  muSumWeights = sum(muWeights)
  sigSumWeights = sum(sigWeights)
  muMean = sum([mus[i]*muWeights[i] for i in range(n)])/muSumWeights
  sigMean = sum([sigs[i]*sigWeights[i] for i in range(n)])/sigSumWeights
  muMeanError = (muSumWeights)**(-0.5)
  sigMeanError = (sigSumWeights)**(-0.5)
  muDigits = getNDecPlacesStr(muMeanError)
  sigDigits = getNDecPlacesStr(sigMeanError)
  muMean = ("{:."+muDigits+"f}").format(muMean)
  sigMean = ("{:."+sigDigits+"f}").format(sigMean)
  muMeanError = ("{:."+muDigits+"f}").format(muMeanError)
  sigMeanError = ("{:."+sigDigits+"f}").format(sigMeanError)

  return muMean, muMeanError, sigMean, sigMeanError
        

def drawGausFitCaptions(*args,**kargs):
  """
  call as drawGausFitCaptions(canvas, topCaption, fitresultPointer, ... args to drawStandardCaptions)
  """

  args = list(args)
  fitresult = args.pop(2)
  kargs["captionright1"] = "#chi^{{2}}/NDF = {:.2f}".format(fitresult.Chi2()/fitresult.Ndf())
  nDigits = getNDecPlacesStr(fitresult.ParError(1))
  kargs["captionright2"] = ("#mu = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(1),fitresult.ParError(1))
  nDigits = getNDecPlacesStr(fitresult.ParError(2))
  kargs["captionright3"] = ("#sigma = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(2),fitresult.ParError(2))
  nDigits = getNDecPlacesStr(fitresult.ParError(0))
  kargs["captionright4"] = ("Const = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(0),fitresult.ParError(0))
  drawStandardCaptions(*args,**kargs)

def fitGauss(hist,histName,sampleName):
  #medianBin = getHistMedian(hist)
  #median = hist.GetXaxis().GetBinCenter(medianBin)
  mean = hist.GetMean()
  rms = hist.GetRMS()
  fitResult = None
  binWidth = hist.GetXaxis().GetBinWidth(1)
  if rms < 1.5*binWidth:
    print "Warning: rms <= 1.5* bin width for '{}' '{}' with mean {:.2f} rms: {:.2f}, bin width: {.2f}, trying rms = 3*binWidth".format(histName,sampleName,mean,rms,binWidth)
    rms = 3*binWidth
  for iTry in range(5):
    fitResult = hist.Fit("gaus","WLQMS","",mean-rms,mean+rms)
    #fitResult.Print()
    if not fitResult.IsValid() or fitResult.Ndf()==0:
      hist.SetTitle(sampleName)
      hist.Draw("")
      hist.GetXaxis().SetRangeUser(mean-5*rms,mean+5*rms)
      drawStandardCaptions(c,"",captionright1="fit range: {:.2f} to  {:.2f}".format(mean-rms,mean+rms),captionright2="NDF: {}".format(fitResult.Ndf()),captionleft3="mean: {:.2f}".format(hist.GetMean()),captionleft2="RMS = {:.2f}".format(hist.GetRMS()),captionleft1="bin width: {}".format(binWidth))
      c.SaveAs("AnalyzeCuts_widthTest_"+histName+'_'+sampleName+".png")
      c.SaveAs("AnalyzeCuts_widthTest_"+histName+'_'+sampleName+".pdf")
      return fitResult
    normChi2 = fitResult.Chi2()/fitResult.Ndf()
    if normChi2 < 3:
      break
    elif rms <= 2.5*binWidth:
      print "Warning: bad fit,chi2/ndf: {:.2f}, of gauss to '{}' '{}' with mean {:.2f} rms: {:.2f}, and rms on order of bin width: {:.2f}. Stopping trying.".format(normChi2,histName,sampleName,mean,rms,binWidth)
      break
    else:
      print "Warning: bad fit,chi2/ndf: {:.2f}, of gauss to '{}' '{}' with mean {:.2f} rms: {:.2f}, trying rms *= 0.5".format(normChi2,histName,sampleName,mean,rms)
      rms *= 0.75
  #fitResult.Print()
  #axisHist = makeStdAxisHist([hist],freeTopSpace=0.1,includeErrorBar=True,xlim=[-1,3])
  #axisHist.Draw()
  hist.GetXaxis().SetRangeUser(mean-3*rms,mean+3*rms)
  hist.SetTitle(sampleName)
  hist.Draw("")
  #drawGausFitCaptions(c,"",fitResult,captionleft3="mean: {:.2f}".format(hist.GetMean()),captionleft2="RMS = {:.2f}".format(hist.GetRMS()),captionleft1="median = {:.1f}".format(median))
  drawGausFitCaptions(c,"",fitResult)
  c.SaveAs("AnalyzeCuts_widthTest_"+histName+'_'+sampleName+".png")
  c.SaveAs("AnalyzeCuts_widthTest_"+histName+'_'+sampleName+".pdf")
  return fitResult

def getMeansSigmas(c,fns,histTitles,sampleTitles):
  results = []
  for fn in sorted(fns):
    f = root.TFile(fn)
    sampleMatch = re.match(r"Inelastic_(.+).root",fn)
    if not sampleMatch:
        raise Exception("Couldn't parse filename: ",fn)
    sampleName = sampleMatch.group(1)
    for key in sorted(f.GetListOfKeys()):
      name = key.GetName()
      #print name
      matchMCSum = re.match(r"(.+)_mcSumHist",name)
      matchMCC11 = re.match(r"(.+)_(mcc11.*)",name)
      matchRun = re.match(r"(.+)_run(.+)",name)
      histName = None
      subSampleName = None
      if matchMCSum:
        histName = matchMCSum.group(1)
        subSampleName = "mcSumHist"
      elif matchMCC11:
        continue
      elif matchRun:
        histName = matchRun.group(1)
        subSampleName = matchRun.group(2)
      #print bool(matchMCSum), bool(matchMCC11), bool(matchRun)
      if not ("Delta" in histName) and not ("PFBeamPrimAngleStartBI" in histName):
        continue
      if "wide" in histName:
        continue
      hist = key.ReadObj()
      fr = fitGauss(hist,histName,sampleName+"_"+subSampleName)
      results.append((histName,sampleName,subSampleName,fr))
  resultsDict = {}
  for result in results:
    histName = result[0]
    sampleName = sampleTitles[result[1]]
    if not (histName in resultsDict):
      resultsDict[histName] = {}
    if not (sampleName in resultsDict[histName]):
      resultsDict[histName][sampleName] = {}
    subName = "Data"
    if ("mc" in result[2]):
      subName = "MC"
    resultsDict[histName][sampleName][subName] = result[3]
  print "          &        "+5*r" & {Data}"+ 5*" & {MC}"+r" \\"
  print " Variable & Sample "+2*r" & {$\mu$} & {$\mu$ Error} & {$\sigma$} & {$\sigma$ Error} &{$\chi^2$/NDF}"+r" \\ \toprule"
  finalResult = {}
  for iHistName, histName in enumerate(sorted(resultsDict)):
    histTitle = histTitles[histName]
    for iSampleName, sampleName in enumerate(sorted(resultsDict[histName])):
      frDictData = makeFRDict(resultsDict[histName][sampleName]["Data"])
      frDictMC =  makeFRDict(resultsDict[histName][sampleName]["MC"])
      outStr = r"{} & {} & {}& {} & {} & {} & {} & {} & {} & {} & {} & {} \\".format(histTitle,sampleName,
                                frDictData["mu"],frDictData["muErr"],frDictData["sigma"],frDictData["sigmaErr"],frDictData["chi2"],
                                frDictMC["mu"],frDictMC["muErr"],frDictMC["sigma"],frDictMC["sigmaErr"],frDictMC["chi2"]
                        )
      print outStr
    muMeanData, muMeanErrData, sigMeanData, sigMeanErrData = getAvgMuSigma([resultsDict[histName][sampleName]["Data"] for sampleName in resultsDict[histName]])
    muMeanMC, muMeanErrMC, sigMeanMC, sigMeanErrMC = getAvgMuSigma([resultsDict[histName][sampleName]["MC"] for sampleName in resultsDict[histName]])
    finalResult[histName] = (float(muMeanData),float(sigMeanData),float(muMeanMC),float(sigMeanMC))
    print r"\midrule"
    print r"{} & {} & {}& {} & {} & {} & {} & {} & {} & {} & {} & {} \\".format(histTitle,"Weighted Mean",
                                 muMeanData,muMeanErrData,sigMeanData,sigMeanErrData,"",
                                 muMeanMC,muMeanErrMC,sigMeanMC,sigMeanErrMC,""
                         )
    print r"\midrule"
  return finalResult
    
def getEffPurOfGausCuts(c,fns,histTitlesRoot,sampleTitlesRoot,gausParams):
  allCurves = {}
  allCurvesSig = {}
  rootFiles = []
  for fn in sorted(fns):
    f = root.TFile(fn)
    rootFiles.append(f)
    sampleMatch = re.match(r"Inelastic_(.+).root",fn)
    if not sampleMatch:
        raise Exception("Couldn't parse filename: ",fn)
    sampleName = sampleMatch.group(1)
    for key in sorted(f.GetListOfKeys()):
      name = key.GetName()
      #print name
      matchMCSum = re.match(r"(.+)_mcSumHist",name)
      matchMCC11 = re.match(r"(.+)_(mcc11.*)",name)
      matchRun = re.match(r"(.+)_run(.+)",name)
      histName = None
      subSampleName = None
      if matchMCSum:
        histName = matchMCSum.group(1)
        subSampleName = "mcSumHist"
      elif matchMCC11:
        histName = matchMCC11.group(1)
        subSampleName = matchMCC11.group(2)
      elif matchRun:
        histName = matchRun.group(1)
        subSampleName = sampleName
      if histName in gausParams:
        hist = key.ReadObj()
        muMeanData,sigMeanData,muMeanMC,sigMeanMC = gausParams[histName]
        #muMean = muMeanData
        #sigMean = sigMeanData
        #if not matchRun:
        #  muMean = muMeanMC
        #  sigMean = sigMeanMC
        muMean = muMeanMC
        sigMean = sigMeanMC
        iBinMean = hist.FindBin(muMean)
        binMeanCenter = hist.GetXaxis().GetBinCenter(iBinMean)
        binMeanWidth = hist.GetXaxis().GetBinWidth(iBinMean)
        nBins = hist.GetNbinsX()
        #print muMean, iBinMean, binMeanCenter, nBins, hist.GetXaxis().GetBinLowEdge(1), hist.GetXaxis().GetBinUpEdge(nBins)
        nSteps = max(nBins-iBinMean,iBinMean-1)
        nSigmasMax = 20.
        nSteps = int(math.ceil(min(nSteps,nSigmasMax*sigMean/binMeanWidth)))
        histBinning = [nSteps,0,nSteps*binMeanWidth]
        histSigBinning = [nSteps,0,nSteps*binMeanWidth/sigMean]
        intHist = Hist(*histBinning)
        intSigHist = Hist(*histSigBinning)
        for iStep in range(nSteps):
          lowBin = max(iBinMean-iStep,1)
          highBin = min(iBinMean+iStep,nBins)
          width = hist.GetXaxis().GetBinUpEdge(highBin)-hist.GetXaxis().GetBinLowEdge(lowBin)
          count = hist.Integral(lowBin,highBin)
          widthSigmas = width/sigMean
          intHist.SetBinContent(iStep+2,count)
          intHist.SetBinError(iStep+2,count**0.5)
          intSigHist.SetBinContent(iStep+2,count)
          intSigHist.SetBinError(iStep+2,count**0.5)
          #if iStep == 0:
          #  print iStep, lowBin, highBin, width, widthSigmas, count
          #  print intHist.GetXaxis().GetBinLowEdge(iStep+2), intHist.GetXaxis().GetBinUpEdge(iStep+2)
          #  print intSigHist.GetXaxis().GetBinLowEdge(iStep+2), intSigHist.GetXaxis().GetBinUpEdge(iStep+2)
        intAll = hist.Integral(0,hist.GetNbinsX()+1) # include under/overflow
        intHist.SetBinContent(nSteps+1,intAll)
        intSigHist.SetBinContent(nSteps+1,intAll)
        if not (histName in allCurves):
          allCurves[histName] = {}
          allCurvesSig[histName] = {}
        if not (sampleName in allCurves[histName]):
          allCurves[histName][sampleName] = {}
          allCurvesSig[histName][sampleName] = {}
        allCurves[histName][sampleName][subSampleName] = intHist
        allCurvesSig[histName][sampleName][subSampleName] = intSigHist
  for iHistName, histName in enumerate(sorted(allCurves)):

    sampleTitles = []
    sampleGoodTrackMatchHists = []
    sampleGoodTrackMatchHistsSig = []
    sampleGoodTrackMatchPurityHists = []
    sampleGoodTrackMatchPurityHistsSig = []
    for iSampleName, sampleName in enumerate(sorted(allCurves[histName])):

      fileConfigsMC = [
        {
          'name': "mcc11_piInel_good",
          'title': "MCC11 #pi Inelastic--Good Reco",
        },
        {
          'name': "mcc11_piInel_badIntMatch",
          'title': "MCC11 #pi Inelastic--Bad Reco/True Interaction Match",
        },
        {
          'name': "mcc11_piInel_badTrkMatch",
          'title': "MCC11 #pi Inelastic--Bad Track/True Primary Match",
        },
        {
          'name': "mcc11_piDecay",
          'title': "MCC11 #pi Decay",
        },
        {
          'name': "mcc11_piOutsideTPC",
          'title': "MCC11 #pi Interacted Outside TPC",
        },
        {
          'name': "mcc11_mu",
          'title': "MCC11 Primary Muon",
        },
      ]
      if ('6GeV' in sampleName) or ('7GeV' in sampleName):
        fileConfigsMC.append({
          'name': "mcc11_e",
          'title': "MCC11 Primary Electron",
        })

      hists = []
      histsSig = []
      labels = []
      stack = root.THStack("histStack_{}_{}_noSig".format(histName,sampleName),"")
      stackSig = root.THStack("histStack_{}_{}_sigig".format(histName,sampleName),"")
      sumHist = allCurves[histName][sampleName]["mcSumHist"]
      sumHistSig = allCurvesSig[histName][sampleName]["mcSumHist"]
      dataHist = allCurves[histName][sampleName][sampleName]
      dataHistSig = allCurvesSig[histName][sampleName][sampleName]
      #for iSubSampleName, subSampleName in enumerate(sorted(allCurves[histName][sampleName])):
      for iSubSampleName, subSampleConfig in enumerate(fileConfigsMC):
        subSampleName = subSampleConfig['name']
        hist = allCurves[histName][sampleName][subSampleName]
        #hist = hist.Clone(hist.GetName()+"_norm")
        #hist.Scale(1./hist.GetBinContent(hist.GetNbinsX()+1))
        histSig = allCurvesSig[histName][sampleName][subSampleName]
        #histSig = histSig.Clone(histSig.GetName()+"_norm")
        #histSig.Scale(1./histSig.GetBinContent(histSig.GetNbinsX()+1))
        hists.append(hist)
        histsSig.append(histSig)
        labels.append(subSampleConfig['title'])
      for i in range(len(labels)):
        hists[i].SetFillColor(COLORLIST[i])
        hists[i].SetLineColor(COLORLIST[i])
        histsSig[i].SetFillColor(COLORLIST[i])
        histsSig[i].SetLineColor(COLORLIST[i])
        #nBins = hists[i].GetNbinsX()
        #for iBin in range(1,nBins+1):
        #  if sumHist.GetBinContent(iBin) > 0:
        #    hists[i].SetBinContent(iBin,hists[i].GetBinContent(iBin)/sumHist.GetBinContent(iBin))
        #  if sumHistSig.GetBinContent(iBin) > 0:
        #    histsSig[i].SetBinContent(iBin,histsSig[i].GetBinContent(iBin)/sumHistSig.GetBinContent(iBin))
      for i in reversed(range(len(labels))):
        stack.Add(hists[i])
        stackSig.Add(histsSig[i])
      axisHist = makeStdAxisHist([sumHist])
      setHistTitles(axisHist,"Cut Width: "+histTitlesRoot[histName]+" [cm]","Events")
      axisHist.Draw()
      stack.Draw("histsame")
      #dataHist.Draw("same")
      leg = drawNormalLegend(hists,labels,option='f',wide=True)
      c.RedrawAxis()
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.SaveAs("AnalyzeCuts_width_comb_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_width_comb_{}_{}.pdf".format(histName,sampleName))
      axisHistSig = makeStdAxisHist([sumHistSig],xlim=[0,5])
      setHistTitles(axisHistSig,"Cut Width: "+histTitlesRoot[histName]+" [#sigma]","Events")
      axisHistSig.Draw()
      stackSig.Draw("histsame")
      #dataHistSig.Draw("same")
      legSig = drawNormalLegend(histsSig,labels,option='f',wide=True)
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.RedrawAxis()
      c.SaveAs("AnalyzeCuts_widthSig_comb_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_widthSig_comb_{}_{}.pdf".format(histName,sampleName))

      #plotHistsSimple(hists,labels,"Cut Width: "+histTitlesRoot[histName]+" [cm]","Events",c,"AnalyzeCuts_width_comb_{}_{}".format(histName,sampleName),captionArgs=[sampleTitlesRoot[sampleName]])
      #plotHistsSimple(histsSig,labels,"Cut Width: "+histTitlesRoot[histName]+" [#sigma]","Events",c,"AnalyzeCuts_widthSig_comb_{}_{}".format(histName,sampleName),captionArgs=[sampleTitlesRoot[sampleName]])

      goodTrackMatchHist = hists[0].Clone(hists[0].GetName()+"_goodTrackMatch")
      goodTrackMatchHist.Add(hists[1])
      goodTrackMatchHistSig = histsSig[0].Clone(histsSig[0].GetName()+"_goodTrackMatch")
      goodTrackMatchHistSig.Add(histsSig[1])
      goodTrackMatchHist.Scale(1./goodTrackMatchHist.GetBinContent(goodTrackMatchHist.GetNbinsX()+1))
      goodTrackMatchHistSig.Scale(1./goodTrackMatchHistSig.GetBinContent(goodTrackMatchHistSig.GetNbinsX()+1))
      sampleGoodTrackMatchHists.append(goodTrackMatchHist)
      sampleGoodTrackMatchHistsSig.append(goodTrackMatchHistSig)

      stack = root.THStack("histStack_{}_{}_noSig_comp".format(histName,sampleName),"")
      stackSig = root.THStack("histStack_{}_{}_sigig_comp".format(histName,sampleName),"")
      for i in range(len(labels)):
        nBins = hists[i].GetNbinsX()
        for iBin in range(1,nBins+1):
          if sumHist.GetBinContent(iBin) > 0:
            hists[i].SetBinContent(iBin,hists[i].GetBinContent(iBin)/sumHist.GetBinContent(iBin))
          if sumHistSig.GetBinContent(iBin) > 0:
            histsSig[i].SetBinContent(iBin,histsSig[i].GetBinContent(iBin)/sumHistSig.GetBinContent(iBin))
      for i in reversed(range(len(labels))):
        stack.Add(hists[i])
        stackSig.Add(histsSig[i])
      xMax = sumHist.GetXaxis().GetBinUpEdge(sumHist.GetNbinsX())*0.25
      axisHist = makeStdAxisHist([sumHist],xlim=[0,xMax],ylim=[0,2])
      setHistTitles(axisHist,"Cut Width: "+histTitlesRoot[histName]+" [cm]","Fraction")
      axisHist.Draw()
      stack.Draw("histsame")
      leg = drawNormalLegend(hists,labels,option='f',wide=True)
      c.RedrawAxis()
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.SaveAs("AnalyzeCuts_width_comp_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_width_comp_{}_{}.pdf".format(histName,sampleName))
      axisHistSig = makeStdAxisHist([sumHistSig],xlim=[0,5],ylim=[0,2])
      setHistTitles(axisHistSig,"Cut Width: "+histTitlesRoot[histName]+" [#sigma]","Fraction")
      axisHistSig.Draw()
      stackSig.Draw("histsame")
      legSig = drawNormalLegend(histsSig,labels,option='f',wide=True)
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.RedrawAxis()
      c.SaveAs("AnalyzeCuts_widthSig_comp_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_widthSig_comp_{}_{}.pdf".format(histName,sampleName))

      goodTrackMatchPurityHist = hists[0].Clone(hists[0].GetName()+"_goodTrackMatchPurity")
      goodTrackMatchPurityHist.Add(hists[1])
      goodTrackMatchPurityHistSig = histsSig[0].Clone(histsSig[0].GetName()+"_goodTrackMatchPurity")
      goodTrackMatchPurityHistSig.Add(histsSig[1])
      sampleTitles.append(sampleTitlesRoot[sampleName])
      sampleGoodTrackMatchPurityHists.append(goodTrackMatchPurityHist)
      sampleGoodTrackMatchPurityHistsSig.append(goodTrackMatchPurityHistSig)

    muMeanData,sigMeanData,muMeanMC,sigMeanMC = gausParams[histName]
    plotHistsSimple(sampleGoodTrackMatchHists,sampleTitles,"Cut Width: "+histTitlesRoot[histName]+" [cm]","Efficiency",c,"AnalyzeCuts_width_all_{}".format(histName),xlim=[0,sigMeanMC*10])
    plotHistsSimple(sampleGoodTrackMatchHistsSig,sampleTitles,"Cut Width: "+histTitlesRoot[histName]+" [#sigma]","Efficiency",c,"AnalyzeCuts_widthSig_all_{}".format(histName),xlim=[0,10])

    plotHistsSimple(sampleGoodTrackMatchPurityHists,sampleTitles,"Cut Width: "+histTitlesRoot[histName]+" [cm]","Purity",c,"AnalyzeCuts_width_all_purity_{}".format(histName),xlim=[0,sigMeanMC*5])
    plotHistsSimple(sampleGoodTrackMatchPurityHistsSig,sampleTitles,"Cut Width: "+histTitlesRoot[histName]+" [#sigma]","Purity",c,"AnalyzeCuts_widthSig_all_purity_{}".format(histName),xlim=[0,5])

    gs = [root.TGraph() for i in sampleGoodTrackMatchHists]
    for i, g in enumerate(gs):
        g.SetLineColor(COLORLIST[i])
    nBins = sampleGoodTrackMatchHists[0].GetNbinsX()
    for iBin in range(nBins+1):
      for effHist, purHist, g in zip(sampleGoodTrackMatchHists,sampleGoodTrackMatchPurityHists,gs):
        g.SetPoint(iBin,effHist.GetBinContent(iBin),purHist.GetBinContent(iBin))
    axisHist = drawGraphs(c,gs,"Efficiency","Purity",drawOptions="L",xlims=[0,1],ylims=[0.6,1.2])
    leg = drawNormalLegend(gs,sampleTitles,option='l',wide=True)
    drawStandardCaptions(c,"Cut Width: "+histTitlesRoot[histName])
    c.SaveAs("AnalyzeCuts_width_purVeff_{}.png".format(histName))
    c.SaveAs("AnalyzeCuts_width_purVeff_{}.pdf".format(histName))



def doOneSideOptimization(c,fns,histTitlesRoot,sampleTitlesRoot):
  allCurves = {}
  fs = []
  for fn in sorted(fns):
    f = root.TFile(fn)
    fs.append(f)
    sampleMatch = re.match(r"Inelastic_(.+).root",fn)
    if not sampleMatch:
        raise Exception("Couldn't parse filename: ",fn)
    sampleName = sampleMatch.group(1)
    for key in sorted(f.GetListOfKeys()):
      name = key.GetName()
      #print name
      matchMCSum = re.match(r"(.+)_mcSumHist",name)
      matchMCC11 = re.match(r"(.+)_(mcc11.*)",name)
      matchRun = re.match(r"(.+)_run(.+)",name)
      histName = None
      subSampleName = None
      if matchMCSum:
        histName = matchMCSum.group(1)
        subSampleName = "mcSumHist"
      elif matchMCC11:
        histName = matchMCC11.group(1)
        subSampleName = matchMCC11.group(2)
      elif matchRun:
        histName = matchRun.group(1)
        subSampleName = sampleName
      if ("Delta" in histName) or ("PFBeamPrimAngleStartBI" in histName) or "PFBeamPrimEndZ_start"==histName:
        continue
      if not ("PFBeamPrimEndZ" in histName) and not ("PFBeamPrimStartZ" in histName):
        continue
      #if "wide" in histName:
      #  continue
      hist = key.ReadObj()
      startTime = time.time()
      hist.Rebin(10)
      cutHist = getIntegralHist(hist,setErrors=True,reverse=True)
      endTime = time.time()
      print "{:45} {:25} {:40} {:10.2f}".format(histName,sampleName,subSampleName,endTime-startTime)
      #cutHist.Draw("PE")
      #c.SaveAs("AnalyzeCuts_oneSideTest_{}_{}_{}.png".format(histName,sampleName,subSampleName))
      if not (histName in allCurves):
        allCurves[histName] = {}
      if not (sampleName in allCurves[histName]):
        allCurves[histName][sampleName] = {}
      allCurves[histName][sampleName][subSampleName] = cutHist
  for iHistName, histName in enumerate(sorted(allCurves)):
    sampleTitles = []
    sampleGoodTrackMatchEffHists = []
    sampleGoodTrackMatchPurityHists = []
    for iSampleName, sampleName in enumerate(sorted(allCurves[histName])):

      fileConfigsMC = [
        {
          'name': "mcc11_piInel_good",
          'title': "MCC11 #pi Inelastic--Good Reco",
        },
        {
          'name': "mcc11_piInel_badIntMatch",
          'title': "MCC11 #pi Inelastic--Bad Reco/True Interaction Match",
        },
        {
          'name': "mcc11_piInel_badTrkMatch",
          'title': "MCC11 #pi Inelastic--Bad Track/True Primary Match",
        },
        {
          'name': "mcc11_piDecay",
          'title': "MCC11 #pi Decay",
        },
        {
          'name': "mcc11_piOutsideTPC",
          'title': "MCC11 #pi Interacted Outside TPC",
        },
        {
          'name': "mcc11_mu",
          'title': "MCC11 Primary Muon",
        },
      ]
      if ('6GeV' in sampleName) or ('7GeV' in sampleName):
        fileConfigsMC.append({
          'name': "mcc11_e",
          'title': "MCC11 Primary Electron",
        })

      hists = []
      histsFrac = []
      labels = []
      stack = root.THStack("histStack_{}_{}_oneSide".format(histName,sampleName),"")
      stackFrac = root.THStack("histStack_{}_{}_oneSide_frac".format(histName,sampleName),"")
      sumHist = allCurves[histName][sampleName]["mcSumHist"]
      dataHist = allCurves[histName][sampleName][sampleName]
      for iSubSampleName, subSampleConfig in enumerate(fileConfigsMC):
        subSampleName = subSampleConfig['name']
        hist = allCurves[histName][sampleName][subSampleName]
        hists.append(hist)
        labels.append(subSampleConfig['title'])
        histFrac = hist.Clone(hist.GetName()+"oneSide_FracHist")
        histFrac.Divide(sumHist)
        histsFrac.append(histFrac)
      for i in range(len(labels)):
        hists[i].SetFillColor(COLORLIST[i])
        hists[i].SetLineColor(COLORLIST[i])
        histsFrac[i].SetFillColor(COLORLIST[i])
        histsFrac[i].SetLineColor(COLORLIST[i])
      for i in reversed(range(len(labels))):
        stack.Add(hists[i])
        stackFrac.Add(histsFrac[i])
      axisHist = makeStdAxisHist([sumHist])
      setHistTitles(axisHist,sumHist.GetXaxis().GetTitle(),"Events < X")
      axisHist.Draw()
      stack.Draw("histsame")
      dataHist.Draw("same")
      leg = drawNormalLegend(hists,labels,option='f',wide=True)
      c.RedrawAxis()
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.SaveAs("AnalyzeCuts_oneSide_comb_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_oneSide_comb_{}_{}.pdf".format(histName,sampleName))

      axisHist = makeStdAxisHist([sumHist],ylim=[0,2])
      setHistTitles(axisHist,sumHist.GetXaxis().GetTitle(),"Fraction < X")
      axisHist.Draw()
      stackFrac.Draw("histsame")
      leg = drawNormalLegend(histsFrac,labels,option='f',wide=True)
      c.RedrawAxis()
      drawStandardCaptions(c,sampleTitlesRoot[sampleName])
      c.SaveAs("AnalyzeCuts_oneSide_comp_{}_{}.png".format(histName,sampleName))
      c.SaveAs("AnalyzeCuts_oneSide_comp_{}_{}.pdf".format(histName,sampleName))

      goodTrackMatchEffHist = hists[0].Clone(hists[0].GetName()+"_goodTrackMatchEfficiency")
      goodTrackMatchEffHist.Add(hists[1])
      totalNorm = goodTrackMatchEffHist.GetBinContent(goodTrackMatchEffHist.GetNbinsX()+1)
      if totalNorm != 0.:
        goodTrackMatchEffHist.Scale(1./totalNorm)
      goodTrackMatchPurityHist = histsFrac[0].Clone(histsFrac[0].GetName()+"_goodTrackMatchPurity")
      goodTrackMatchPurityHist.Add(histsFrac[1])
      sampleTitles.append(sampleTitlesRoot[sampleName])
      sampleGoodTrackMatchPurityHists.append(goodTrackMatchPurityHist)
      sampleGoodTrackMatchEffHists.append(goodTrackMatchEffHist)

    plotHistsSimple(sampleGoodTrackMatchEffHists,sampleTitles,sampleGoodTrackMatchEffHists[0].GetXaxis().GetTitle(),"Efficiency",c,"AnalyzeCuts_oneSide_eff_{}".format(histName))
    plotHistsSimple(sampleGoodTrackMatchPurityHists,sampleTitles,sampleGoodTrackMatchEffHists[0].GetXaxis().GetTitle(),"Purity",c,"AnalyzeCuts_oneSide_purity_{}".format(histName))

    gs = [root.TGraph() for i in sampleGoodTrackMatchEffHists]
    for i, g in enumerate(gs):
        g.SetLineColor(COLORLIST[i])
    nBins = sampleGoodTrackMatchEffHists[0].GetNbinsX()
    for iBin in range(nBins+1):
      for effHist, purHist, g in zip(sampleGoodTrackMatchEffHists,sampleGoodTrackMatchPurityHists,gs):
        g.SetPoint(iBin,effHist.GetBinContent(iBin),purHist.GetBinContent(iBin))
    xlims = [0,1]
    ylims = [0.6,1.2]
    if histName == "PFBeamPrimEndZ_end":
      xlims = [0.98,1.]
    axisHist = drawGraphs(c,gs,"Efficiency","Purity",drawOptions="L",xlims=xlims,ylims=ylims)
    leg = drawNormalLegend(gs,sampleTitles,option='l',wide=True)
    drawStandardCaptions(c,sampleGoodTrackMatchEffHists[0].GetXaxis().GetTitle())
    c.SaveAs("AnalyzeCuts_oneSide_purVeff_{}.png".format(histName))
    c.SaveAs("AnalyzeCuts_oneSide_purVeff_{}.pdf".format(histName))


if __name__ == "__main__":

  fns = [
          "Inelastic_run5387_1GeV.root",
          "Inelastic_run5432_2GeV.root",
          "Inelastic_run5786_3GeV.root",
          "Inelastic_run5770_6GeV.root",
          "Inelastic_run5204_7GeV.root",
        ]

  histTitles = {
    "DeltaXPFBeamPrimStartBI": r"$\Delta X$ PF-BI",
    "DeltaYPFBeamPrimStartBI": r"$\Delta Y$ PF-BI",
    "PFBeamPrimAngleStartBIXZ": r"$\Delta \theta_{xz}$",
    "PFBeamPrimAngleStartBIYZ": r"$\Delta \theta_{yz}$",
  }
  histTitlesRoot = {
    "DeltaXPFBeamPrimStartBI": r"#Delta X PF-BI",
    "DeltaYPFBeamPrimStartBI": r"#Delta Y PF-BI",
    "PFBeamPrimAngleStartBIXZ": r"#Delta #theta_{xz}",
    "PFBeamPrimAngleStartBIYZ": r"#Delta #theta_{yz}",
  }
  sampleTitles = {
    "run5387_1GeV": r"Run 5387 \SI{1}{\GeVc{}}",
    "run5432_2GeV": r"Run 5432 \SI{2}{\GeVc{}}",
    "run5786_3GeV": r"Run 5786 \SI{3}{\GeVc{}}",
    "run5770_6GeV": r"Run 5770 \SI{6}{\GeVc{}}",
    "run5204_7GeV": r"Run 5204 \SI{7}{\GeVc{}}",
  }
  sampleTitlesRoot = {
    "run5387_1GeV": r"Run 5387 1 GeV/c",
    "run5432_2GeV": r"Run 5432 2 GeV/c",
    "run5786_3GeV": r"Run 5786 3 GeV/c",
    "run5770_6GeV": r"Run 5770 6 GeV/c",
    "run5204_7GeV": r"Run 5204 7 GeV/c",
  }

  c = root.TCanvas('c1')
  if False:
    gausParams = getMeansSigmas(c,fns,histTitles,sampleTitles)
    getEffPurOfGausCuts(c,fns,histTitlesRoot,sampleTitlesRoot,gausParams)
  doOneSideOptimization(c,fns,histTitlesRoot,sampleTitlesRoot)
