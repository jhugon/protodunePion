from misc import *

def Hist(*args,**kargs):
  """
  Returns TH1F with UUID for name and "" for title.
  The arguments are used as the binning.
  """
  func = root.TH1F
  if "TH1D" in kargs and kargs["TH1D"]:
    func = root.TH1D
  if "TEfficiency" in kargs and kargs["TEfficiency"]:
    func = root.TEfficiency
  name = uuid.uuid1().hex
  hist = None
  if len(args) == 1 and type(args[0]) == list:
    hist = func(name,"",len(args[0])-1,array.array('f',args[0]))
  elif len(args) == 3:
    for i in range(3):
      if not isinstance(args[i],numbers.Number):
        raise Exception(i,"th argument is not a number")
    hist = func(name,"",args[0],args[1],args[2])
  else:
    raise Exception("Hist: Innapropriate arguments, requires either nBins, low, high or a list of bin edges:",args)
  return hist

def Hist2D(*args,**kargs):
  """
  Returns TH2F with UUID for name and "" for title.
  The arguments are used as the binning.
  """
  func = root.TH2F
  if "TH2D" in kargs and kargs["TH2D"]:
    func = root.TH2D
  if "TEfficiency" in kargs and kargs["TEfficiency"]:
    func = root.TEfficiency
  name = uuid.uuid1().hex
  hist = None
  if len(args) == 2 and type(args[0]) == list and type(args[1]) == list:
    hist = func(name,"",len(args[0])-1,array.array('f',args[0]),len(args[1])-1,array.array('f',args[1]))
  elif len(args) == 6:
    for i in range(6):
      if not isinstance(args[i],numbers.Number):
        raise Exception(i,"th argument is not a number")
    hist = func(name,"",args[0],args[1],args[2],args[3],args[4],args[5])
  elif len(args) == 4:
    if type(args[0]) == list:
      for i in range(1,4):
        if not isinstance(args[i],numbers.Number):
          raise Exception(i,"th argument is not a number")
      hist = func(name,"",len(args[0])-1,array.array('d',args[0]),args[1],args[2],args[3])
    elif type(args[3]) == list:
      for i in range(3):
        if not isinstance(args[i],numbers.Number):
          raise Exception(i,"th argument is not a number")
      hist = func(name,"",args[0],args[1],args[2],len(args[3])-1,array.array('d',args[3]))
  else:
    raise Exception("Hist: Innapropriate arguments, requires either nBins, low, high or a list of bin edges:",args)
  return hist

def Hist3D(*args,**kargs):
  """
  Returns TH3F with UUID for name and "" for title.
  The arguments are used as the binning.
  """
  func = root.TH3F
  if "TH3D" in kargs and kargs["TH3D"]:
    func = root.TH3D
  name = uuid.uuid1().hex
  hist = None
  if len(args) == 3 and type(args[0]) == list and type(args[1]) == list and type(args[2]) == list:
    hist = func(name,"",len(args[0])-1,array.array('f',args[0]),len(args[1])-1,array.array('f',args[1]),len(args[2])-2,array.array('f',args[2]))
  elif len(args) == 9:
    for i in range(9):
      if not isinstance(args[i],numbers.Number):
        raise Exception(i,"th argument is not a number")
    hist = func(name,"",args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
  else:
    raise Exception("Hist: Innapropriate arguments, requires either nBins, low, high or a list of bin edges:",args)
  return hist


def setHistTitles(hist,xlabel,ylabel,zlabel=None,title=""):
    hist.SetTitle(title)
    hist.GetXaxis().SetTitle(xlabel)
    hist.GetYaxis().SetTitle(ylabel)
    if zlabel:
      hist.GetZaxis().SetTitle(zlabel)

def getXBinHist(inHist, xBin):
  """
  Makes a TH1 hisogram from a TH2
  A vertical slice of a 2D histo
  """
  outHist = inHist.ProjectionY("_slice{}".format(xBin))
  outHist.Reset()
  outHist.SetName(inHist.GetName()+"XSliceBin"+str(xBin))
  outHist.Sumw2()
  nBins = outHist.GetXaxis().GetNbins()
  for i in range(0,nBins+2):
    outHist.SetBinContent(i,inHist.GetBinContent(xBin,i))
    outHist.SetBinError(i,inHist.GetBinError(xBin,i))
  return outHist

def getYBinHist(inHist, yBin):
  """
  Makes a TH1 hisogram from a TH2
  A horizontal slice of a 2D histo
  """
  outHist = inHist.ProjectionX()
  outHist.Reset()
  outHist.SetName(inHist.GetName()+"YSliceBin"+str(yBin))
  outHist.Sumw2()
  nBins = outHist.GetXaxis().GetNbins()
  for i in range(0,nBins+2):
    outHist.SetBinContent(i,inHist.GetBinContent(i,yBin))
    outHist.SetBinError(i,inHist.GetBinError(i,yBin))
  return outHist

def getHistMedian(hist):
  """
  Gets Median of 1D hist
  """
  nBins = hist.GetXaxis().GetNbins()
  total = hist.Integral(1,nBins)
  if total == 0:
    return None
  half = total/2.
  count = 0.
  iLast = 0
  for i in range(1,nBins+1):
    n = hist.GetBinContent(i)
    count += n
    iLast = i
    if count > half:
        pass
  return iLast

def getHistMode(hist):
  """
  Gets Mode of 1D hist
  """
  iMax = -1
  histMax = -999999.
  nBins = hist.GetXaxis().GetNbins()
  for i in range(1,nBins+1):
    n = hist.GetBinContent(i)
    if n > histMax:
        histMax = n
        iMax = i
  if iMax != -1:
    return hist.GetXaxis().GetBinCenter(iMax)
  else:
    return None

def getHistFracMaxVals(hist,frac,mode=None):
    """
    Finds the values on either side of the mode
    where the data has dropped below frac of the
    max value
    """
    nBins = hist.GetXaxis().GetNbins()
    if mode is None:
        mode = getHistMode(hist)
    iMode = hist.GetXaxis().FindBin(mode)
    nFracMax = hist.GetBinContent(iMode)*frac
    minVal = None
    maxVal = None
    for i in range(iMode,0,-1):
      if hist.GetBinContent(i) <= nFracMax:
        minVal = hist.GetXaxis().GetBinUpEdge(i)
        break
    for i in range(iMode,nBins+1):
      if hist.GetBinContent(i) <= nFracMax:
        maxVal = hist.GetXaxis().GetBinLowEdge(i)
        break
    return minVal,maxVal

def getHistFWHM(hist,mode=None):
    minVal, maxVal = getHistFracMaxVals(hist,0.5,mode=mode)
    if (minVal is None) or (maxVal is None):
        return None
    return maxVal-minVal

def divideYValByXVal(hist):
    nBinsX = hist.GetXaxis().GetNbins()
    for iBinX in range(1,nBinsX+1):
	binVal = hist.GetBinContent(iBinX)
	binErrVal = hist.GetBinError(iBinX)
	xVal = hist.GetXaxis().GetBinCenter(iBinX)
	hist.SetBinContent(iBinX,binVal/xVal)
	hist.SetBinError(iBinX,binErrVal/xVal)

def setHistRange(hist,xMin,xMax,yMin,yMax):
    hist.GetXaxis().SetRangeUser(xMin,xMax)
    hist.GetYaxis().SetRangeUser(yMin,yMax)

def makeWeightHist(f1,canvas,leg):
  firstHist = True
  canvas.cd()
  canvas.SetLogy()
  colorsList = [1,2,3,4,5,6,7,8]
  nColors = len(colorsList)
  iDir = 0
  leg.Clear()
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  tmpList = []
  for dirName in f1.GetListOfKeys():
    tmpList.append(dirName)
  tmpList.reverse()
  for dirName in tmpList:
    print(dirName.GetName())
    if(re.search(r"data",dirName.GetName())):
	continue
    directory = dirName.ReadObj()
    for histKey in directory.GetListOfKeys():
      if(histKey.GetName()=="hWeight"):
        hist = histKey.ReadObj()
	hist.UseCurrentStyle()
	hist.SetLineColor(colorsList[iDir % nColors])
	hist.SetMarkerColor(colorsList[iDir % nColors])
	allIntegral = hist.Integral(0,hist.GetNbinsX()+1)
	integral = hist.Integral()
	if integral > 0.0:
	  print("Fraction Outside of bounds: %f" % (allIntegral/integral-1.0))
	  #hist.Scale(1.0/allIntegral)
	  hist.Scale(1.0/integral)
	else:
	  leg.AddEntry(hist,dirName.GetName(),"lep")
	if(firstHist):
	  firstHist=False
	  hist.GetYaxis().SetTitle("Fraction of Events")
	  hist.GetXaxis().SetTitle("Event Weight")
	  #hist.GetXaxis().SetRangeUser(0.0,1.0)
	  hist.Draw()
	else:
	  hist.Draw("same")
    iDir += 1
  leg.Draw("same")

def makeBootstrapHist(hist,outHist,entries=None):
 outHist.Reset()
 samples = entries
 if samples == None:
   integral = hist.Integral()
 for i in range(samples):
   outHist.Fill(hist.GetRandom())

def sqrtThisHistogram(hist):
    """
        Sqrt's bin contents 
        of the input hist bin contents, properly treating the errors.
    """
    nBins = hist.GetNbinsX()

    for i in range(nBins+2):
      y = hist.GetBinContent(i)
      yErr = hist.GetBinError(i)
      if y < 0.0:
        print("Warning sqrtThisHIstogram: hist named %s bin %i has negative y value %f" % (hist.GetName(),i,y))
        hist.SetBinContent(i,0.0)
        hist.SetBinError(i,0.0)
        continue
      if y == 0.0:
        print("Warning sqrtThisHIstogram: hist named %s bin %i has zero y value" % (hist.GetName(),i))
        hist.SetBinContent(i,0.0)
        hist.SetBinError(i,0.0)
        continue
      hist.SetBinContent(i,sqrt(y))
      hist.SetBinError(i,yErr/(sqrt(2*y)))

def getSqrtCopyOfHistogram(hist):
    """
        Reterns a histogram of where the bin contents are the sqrt
        of the input hist bin contents, properly treating the errors.
    """
    outHist = hist.Clone(hist.GetName()+"SqrtHist")
    sqrtThisHistogram(outHist)
    return outHist

def normalizeHist(hist):
  integral = hist.Integral(0,hist.GetNbinsX()+1)
  if integral != 0.0:
    hist.Scale(1.0/integral)

def showHistOverflow(hist):
  nBins = hist.GetNbinsX()

  overflow = hist.GetBinContent(nBins+1)
  overflowErr = hist.GetBinError(nBins+1)
  lastBin = hist.GetBinContent(nBins)
  lastBinErr = hist.GetBinError(nBins)

  hist.SetBinContent(nBins,lastBin+overflow)
  hist.SetBinError(nBins,sqrt(lastBinErr**2+overflowErr**2))

  underflow = hist.GetBinContent(0)
  underflowErr = hist.GetBinError(0)
  firstBin = hist.GetBinContent(1)
  firstBinErr = hist.GetBinError(1)

  hist.SetBinContent(1,firstBin+underflow)
  hist.SetBinError(1,sqrt(firstBinErr**2+underflowErr**2))

class PlotOfSlices:
  def __init__(self, hist2D, xtitle, ytitle, canvas, xlimits=[], ylimits=[],sliceLabelPrefix="",isPreliminary=True,is7TeV=False):
    canvas.cd(0)
    canvas.Clear()
    nBinsX = hist2D.GetNbinsX()
    nBinsY = hist2D.GetNbinsY()
    self.nBinsX = nBinsX
    self.nBinsY = nBinsY
    self.hist2D = hist2D
    self.canvas = canvas
    self.sliceLabelPrefix = sliceLabelPrefix
    self.tlatex = root.TLatex()
    self.tlatex.SetNDC()
    self.tlatex.SetTextFont(root.gStyle.GetLabelFont())
    self.tlatex.SetTextSize(0.05)
    self.tlatex.SetTextAlign(22)
    self.histList = []

    colorsListTmp = [root.kRed+1,root.kBlue+1,root.kGreen+1,root.kCyan,root.kMagenta+1]
    self.colorsList=[]
    for i in [0,-11,+2]:
        for j in range(len(colorsListTmp)):
            self.colorsList.append(colorsListTmp[j]+i)

    if xlimits != []:
      self.hist2D.GetXaxis().SetRangeUser(*xlimits)
    if ylimits != []:
      self.hist2D.GetYaxis().SetRangeUser(*ylimits)

    ymax = 0.0
    for i in range(nBinsX+2):
        tmpHist = root.TH1F(hist2D.GetName()+"_slice"+str(i),"",
                            nBinsY,hist2D.GetYaxis().GetXbins().GetArray())
        for j in range(nBinsY+2):
            tmpHist.SetBinContent(j,hist2D.GetBinContent(i,j))
        tmpMax = tmpHist.GetMaximum()
        if tmpMax > ymax:
            ymax = tmpMax
        tmpHist.SetLineColor(self.colorsList[i])
        self.histList.append(tmpHist)
    
    firstHist = self.histList[0]
    firstHist.SetTitle("")
    firstHist.GetXaxis().SetTitle(xtitle)
    firstHist.GetYaxis().SetTitle(ytitle)
    if xlimits != []:
        firstHist.GetXaxis().SetRangeUser(*xlimits)
    if ylimits==[]:
        firstHist.GetYaxis().SetRangeUser(0.0,ymax*1.05)
    else:
        firstHist.GetYaxis().SetRangeUser(*ylimits)

    firstHist.Draw("")
    for hist in self.histList[1:]:
        hist.Draw("same")

    if isPreliminary:
      self.tlatex.DrawLatex(0.33,0.96,"CMS Preliminary")
    if is7TeV:
      self.tlatex.DrawLatex(0.75,0.96,"#sqrt{s}=8 TeV, L=4.7 fb^{-1}")

    ## Lgend Part

    leg = root.TLegend(0.6,0.3,0.9,0.9)
    leg.SetLineColor(root.kWhite)
    leg.SetFillColor(root.kWhite)
    self.leg = leg
    xAxis = self.hist2D.GetXaxis()
    xBin = 0
    for hist in self.histList:
      tmpLabel = ""
      if xBin == 0:
        tmpLabel = "%s [0.0,%.1f]" % (sliceLabelPrefix,xAxis.GetBinUpEdge(xBin))
      elif xBin == nBinsX+1:
        tmpLabel = "%s [%.1f,#infty]" % (sliceLabelPrefix,xAxis.GetBinLowEdge(xBin))
      else:
        tmpLabel = "%s [%.1f,%.1f]" % (sliceLabelPrefix,xAxis.GetBinLowEdge(xBin),xAxis.GetBinUpEdge(xBin))
      leg.AddEntry(hist,tmpLabel,"l")
      xBin += 1
    leg.Draw("same")

def getIntegralHist(hist,setErrors=True,reverse=False):
  result = hist.Clone(hist.GetName()+"_Integral")
  if hist.InheritsFrom("TH2"):
    nBinsX = result.GetNbinsX()
    nBinsY = result.GetNbinsY()
    iXRange = range(nBinsX+2)
    if reverse:
        iXRange.reverse()
    iYRange = range(nBinsY+2)
    if reverse:
        iYRange.reverse()
    for iX in iXRange:
      for iY in iYRange:
        sumw = 0.0
        sumw2 = 0.0
        if reverse:
          for jX in range(0,iX+1):
            for jY in range(0,iY+1):
              sumw += result.GetBinContent(jX,jY)
              sumw2 += (result.GetBinError(jX,jY))**2
        else:
          for jX in range(iX,nBinsX+2):
            for jY in range(iY,nBinsY+2):
              sumw += result.GetBinContent(jX,jY)
              sumw2 += (result.GetBinError(jX,jY))**2
        result.SetBinContent(iX,iY,sumw)
        if setErrors:
            result.SetBinError(iX,iY,sumw2**0.5)
  else:
    nBins = result.GetNbinsX()
    iRange = range(nBins+1)
    if reverse:
        iRange.reverse()
    for i in iRange:
      sumw = 0.0
      sumw2 = 0.0
      if reverse:
        for j in range(0,i+1): # include underflow 0 and current bin i
          sumw += result.GetBinContent(j)
          sumw2 += (result.GetBinError(j))**2
      else:
        for j in range(i,nBins+2): # include current bin i and overflow nBins + 1
          sumw += result.GetBinContent(j)
          sumw2 += (result.GetBinError(j))**2
      result.SetBinContent(i,sumw)
      if setErrors:
          result.SetBinError(i,sumw2**0.5)
  return result

def normalizeYSlices(hist):
  assert(hist.InheritsFrom("TH2"))
  nBinsX = hist.GetNbinsX()
  nBinsY = hist.GetNbinsY()
  for iBinX in range(1,nBinsX+1):
    sliceTotal = 0.
    for iBinY in range(0,nBinsY+2):
      sliceTotal += hist.GetBinContent(iBinX,iBinY)
    if sliceTotal > 0.:
      for iBinY in range(0,nBinsY+2):
        hist.SetBinContent(iBinX,iBinY,hist.GetBinContent(iBinX,iBinY)/sliceTotal)

def hist2to1(hist):
  assert(hist.InheritsFrom("TH1"))
  result = None
  nBinsX = hist.GetNbinsX()
  nBinsY = hist.GetNbinsY()
  totalBins = (nBinsX+2)*(nBinsY+2) - 2 #include underflow/overflow
  if hist.InheritsFrom("TH2F"):
    result = root.TH1F(hist.GetName()+"_1d","",totalBins,0,totalBins)
  elif hist.InheritsFrom("TH2D"):
    result = root.TH1D(hist.GetName()+"_1d","",totalBins,0,totalBins)
  else:
    print("Error: hist2to1: Input hist must be TH2F or TH2D, exiting.")
    sys.exit(1)
  k = 0
  for i in range(nBinsX+2):
    for j in range(nBinsY+2):
      tmp = hist.GetBinContent(i,j)
      tmpErr = hist.GetBinError(i,j)
      result.SetBinContent(k,tmp)
      result.SetBinError(k,tmpErr)
      k += 1
  return result

def hist2to1CollapseY(hist,xcuts=[]):
  assert(hist.InheritsFrom("TH1"))
  result = None
  nBinsX = hist.GetNbinsX()
  nBinsY = hist.GetNbinsY()
  ymin = hist.GetYaxis().GetXmin()
  ymax = hist.GetYaxis().GetXmax()
  totalBins = (nBinsX+2)*(nBinsY+2) - 2 #include underflow/overflow
  if hist.InheritsFrom("TH2F"):
    result = root.TH1F(hist.GetName()+"_1d","",nBinsY,ymin,ymax)
  elif hist.InheritsFrom("TH2D"):
    result = root.TH1D(hist.GetName()+"_1d","",nBinsY,ymin,ymax)
  else:
    print("Error: hist2to1CollapseY: Input hist must be TH2F or TH2D, exiting.")
    sys.exit(1)
  minBinX = 0
  maxBinX = nBinsX+2
  if len(xcuts)==2:
    minBinX = hist.GetXaxis().FindBin(xcuts[0])
    maxBinX = hist.GetXaxis().FindBin(xcuts[1])
    if hist.GetXaxis().GetBinCenter(maxBinX)> xcuts[1]:
        maxBinX -= 1
  for j in range(nBinsY+2):
    tmpSum = 0.0
    tmpSumErr2 = 0.0
    for i in range(minBinX,maxBinX):
      tmp = hist.GetBinContent(i,j)
      tmpErr = hist.GetBinError(i,j)
      tmpSum += tmp
      tmpSumErr2 += tmpErr*tmpErr
    result.SetBinContent(j,tmpSum)
    result.SetBinError(j,sqrt(tmpSumErr2))
  return result

def shrinkTH1(hist,xlow,xhigh,deleteOld=False):
  assert(hist.InheritsFrom("TH1"))
  taxis=hist.GetXaxis()
  oldXlow=taxis.GetXmin()
  oldXhigh=taxis.GetXmax()
  assert(xlow >= oldXlow)
  assert(xhigh <= oldXhigh)
  lowBin = taxis.FindBin(xlow)
  highBin = taxis.FindBin(xhigh)
  if taxis.GetBinLowEdge(highBin)==float(xhigh):
    highBin -= 1
  xlow = taxis.GetBinLowEdge(lowBin)
  xhigh = taxis.GetBinUpEdge(highBin)
  oldN = hist.GetNbinsX()
  newN = int((xhigh-xlow)/(oldXhigh-oldXlow)*oldN)
  name = hist.GetName()
  title = hist.GetTitle()
  hist.SetName(name+"_Old")
  newHist = root.TH1F(name,title,newN,xlow,xhigh)
  newHist.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
  newHist.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
  for iOld,iNew in zip(range(lowBin,highBin+1),range(1,newN+1)):
    newHist.SetBinContent(iNew,hist.GetBinContent(iOld))
    newHist.SetBinError(iNew,hist.GetBinError(iOld))
  if deleteOld:
    hist.Delete()
  return newHist

def toyHistogram(hist):
  nBins = hist.GetNbinsX()
  random = root.TRandom3()
  for i in range(nBins+2):
    mean = hist.GetBinContent(i)
    n = random.Poisson(mean)
    err = sqrt(n)
    hist.SetBinContent(i,n)
    hist.SetBinError(i,err)

def getXbinsHighLow(hist,low,high):
  axis = hist.GetXaxis()
  xbinLow = axis.FindBin(low)
  xbinHigh = axis.FindBin(high)
  #print("xbinhigh: {0}, {1}, {2}".format(xbinHigh,axis.GetBinLowEdge(xbinHigh),float(high)))
  if axis.GetBinLowEdge(xbinHigh)==float(high):
    xbinHigh -= 1
  return xbinLow, xbinHigh

def getIntegralAll(hist,boundaries=[]):
  xbinLow = None
  xbinHigh = None
  if len(boundaries)==0:
    xbinLow = 0
    xbinHigh = hist.GetXaxis().GetNbins()+1
  elif len(boundaries)==2:
    xbinLow, xbinHigh = getXbinsHighLow(hist,boundaries[0],boundaries[1])
  else:
    return -1
  if hist.InheritsFrom("TH2"):
    nBinsY = hist.GetYaxis().GetNbins()
    return hist.Integral(xbinLow,xbinHigh,0,nBinsY+1)
  elif hist.InheritsFrom("TH1"):
    return hist.Integral(xbinLow,xbinHigh)
  else:
    return -1

def getIntegralLowHigh(hist,lowBoundaries,highBoundaries):
  lowInt = getIntegralAll(hist,lowBoundaries)
  highInt = getIntegralAll(hist,highBoundaries)
  return lowInt+highInt

def sqrtTH1(hist):
  nBins = hist.GetNbinsX()
  for i in range(nBins+2):
    n = hist.GetBinContent(i)
    nErr = hist.GetBinError(i)
    if n < 0.0:
      n = 0.0
    hist.SetBinContent(i,sqrt(n))
    hist.SetBinError(i,sqrt(nErr))

def getBinWidthStr(hist):
    binWidth = (hist.GetXaxis().GetXmax()-hist.GetXaxis().GetXmin())/hist.GetXaxis().GetNbins()
    binWidthPrec = "0"
    if binWidth % 1 > 0.0:
      binWidthPrec = "1"
      if binWidth*10 % 1 > 0.0:
        binWidthPrec = "2"
    return ("%."+binWidthPrec+"f") % (binWidth)

def getHistMax(hist,includeErrorBar=False):
  if hist.InheritsFrom("TEfficiency"):
    return 1.0
  else:
    iBin = hist.GetMaximumBin()
    result = hist.GetBinContent(iBin)
    if includeErrorBar:
      result += hist.GetBinError(iBin)
    return result

def normToBinWidth(hist):
  """
  For TH1, normalizes bin contents to bin width (divides by bin width)
  For TH2, normalizes bin contents to bin area (divides by bin area)
  """
  if hist.InheritsFrom("TH2"):
    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()
    for iX in range(1,nBinsX+1):
      for iY in range(1,nBinsY+1):
        binContent = hist.GetBinContent(iX,iY)
        binWidthX = hist.GetXaxis().GetBinWidth(iX)
        binWidthY = hist.GetYaxis().GetBinWidth(iY)
        binArea = binWidthX*binWidthY
        hist.SetBinContent(iX,iY,binContent/binArea)
    return hist
  else:
    xaxis = hist.GetXaxis()
    nBins = xaxis.GetNbins()
    for i in range(1,nBins+1):
      binContent = hist.GetBinContent(i)
      binWidth = hist.GetBinWidth(i)
      hist.SetBinContent(i,binContent/binWidth)
    return hist

