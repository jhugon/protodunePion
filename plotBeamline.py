#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import multiprocessing
import copy

if __name__ == "__main__":
  c = root.TCanvas("c")
  f = root.TFile("PiAbsSelector_run5145_50evt_v7.4_5a76d2fe.root")
  #f = root.TFile("PiAbsSelector_run5145_50evt_oldPos_v7.4_5a76d2fe.root")
  tree = f.Get("PiAbsSelector/tree")
  gNewXZ = root.TGraph()
  gOldXZ = root.TGraph()
  gNewYZ = root.TGraph()
  gOldYZ = root.TGraph()
  iPoint = 0
  for iEvent in range(tree.GetEntries()):
    tree.GetEntry(iEvent)
    if tree.nBeamTracksOld > 0:
      print "New: "
      print tree.xWC1Hit, tree.yWC1Hit, tree.zWC1Hit
      print tree.xWC2Hit, tree.yWC2Hit, tree.zWC2Hit
      print tree.xWC, tree.yWC, 0.
      print "Old: "
      print tree.xWC1Old, tree.yWC1Old, tree.zWC1Old
      print tree.xWC2Old, tree.yWC2Old, tree.zWC2Old
      print tree.beamTrackXFrontTPCOld[0], tree.beamTrackYFrontTPCOld[0], 0.
      gNewXZ.SetPoint(iPoint,tree.zWC1Hit,tree.xWC1Hit)
      gOldXZ.SetPoint(iPoint,tree.zWC1Old,tree.xWC1Old)
      gNewYZ.SetPoint(iPoint,tree.zWC1Hit,tree.yWC1Hit)
      gOldYZ.SetPoint(iPoint,tree.zWC1Old,tree.yWC1Old)
      iPoint += 1
      gNewXZ.SetPoint(iPoint,tree.zWC2Hit,tree.xWC2Hit)
      gOldXZ.SetPoint(iPoint,tree.zWC2Old,tree.xWC2Old)
      gNewYZ.SetPoint(iPoint,tree.zWC2Hit,tree.yWC2Hit)
      gOldYZ.SetPoint(iPoint,tree.zWC2Old,tree.yWC2Old)
      iPoint += 1
      gNewXZ.SetPoint(iPoint,0,tree.xWC)
      gOldXZ.SetPoint(iPoint,0,tree.beamTrackXFrontTPCOld[0])
      gNewYZ.SetPoint(iPoint,0,tree.yWC)
      gOldYZ.SetPoint(iPoint,0,tree.beamTrackYFrontTPCOld[0])
      iPoint += 1
    #if iEvent > 1000:
    #  break
  gNewXZ.SetMarkerColor(COLORLIST[0])
  gOldXZ.SetMarkerColor(COLORLIST[2])
  gNewYZ.SetMarkerColor(COLORLIST[0])
  gOldYZ.SetMarkerColor(COLORLIST[2])
  axisHistXZ = root.TH2F("axisHistXZ","",1,-1200,200,1,-400,400)
  setHistTitles(axisHistXZ,"Z [cm]", "X [cm]")
  axisHistXZ.Draw()
  duneXZ = root.TBox(-0.5,-360,200,360)
  duneXZ.SetFillColor(root.kRed-9)
  duneXZ.Draw()
  gOldXZ.Draw("P")
  gNewXZ.Draw("P")
  leg = drawNormalLegend([duneXZ,gNewXZ,gOldXZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.18,0.8,0.45))
  c.SaveAs("beamlineXZ.png")

  axisHistYZ = root.TH2F("axisHistYZ","",1,-1200,200,1,-50,750)
  setHistTitles(axisHistYZ,"Z [cm]", "Y [cm]")
  axisHistYZ.Draw()
  duneYZ = root.TBox(-0.5,0,200,608)
  duneYZ.SetFillColor(root.kRed-9)
  duneYZ.Draw()
  gOldYZ.Draw("P")
  gNewYZ.Draw("P")
  leg = drawNormalLegend([duneYZ,gNewYZ,gOldYZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.18,0.8,0.45))
  c.SaveAs("beamlineYZ.png")
