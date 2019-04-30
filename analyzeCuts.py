#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys
import signal
import multiprocessing

def getNDecPlacesStr(parError):
  if parError >= 10:
    return '0'
  sfs = -math.log10(parError)
  sfs = abs(math.ceil(sfs))
  return "{:.0f}".format(sfs)

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
      c.SaveAs("AnalyzeCuts_Test_"+histName+'_'+sampleName+".png")
      c.SaveAs("AnalyzeCuts_Test_"+histName+'_'+sampleName+".pdf")
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
  c.SaveAs("AnalyzeCuts_Test_"+histName+'_'+sampleName+".png")
  c.SaveAs("AnalyzeCuts_Test_"+histName+'_'+sampleName+".pdf")
  return fitResult

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
  sampleTitles = {
    "run5387_1GeV": r"Run 5387 \SI{1}{\GeVc{}}",
    "run5432_2GeV": r"Run 5432 \SI{2}{\GeVc{}}",
    "run5786_3GeV": r"Run 5786 \SI{3}{\GeVc{}}",
    "run5770_6GeV": r"Run 5770 \SI{6}{\GeVc{}}",
    "run5204_7GeV": r"Run 5204 \SI{7}{\GeVc{}}",
  }


  c = root.TCanvas('c1')
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
    fitresult = result[3]
    frDict = {}
    frDict["chi2"] = "{:.2f}".format(fitresult.Chi2()/fitresult.Ndf())
    nDigits = getNDecPlacesStr(fitresult.ParError(1))
    frDict["mu"] = ("{:."+nDigits+"f}").format(fitresult.Value(1))
    frDict["muErr"] = ("{:."+nDigits+"f}").format(fitresult.ParError(1))
    nDigits = getNDecPlacesStr(fitresult.ParError(2))
    frDict["sigma"] = ("{:."+nDigits+"f}").format(fitresult.Value(2))
    frDict["sigmaErr"] = ("{:."+nDigits+"f}").format(fitresult.ParError(2))
    outStr = "{} {} {} {} {} {}".format(result[0],result[1],result[2],frDict["mu"],frDict["muErr"],frDict["sigma"],frDict["sigmaErr"],frDict["chi2"])
    print outStr
    histName = histTitles[result[0]]
    sampleName = sampleTitles[result[1]]
    if not (histName in resultsDict):
      resultsDict[histName] = {}
    if not (sampleName in resultsDict[histName]):
      resultsDict[histName][sampleName] = {}
    subName = "Data"
    if ("mc" in result[2]):
      subName = "MC"
    resultsDict[histName][sampleName][subName] = frDict
  for iHistName, histName in enumerate(sorted(resultsDict)):
    for iSampleName, sampleName in enumerate(sorted(resultsDict[histName])):
      for iSubName, subName in enumerate(sorted(resultsDict[histName][sampleName])):
        frDict =  resultsDict[histName][sampleName][subName]
        outStr = r"{} & {} & {} & {} & {} & {} & {} & {}\\".format(histName,sampleName,subName,frDict["mu"],frDict["muErr"],frDict["sigma"],frDict["sigmaErr"],frDict["chi2"])
        print outStr
