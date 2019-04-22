#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import multiprocessing
import copy

def otherPoint(tree,doOld,z):
  x1=None
  y1=None
  z1=None
  x2=None
  y2=None
  z2=None
  if doOld:
    x1=tree.xWC1Old
    y1=tree.yWC1Old
    z1=tree.zWC1Old
    x2=tree.xWC2Old
    y2=tree.yWC2Old
    z2=tree.zWC2Old
  else:
    x1=tree.xWC1Hit
    y1=tree.yWC1Hit
    z1=tree.zWC1Hit
    x2=tree.xWC2Hit
    y2=tree.yWC2Hit
    z2=tree.zWC2Hit
  xSlope = (x2-x1)/(z2-z1)
  ySlope = (y2-y1)/(z2-z1)
  xIntercept = x1-xSlope*z1
  yIntercept = y1-ySlope*z1
  return (xSlope*z+xIntercept,ySlope*z+yIntercept,z)

def getBeamlineCoords(tree,doOld,debug=False):

  def rotate(v,doOld):
    pi = math.pi
    if doOld:
      v.RotateY(-10.3*pi/180.)
      v.RotateX(11.7*pi/180.)
    else:
      v.RotateY(15.676709377408265*pi/180.)
      v.RotateZ(227.18669653445150*pi/180.)

  FirstTrackingProfZ= 70755.5
  SecondTrackingProfZ= 71612.4
  NP04FrontZ= 71724.3
  if doOld:
    FirstTrackingProfZ= 70747.9
    SecondTrackingProfZ= 71604.8
    NP04FrontZ= 71724.3
  off1 = NP04FrontZ - FirstTrackingProfZ
  off2 = NP04FrontZ - SecondTrackingProfZ
  if debug:
    print "Z offset 1: ", off1, " offset 2: ", off2

  #Position of Beam in [cm]
  BeamX= 8.0757
  BeamY= 461.06
  BeamZ= -196.11
  ##New from Martin:
  if not doOld:
    BeamX= -4.994
    BeamY= 448.449
    BeamZ= -129.804

  xhat = root.TVector3(1,0,0)
  yhat = root.TVector3(0,1,0)
  zhat = root.TVector3(0,0,1)
  rotate(xhat,doOld)
  rotate(yhat,doOld)
  rotate(zhat,doOld)
  xhatyoverx = xhat.Y()/xhat.X()
  hatdenom = yhat.Y()-xhatyoverx*yhat.X()
  if debug:
    print "xhat: "
    xhat.Print()
    print "yhat: "
    yhat.Print()
    print "zhat: "
    zhat.Print()
    print "xhatyoverx: ", xhatyoverx, "hatdenom: ", hatdenom

  x1=None
  y1=None
  z1=None
  x2=None
  y2=None
  z2=None
  if doOld:
    x1=tree.xWC1Old
    y1=tree.yWC1Old
    z1=tree.zWC1Old
    x2=tree.xWC2Old
    y2=tree.yWC2Old
    z2=tree.zWC2Old
  else:
    x1=tree.xWC1Hit
    y1=tree.yWC1Hit
    z1=tree.zWC1Hit
    x2=tree.xWC2Hit
    y2=tree.yWC2Hit
    z2=tree.zWC2Hit

  if debug:
    print "TPC coords: "
    print (x1,y1,z1)
    print (x2,y2,z2)

  x1 -= BeamX
  x2 -= BeamX
  y1 -= BeamY
  y2 -= BeamY
  z1 -= BeamZ
  z2 -= BeamZ

  if debug:
    print "Remove beam window: "
    print (x1,y1,z1)
    print (x2,y2,z2)

  x1 -= off1*abs(zhat.X())
  x2 -= off2*abs(zhat.X())
  y1 -= off1*abs(zhat.Y())
  y2 -= off2*abs(zhat.Y())
  z1 += off1*abs(zhat.Z())
  z2 += off2*abs(zhat.Z())

  # now xi = xi_beam * xhat.X() + yi_beam * yhat.X()
  # now yi = xi_beam * xhat.Y() + yi_beam * yhat.Y()
  # now zi = xi_beam * xhat.Z() + yi_beam * yhat.Z()

  if debug:
    print "Remove Z offset: "
    print (x1,y1,z1)
    print (x2,y2,z2)

  y1beam = (y1-xhatyoverx*x1)/hatdenom
  y2beam = (y2-xhatyoverx*x2)/hatdenom
  x1beam = (x1-y1beam*yhat.X())/xhat.X()
  x2beam = (x2-y2beam*yhat.X())/xhat.X()

  if debug:
    print "Beamline dx dy: "
    print (x1beam,y1beam)
    print (x2beam,y2beam)

  return x1beam,y1beam,x2beam,y2beam

def myway(x1,y1,x2,y2,debug=False):
  FirstTrackingProfZ= 70755.5
  SecondTrackingProfZ= 71612.4
  NP04FrontZ= 71724.3
  off1 = NP04FrontZ - FirstTrackingProfZ
  off2 = NP04FrontZ - SecondTrackingProfZ
  BeamX= -4.994
  BeamY= 448.449
  BeamZ= -129.804

  theta = 15.676709377408265*math.pi/180.
  phi = 227.18669653445150*math.pi/180.

  v1 = root.TVector3(x1,y1,-off1)
  v2 = root.TVector3(x2,y2,-off2)
  if debug:
    print "Beam Coords"
    v1.Print()
    v2.Print()

  # forward rotation is around Z: 227 deg
  # then around Y: 15.6 deg

  # backward rotation would be around Y then Z

  v1.RotateY(theta)
  v2.RotateY(theta)
  v1.RotateZ(phi)
  v2.RotateZ(phi)

  if debug:
    print "After rotations: "
    v1.Print()
    v2.Print()

  v1 += root.TVector3(BeamX,BeamY,BeamZ)
  v2 += root.TVector3(BeamX,BeamY,BeamZ)

  if debug:
    print "After beam window shifts: "
    v1.Print()
    v2.Print()

  return v1, v2

def jakesway(x1,y1,x2,y2,debug=False):
  FirstTrackingProfZ= 70755.5
  SecondTrackingProfZ= 71612.4
  NP04FrontZ= 71724.3
  off1 = NP04FrontZ - FirstTrackingProfZ
  off2 = NP04FrontZ - SecondTrackingProfZ
  BeamX= -4.994
  BeamY= 448.449
  BeamZ= -129.804

  xRot = 11.4328*math.pi/180.
  yRot = -10.7985*math.pi/180.

  v1 = root.TVector3(x1,y1,-off1)
  v2 = root.TVector3(x2,y2,-off2)
  if debug:
    print "Beam Coords"
    v1.Print()
    v2.Print()

  # forward rotation is around Z: 227 deg
  # then around Y: 15.6 deg

  # backward rotation would be around Y then Z

  v1.RotateX(xRot)
  v2.RotateX(xRot)
  v1.RotateY(yRot)
  v2.RotateY(yRot)

  if debug:
    print "After rotations: "
    v1.Print()
    v2.Print()

  v1 += root.TVector3(BeamX,BeamY,BeamZ)
  v2 += root.TVector3(BeamX,BeamY,BeamZ)

  if debug:
    print "After beam window shifts: "
    v1.Print()
    v2.Print()

  return v1, v2


def getFront(v1,v2):
  xSlope = (v2.X()-v1.X())/(v2.Z()-v1.Z())
  ySlope = (v2.Y()-v1.Y())/(v2.Z()-v1.Z())
  xIntercept = v1.X()-xSlope*v1.Z()
  yIntercept = v1.Y()-ySlope*v1.Z()
  return xIntercept,yIntercept

if __name__ == "__main__":

  c = root.TCanvas("c")
  #f = root.TFile("PiAbsSelector_run5145_50evt_v7.4_5a76d2fe.root")
  ##f = root.TFile("PiAbsSelector_run5145_50evt_oldPos_v7.4_5a76d2fe.root")
  #tree = f.Get("PiAbsSelector/tree")
  tree = root.TChain("PiAbsSelector/tree")
  for name in glob.glob("/cshare/vol2/users/jhugon/condor_output/piAbsSelector_data_oldCalo_v7.4_5a76d2fe/*.root")[:20]:
    tree.AddFile(name)
  histXOldVPF = root.TH2F("XOldVPF","",100,-50,0,100,-50,0)
  histXNewVPF = root.TH2F("XNewVPF","",100,-50,0,100,-50,0)
  histXMyVPF = root.TH2F("XFixVPF","",100,-50,0,100,-50,0)
  histXFixVOld = root.TH2F("XFixVOld","",100,-50,0,100,-50,0)
  histYOldVPF = root.TH2F("YOldVPF","",75,375,450,75,375,450)
  histYNewVPF = root.TH2F("YNewVPF","",75,375,450,75,375,450)
  histYMyVPF = root.TH2F("YFixVPF","",75,375,450,75,375,450)
  histYFixVOld = root.TH2F("YFixVOld","",75,375,450,75,375,450)
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
      print "Beamline coords:"
      x1beamNew,y1beamNew,x2beamNew,y2beamNew = getBeamlineCoords(tree,False)
      print x1beamNew,y1beamNew
      print x2beamNew,y2beamNew
      print "Old: "
      print tree.xWC1Old, tree.yWC1Old, tree.zWC1Old
      print tree.xWC2Old, tree.yWC2Old, tree.zWC2Old
      print tree.beamTrackXFrontTPCOld[0], tree.beamTrackYFrontTPCOld[0], 0.
      print "Beamline coords:"
      x1beamOld,y1beamOld,x2beamOld,y2beamOld = getBeamlineCoords(tree,True)
      print x1beamOld,y1beamOld
      print x2beamOld,y2beamOld
      print "Fix: "
      v1,v2 = jakesway(x1beamNew,y1beamNew,x2beamNew,y2beamNew)
      myX, myY = getFront(v1,v2)
      v1.Print()
      v2.Print()
      print myX, myY
      print "Fix direction: "
      mydirection = (v2-v1)
      mydirection *= 1./mydirection.Mag()
      mydirection.Print()
      print "TPC Track: "
      print tree.PFBeamPrimStartX, tree.PFBeamPrimStartY, tree.PFBeamPrimStartZ
      histXMyVPF.Fill(tree.PFBeamPrimStartX,myX)
      histXNewVPF.Fill(tree.PFBeamPrimStartX,tree.xWC)
      histXOldVPF.Fill(tree.PFBeamPrimStartX,tree.beamTrackXFrontTPCOld[0])
      histXFixVOld.Fill(tree.beamTrackXFrontTPCOld[0],myX)
      histYMyVPF.Fill(tree.PFBeamPrimStartY,myY)
      histYNewVPF.Fill(tree.PFBeamPrimStartY,tree.yWC)
      histYOldVPF.Fill(tree.PFBeamPrimStartY,tree.beamTrackYFrontTPCOld[0])
      histYFixVOld.Fill(tree.beamTrackYFrontTPCOld[0],myY)
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
      # Just one event
      g1NewXZ = root.TGraph()
      g1OldXZ = root.TGraph()
      g1NewYZ = root.TGraph()
      g1OldYZ = root.TGraph()
      jPoint = 0
      g1NewXZ.SetPoint(jPoint,tree.zWC1Hit,tree.xWC1Hit)
      g1OldXZ.SetPoint(jPoint,tree.zWC1Old,tree.xWC1Old)
      g1NewYZ.SetPoint(jPoint,tree.zWC1Hit,tree.yWC1Hit)
      g1OldYZ.SetPoint(jPoint,tree.zWC1Old,tree.yWC1Old)
      jPoint += 1
      g1NewXZ.SetPoint(jPoint,tree.zWC2Hit,tree.xWC2Hit)
      g1OldXZ.SetPoint(jPoint,tree.zWC2Old,tree.xWC2Old)
      g1NewYZ.SetPoint(jPoint,tree.zWC2Hit,tree.yWC2Hit)
      g1OldYZ.SetPoint(jPoint,tree.zWC2Old,tree.yWC2Old)
      jPoint += 1
      g1NewXZ.SetPoint(jPoint,0,tree.xWC)
      g1OldXZ.SetPoint(jPoint,0,tree.beamTrackXFrontTPCOld[0])
      g1NewYZ.SetPoint(jPoint,0,tree.yWC)
      g1OldYZ.SetPoint(jPoint,0,tree.beamTrackYFrontTPCOld[0])
      jPoint += 1
      oldPoint = otherPoint(tree,True,100.)
      newPoint = otherPoint(tree,False,100.)
      g1NewXZ.SetPoint(jPoint,newPoint[2],newPoint[0])
      g1OldXZ.SetPoint(jPoint,oldPoint[2],oldPoint[0])
      g1NewYZ.SetPoint(jPoint,newPoint[2],newPoint[1])
      g1OldYZ.SetPoint(jPoint,oldPoint[2],oldPoint[1])
      jPoint += 1
      g1NewXZ.SetMarkerColor(COLORLIST[0])
      g1OldXZ.SetMarkerColor(COLORLIST[2])
      g1NewYZ.SetMarkerColor(COLORLIST[0])
      g1OldYZ.SetMarkerColor(COLORLIST[2])
      g1NewXZ.SetLineColor(COLORLIST[0])
      g1OldXZ.SetLineColor(COLORLIST[2])
      g1NewYZ.SetLineColor(COLORLIST[0])
      g1OldYZ.SetLineColor(COLORLIST[2])
      axisHistXZ = root.TH2F("axisHistXZ"+str(iEvent),"",1,-500,500,1,-200,100)
      setHistTitles(axisHistXZ,"Z [cm]", "X [cm]")
      axisHistXZ.Draw()
      duneXZ = root.TBox(
                        max(-0.5,axisHistXZ.GetXaxis().GetBinLowEdge(1)),
                        max(-360,axisHistXZ.GetYaxis().GetBinLowEdge(1)),
                        min(500,axisHistXZ.GetXaxis().GetBinUpEdge(1)),
                        min(360,axisHistXZ.GetYaxis().GetBinUpEdge(1)),
                        )
      duneXZ.SetFillColor(root.kRed-9)
      duneXZ.Draw()
      c.RedrawAxis()
      g1OldXZ.Draw("PL")
      g1NewXZ.Draw("PL")
      leg = drawNormalLegend([duneXZ,g1NewXZ,g1OldXZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.15,0.8,0.30))
      c.SaveAs("beamline_Run{:04d}_Event{:05d}_XZ.png".format(tree.runNumber,tree.eventNumber))

      axisHistYZ = root.TH2F("axisHistYZ"+str(iEvent),"",1,-500,500,1,320,540)
      setHistTitles(axisHistYZ,"Z [cm]", "Y [cm]")
      axisHistYZ.Draw()
      duneYZ = root.TBox(
                        max(-0.5,axisHistYZ.GetXaxis().GetBinLowEdge(1)),
                        max(0,axisHistYZ.GetYaxis().GetBinLowEdge(1)),
                        min(500,axisHistYZ.GetXaxis().GetBinUpEdge(1)),
                        min(608,axisHistYZ.GetYaxis().GetBinUpEdge(1)),
                        )
      duneYZ.SetFillColor(root.kRed-9)
      duneYZ.Draw()
      c.RedrawAxis()
      g1OldYZ.Draw("PL")
      g1NewYZ.Draw("PL")
      leg = drawNormalLegend([duneYZ,g1NewYZ,g1OldYZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.15,0.8,0.30))
      c.SaveAs("beamline_Run{:04d}_Event{:05d}_YZ.png".format(tree.runNumber,tree.eventNumber))
    if iEvent > 1000:
      break
  gNewXZ.SetMarkerColor(COLORLIST[0])
  gOldXZ.SetMarkerColor(COLORLIST[2])
  gNewYZ.SetMarkerColor(COLORLIST[0])
  gOldYZ.SetMarkerColor(COLORLIST[2])
  gNewXZ.SetLineColor(COLORLIST[0])
  gOldXZ.SetLineColor(COLORLIST[2])
  gNewYZ.SetLineColor(COLORLIST[0])
  gOldYZ.SetLineColor(COLORLIST[2])
  axisHistXZ = root.TH2F("axisHistXZ","",1,-1200,200,1,-400,400)
  setHistTitles(axisHistXZ,"Z [cm]", "X [cm]")
  axisHistXZ.Draw()
  duneXZ = root.TBox(-0.5,-360,200,360)
  duneXZ.SetFillColor(root.kRed-9)
  duneXZ.Draw()
  c.RedrawAxis()
  gOldXZ.Draw("PL")
  gNewXZ.Draw("PL")
  leg = drawNormalLegend([duneXZ,gNewXZ,gOldXZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.15,0.8,0.45))
  c.SaveAs("beamlineXZ.png")

  axisHistYZ = root.TH2F("axisHistYZ","",1,-1200,200,1,-50,750)
  setHistTitles(axisHistYZ,"Z [cm]", "Y [cm]")
  axisHistYZ.Draw()
  duneYZ = root.TBox(-0.5,0,200,608)
  duneYZ.SetFillColor(root.kRed-9)
  duneYZ.Draw()
  c.RedrawAxis()
  gOldYZ.Draw("PL")
  gNewYZ.Draw("PL")
  leg = drawNormalLegend([duneYZ,gNewYZ,gOldYZ],["TPC Active Volume","New BI Hits", "Old BI Hits"],["f","p","p"],position=(0.2,0.18,0.8,0.45))
  c.SaveAs("beamlineYZ.png")

  setHistTitles(histXMyVPF,"TPC Track Start X [cm]", "Fix BI X at TPC Front [cm]")
  setHistTitles(histXNewVPF,"TPC Track Start X [cm]", "New BI X at TPC Front [cm]")
  setHistTitles(histXOldVPF,"TPC Track Start X [cm]", "Old BI X at TPC Front [cm]")
  setHistTitles(histXFixVOld, "Old BI X at TPC Front [cm]", "Fix BI X at TPC Front [cm]")
  histXMyVPF.Draw("colz")
  c.SaveAs("beamlineXFixVPF.png")
  histXNewVPF.Draw("colz")
  c.SaveAs("beamlineXNewVPF.png")
  histXOldVPF.Draw("colz")
  c.SaveAs("beamlineXOldVPF.png")
  histXFixVOld.Draw("colz")
  c.SaveAs("beamlineXFixVOld.png")
  
  setHistTitles(histYMyVPF,"TPC Track Start Y [cm]", "Fix BI Y at TPC Front [cm]")
  setHistTitles(histYNewVPF,"TPC Track Start Y [cm]", "New BI Y at TPC Front [cm]")
  setHistTitles(histYOldVPF,"TPC Track Start Y [cm]", "Old BI Y at TPC Front [cm]")
  setHistTitles(histYFixVOld,"Old BI Y at TPC Front [cm]", "Fix BI Y at TPC Front [cm]")
  histYMyVPF.Draw("colz")
  c.SaveAs("beamlineYFixVPF.png")
  histYNewVPF.Draw("colz")
  c.SaveAs("beamlineYNewVPF.png")
  histYOldVPF.Draw("colz")
  c.SaveAs("beamlineYOldVPF.png")
  histYFixVOld.Draw("colz")
  c.SaveAs("beamlineYFixVOld.png")
  
