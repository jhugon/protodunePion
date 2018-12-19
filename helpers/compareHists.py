from misc import *

class CompareTwoHists:
  def __init__(self, hist1,hist2, canvas, xtitle, ytitle="Events",nDivX=7,nDivPullY=5,xlimits=[],ylimits=[],pullHistRangeY=[0.0,2.0],energyStr="8TeV",lumi=19.4):
    nBinsX = hist1.GetNbinsX()
    assert(nBinsX == hist2.GetNbinsX())
    self.nBinsX = nBinsX
    self.hist1 = hist1
    self.hist2 = hist2
    self.canvas = canvas
    self.tlatex = root.TLatex()
    self.tlatex.SetNDC()
    self.tlatex.SetTextFont(root.gStyle.GetLabelFont())
    self.tlatex.SetTextSize(0.05)
    self.tlatex.SetTextAlign(22)

    if xlimits != []:
      self.hist1.GetXaxis().SetRangeUser(*xlimits)
      self.hist2.GetXaxis().SetRangeUser(*xlimits)
  
    # Make Pull Hist
    self.pullHist = hist1.Clone("pullHist"+hist1.GetName())
    self.pullHist.Reset()
    self.pullHist.SetLineColor(hist2.GetLineColor())
    self.pullHist.SetMarkerColor(hist2.GetMarkerColor())
    self.pullErrorBand = root.TGraphAsymmErrors()
    self.pullErrorBand.SetFillColor(856)
    self.pullErrorBand.SetFillStyle(1001)
    self.pullErrorBand.SetLineStyle(2)
    self.pullErrorBand.SetLineColor(root.kBlack)
    for i in range(0,nBinsX+2):
      nhist1 = hist1.GetBinContent(i)
      nhist2 = hist2.GetBinContent(i)
      nhist1Err = hist1.GetBinError(i)
      nhist2Err = hist2.GetBinError(i)
      ratio = 0.0
      ratioErr = 0.0
      if nhist1 != 0.0 and nhist2 != 0.0:
        ratio = nhist2/nhist1
        ratioErr = nhist2/nhist1 * sqrt((nhist1Err/nhist1)**2+(nhist2Err/nhist2)**2)
      self.pullHist.SetBinContent(i,ratio)
      self.pullHist.SetBinError(i,ratioErr)
      tmpAxis = hist1.GetXaxis()
      self.pullErrorBand.SetPoint(i,tmpAxis.GetBinCenter(i),1.0)
      if nhist1 != 0.0:
        self.pullErrorBand.SetPointError(i,tmpAxis.GetBinLowEdge(i),tmpAxis.GetBinUpEdge(i),
                                                            nhist1Err/nhist1,nhist1Err/nhist1)
      else:
        self.pullErrorBand.SetPointError(i,tmpAxis.GetBinLowEdge(i),tmpAxis.GetBinUpEdge(i),0.,0.)
      #print("nData: %f, nMC: %f, error: %f, pull: %f" % (nData,nMC,error,pull))

    firstVizBin = self.pullHist.GetXaxis().GetFirst()
    lastVizBin = self.pullHist.GetXaxis().GetLast()
    for i in range(0,firstVizBin):
      self.pullErrorBand.SetPointEYhigh(i,self.pullErrorBand.GetErrorYhigh(firstVizBin))
      self.pullErrorBand.SetPointEYlow(i,self.pullErrorBand.GetErrorYlow(firstVizBin))
    for i in range(lastVizBin+1,nBinsX+2):
      self.pullErrorBand.SetPointEYhigh(i,self.pullErrorBand.GetErrorYhigh(lastVizBin))
      self.pullErrorBand.SetPointEYlow(i,self.pullErrorBand.GetErrorYlow(lastVizBin))

    #Find Maximum y-value
    max1 = hist1.GetMaximum()
    max2 = hist2.GetMaximum()
    max1Bin = hist1.GetMaximumBin()
    max2Bin = hist2.GetMaximumBin()
    max1 = hist1.GetBinContent(max1Bin)+hist1.GetBinError(max1Bin)
    max2 = hist2.GetBinContent(max2Bin)+hist2.GetBinError(max2Bin)
    ymax = 0.0
    if max1 > max2:
       ymax = max1
    else:
       ymax = max2
    self.ymax = ymax

    #Setup Canvas
    canvas.cd()
    canvas.Clear()
    pad1 = root.TPad("pad1"+hist1.GetName(),"",0.02,0.30,0.98,0.98,0)
    pad2 = root.TPad("pad2"+hist1.GetName(),"",0.02,0.01,0.98,0.29,0)
    self.pad1 = pad1
    self.pad2 = pad2
  
    pad1.SetBottomMargin(0.005);
    pad2.SetTopMargin   (0.005);
    pad2.SetBottomMargin(0.33);
  
    pad1.Draw() # Projections pad
    pad2.Draw() # Residuals   pad

    pad1Width = pad1.XtoPixel(pad1.GetX2())
    pad1Height = pad1.YtoPixel(pad1.GetY1())
    pad2Height = pad2.YtoPixel(pad2.GetY1())
    #pad1ToPad2FontScalingFactor = float(pad1Width)/pad2Height
    pad1ToPad2FontScalingFactor = float(pad1Height)/pad2Height
  
    # Main Pad
    pad1.cd();
    self.hist2.GetXaxis().SetTitle("")
    self.hist2.GetXaxis().SetLabelSize(0)
    self.hist2.GetYaxis().SetTitle(ytitle)
    self.hist2.GetYaxis().SetLabelSize(0.050)
    self.hist2.GetYaxis().SetTitleSize(0.055)
    self.hist2.GetXaxis().SetNdivisions(nDivX)
    if ylimits==[]:
      self.hist2.GetYaxis().SetRangeUser(0.0,ymax*1.04)
    else:
      self.hist2.GetYaxis().SetRangeUser(*ylimits)
    self.hist2.Draw("")
    self.hist1.Draw("same")
  
    # Pulls Pad
    pad2.cd()
    self.pullHist.SetTitle("")
    if xlimits != []:
      self.pullHist.GetXaxis().SetRangeUser(*xlimits)
    self.pullHist.GetXaxis().SetTitle(xtitle)
    self.pullHist.GetXaxis().CenterTitle(1)
    self.pullHist.GetXaxis().SetNdivisions(nDivX)
    self.pullHist.GetXaxis().SetTitleSize(0.055*pad1ToPad2FontScalingFactor)
    self.pullHist.GetXaxis().SetLabelSize(0.050*pad1ToPad2FontScalingFactor)
    self.pullHist.GetYaxis().SetTitle("Ratio")
    self.pullHist.GetYaxis().SetTitleSize(0.050*pad1ToPad2FontScalingFactor)
    self.pullHist.GetYaxis().SetLabelSize(0.040*pad1ToPad2FontScalingFactor)
    self.pullHist.GetYaxis().CenterTitle(1)
    self.pullHist.GetYaxis().SetTitleOffset(0.5)
    self.pullHist.GetYaxis().SetNdivisions(nDivPullY)
    self.pullHist.GetYaxis().SetRangeUser(*pullHistRangeY)
    self.pullHist.GetXaxis().SetTitleOffset(0.75*self.pullHist.GetXaxis().GetTitleOffset())
    self.pullHist.GetYaxis().SetTitleOffset(0.70)
    self.pullHist.SetFillColor(856)
    self.pullHist.SetFillStyle(1001)
    self.pullHist.Draw("")
    self.pullErrorBand.Draw("3")
    self.pullErrorBand.Draw("LX")
    #self.pullErrorBandLine = self.pullErrorBand.Clone(self.pullErrorBand.GetName()+"Line")
    #self.pullErrorBandLine.SetFillStyle(0)
    #self.pullErrorBandLine.Draw("same HIST L")
    self.pullHist.Draw("same")

    pad1.RedrawAxis() # Updates Axis Lines
    pad2.RedrawAxis() # Updates Axis Lines
  
    #canvas.cd()
    pad1.cd()
    #self.tlatex.DrawLatex(0.33,0.96,PRELIMINARYSTRING)
    self.tlatex.DrawLatex(0.75,0.96,"#sqrt{s}=%s, L=%.1f fb^{-1}" % (energyStr,lumi))

class CompareTwoHistsAndData:
  def __init__(self, hist1,hist2, data, canvas, xtitle, ytitle="Events",nDivX=7,nDivPullY=5,xlimits=[],ylimits=[],pullHistRangeY=[0.0,2.0],isPreliminary=True,is7TeV=False,lumi=5.0,logy=False,integralPlot=False,energyStr="8TeV"):
    nBinsX = hist1.GetNbinsX()
    assert(nBinsX == hist2.GetNbinsX())
    assert(nBinsX == data.GetNbinsX())
    self.nBinsX = nBinsX
    self.hist1 = hist1
    self.hist2 = hist2
    self.data = data
    self.canvas = canvas
    self.tlatex = root.TLatex()
    self.tlatex.SetNDC()
    self.tlatex.SetTextFont(root.gStyle.GetLabelFont())
    self.tlatex.SetTextSize(0.05)
    self.tlatex.SetTextAlign(22)

    if xlimits != []:
      self.hist1.GetXaxis().SetRangeUser(*xlimits)
      self.hist2.GetXaxis().SetRangeUser(*xlimits)
  
    # Make Pull Hist
    self.pullHist1 = hist1.Clone("pullHist1"+data.GetName())
    self.pullHist1.Reset()
    self.pullHist2 = hist2.Clone("pullHist2"+data.GetName())
    self.pullHist2.Reset()
    for i in range(1,self.pullHist1.GetNbinsX()):
      nData = data.GetBinContent(i)
      nMC1 = hist1.GetBinContent(i)
      nMC2 = hist2.GetBinContent(i)
      error = data.GetBinError(i)
      pull1 = 0.0
      pull2 = 0.0
      if error != 0.0:
        pull1 = (nMC1 - nData)/error
        pull2 = (nMC2 - nData)/error
      self.pullHist1.SetBinContent(i,pull1)
      self.pullHist2.SetBinContent(i,pull2)

    #Find Maximum y-value
    max1 = hist1.GetMaximum()
    max2 = hist2.GetMaximum()
    max1Bin = hist1.GetMaximumBin()
    max2Bin = hist2.GetMaximumBin()
    max1 = hist1.GetBinContent(max1Bin)+hist1.GetBinError(max1Bin)
    max2 = hist2.GetBinContent(max2Bin)+hist2.GetBinError(max2Bin)
    ymax = 0.0
    if max1 > max2:
       ymax = max1
    else:
       ymax = max2
    self.ymax = ymax

    #Find min/max pulls
    max1 = self.pullHist1.GetMaximum()
    max2 = self.pullHist2.GetMaximum()
    pullmax = 0.0
    if max1 > max2:
       pullmax = max1
    else:
       pullmax = max2
    self.pullmax = pullmax
    min1 = self.pullHist1.GetMinimum()
    min2 = self.pullHist2.GetMinimum()
    pullmin = 0.0
    if min1 < min2:
       pullmin = min1
    else:
       pullmin = min2
    self.pullmin = pullmin

    #Setup Canvas
    canvas.cd()
    canvas.Clear()
    pad1 = root.TPad("pad1"+hist1.GetName(),"",0.02,0.30,0.98,0.98,0)
    pad2 = root.TPad("pad2"+hist1.GetName(),"",0.02,0.01,0.98,0.29,0)
  
    pad1.SetBottomMargin(0.005);
    pad2.SetTopMargin   (0.005);
    pad2.SetBottomMargin(0.33);
  
    pad1.Draw() # Projections pad
    pad2.Draw() # Residuals   pad

    pad1Width = pad1.XtoPixel(pad1.GetX2())
    pad1Height = pad1.YtoPixel(pad1.GetY1())
    pad2Height = pad2.YtoPixel(pad2.GetY1())
    #pad1ToPad2FontScalingFactor = float(pad1Width)/pad2Height
    pad1ToPad2FontScalingFactor = float(pad1Height)/pad2Height
  
    # Main Pad
    pad1.cd();
    self.hist2.SetTitle("")
    self.hist2.GetXaxis().SetTitle("")
    self.hist2.GetXaxis().SetLabelSize(0)
    self.hist2.GetYaxis().SetTitle(ytitle)
    self.hist2.GetYaxis().SetLabelSize(0.050)
    self.hist2.GetYaxis().SetTitleSize(0.055)
    self.hist2.GetXaxis().SetNdivisions(nDivX)
    if ylimits==[]:
      self.hist2.GetYaxis().SetRangeUser(0.0,ymax*1.04)
    else:
      self.hist2.GetYaxis().SetRangeUser(*ylimits)
    self.hist2.SetFillStyle(0)
    self.hist1.SetFillStyle(0)
    self.hist2.Draw("hist")
    self.hist1.Draw("hist same")
    self.data.Draw("pe same")
  
    # Pulls Pad
    pad2.cd()
    self.pullHist1.SetTitle("")
    if xlimits != []:
      self.pullHist1.GetXaxis().SetRangeUser(*xlimits)
    self.pullHist0 = self.pullHist1.Clone("pullHist0")
    self.pullHist0.Reset()
    self.pullHist0.SetLineColor(1)
    self.pullHist0.SetLineStyle(2)
    self.pullHist0.SetFillStyle(0)
    self.pullHist1.GetXaxis().SetTitle(xtitle)
    self.pullHist1.GetXaxis().CenterTitle(1)
    self.pullHist1.GetXaxis().SetNdivisions(nDivX)
    self.pullHist1.GetXaxis().SetTitleSize(0.055*pad1ToPad2FontScalingFactor)
    self.pullHist1.GetXaxis().SetLabelSize(0.050*pad1ToPad2FontScalingFactor)
    self.pullHist1.GetYaxis().SetTitle("#frac{MC-Data}{Error}")
    self.pullHist1.GetYaxis().SetTitleSize(0.050*pad1ToPad2FontScalingFactor)
    self.pullHist1.GetYaxis().SetLabelSize(0.040*pad1ToPad2FontScalingFactor)
    self.pullHist1.GetYaxis().CenterTitle(1)
    self.pullHist1.GetYaxis().SetTitleOffset(0.5)
    self.pullHist1.GetYaxis().SetNdivisions(nDivPullY)
    self.pullHist1.GetYaxis().SetRangeUser(pullmin*0.90,pullmax*1.1)
    self.pullHist1.GetXaxis().SetTitleOffset(0.75*self.pullHist1.GetXaxis().GetTitleOffset())
    #self.pullHist1.GetYaxis().SetTitleOffset(0.70)
    self.pullHist1.SetFillStyle(0)
    self.pullHist2.SetFillStyle(0)
    self.pullHist1.Draw("hist")
    self.pullHist0.Draw("hist same")
    self.pullHist1.Draw("hist same")
    self.pullHist2.Draw("hist same")
    pad2.Update()
    pad2.GetFrame().DrawClone()
  
    canvas.cd()
    #self.tlatex.DrawLatex(0.33,0.96,PRELIMINARYSTRING)
    self.tlatex.DrawLatex(0.75,0.96,"#sqrt{s}=%s, L=%.1f fb^{-1}" % (energyStr,lumi))

