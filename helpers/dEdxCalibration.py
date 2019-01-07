from histFuncs import *
from misc import *

def plotSlices(c,hist,savename,xlimits,xtitle,ytitle,xvarname,rebinX=1,rebinY=1,xunits=None,normalize=False):
  print(hist)
  if not hist:
    return
  hist = hist.Clone(uuid.uuid1().hex)

  hist.RebinX(rebinX)
  hist.RebinY(rebinY)
  histAll = hist.ProjectionY("_pyAll",1,hist.GetNbinsX())
  if normalize:
    integral = histAll.Integral()
    if integral != 0.:
        histAll.Scale(1./integral)
  ymax = histAll.GetMaximum()
  histAll.SetLineColor(root.kBlack)
  histAll.SetMarkerColor(root.kBlack)
  labels = ["All"]

  nBinsX = hist.GetNbinsX()
  sliceHists = []
  for iBin in range(1,nBinsX+1):
    sliceHist = getXBinHist(hist,iBin)
    if normalize:
      integral = sliceHist.Integral()
      if integral != 0.:
          sliceHist.Scale(1./integral)
    ymax = max(sliceHist.GetMaximum(),ymax)
    sliceHist.SetLineColor(COLORLIST[iBin-1])
    sliceHist.SetMarkerColor(COLORLIST[iBin-1])
    sliceHists.append(sliceHist)
    xlow = hist.GetXaxis().GetBinLowEdge(iBin)
    xhigh = hist.GetXaxis().GetBinUpEdge(iBin)
    if xunits:
      labels.append("{0:.4g} {3} < {1} < {2:.4g} {3}".format(xlow,xvarname,xhigh,xunits))
    else:
      labels.append("{0:.4g} < {1} < {2:.4g}".format(xlow,xvarname,xhigh))
  if c.GetLogy() == 1:
    ybound = ymax * 10**((log10(ymax)+1)*0.5)
    axisHist = Hist2D(1,xlimits[0],xlimits[1],1,0.1,ybound)
  else:
    axisHist = Hist2D(1,xlimits[0],xlimits[1],1,0,ymax*1.1)
  setHistTitles(axisHist,xtitle,ytitle)
  axisHist.Draw()
  for sliceHist in sliceHists:
    sliceHist.Draw("histsame")
  histAll.Draw("histsame")
  leg = drawNormalLegend([histAll]+sliceHists,labels)
  c.SaveAs(savename+".png")
  c.SaveAs(savename+".pdf")

def getMaxAndFWHM(hist,xBin):
  sliceHist = getXBinHist(hist,xBin)
  nBins = sliceHist.GetNbinsX()
  contentMax = sliceHist.GetMaximum()
  halfContentMax = 0.5*contentMax
  iMax = sliceHist.GetMaximumBin()
  xMax = sliceHist.GetXaxis().GetBinCenter(iMax)
  xHalfMaxAbove = float('nan')
  xHalfMaxBelow = float('nan')
  for iBin in range(iMax,nBins+2):
    if sliceHist.GetBinContent(iBin) <= halfContentMax:
        xHalfMaxAbove = sliceHist.GetXaxis().GetBinLowEdge(iBin)
        break
  for iBin in range(iMax,-1,-1):
    if sliceHist.GetBinContent(iBin) <= halfContentMax:
        xHalfMaxBelow = sliceHist.GetXaxis().GetBinUpEdge(iBin)
        break
  fwhm = xHalfMaxAbove-xHalfMaxBelow
  return xMax, fwhm

def getFracMaxVals(hist,frac=0.5):
  nBins = hist.GetNbinsX()
  contentMax = hist.GetMaximum()
  halfContentMax = frac*contentMax
  iMax = hist.GetMaximumBin()
  xMax = hist.GetXaxis().GetBinCenter(iMax)
  xHalfMaxAbove = float('nan')
  xHalfMaxBelow = float('nan')
  for iBin in range(iMax,nBins+2):
    if hist.GetBinContent(iBin) <= halfContentMax:
        xHalfMaxAbove = hist.GetXaxis().GetBinLowEdge(iBin)
        break
  for iBin in range(iMax,-1,-1):
    if hist.GetBinContent(iBin) <= halfContentMax:
        xHalfMaxBelow = hist.GetXaxis().GetBinUpEdge(iBin)
        break
  return xHalfMaxBelow, xHalfMaxAbove


def makeGraphsModeAndFWHM(hist):
  hist = hist.Clone(uuid.uuid1().hex)
  graph = root.TGraph()
  graphFWHM = root.TGraph()
  for iBin in range(1,hist.GetNbinsX()+1):
    yMax, fwhm = getMaxAndFWHM(hist,iBin)
    x = hist.GetXaxis().GetBinCenter(iBin)
    graph.SetPoint(iBin-1,x,yMax)
    graphFWHM.SetPoint(iBin-1,x,fwhm)
  return graph, graphFWHM

def fitLandaus(c,hist,postfix,caption,fitMin=1.6,fitMax=2.3,nLandaus=3,smearGauss=True,fixedLandauWidth=None,dQdx=False,dumpFitPlot=False):
  if nLandaus <= 0:
    raise ValueError("nLandaus must be > 0")

  xTitle = "dE/dx [MeV/cm]"
  if dQdx:
    xTitle = "dQ/dx [ADC ns / cm]"

  t = root.RooRealVar("t",xTitle,0.,30)
  t.setBins(10000,"cache")
  observables = root.RooArgSet(t)

  data = root.RooDataHist("data_"+hist.GetName(),"Data Hist",root.RooArgList(t),hist)

  ##############

  mg = root.RooRealVar("mg","mg",0)
  sg = root.RooRealVar("sg","sg",0.1,0.01,2.)
  gauss = root.RooGaussian("gauss","gauss",t,mg,sg)

  landauParams = []
  landaus = []
  langauses = []

  for iLandau in range(1,nLandaus+1):
    iLandauStr = str(iLandau)
    mpvl = root.RooRealVar("mpvl"+iLandauStr,"mpv landau "+iLandauStr,1.7,0,5)
    wl = None
    if fixedLandauWidth is None:
      wl = root.RooRealVar("wl"+iLandauStr,"width landau "+iLandauStr,0.42,0.01,10)
    else:
      wl = root.RooRealVar("wl"+iLandauStr,"width landau "+iLandauStr,fixedLandauWidth)
    ml = root.RooFormulaVar("ml"+iLandauStr,"first landau param "+iLandauStr,"@0+0.22278*@1",root.RooArgList(mpvl,wl))
    landau = root.RooLandau("lx"+iLandauStr,"lx "+iLandauStr,t,ml,wl)

    landauParams += [mpvl,wl,ml]
    landaus.append(landau)

    langaus = root.RooFFTConvPdf("langaus"+iLandauStr,"landau (X) gauss "+iLandauStr,t,landau,gauss)
    langaus.setBufferFraction(0.2)
    langauses.append(langaus)

  ratioParams = []

  for iRatio in range(1,nLandaus):
    iRatioStr = str(iRatio)
    ratio = root.RooRealVar("ratio"+iRatioStr,"ratio "+iRatioStr,0.18,0,1)
    ratioParams.append(ratio)

  model = landaus[0]
  multiLandaus = None
  multiLangaus = None
  if nLandaus > 1:
    multiLandaus = root.RooAddPdf("multiLandaus","multiLandaus",root.RooArgList(*landaus),root.RooArgList(*ratioParams))
    multiLangaus = root.RooAddPdf("multiLangaus","multiLangaus",root.RooArgList(*langauses),root.RooArgList(*ratioParams))
    model = multiLandaus
    if smearGauss:
      model = multiLangaus

  ##############

  plotOnBaseArgs = []

  printLevel = root.RooFit.PrintLevel(-1) #Makes RooFit and MINUIT mostly quiet
  if not (fitMin is None or fitMax is None):
    model.fitTo(data,root.RooFit.Range(fitMin,fitMax),printLevel)
    plotOnBaseArgs.append(root.RooFit.Range(fitMin,fitMax))
  else:
    model.fitTo(data,printLevel)

  if dumpFitPlot:
    frame = t.frame(root.RooFit.Title(""))
    plotOnBaseArgs.insert(0,frame)

    data.plotOn(frame)

    print "plotOnBaseArgs", plotOnBaseArgs
    model.plotOn(*plotOnBaseArgs)

    for iLandau in range(2,nLandaus+1):
      iLandauStr = str(iLandau)
      plotOnArgs = plotOnBaseArgs + [root.RooFit.LineStyle(root.kDashed),root.RooFit.LineColor(COLORLIST[iLandau])]
      if smearGauss:
        plotOnArgs.append(root.RooFit.Components("langaus"+iLandauStr))
      else:
        plotOnArgs.append(root.RooFit.Components("lx"+iLandauStr))
      model.plotOn(*plotOnArgs)

    #root.gPad.SetLeftMargin(0.15)
    #frame.GetYaxis().SetTitleOffset(1.4)
    #frame.Draw("same")
    #axisHist = root.TH2F("axisHist","",1,0,50,1,0,1000)
    ##axisHist = root.TH2F("axisHist","",1,-1,1,1,1000,1300)
    #axisHist.Draw()
    #frame.Draw("same")
    frame.Draw()
    frame.SetTitle(caption)
    c.SaveAs("roofit_landau_{}.png".format(postfix))

  bestFits = []
  errs = []
  for iLandau in range(nLandaus):
    for iParam in range(2):
      param = landauParams[iParam+iLandau*3]
      bestFits.append(param.getVal())
      errs.append(param.getError())

  if smearGauss:
    bestFits.append(sg.getVal())
    errs.append(sg.getError())

  return bestFits, errs

def fitSlicesLandaus(c,hist,fileprefix,nJump=1,nLandaus=1,smearGauss=False,fracMax=None,dumpFitPlots=False):
  xaxis = hist.GetXaxis()
  xTitle = xaxis.GetTitle()
  yaxis = hist.GetYaxis()
  yTitle = yaxis.GetTitle()
  mpvlGraph = root.TGraphErrors()
  wlGraph = root.TGraphErrors()
  sgGraph = root.TGraphErrors()
  fwhmGraph = root.TGraphErrors()
  iPoint=0
  for i in range(hist.GetNbinsX()//nJump):
      firstBin = i*nJump+1
      lastBin = (i+1)*(nJump)
      lastBin = min(lastBin,hist.GetNbinsX())
      histAll = hist.ProjectionY("_pyAll",firstBin,lastBin)
      if histAll.GetEntries() < 10:
        continue
      postfix = "_"+fileprefix+"bins{}".format(i)
      xMin = xaxis.GetBinLowEdge(firstBin)
      xMax = xaxis.GetBinUpEdge(lastBin)
      caption = "{} from {} to {}".format(xTitle,xMin,xMax)
      xMiddle = 0.5*(xMax+xMin)
      xError = 0.5*(xMax-xMin)
      startFit = 0.
      endFit = 0.
      startFit = None
      endFit = None
      if not (fracMax is None):
        startFit, endFit = getFracMaxVals(histAll,fracMax)
      bestFits,errors = fitLandaus(c,histAll,postfix,caption,fitMin=startFit,fitMax=endFit,nLandaus=1,smearGauss=smearGauss,dumpFitPlot=dumpFitPlots)
      #if and (mpvlErr > 0.5 or wlErr > 0.5 or sgErr > 0.5):
      #      continue
      mpvlGraph.SetPoint(iPoint,xMiddle,bestFits[0])
      wlGraph.SetPoint(iPoint,xMiddle,bestFits[1])
      mpvlGraph.SetPointError(iPoint,xError,errors[0])
      wlGraph.SetPointError(iPoint,xError,errors[1])
      iPoint += 1
  graphs = [mpvlGraph,wlGraph]
  labels = ["Landau MPV", "Landau Width"]
  #graphs = [mpvlGraph,sgGraph]
  #labels = ["Landau MPV", "Gaussian #sigma"]
  for i, graph in enumerate(graphs):
    graph.SetLineColor(COLORLIST[i])
    graph.SetMarkerColor(COLORLIST[i])
  pad1 = root.TPad("pad1"+hist.GetName(),"",0.02,0.50,0.98,0.98,0)
  pad2 = root.TPad("pad2"+hist.GetName(),"",0.02,0.01,0.98,0.49,0)
  c.cd()
  c.Clear()
  pad1.Draw()
  pad2.Draw()
  pad1.cd()
  axis1 = drawGraphs(pad1,[mpvlGraph],xTitle,"Landau MPV [MeV/cm]",yStartZero=False)
  pad2.cd()
  #axis2 = drawGraphs(pad2,[sgGraph],xTitle,"Gaussian #sigma [MeV/cm]")
  axis2 = drawGraphs(pad2,[wlGraph],xTitle,"Landau Width [MeV/cm]")
  #leg = drawNormalLegend(graphs,labels,option="lep",position=[0.2,0.50,0.6,0.70])
  c.cd()
  c.SaveAs("SliceFitParams_"+fileprefix+".png")
  c.SaveAs("SliceFitParams_"+fileprefix+".pdf")
  return mpvlGraph,wlGraph

def fitGaussCore(c,hist,postfix,caption,fitMin=1.4,fitMax=2.4):

  xMin = hist.GetXaxis().GetBinLowEdge(1)
  xMax = hist.GetXaxis().GetBinUpEdge(hist.GetNbinsX())
  t = root.RooRealVar("t","dE/dx [MeV/cm]",xMin,xMax)
  observables = root.RooArgSet(t)

  data = root.RooDataHist("data_"+hist.GetName(),"Data Hist",root.RooArgList(t),hist)

  ##############
  mg = root.RooRealVar("mg","mg",1.7,0.,5.)
  sg = root.RooRealVar("sg","sg",0.1,0.01,2.)
  gauss = root.RooGaussian("gauss","gauss",t,mg,sg)

  model = gauss

  ##############

  fitResult = model.fitTo(data,root.RooFit.Save(),root.RooFit.Range(fitMin,fitMax))

  frame = t.frame(root.RooFit.Title(""))
  data.plotOn(frame)
  model.plotOn(frame,root.RooFit.Range(fitMin,fitMax))

  #root.gPad.SetLeftMargin(0.15)
  #frame.GetYaxis().SetTitleOffset(1.4)
  #frame.Draw("same")
  #axisHist = root.TH2F("axisHist","",1,0,50,1,0,1000)
  ##axisHist = root.TH2F("axisHist","",1,-1,1,1,1000,1300)
  #axisHist.Draw()
  #frame.Draw("same")
  frame.Draw()
  frame.SetTitle(caption)
  c.SaveAs("roofit_gauss_{}.png".format(postfix))
  c.SaveAs("roofit_gauss_{}.pdf".format(postfix))

  fwhm = calcFWHM(model,t,1.,4.,0.01)

  return (mg.getVal(),float('nan'),sg.getVal()), (mg.getError(),float('nan'),sg.getError()), fwhm

def fitLandauCore(c,hist,postfix,caption,fitMin=1.6,fitMax=2.3,fixedLandauWidth=None,dQdx=False):

  xMin = hist.GetXaxis().GetBinLowEdge(1)
  xMax = hist.GetXaxis().GetBinUpEdge(hist.GetNbinsX())
  if not dQdx:
    xMax = min(xMax,5.)
  xTitle = "dE/dx [MeV/cm]"
  if dQdx:
    xTitle = "dQ/dx [ADC ns / cm]"
  t = root.RooRealVar("t",xTitle,xMin,xMax)
  observables = root.RooArgSet(t)

  data = root.RooDataHist("data_"+hist.GetName(),"Data Hist",root.RooArgList(t),hist)

  mpvl = None
  wl = None
  ml = None
  mg = None
  sg = None
  ##############
  if dQdx:
    mpvl = root.RooRealVar("mpvl","mpv landau",0.5*(fitMin+fitMax),0,xMax*1.5)
    if fixedLandauWidth is None:
      wl = root.RooRealVar("wl","width landau",0.5*(fitMax-fitMin),0.01*(fitMax-fitMin),2*(fitMax-fitMin))
    else:
      wl = root.RooRealVar("wl","width landau",fixedLandauWidth)
    ml = root.RooFormulaVar("ml","first landau param","@0+0.22278*@1",root.RooArgList(mpvl,wl))

    mg = root.RooRealVar("mg","mg",0)
    sg = root.RooRealVar("sg","sg",0.5*(fitMax-fitMin),0.01*(fitMax-fitMin),2*(fitMax-fitMin))
  else:
    mpvl = root.RooRealVar("mpvl","mpv landau",1.7,0,5)
    if fixedLandauWidth is None:
      wl = root.RooRealVar("wl","width landau",0.42,0.01,10)
    else:
      wl = root.RooRealVar("wl","width landau",fixedLandauWidth)
    ml = root.RooFormulaVar("ml","first landau param","@0+0.22278*@1",root.RooArgList(mpvl,wl))

    mg = root.RooRealVar("mg","mg",0)
    sg = root.RooRealVar("sg","sg",0.1,0.01,2.)

  t.Print()
  mpvl.Print()
  wl.Print()
  ml.Print()
  mg.Print()
  sg.Print()

  landau = root.RooLandau("lx","lx",t,ml,wl)
  gauss = root.RooGaussian("gauss","gauss",t,mg,sg)

  t.setBins(10000,"cache")
  langaus = root.RooFFTConvPdf("langaus","landau (X) gauss",t,landau,gauss)
  langaus.setBufferFraction(0.4)

  model = langaus

  ##############

  fitResult = model.fitTo(data,root.RooFit.Save(),root.RooFit.Range(fitMin,fitMax))

  fwhm = None
  if dQdx:
    fwhm = calcFWHM(model,t,0.5*fitMin,fitMax*1.5,(fitMax-fitMin)/200.)
  else:
    fwhm = calcFWHM(model,t,1.,4.,0.01)

  if False:
    frame = t.frame(root.RooFit.Title("landau (x) gauss convolution"))
    data.plotOn(frame)
    model.plotOn(frame,root.RooFit.Range(fitMin,fitMax))

    frame.Draw()
    frame.SetTitle(caption)
    c.SaveAs("roofit_landau_{}.png".format(postfix))
    c.SaveAs("roofit_landau_{}.pdf".format(postfix))

  return (mpvl.getVal(),wl.getVal(),sg.getVal()), (mpvl.getError(),wl.getError(),sg.getError()), fwhm

def fitSlicesLandauCore(c,hist,fileprefix,nJump=1,fracMax=0.4,fixedLandauWidth=0.12,dQdx=False):
  xaxis = hist.GetXaxis()
  xTitle = xaxis.GetTitle()
  yaxis = hist.GetYaxis()
  yTitle = yaxis.GetTitle()
  mpvlGraph = root.TGraphErrors()
  wlGraph = root.TGraphErrors()
  sgGraph = root.TGraphErrors()
  fwhmGraph = root.TGraphErrors()
  iPoint=0
  for i in range(hist.GetNbinsX()//nJump):
      firstBin = i*nJump+1
      lastBin = (i+1)*(nJump)
      lastBin = min(lastBin,hist.GetNbinsX())
      histAll = hist.ProjectionY("_pyAll",firstBin,lastBin)
      if histAll.GetEntries() < 10:
        continue
      postfix = "_"+fileprefix+"bins{}".format(i)
      xMin = xaxis.GetBinLowEdge(firstBin)
      xMax = xaxis.GetBinUpEdge(lastBin)
      caption = "{} from {} to {}".format(xTitle,xMin,xMax)
      xMiddle = 0.5*(xMax+xMin)
      xError = 0.5*(xMax-xMin)
      startFit = 0.
      endFit = 0.
      if dQdx:
        histAllRebin = histAll.Clone(histAll.GetName()+"_rebin")
        histAllRebin.Rebin(2)
        startFit, endFit = getFracMaxVals(histAllRebin,fracMax)
      else:
        startFit, endFit = getFracMaxVals(histAll,fracMax)
      (mpvl,wl,sg),(mpvlErr,wlErr,sgErr), fwhm = fitLandauCore(c,histAll,postfix,caption,startFit,endFit,fixedLandauWidth=fixedLandauWidth,dQdx=dQdx)
      if (not dQdx) and (mpvlErr > 0.5 or wlErr > 0.5 or sgErr > 0.5):
            continue
      if dQdx and mpvl > 4000 :
            continue
      mpvlGraph.SetPoint(iPoint,xMiddle,mpvl)
      wlGraph.SetPoint(iPoint,xMiddle,wl)
      sgGraph.SetPoint(iPoint,xMiddle,sg)
      fwhmGraph.SetPoint(iPoint,xMiddle,fwhm)
      mpvlGraph.SetPointError(iPoint,xError,mpvlErr)
      wlGraph.SetPointError(iPoint,xError,wlErr)
      sgGraph.SetPointError(iPoint,xError,sgErr)
      iPoint += 1
  graphs = [mpvlGraph,wlGraph,sgGraph,fwhmGraph]
  labels = ["Landau MPV", "Landau Width", "Gaussian #sigma","FWHM"]
  #graphs = [mpvlGraph,sgGraph]
  #labels = ["Landau MPV", "Gaussian #sigma"]
  for i, graph in enumerate(graphs):
    graph.SetLineColor(COLORLIST[i])
    graph.SetMarkerColor(COLORLIST[i])
  pad1 = root.TPad("pad1"+hist.GetName(),"",0.02,0.50,0.98,0.98,0)
  pad2 = root.TPad("pad2"+hist.GetName(),"",0.02,0.01,0.98,0.49,0)
  c.cd()
  c.Clear()
  pad1.Draw()
  pad2.Draw()
  pad1.cd()
  axis1 = drawGraphs(pad1,[mpvlGraph],xTitle,"Landau MPV [MeV/cm]",yStartZero=False)
  pad2.cd()
  axis2 = drawGraphs(pad2,[sgGraph],xTitle,"Gaussian #sigma [MeV/cm]")
  #leg = drawNormalLegend(graphs,labels,option="lep",position=[0.2,0.50,0.6,0.70])
  c.cd()
  c.SaveAs(fileprefix+".png")
  c.SaveAs(fileprefix+".pdf")
  return mpvlGraph,wlGraph,sgGraph

def fitSlicesLandauCore3D(c,hist,fileprefix,nJump=1,fracMax=0.4,fixedLandauWidth=0.12,dQdx=False):
  xaxis = hist.GetXaxis()
  xTitle = xaxis.GetTitle()
  yaxis = hist.GetYaxis()
  yTitle = yaxis.GetTitle()
  zaxis = hist.GetZaxis()
  zTitle = zaxis.GetTitle()
  binning = [xaxis.GetNbins(),xaxis.GetXmin(),xaxis.GetXmax(),
             yaxis.GetNbins(),yaxis.GetXmin(),yaxis.GetXmax()
  ]
  zBinning = [zaxis.GetNbins(),zaxis.GetXmin(),zaxis.GetXmax()]
  mpvlHist = Hist2D(*binning)
  wlHist = Hist2D(*binning)
  sgHist = Hist2D(*binning)
  mpvlErrorHist = Hist2D(*binning)
  wlErrorHist = Hist2D(*binning)
  sgErrorHist = Hist2D(*binning)
  fwhmHist = Hist2D(*binning)
  minMPV = 1e9
  minWL = 1e9
  minSG = 1e9
  maxMPV = -1e9
  maxWL = -1e9
  maxSG = -1e9
  for iBinX in range(1,xaxis.GetNbins()+1):
    for iBinY in range(1,yaxis.GetNbins()+1):
      postfix = "_"+fileprefix+"bins{}_{}".format(iBinX,iBinY)
      xMin = xaxis.GetBinLowEdge(iBinX)
      xMax = xaxis.GetBinUpEdge(iBinX)
      yMin = yaxis.GetBinLowEdge(iBinY)
      yMax = yaxis.GetBinUpEdge(iBinY)
      caption = "{} in [{},{}), {} in [{},{})".format(xTitle,xMin,xMax,yTitle,yMin,yMax)
      histForFit = Hist(*zBinning)
      histForFit.GetXaxis().SetTitle(zTitle)
      for iBinZ in range(1,zaxis.GetNbins()+1):
        histForFit.SetBinContent(iBinZ,hist.GetBinContent(iBinX,iBinY,iBinZ))
      if histForFit.Integral(1,zaxis.GetNbins()+1) < 10:
        continue
      if dQdx:
        histForFit.Rebin(2)

      startFit = 0.
      endFit = 0.
      startFit, endFit = getFracMaxVals(histForFit,fracMax)
      (mpvl,wl,sg),(mpvlErr,wlErr,sgErr), fwhm = fitLandauCore(c,histForFit,postfix,caption,startFit,endFit,fixedLandauWidth=fixedLandauWidth,dQdx=dQdx)
      if (mpvlErr/mpvl > 0.02 or wlErr/wl > 0.2 or sgErr/sg > 0.2):
            continue
      mpvlHist.SetBinContent(iBinX,iBinY,mpvl)
      wlHist.SetBinContent(iBinX,iBinY,wl)
      sgHist.SetBinContent(iBinX,iBinY,sg)
      fwhmHist.SetBinContent(iBinX,iBinY,fwhm)
      mpvlErrorHist.SetBinContent(iBinX,iBinY,mpvlErr/mpvl)
      wlErrorHist.SetBinContent(iBinX,iBinY,wlErr/wl)
      sgErrorHist.SetBinContent(iBinX,iBinY,sgErr/sg)
      minMPV = min(mpvl,minMPV)
      minWL = min(wl,minWL)
      minSG = min(sg,minSG)
      maxMPV = max(mpvl,maxMPV)
      maxWL = max(wl,maxWL)
      maxSG = max(sg,maxSG)
  if maxMPV > minMPV:
    mpvlHist.GetZaxis().SetRangeUser(minMPV,maxMPV)
  if maxWL > minWL:
    wlHist.GetZaxis().SetRangeUser(minWL,maxWL)
  if maxSG > minSG:
    sgHist.GetZaxis().SetRangeUser(minSG,maxSG)
  graphs = [mpvlHist,wlHist,sgHist,mpvlErrorHist,wlErrorHist,sgErrorHist,fwhmHist]
  labels = ["Best-Fit Landau MPV", "Best-Fit Landau Width", "Best-Fit Gaussian #sigma",
            "Relative Error Landau MPV", "Relative Error Landau Width", "Relative Error Gaussian #sigma",
            "FWHM"]
  names = ["bfMPV", "bfWL", "bfSigma",
            "relerrMPV", "relerrWL", "relerrSigma",
            "FWHM"]
  setupCOLZFrame(c)
  for graph,label,name in zip(graphs,labels,names):
    graph.Draw("colz")
    print xTitle,yTitle
    setHistTitles(graph,xTitle,yTitle)
    drawStandardCaptions(c,label)
    c.SaveAs(fileprefix+name+".png")
    c.SaveAs(fileprefix+name+".pdf")
  setupCOLZFrame(c,True)
  return mpvlHist,wlHist,sgHist

def compareGraphs(c,outfilePrefix,graphsList,histIndex,xTitle,yTitle,legendTitles,yStartZero=False):
  c.Clear()
  for iColor, graphs in enumerate(graphsList):
        graphs[histIndex].SetMarkerColor(COLORLIST[iColor])
        graphs[histIndex].SetLineColor(COLORLIST[iColor])
  axisHist = drawGraphs(c,[x[histIndex] for x in graphsList],xTitle,yTitle,yStartZero=yStartZero,freeTopSpace=0.4)
  leg = drawNormalLegend([x[histIndex] for x in graphsList],legendTitles,option="ep")
  c.SaveAs(outfilePrefix+".png")
  c.SaveAs(outfilePrefix+".pdf")
  c.Clear()
