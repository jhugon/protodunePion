#!/usr/bin/env python

import ROOT as root
from helpers import *
from helpers.dEdxCalibration import fitSlicesLandauCore, fitSlicesLandaus
root.gROOT.SetBatch(True)
import copy
import sys

SLABTHICKNESS = 0.5

if __name__ == "__main__":

  c = root.TCanvas()
  histFileName = "WireHists.root"
  histname = "dEdxVWireNum"

  mpvGraphs = []
  wGraphs = []
  labels = []
  names = []

  hf = HistFile(histFileName)
  for key in sorted(hf.keysStartsWith(histname)):
    hist = hf[key]
    samplename = key.replace(histname+"_","")
    
    fracMax = 0.4
    nJump = 1
    if "mcc" in samplename:
      continue
    elif not ("run5145" in samplename):
      continue
    else:
      hist.RebinY(2)
      
    mpvGraph, wGraph = fitSlicesLandaus(c,hist,samplename,fracMax=fracMax,nJump=nJump,dumpFitPlots=True)
    mpvGraphs.append(mpvGraph)
    wGraphs.append(wGraph)
    label = samplename
    #for fileConfig in fileConfigsData+fileConfigsMC:
    #  if fileConfig['name'] == samplename:
    #    label = fileConfig['title']
    labels.append(label)
    names.append(samplename)
    #fitSlicesLandauCore(c,hist,samplename)
  c.Clear()
  for i in range(len(mpvGraphs)):
      mpvGraphs[i].SetLineColor(COLORLIST[i])
      mpvGraphs[i].SetMarkerColor(COLORLIST[i])
  ax = drawGraphs(c,mpvGraphs,"Z Wire Number","Landau MPV [MeV/cm]",xlims=[0,480*3],ylims=[0,12],freeTopSpace=0.5,drawOptions=["pez"]*len(mpvGraphs),reverseDrawOrder=True)
  leg = drawNormalLegend(mpvGraphs,labels,["lep"]*len(mpvGraphs))
  drawStandardCaptions(c,"")

  c.SaveAs("Calibrate_mpvs.png")
  c.SaveAs("Calibrate_mpvs.pdf")

  for i in range(len(mpvGraphs)):
    with open("Calibration_"+labels[i]+".txt",'w') as outfile:
      xs = mpvGraphs[i].GetX()
      ys = mpvGraphs[i].GetY()
      errs = mpvGraphs[i].GetEY()
      for j in range(mpvGraphs[i].GetN()):
        line = "{},{},{}".format(xs[j],ys[j],errs[j])
        outfile.write(line+"\n")

