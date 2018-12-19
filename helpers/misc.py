
import ROOT as root
from ROOT import gStyle as gStyle
#from ROOT import RooRealVar, RooGaussian, RooArgList, RooDataHist
import re
import csv
import glob
from math import exp
from math import sqrt
from math import log
from math import log10
import math
import array
import os
import os.path
import sys
import time
import datetime
import random
import uuid
import numbers
import copy
import itertools
try:
  import matplotlib.pyplot as mpl
  import matplotlib.patches
  import matplotlib.collections
except ImportError:
  pass

def loadTree(fileConfig,treename):
  """
  Loads a tree and puts it in fileConfig["tree"]

  fileConfig must have a 'fn' member
  that file must have a tree at "treename"

  If fileConfig has "addFriend" in it, then will add
    as a friend tree to the tree
  """
  if len(fileConfig) == 0:
    return
  fileConfig['tree'] = root.TChain(treename)
  try:
    if type(fileConfig['fn']) is str:
        fileConfig['tree'].AddFile(fileConfig['fn'])
    elif type(fileConfig['fn']) is list:
        for fn in fileConfig['fn']:
            fileConfig['tree'].AddFile(fn)
    else:
        raise Exception("")
  except KeyError:
    return
  if 'addFriend' in fileConfig:
    fileConfig['tree'].AddFriend(*(fileConfig['addFriend']))
  fileConfig['tree'].SetCacheSize(10000000);
  fileConfig['tree'].AddBranchToCache("*");

def loadHist(histConfig,fileConfig,binning,var,cuts,nMax,isData):
  """
  Creates a TH1 from a histConfig and fileConfig

  doesn't use histConfig['cuts'], uses cuts argument instead
  does add fileConfig['cuts'] to cuts argument
  
  """
  hist = None
  if len(binning) == 3:
    hist = Hist(*binning)
  else:
    hist = Hist(binning)
  varAndHist = var + " >> " + hist.GetName()
  try:
    tree = fileConfig['tree']
  except KeyError:
    return hist
  thiscuts = copy.deepcopy(cuts)
  if "cuts" in fileConfig:
    thiscuts += fileConfig['cuts']
  tree.Draw(varAndHist,thiscuts,"",nMax)
  hist.UseCurrentStyle()
  hist.Sumw2()
  scaleFactor = 1.
  if not isData and "scaleFactor" in fileConfig: scaleFactor = fileConfig['scaleFactor']
  hist.Scale(scaleFactor)
  if "normToBinWidth" in histConfig and histConfig["normToBinWidth"]:
    normToBinWidth(hist)
  if "integral" in histConfig and histConfig['integral']:
    hist = getIntegralHist(hist)
  if not isData and "color" in fileConfig:
    hist.SetLineColor(fileConfig['color'])
    hist.SetMarkerColor(fileConfig['color'])
    hist.SetFillColor(fileConfig['color'])
  return hist

def getOrdinalStr(inInt):
  result = str(inInt)
  if result[-1] == "1":
    result += "st"
  elif result[-1] == "2":
    result += "nd"
  elif result[-1] == "3":
    result += "rd"
  else:
    result += "th"
  return result

# calculate FWHM
def calcFWFracMax(pdf,obs,lowVal,highVal,step,frac):

  var = pdf.getObservables(root.RooArgSet(obs)).first();

  ymaxVal = float(0)
  xmaxVal = float(0)

  nSteps = int(math.ceil((highVal-lowVal)/step))

  # find the maximum value
  for iStep in range(nSteps):
    x = lowVal + iStep*step

    var.setVal(x)
    pdfVal = pdf.getVal(root.RooArgSet(var)) 

    if (pdfVal > ymaxVal):
       xmaxVal = x
       ymaxVal = pdfVal
       
    #print "x=%s, pdfVal=%s" % (x,pdfVal)

  #print "xMax=%s, ymaxVal=%s\n\n\n\n" % (xmaxVal,ymaxVal)


  # find lower boundary with y=max/2
  xLow = float(0)
  for iStep in range(nSteps):
    x = lowVal + iStep*step
   
    var.setVal(x)
    pdfVal = pdf.getVal(root.RooArgSet(var)) 

    #print "x=%s, pdfVal=%s, ymaxVal/2.=%s" % (x,pdfVal, ymaxVal/2.)
    if (pdfVal > ymaxVal/2. and xLow==0):
       xLow = x

  #print "xLow=%s" % xLow
  

  # find higher boundary with y=max/2
  xHigh = float(0)
  for iStep in reversed(range(nSteps)):
    x = lowVal + iStep*step
   
    var.setVal(x)
    pdfVal = pdf.getVal(root.RooArgSet(var)) 

    if (pdfVal > ymaxVal/2. and xHigh==0):
       xHigh = x

  #print "xHigh=%s" % xHigh
  #print("FWHM low, high",xLow,xHigh)
  
  return (xHigh-xLow)

def calcFWHM(pdf,obs,lowVal,highVal,step):
    return calcFWFracMax(pdf,obs,lowVal,highVal,step,0.5)

def doubleGauss(x,par):
  meanG1  = par[0]
  widthG1 = par[1]
  meanG2  = par[2]
  widthG2 = par[3]
  mixGG   = par[4]
  scale   = par[5]
  
  #if (par[1] != 0.0):
  
  arg1 = (x[0]-meanG1)/widthG1
  arg2 = (x[0]-meanG2)/widthG2
  
  gauss1 = exp(-0.5*arg1*arg1)
  gauss2 = exp(-0.5*arg2*arg2)
  dgauss = (1-mixGG)*gauss1 + mixGG*gauss2 
  
  return scale*dgauss
  #return meanG1 + widthG1*x[0]
  
def setNormalColorTable(diverging=False):
  if diverging:
    gStyle.SetPalette(54)
  else:
    ## My old GYR colors
    #rArray = array.array('d',[0.0,1.0,1.0])
    #gArray = array.array('d',[1.0,1.0,0.0])
    #bArray = array.array('d',[0.0,0.0,0.0])
    #stopArray = array.array('d',[0.,0.5,1.])
    #nTabColors = 500
    #root.TColor.CreateGradientColorTable(len(stopArray),
    #          stopArray,rArray,gArray,bArray,nTabColors
    #       )

    ## nice grey scale
    #alpha = 1.
    #stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
    #red   = [ 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.];
    #green = [ 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.];
    #blue  = [ 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.];
    #root.TColor.CreateGradientColorTable(len(stops), 
    #              array.array('d',stops), array.array('d',red), 
    #              array.array('d',green), array.array('d',blue), 255, alpha
    #          )

    # bird color palette from root 6
    alpha = 1.
    stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
    red = [ 0.2082, 0.0592, 0.0780, 0.0232, 0.1802, 0.5301, 0.8186, 0.9956, 0.9764]
    green = [ 0.1664, 0.3599, 0.5041, 0.6419, 0.7178, 0.7492, 0.7328, 0.7862, 0.9832]
    blue = [ 0.5293, 0.8684, 0.8385, 0.7914, 0.6425, 0.4662, 0.3499, 0.1968, 0.0539]
    root.TColor.CreateGradientColorTable(len(stops), 
                  array.array('d',stops), array.array('d',red), 
                  array.array('d',green), array.array('d',blue), 255, alpha
              )


def setStyle():
  gStyle.SetCanvasColor(0)
  gStyle.SetCanvasBorderSize(10)
  gStyle.SetCanvasBorderMode(0)
  gStyle.SetCanvasDefH(700)
  gStyle.SetCanvasDefW(700)

  gStyle.SetPadColor       (0)
  gStyle.SetPadBorderSize  (10)
  gStyle.SetPadBorderMode  (0)
  gStyle.SetPadBottomMargin(0.13)
  gStyle.SetPadTopMargin   (0.08)
  gStyle.SetPadLeftMargin  (0.15)
  gStyle.SetPadRightMargin (0.05)
  gStyle.SetPadGridX       (0)
  gStyle.SetPadGridY       (0)
  gStyle.SetPadTickX       (1)
  gStyle.SetPadTickY       (1)

  gStyle.SetFrameFillStyle ( 0)
  gStyle.SetFrameFillColor ( 0)
  gStyle.SetFrameLineColor ( 1)
  gStyle.SetFrameLineStyle ( 0)
  gStyle.SetFrameLineWidth ( 1)
  gStyle.SetFrameBorderSize(10)
  gStyle.SetFrameBorderMode( 0)

  gStyle.SetNdivisions(505)

  gStyle.SetLineWidth(2)
  gStyle.SetHistLineWidth(2)
  gStyle.SetFrameLineWidth(2)
  gStyle.SetLegendFillColor(root.kWhite)
  gStyle.SetLegendFont(42)
  gStyle.SetMarkerSize(1.2)
  gStyle.SetMarkerStyle(20)
  gStyle.SetHistLineColor(1)
 
  gStyle.SetLabelSize(0.040,"X")
  gStyle.SetLabelSize(0.040,"Y")

  gStyle.SetLabelOffset(0.010,"X")
  gStyle.SetLabelOffset(0.010,"Y")
 
  gStyle.SetLabelFont(42,"X")
  gStyle.SetLabelFont(42,"Y")
 
  gStyle.SetTitleBorderSize(0)
  gStyle.SetTitleFont(42)
  gStyle.SetTitleFont(42,"X")
  gStyle.SetTitleFont(42,"Y")

  gStyle.SetTitleSize(0.045,"X")
  gStyle.SetTitleSize(0.045,"Y")
 
  gStyle.SetTitleOffset(1.4,"X")
  gStyle.SetTitleOffset(1.6,"Y")
 
  gStyle.SetTextSize(0.055)
  gStyle.SetTextFont(42)
 
  gStyle.SetOptStat(0)
  setNormalColorTable()
  #gStyle.SetPalette(53)
  
setStyle()

def drawSilly(isPreliminary=True,is7TeV=False):
    tlatex = root.TLatex()
    tlatex.SetNDC()
    tlatex.SetTextFont(root.gStyle.GetLabelFont())
    tlatex.SetTextSize(0.05)
    tlatex.SetTextAlign(22)
    if isPreliminary:
      tlatex.DrawLatex(0.33,0.96,"CMS Preliminary")
    if is7TeV:
      tlatex.DrawLatex(0.75,0.96,"#sqrt{s}=8 TeV, L=4.7 fb^{-1}")

def saveAs(canvas,name):
  canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".pdf")
  canvas.SaveAs(name+".eps")
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")

def setLegPos(leg,legPos):
  leg.SetX1NDC(legPos[0])
  leg.SetX2NDC(legPos[2])
  leg.SetY1NDC(legPos[1])
  leg.SetY2NDC(legPos[3])

def getEfficiencyInterval(passed,total):
  eff = root.TEfficiency()
  nom = 0.
  quant=0.682689492137
  if total>0:
    nom = float(passed)/total
  low = eff.ClopperPearson(int(total),int(passed),quant,False)
  high = eff.ClopperPearson(int(total),int(passed),quant,True)
  return [low,nom,high]

def drawStandardCaptions(canvas,caption,captionleft1="",captionleft2="",captionleft3="",captionright1="",captionright2="",captionright3="",preliminaryString="",colorInside=root.kBlack):
  tlatex = root.TLatex()
  tlatex.SetNDC()

  tlatex.SetTextFont(root.gStyle.GetLabelFont())
  tlatex.SetTextSize(0.04)
  tlatex.SetTextAlign(12)
  tlatex.DrawLatex(gStyle.GetPadLeftMargin(),0.96,preliminaryString)

  tlatex.SetTextAlign(32)
  tlatex.DrawLatex(1.0-canvas.GetRightMargin(),0.96,caption)
  tlatex.SetTextAlign(12)
  tlatex.SetTextColor(colorInside)
  tlatex.DrawLatex(0.02+canvas.GetLeftMargin(),0.88,captionleft1)
  tlatex.DrawLatex(0.02+canvas.GetLeftMargin(),0.82,captionleft2)
  tlatex.DrawLatex(0.02+canvas.GetLeftMargin(),0.76,captionleft3)
  tlatex.SetTextAlign(32)
  tlatex.DrawLatex(0.97-canvas.GetRightMargin(),0.88,captionright1)
  tlatex.DrawLatex(0.97-canvas.GetRightMargin(),0.82,captionright2)
  tlatex.DrawLatex(0.97-canvas.GetRightMargin(),0.76,captionright3)
  return tlatex

def copyTreeBranchToNewNameTree(tree,oldBranchName,newBranchName):
  """
  Returns a new tree with the contents of oldBranchName in the old tree, but with
  the branch name newBranchName

  Assumes both branches just contain floats!!
  """
  result = root.TTree(tree.GetName()+"_newNames","")

  newVal = array.array( 'f', [ 0. ] ) # one element array so we get a pointer to the value
  newBranch = result.Branch( newBranchName, newVal, newBranchName+'/F' )

  nEntries = tree.GetEntries()

  for i in range(nEntries):
    tree.GetEntry(i)
    oldVal = getattr(tree,oldBranchName)
    newVal[0] = oldVal
    #print i,newVal[0]
    result.Fill()
  newBranch.SetAddress(0)
  return result

def makeStdAxisHist(histList,logy=False,freeTopSpace=0.5,xlim=[],ylim=[],includeErrorBar=False):
  assert(len(histList)>0)
  assert(len(xlim)==0 or len(xlim)==2)
  assert(len(ylim)==0 or len(ylim)==2)
  multiplier = 1./(1.-freeTopSpace)
  yMin = 1e15
  yMax = -1e15
  xMin = 1e15
  xMax = -1e15
  for hist in histList:
    if isinstance(hist,root.TH1) or isinstance(hist,root.TEfficiency):
        histMax = getHistMax(hist,includeErrorBar=includeErrorBar)
        yMax = max(yMax,histMax)
        if logy:
            histMin = hist.GetMinimum(0.) # should get minimum bin greater than 0.
            yMin = min(yMin,histMin)
        histX = hist
        if hist.InheritsFrom("TEfficiency"):
            histX = hist.GetTotalHistogram()
        nBins = histX.GetNbinsX()
        xMax = max(xMax,histX.GetXaxis().GetBinUpEdge(nBins))
        xMin = min(xMin,histX.GetBinLowEdge(1))
    elif isinstance(hist,root.TGraph):
        x = root.Double(0.)
        y = root.Double(0.)
        for i in range(hist.GetN()):
            hist.GetPoint(i,x,y)
            xMax = max(xMax,float(x))
            yMax = max(yMax,float(y))
            xMin = min(xMin,float(x))
            yMin = min(yMin,float(y))
  #print xMin, xMax, yMin, yMax
  if yMax == -1e15:
    yMax = 1.
  if logy:
    if yMin == 1e15:
      yMin = 0.
    try:
        yMin = math.log10(yMin)
    except ValueError as e:
        yMin = -1.
    else:
        try:
            yMin -= abs(math.log10(yMax) - yMin)*0.25
        except ValueError as e:
            pass
    yMin = min(yMin,-1.)
    try:
        yMax = math.log10(yMax)
    except ValueError as e:
        yMax = 1.
    else:
        yMax += abs(yMax-yMin)*(multiplier-1.)
    if abs(yMax-yMin) < 1.:
        yMax += 0.75
        yMin -= 0.25
    yMin = 10**yMin
    yMax = 10**yMax
  else:
    yMax = yMax*multiplier
    if yMax == 0.:
      yMax = 1.
    if yMin == 1e15:
      yMin = 0.
    else:
      yMin -= (yMax-yMin)*0.1
  if len(xlim)==2:
    xMin = xlim[0]
    xMax = xlim[1]
  if len(ylim)==2:
    yMin = ylim[0]
    yMax = ylim[1]
  axisHist = root.TH2F(uuid.uuid1().hex,"",1,xMin,xMax,1,yMin,yMax)
  return axisHist

def getLinBins(nBins,xMin,xMax):
  delta = (xMax-xMin)/float(nBins)
  return [xMin + x*delta for x in range(nBins+1)]

def getLogBins(nBins,xMin,xMax):
  xMinLog = math.log10(xMin)
  delta = (math.log10(xMax)-xMinLog)/nBins
  return [10**(xMinLog + x*delta) for x in range(nBins+1)]

def drawNormalLegend(hists,labels,option="l",wide=False,position=None):
  assert(len(hists)==len(labels))
  options = None
  if type(option) is list and len(option) == len(labels):
    options = option
  elif type(option) is str:
    options = itertools.repeat(option,len(labels))
  else:
    raise Exception("option must be a str or a list of str with length == lenght of labels")
  leg = None
  if position:
    leg = root.TLegend(*position)
  elif wide:
    leg = root.TLegend(0.2,0.7,0.91,0.89)
  else:
    leg = root.TLegend(0.55,0.7,0.91,0.89)
    #leg = root.TLegend(0.35,0.6,0.91,0.89)
    #leg = root.TLegend(0.40,0.7,0.91,0.89)
  leg.SetLineColor(root.kWhite)
  for hist,label,op in zip(hists,labels,options):
    leg.AddEntry(hist,label,op)
  leg.Draw()
  return leg

def setupCOLZFrame(pad,reset=False):
   if reset:
     pad.SetRightMargin(gStyle.GetPadRightMargin())
   else:
     pad.SetRightMargin(0.15)

def drawVline(axisHist,x):
  axis = axisHist.GetYaxis()
  nBins = axis.GetNbins()
  yLow = axis.GetBinLowEdge(1)
  yHigh = axis.GetBinUpEdge(nBins)
  result = root.TGraph()
  result.SetPoint(0,x,yLow)
  result.SetPoint(1,x,yHigh)
  result.SetLineColor(root.kGray+1)
  result.Draw("lsame")
  return result

def drawHline(axisHist,y):
  axis = axisHist.GetXaxis()
  nBins = axis.GetNbins()
  xLow = axis.GetBinLowEdge(1)
  xHigh = axis.GetBinUpEdge(nBins)
  result = root.TGraph()
  result.SetPoint(0,xLow,y)
  result.SetPoint(1,xHigh,y)
  result.SetLineColor(root.kGray+1)
  result.Draw("lsame")
  return result

def drawVSpan(axisHist,xMin,xMax):
  axis = axisHist.GetYaxis()
  if xMin is None:
    xMin = axisHist.GetXaxis().GetBinLowEdge(1)
  if xMax is None:
    xMax = axisHist.GetXaxis().GetBinUpEdge(axisHist.GetXaxis().GetNbins())
  nBins = axis.GetNbins()
  yLow = axis.GetBinLowEdge(1)
  yHigh = axis.GetBinUpEdge(nBins)
  result = root.TBox(xMin,yLow,xMax,yHigh)
  result.SetLineWidth(0)
  result.SetFillColor(root.kGray)
  result.Draw("same")
  return result

def drawHSpan(axisHist,yMin,yMax):
  axis = axisHist.GetXaxis()
  nBins = axis.GetNbins()
  xLow = axis.GetBinLowEdge(1)
  xHigh = axis.GetBinUpEdge(nBins)
  result = root.TBox(xLow,yMin,xHigh,yMax)
  result.SetLineWidth(0)
  result.SetFillColor(root.kGray)
  result.Draw("same")
  return result

def cutStringParser(cutString):
  """
  returns a list of len 2 tuples of cut spans.
  If one end is not cut on, then will be None.

  Example strings that can be parsed are:
    "x < 6"
    "x < 6 && x >= 3"
    "x < 6e7 && x >= 3e2"
    "x < 6e7 && x >= 3e2"
  """

  def compareFunc(x,y):
    for i in x:
      for j in y:
        try:
          return float(i) < float(j)
        except TypeError:
          pass

  result = []
  if cutString.strip(' ') == "1":
    return result
  cutElements = cutString.split("&&")
  cutVals = []
  for cutElement in cutElements:
    nGt = 0
    nLt = 0
    nGeq = 0
    nLeq = 0
    nLeq = cutElement.count("<=")
    nGeq = cutElement.count(">=")
    nLt = cutElement.count("<") - nLt
    nGt = cutElement.count(">") - nGeq
    if nGt + nLt + nGeq + nLeq == 0:
      continue
    elif nGt + nLt + nGeq + nLeq == 1:
      cutVal = cutElementParser(cutElement)
      if cutVal:
        cutVals.append(list(reversed(cutVal)))
    else:
      print "Warning: cutStringParser: '{}' has more than one comparison operator, can't parse".format(cutElement)
  cutVals.sort(compareFunc)
  #'cut': "mcPartYFrontTPC > 400 && mcPartYFrontTPC < 445",
  # [[400.0, None], [None, 445.0]]
  if len(cutVals) == 2 and cutVals[0][1] is None and cutVals[1][0] is None:
    result = [(cutVals[0][0],cutVals[1][1])]
  else:
    result = cutVals
  return result

def cutElementParser(cutElement):
  """
  Used to parse a string like "value < 124124"

  returns two element list "result" where
    result[0] <= result[1]
    and the one that is the varialble is None
  """
  for comparison in ["<=",">=","<",">"]:
    cutAtoms = cutElement.split(comparison)
    if len(cutAtoms) > 2:
      print "Warning: cutElementParser: too many '{}' for '{}'".format(comparison,cutElement)
      return None
    if len(cutAtoms) > 1:
      cutAtoms = [i.strip(' ') for i in cutAtoms]
      valLeft = None
      valRight = None
      try:
        valLeft = float(cutAtoms[0])
      except ValueError:
        pass
      try:
        valRight = float(cutAtoms[1])
      except ValueError:
        pass
      if (valLeft is None) and (valRight is None):
        print "Warning: cutElementParser: couldn't find float on either side of '{}' for '{}'".format(comparison,cutElement)
        return None
      if not ((valLeft is None) or (valRight is None)):
        print "Warning: cutElementParser: found float on both sides of '{}' for '{}'".format(comparison,cutElement)
        return None
      result = [valLeft,valRight]
      if '>' in comparison:
        result = [valRight,valLeft]
      return result

def drawGraphs(canvas,graphs,xTitle,yTitle,yStartZero=True,xlims=None,ylims=None,freeTopSpace=0.,drawOptions="PEZ",reverseDrawOrder=False):
  xMin = 1e15
  xMax = -1e15
  yMin = 1e15
  yMax = -1e15
  multiplier = 1./(1.-freeTopSpace)
  xArr = array.array("d", [0.])
  yArr = array.array("d", [0.])
  for graph in graphs:
    for iPoint in range(graph.GetN()):
        graph.GetPoint(iPoint,xArr,yArr)
        x = xArr[0]
        y = yArr[0]
        xMin = min(x,xMin)
        xMax = max(x,xMax)
        yMin = min(y,yMin)
        yMax = max(y,yMax)
        xMax = max(x+graph.GetErrorXhigh(iPoint),xMax)
        xMin = min(x-graph.GetErrorXlow(iPoint),xMin)
        yMax = max(y+graph.GetErrorYhigh(iPoint),yMax)
        yMin = min(y-graph.GetErrorYlow(iPoint),yMin)
  if yStartZero:
    yMin = min(0.,yMin)
  xRange = xMax-xMin
  yRange = yMax-yMin
  xMin -= xRange*0.1
  xMax += xRange*0.1
  yMin -= yRange*0.1
  if freeTopSpace > 0.:
    yMax = yMin + yRange*multiplier

  if xlims:
    xMin = xlims[0]
    xMax = xlims[1]
  if ylims:
    yMin = ylims[0]
    yMax = ylims[1]
  axisHist = Hist2D(1,xMin,xMax,1,yMin,yMax)
  setHistTitles(axisHist,xTitle,yTitle)
  axisHist.Draw()
  drawOptionsList = drawOptions
  if type(drawOptionsList) is str:
    drawOptionsList = [drawOptionsList]*len(graphs)
  if len(drawOptionsList) != len(graphs):
    raise Exception("Different number of drawOptions and graphs")
  rangeOfGraphs = range(len(graphs))
  if reverseDrawOrder:
    rangeOfGraphs.reverse()
  for iGraph in rangeOfGraphs:
    graphs[iGraph].Draw(drawOptionsList[iGraph])
  return axisHist

def mplDrawErrorRegion(ax,xs,ys,dxs,dys,**kargs):
  """
  Draws rectangles as error boxes, with rectangles centered at xs, ys
    with widths 2*dxs and heights 2*dys
    kargs are passed to matplotlib.collections.PatchCollection
  """
  assert(len(xs)==len(ys))
  assert(len(dxs)==len(dys))
  assert(len(dxs)==len(xs))
  patchList = []
  for x, y, dx, dy in zip(xs,ys,dxs,dys):
    patchList.append(matplotlib.patches.Rectangle((x-dx,y-dy),2*dx,2*dy))
  patchCollection = matplotlib.collections.PatchCollection(patchList,**kargs)
  ax.add_collection(patchCollection)

def smallMultiples(histLists,axisLabels=None,xlimits=[0.001,0.999],ylimits=[0.001,0.999],xlabel="X", ylabel="Counts",wide=True):
  """
  Don Bluth's small multiples for ROOT

  histLists: a 2D list of histograms or tgraphs, (can be 3D)
    Outermost list is list of rows
    Next innermost list is list of columns
    Innermost list (if present) is list of multiple hists
      or graphs to plot on same axis

  """
  def getPadNumber(row,col): # index from 0
    return row*nColumns + col + 1
    padNum = getPadNumber(iRow,iCol)

  nRows = len(histLists)
  nColumns = 1
  nHists = 1
  for iRow in range(nRows):
    tmpNColumns = len(histLists[iRow])
    for iCol in range(tmpNColumns):
      try:
        tmpNHists = len(histLists[iRow][iCol])
      except:
        pass
      else:
        nHists = max(tmpNHists,nHists)
    nColumns = max(tmpNColumns,nColumns)
  height = 700
  width = 700
  if wide:
    width = 1120
  canvas = root.TCanvas(uuid.uuid1().hex,"",width,height)
  if wide:
    canvas.SetMargin(0.2,0.033,0.22,0.075)
  else:
    canvas.SetMargin(0.22,0.033,0.22,0.075)
  canvas.Divide(nColumns,nRows,0,0)
  axisHists = []
  tlatex = root.TLatex()
  tlatex.SetNDC()
  tlatex.SetTextFont(root.gStyle.GetLabelFont())
  tlatex.SetTextSize(0.04)
  tlatex.SetTextAlign(12)
  xmin = xlimits[0]
  ymin = ylimits[0]
  xmax = xlimits[1]
  ymax = ylimits[1]
  
  for iRow in range(nRows):
    for iCol in range(nColumns):
      padNum = getPadNumber(iRow,iCol)
      canvas.cd(padNum)
      axisHist = Hist2D(1,xmin,xmax,1,ymin,ymax)
      axisHist.GetXaxis().SetNdivisions(505)
      axisHist.GetYaxis().SetNdivisions(505)
      if iCol == 0:
        axisHist.GetYaxis().SetLabelSize(0.08)
      else:
        axisHist.GetYaxis().SetLabelSize(0.)
      if iRow == nRows-1:
        axisHist.GetXaxis().SetLabelSize(0.08)
      else:
        axisHist.GetXaxis().SetLabelSize(0.)
      axisHist.Draw()
      try:
        histLists[iRow][iCol].Draw("same")
      except AttributeError:
        try:
          for hist in histLists[iRow][iCol]:
            hist.Draw("same")
        except TypeError:
          pass
      except IndexError:
        pass
      tlatex.SetTextSize(0.08)
      tlatex.SetTextAlign(33)
      #tlatex.DrawLatex(0.95,0.95,"{} {} {}".format(padNum,iRow,iCol))
      try:
        tlatex.DrawLatex(0.95,0.95,axisLabels[iRow][iCol])
      except TypeError:
        pass
      axisHists.append(axisHist)
  canvas.cd(0)
  tlatex.SetTextSize(0.04)
  tlatex.SetTextAlign(21)
  tlatex.DrawLatex(0.55,0.01,xlabel)
  tlatex.SetTextAlign(23)
  tlatex.SetTextAngle(90)
  tlatex.DrawLatex(0.01,0.55,ylabel)
  
  canvas.SaveAs("Test.png")

COLORLIST=[
      root.kBlue-7,
      root.kRed-4,
      root.kGreen+3,
      root.kMagenta-4,
      root.kOrange-3,
      root.kAzure+10,
      root.kYellow+1,
      root.kViolet+2,
      #root.kGray+1,
]*100


TRUECATEGORYCONFIGS = [
   {
     'title': "Unknown",
     'cuts':"trueCategory==0",
   },
   {
     'title': "#pi Inelastic",
     'cuts':"trueCategory==1",
   },
   {
     'title': "#pi Absorption",
     'cuts':"trueCategory==2",
   },
   {
     'title': "#pi Charge Exchange",
     'cuts':"trueCategory==3",
   },
   {
     'title': "#pi Dbl. Charge Exchange",
     'cuts':"trueCategory==4",
   },
   {
     'title': "Interacted Outside TPC",
     'cuts':"trueCategory==6",
   },
   {
     'title': "Interacted Before TPC",
     'cuts':"trueCategory==7",
   },
   {
     'title': "Left World",
     'cuts':"trueCategory==8",
   },
   {
     'title': "Decay at Rest",
     'cuts':"trueCategory==9",
   },
   {
     'title': "Decay in Flight",
     'cuts':"trueCategory==10",
   },
   {
     'title': "Primary Electron",
     'cuts':"trueCategory==11",
   },
   {
     'title': "Primary Proton",
     'cuts':"trueCategory==12",
   },
   {
     'title': "Primary Muon",
     'cuts':"trueCategory==13",
   },
   {
     'title': "Primary Kaon",
     'cuts':"trueCategory==14",
   },
   {
     'title': "Primary Other",
     'cuts':"trueCategory==15",
   },
   {
     'title': "Other Stopping",
     'cuts':"trueCategory==16",
   },
]

for iCat in range(len(TRUECATEGORYCONFIGS)):
    rootColors = [root.kBlue,root.kCyan,root.kGreen,root.kYellow,root.kRed,root.kMagenta]
    rootAdds = [0,3,-7]
    #TRUECATEGORYCONFIGS[iCat]['color'] = COLORLIST[iCat]
    TRUECATEGORYCONFIGS[iCat]['color'] = rootColors[iCat % len(rootColors)] + rootAdds[iCat // len(rootColors)]

TRUECATEGORYFEWERCONFIGS = [
   ###{
   ###  'title': "#pi Absorption",
   ###  'cuts':"trueCategory==2",
   ###  'color': root.kBlue-7,
   ###},
   ###{
   ###  'title': "#pi Charge Exchange",
   ###  'cuts':"trueCategory==3",
   ###  'color': root.kGreen+3,
   ###},
   ###{
   ###  'title': "#pi Backgrounds",
   ###  'cuts':"trueCategory==1 || trueCategory==9 || trueCategory==10 || trueCategory==4",
   ###  'color': root.kOrange-3,
   ###},
   {
     'title': "#pi Inelastic",
     'cuts':"trueCategory>=1 && trueCategory <=4",
     'color': root.kBlue-7,
   },
   {
     'title': "#pi Decay",
     'cuts':"trueCategory==9 || trueCategory==10",
     'color': root.kOrange-3,
   },
   {
     'title': "#pi Interacted Outside TPC",
     'cuts':"trueCategory==6 || trueCategory==7 || trueCategory==8",
     'color': root.kAzure+10,
   },
   {
     'title': "Primary Electron",
     'cuts':"trueCategory==11",
     #'color': root.kMagenta-4,
     'color': root.kBlack,
   },
   {
     'title': "Primary Proton",
     'cuts':"trueCategory==12",
     'color': root.kRed-4,
   },
   {
     'title': "Primary Muon",
     'cuts':"trueCategory==13",
     'color': root.kYellow+1,
   },
   {
     'title': "Primary Kaon",
     'cuts':"trueCategory==14",
     'color': root.kViolet+2,
   },
   {
     'title': "Unknown",
     'cuts':"trueCategory==0 || trueCategory==16 || trueCategory == 15",
     'color': root.kGray+1,
   },
]

for iCat in range(len(TRUECATEGORYFEWERCONFIGS)):
    TRUECATEGORYFEWERCONFIGS[iCat]['color'] = COLORLIST[iCat]

