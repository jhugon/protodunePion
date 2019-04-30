#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys
import signal
import multiprocessing

def drawGausFitCaptions(*args,**kargs):
  """
  call as drawGausFitCaptions(canvas, topCaption, fitresultPointer, ... args to drawStandardCaptions)
  """
  def getNDecPlacesStr(parError):
    if parError >= 10:
      return '0'
    sfs = -math.log10(parError)
    sfs = abs(sfs)
    sfs = math.ceil(sfs)
    return "{:.0f}".format(sfs)
        

  args = list(args)
  fitresult = args.pop(2)
  kargs["captionright1"] = "#chi^{{2}}/NDF = {:.2f}".format(fitresult.Chi2()/fitresult.Ndf())
  nDigits = getNDecPlacesStr(fitresult.ParError(1))
  kargs["captionright2"] = ("#mu = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(1),fitresult.ParError(1))
  nDigits = getNDecPlacesStr(fitresult.ParError(2))
  kargs["captionright3"] = ("#sigma = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(2),fitresult.ParError(2))
  nDigits = getNDecPlacesStr(fitresult.ParError(0))
  print "#mu = {:."+nDigits+"f} #pm {:."+nDigits+"f}"
  kargs["captionright4"] = ("Const = {:."+nDigits+"f} #pm {:."+nDigits+"f}").format(fitresult.Value(0),fitresult.ParError(0))
  drawStandardCaptions(*args,**kargs)

if __name__ == "__main__":

  fns = ["Inelastic_run5387_1GeV.root"]
  c = root.TCanvas('c1')
  for fn in fns:
    f = root.TFile(fn)
    for key in f.GetListOfKeys():
      name = key.GetName()
      #print name
      matchMCSum = re.match(r"(.+)_mcSumHist",name)
      if not matchMCSum:
        continue
      histName = matchMCSum.group(1)
      if "DeltaXPFBeamPrimStartBI" != histName:
        continue
      #matchMCC11 = re.match(r"(.+)_(mcc11.*)",name)
      #matchRun = re.match(r"(.+)_run(.+)",name)
      #print bool(matchMCSum), bool(matchMCC11), bool(matchRun)
      hist = key.ReadObj()
      fitResult = hist.Fit("gaus","WLQEMS","",0.2,1.4)
      fitResult.Print()
      #axisHist = makeStdAxisHist([hist],freeTopSpace=0.1,includeErrorBar=True,xlim=[-1,3])
      #axisHist.Draw()
      hist.GetXaxis().SetRangeUser(-0.5,2.5)
      hist.SetTitle("MC Sum")
      hist.Draw("")
      drawGausFitCaptions(c,"",fitResult)
      c.SaveAs("AnalyzeCuts_Test_"+histName+".png")
        
