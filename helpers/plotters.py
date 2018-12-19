from misc import *

def plotManyHistsOnePlot(fileConfigs,histConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint):
  """
  For each file, plots multiple different histograms (cuts and/or variables) on one plot. Use to
    compare different cuts or variables on the same sample. Only for 1D Hists.

  fileConfigs is a list of dictionaries configuring the files. fileConfigs is a
    list so you can plots for multiple samples.
  histConfigs is a list of dictionaries configuring the histograms
  canvas is a root TCanvas
  treename is where to find the tree in each file

  fileConfig options:
    fn: filename str or list of str for a chain. REQUIRED
    pdg: PDG ID number (unused)
    name: name of sample, used for savename REQUIRED
    title: title of sample (unused)
    color:  (unused)
    scaleFactor: scale histograms by this much after filling
    addFriend: add friend tree to main tree. Should be a length 2 list [treename,filename]
    caption, captionleft1, captionleft2, captionleft3, captionright1,
        captionright2, captionright3, preliminaryString:
        all are passed to drawStandardCaptions. histConfig arguments override these
    cuts: additional cuts per file concat to histConfig cuts, default ""
  histConfig options:
    name: (unused)
    title: title of histogram, used for legend
    color: sets line/marker color of histogram
    xtitle: x axis title, the first one found in the list is used
    ytitle: y axis title, the first one found in the list is used
    binning: Binning list, either [nBins,min,max] or a list of bin edges REQUIRED
    var: variable to draw, first argument to tree.Draw REQUIRED
    cuts: cut string, second argument to tree.Draw REQUIRED
    xlim: xlimits, a two element list of xlimits for plot, first one found is used
    ylim: ylimits, a two element list of ylimits for plot, first one found is used
    logy: if True, plot on y on log scale. If any are True, will be logy.
    logx: if True, plot on y on log scale. If any are True, will be logx.
    caption, captionleft1, captionleft2, captionleft3, captionright1,
        captionright2, captionright3, preliminaryString:
        all are passed to drawStandardCaptions, first set of captions found is
        used
    normToBinWidth: if True, normalize histogram to bin width (after applying
        scaleFactor)
    normalize: if True normalize histogram (after normToBinWidth)
    integral: if True, makes each bin content Nevents for X >= bin low edge
    efficiencyDenomCuts: If this is a string, it makes this histogram an efficiency. 
        Use this cut string to create the denominator histogram. The main histogram will be
        the numerator in a TEfficiency.
    profileX: if True, draw profileX of 2D hist
    profileY: if True, draw profileY of 2D hist
    profileStdDev: if True, profile errors are std deviation instead of std error on mean
    drawhlines: list of y locations to draw horizontal lines
    drawvlines: list of x locations to draw vertical lines
  """
  
  #print("plotManyHistsOnePlot")
  for fileConfig in fileConfigs:
    #print("  file: {}, {}".format(fileConfig["title"],fileConfig['fn']))
    loadTree(fileConfig,treename)
    tree = fileConfig['tree']
    xlim = []
    ylim = []
    for histConfig in histConfigs:
      if "xlim" in histConfig: 
        xlim = histConfig['xlim']
        break
    for histConfig in histConfigs:
      if "ylim" in histConfig: 
        ylim = histConfig['ylim']
        break
    logy = False
    logx = False
    for histConfig in histConfigs:
      if "logy" in histConfig and histConfig['logy']: logy = True
      if "logx" in histConfig and histConfig['logx']: logx = True
    
    hists = []
    for histConfig in histConfigs:
      binning = histConfig['binning']
      var = histConfig['var']
      cuts = histConfig['cuts']
      isData = False
      try:
        isData = fileConfig["isData"]
      except KeyError:
        pass
      hist = loadHist(histConfig,fileConfig,binning,var,cuts,nMax=nMax,isData=isData)
      if 'color' in histConfig:
        hist.SetLineColor(histConfig['color'])
        hist.SetMarkerColor(histConfig['color'])
      hists.append(hist)
    canvas.SetLogy(logy)
    canvas.SetLogx(logx)
    axisHist = makeStdAxisHist(hists,logy=logy,freeTopSpace=0.35,xlim=xlim,ylim=ylim)
    axisHist.Draw()
    lines = drawVHLinesForPlot(axisHist,histConfigs)
    for h in reversed(hists):
      if "efficiencyDenomCuts" in histConfig and type(histConfig["efficiencyDenomCuts"]) == str:
        h.Draw("PZ0same")
      elif ("profileX" in histConfig and histConfig["profileX"]) \
            or ("profileY" in histConfig and histConfig["profileY"]):
        h.Draw("Esame")
      else:
        h.Draw("histsame")
    labels = [histConfig['title'] for histConfig in histConfigs]
    for iHist in range(len(hists)):
      histConfig = histConfigs[iHist]
      if "showMedian" in histConfig and histConfig["showMedian"]:
              labels[iHist] += " median: {0}".format(getHistMedian(hists[iHist]))
      if "showMode" in histConfig and histConfig["showMode"]:
              labels[iHist] += " mode: {0}".format(getHistMode(hists[iHist]))
    leg = drawNormalLegend(hists,labels,wide=True)
    drawAnnotationsForPlots(canvas,axisHist,fileConfig,histConfigs)
    canvas.RedrawAxis()
    saveNameBase = outPrefix + fileConfig['name'] + outSuffix
    canvas.SaveAs(saveNameBase+".png")
    canvas.SaveAs(saveNameBase+".pdf")
    canvas.SetLogy(False)
    canvas.SetLogx(False)

def plotOneHistOnePlot(fileConfigs,histConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint,writeImages=True):
  """
  For each histogram in each file, plot a histogram on one plot. Works with 1D,
    2D, and 3D histograms.

  fileConfigs is a list of dictionaries configuring the files. fileConfigs is a
    list so you can plots for multiple samples.
  histConfigs is a list of dictionaries configuring the histograms. It is a
    list so you can do multiple plots for each sample
  canvas is a root TCanvas
  treename is where to find the tree in each file

  returns a list of histograms, profiles, or if profileXtoo=True, (histograms, profiles).

  fileConfig options:
    fn: filename str or list of str for a chain. REQUIRED
    name: name of sample, used for savename REQUIRED
    scaleFactor: scale histogram by this much after filling
    pdg: PDG ID number (unused)
    title: title of sample (unused)
    color:  (unused)
    caption, captionleft1, captionleft2, captionleft3, captionright1,
        captionright2, captionright3, preliminaryString:
        all are passed to drawStandardCaptions. histConfig arguments override these
    cuts: additional cuts per file concat to histConfig cuts, default ""
    writeImage: if False, don't make an image for this file
  histConfig options:
    name: name of histogram, used for savename REQUIRED
    color: sets line/marker color of histogram
    xtitle: x axis title
    ytitle: y axis title
    ztitle: z axis title
    binning: Binning list. For 1D, either [nBins,min,max] or a list of bin edges.
        For 2D, [nBinsX,minX,maxX,nBinsY,minY,maxY] 
        or [list of bin edges X, list of bin edges Y] REQUIRED
    var: variable(s) to draw, first argument to tree.Draw REQUIRED
    cuts: cut string, second argument to tree.Draw REQUIRED
    xlim: xlimits, a two element list of xlimits for plot
    ylim: ylimits, a two element list of ylimits for plot
    logz: if True, plot on z on log scale
    logy: if True, plot on y on log scale
    logx: if True, plot on y on log scale
    caption, captionleft1, captionleft2, captionleft3, captionright1,
        captionright2, captionright3, preliminaryString:
        all are passed to drawStandardCaptions
    normToBinWidth: if True, normalize histogram to bin width (after applying
        scaleFactor)
    normalize: if True normalize histogram (after normToBinWidth)
    normalizeYSlices: For a 2D histogram, normalize all bins for iBinX to 1.
    integral: if True, makes each bin content Nevents for X >= bin low edge.
        For 2D plots, makes each bin content Nevents for X >= and Y >= 
        their low bin edges.
    title: (unused)
    addFriend: add friend tree to main tree. Should be a length 2 list [treename,filename]
    efficiencyDenomCuts: If this is a string, it makes this histogram an efficiency. 
        Use this cut string to create the denominator histogram. The main histogram will be
        the numerator in a TEfficiency.
    profileX: if True, draw profileX of 2D hist
    profileY: if True, draw profileY of 2D hist
    profileStdDev: if True, profile errors are std deviation instead of std error on mean
    profileXtoo: if True, draw profileX of 2D hist, on top of 2D hist
    funcs: List of TF1's to draw on top of the histogram
    graphs: List of TGraphs to draw on top of the histogram
    writeImage: if False, don't make an image for this hist
  """
  
  allHists = {}
  allProfilesToo = {}
  for fileConfig in fileConfigs:
    loadTree(fileConfig,treename)
    tree = fileConfig['tree']
    writeImageFile = True
    if "writeImage" in fileConfig: writeImageFile = fileConfig["writeImage"]
    for histConfig in histConfigs:
      # setup
      binning = histConfig['binning']
      var = histConfig['var']
      ncolon = var.count(":")
      is2D = False
      is3D = False
      if ncolon > 2:
        raise Exception("More than 2 ':' not allowed in variable, only 1D/2D/3D hists allowed",var)
      elif ncolon > 1:
        is3D = True
      elif ncolon == 1:
        is2D = True
      cuts = histConfig['cuts']
      thiscuts = copy.deepcopy(cuts)
      if "cuts" in fileConfig:
        thiscuts += fileConfig['cuts']
      xlim = []
      ylim = []
      zlim = []
      if "xlim" in histConfig: xlim = histConfig['xlim']
      if "ylim" in histConfig: ylim = histConfig['ylim']
      if "zlim" in histConfig: zlim = histConfig['zlim']
      logz = False
      logy = False
      logx = False
      if "logz" in histConfig: logz = histConfig['logz']
      if "logy" in histConfig: logy = histConfig['logy']
      if "logx" in histConfig: logx = histConfig['logx']
      doProfileXtoo = False
      if "profileXtoo" in histConfig and histConfig["profileXtoo"]: doProfileXtoo = True
      doProfileX = False
      if doProfileXtoo or "profileX" in histConfig and histConfig["profileX"]: doProfileX = True
      doProfileY = False
      if "profileY" in histConfig and histConfig["profileY"]: doProfileY = True
      funcs = []
      if "funcs" in histConfig and type(histConfig["funcs"]) == list:
        funcs = histConfig["funcs"]
      graphs = []
      if "graphs" in histConfig and type(histConfig["graphs"]) == list:
        graphs = histConfig["graphs"]
      writeImageHist = True
      if "writeImage" in histConfig: writeImageHist = histConfig["writeImage"]
      # now on to the real work
      hist = None
      if is3D:
        if len(binning) == 3:
          hist = Hist3D(binning[0],binning[1],binning[2])
        else:
          hist = Hist3D(*binning)
        hist.SetMarkerStyle(1)
        hist.SetMarkerSize(1)
      elif is2D:
        if len(binning) == 2:
          hist = Hist2D(binning[0],binning[1])
        else:
          hist = Hist2D(*binning)
      else:
        if len(binning) == 3:
          hist = Hist(*binning)
        else:
          hist = Hist(binning)
      if 'color' in histConfig:
        hist.SetLineColor(histConfig['color'])
      varAndHist = var + " >> " + hist.GetName()
      tree.Draw(varAndHist,thiscuts,"",nMax)
      if "efficiencyDenomCuts" in histConfig and type(histConfig["efficiencyDenomCuts"]) == str:
        denomHist = hist.Clone(hist.GetName()+"_denom")
        denomHist.Reset()
        varAndHistDenom = var + " >> " + denomHist.GetName()
        tree.Draw(varAndHistDenom,histConfig["efficiencyDenomCuts"],"",nMax)
        teff = root.TEfficiency(hist,denomHist)
        hist = teff
      else:
        scaleFactor = 1.
        if "scaleFactor" in fileConfig: scaleFactor = fileConfig['scaleFactor']
        hist.Scale(scaleFactor)
        if "normToBinWidth" in histConfig and histConfig["normToBinWidth"]:
          normToBinWidth(hist)
        if "normalizeYSlices" in histConfig and histConfig['normalizeYSlices']:
            normalizeYSlices(hist)
        if "normalize" in histConfig and histConfig['normalize']:
          integral = hist.Integral()
          if integral != 0.:
            hist.Scale(1./integral)
        if "integral" in histConfig and histConfig['integral']:
          hist = getIntegralHist(hist)
      canvas.SetLogy(logy)
      canvas.SetLogx(logx)
      canvas.SetLogz(logz)
      prof = None
      if doProfileX:
        if "profileStdDev" in histConfig and histConfig["profileStdDev"]:
          prof = hist.ProfileX("_pfx",1,-1,'s')
        else:
          prof = hist.ProfileX()
        if not doProfileXtoo:
          hist = prof
      elif doProfileY:
        if "profileStdDev" in histConfig and histConfig["profileStdDev"]:
          prof = hist.ProfileY("_pfy",1,-1,'s')
        else:
          prof = hist.ProfileY()
          hist = prof
      axisHist = None
      if hist.InheritsFrom("TH3"):
        axisHist = hist
        if xlim:
            axisHist.GetXaxis().SetRangeUser(*xlim)
        if ylim:
            axisHist.GetYaxis().SetRangeUser(*ylim)
        if zlim:
            axisHist.GetZaxis().SetRangeUser(*zlim)
        axisHist.GetZaxis().SetTitle(ztitle)
        hist.Draw("")
      elif hist.InheritsFrom("TH2"):
        setupCOLZFrame(canvas)
        axisHist = hist
        if xlim:
            axisHist.GetXaxis().SetRangeUser(*xlim)
        if ylim:
            axisHist.GetYaxis().SetRangeUser(*ylim)
        if zlim:
            axisHist.GetYaxis().SetRangeUser(*zlim)
        hist.Draw("colz")
        if doProfileXtoo:
            prof.Draw("Esame")
            if not (histConfig['name'] in allProfilesToo):
              allProfilesToo[histConfig['name']] = {}
            allProfilesToo[histConfig['name']][fileConfig['name']] = prof
      else:
        axisHist = makeStdAxisHist([hist],logy=logy,freeTopSpace=0.05,xlim=xlim,ylim=ylim)
        axisHist.Draw()
        if "efficiencyDenomCuts" in histConfig and type(histConfig["efficiencyDenomCuts"]) == str:
          hist.Draw("PZ0same")
        elif doProfileX or doProfileY:
          hist.Draw("Esame")
        else:
          hist.Draw("histsame")
      if writeImages and writeImageFile and writeImageHist:
        lines = drawVHLinesForPlot(axisHist,histConfig)
        for func in funcs:
          func.Draw("LSAME")
        for graph in graphs:
          graph.Draw("PEZ")
        drawAnnotationsForPlots(canvas,axisHist,fileConfig,histConfig)
        canvas.RedrawAxis()
        saveNameBase = outPrefix + histConfig['name'] + "_" + fileConfig['name'] + outSuffix
        canvas.SaveAs(saveNameBase+".png")
        canvas.SaveAs(saveNameBase+".pdf")
      if hist.InheritsFrom("TH2"):
        setupCOLZFrame(canvas,True) #reset frame
      canvas.SetLogy(False)
      canvas.SetLogx(False)
      if not (histConfig['name'] in allHists):
        allHists[histConfig['name']] = {}
      allHists[histConfig['name']][fileConfig['name']] = hist
  if len(allProfilesToo) == 0:
    return allHists
  else:
    return allHists, allProfilesToo

def plotManyFilesOnePlot(fileConfigs,histConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint):
  """
  Plots the same histogram and cuts for a variety of files on one plot. Use to
    compare the same histogram from different samples. Only for 1D Hists.

  fileConfigs is a list of dictionaries configuring the files
  histConfigs is a list of dictionaries configuring the histograms. It is a
    list so you can do multiple plots.
  canvas is a root TCanvas
  treename is where to find the tree in each file

  fileConfig options:
    fn: filename str or list of str for a chain. REQUIRED
    title: title of sample: will be used for legends
    color: will be used for line/marker color
    scaleFactor: scale histograms by this much after filling
    pdg: PDG ID number (unused)
    name: name of sample (unused)
    addFriend: add friend tree to main tree. Should be a length 2 list [treename,filename]
    cuts: additional cuts per file concat to histConfig cuts, default ""
  histConfig options:
    name: name of histogram, used for savename REQUIRED
    xtitle: x axis title
    ytitle: y axis title
    binning: Binning list, either [nBins,min,max] or a list of bin edges REQUIRED
    var: variable to draw, first argument to tree.Draw REQUIRED
    cuts: cut string, second argument to tree.Draw REQUIRED
    xlim: xlimits, a two element list of xlimits for plot
    ylim: ylimits, a two element list of ylimits for plot
    logy: if True, plot on y on log scale
    logx: if True, plot on y on log scale
    caption, captionleft1, captionleft2, captionleft3, captionright1,
        captionright2, captionright3, preliminaryString:
        all are passed to drawStandardCaptions
    normToBinWidth: if True, normalize histogram to bin width (after applying
        scaleFactor)
    normalize: if True normalize histogram (after normToBinWidth)
    integral: if True, makes each bin content Nevents for X >= bin low edge
    title: (unused)
    color: (unused)
    efficiencyDenomCuts: If this is a string, it makes this histogram an efficiency. 
        Use this cut string to create the denominator histogram. The main histogram will be
        the numerator in a TEfficiency.
    drawhlines: list of y locations to draw horizontal lines
    drawvlines: list of x locations to draw vertical lines
    printIntegral: if True, print integral after all scaling
    showMedian: if True, put median in legend
    showMode: if True, put mode in legend
  """
  #print("plotManyFilesOnePlot")
  
  for fileConfig in fileConfigs:
    loadTree(fileConfig,treename)

  for histConfig in histConfigs:
    #print(" hist: {}, {}".format(histConfig["var"],histConfig["cuts"]))
    # setup
    hists = []
    binning = histConfig['binning']
    var = histConfig['var']
    #if var.count(":") != 0:
    #  raise Exception("No ':' allowed in variable, only 1D hists allowed",var)
    cuts = histConfig['cuts']
    xlim = []
    ylim = []
    if "xlim" in histConfig: xlim = histConfig['xlim']
    if "ylim" in histConfig: ylim = histConfig['ylim']
    logy = False
    logx = False
    if "logy" in histConfig: logy = histConfig['logy']
    if "logx" in histConfig: logx = histConfig['logx']
    printIntegral = False
    if "printIntegral" in histConfig and histConfig["printIntegral"]:
      printIntegral = True
    # now on to the real work
    for fileConfig in fileConfigs:
      isData = False
      try:
        isData = fileConfig["isData"]
      except KeyError:
        pass
      hist = loadHist(histConfig,fileConfig,binning,var,cuts,nMax=nMax,isData=isData)
      if 'color' in histConfig:
        hist.SetLineColor(histConfig['color'])
        hist.SetMarkerColor(histConfig['color'])
      if printIntegral:
        print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],hist.Integral()))
      hists.append(hist)
    canvas.SetLogy(logy)
    canvas.SetLogx(logx)
    axisHist = makeStdAxisHist(hists,logy=logy,freeTopSpace=0.35,xlim=xlim,ylim=ylim)
    axisHist.Draw()
    lines = drawVHLinesForPlot(axisHist,histConfig)
    for h in reversed(hists):
      if "efficiencyDenomCuts" in histConfig and type(histConfig["efficiencyDenomCuts"]) == str:
        h.Draw("PZ0same")
      else:
        h.Draw("histsame")
    labels = [fileConfig['title'] for fileConfig in fileConfigs]
    if "showMedian" in histConfig and histConfig["showMedian"]:
        for iHist in range(len(hists)):
            labels[iHist] += " median: {0}".format(getHistMedian(hists[iHist]))
    if "showMode" in histConfig and histConfig["showMode"]:
        for iHist in range(len(hists)):
            labels[iHist] += " mode: {0}".format(getHistMode(hists[iHist]))
    leg = drawNormalLegend(hists,labels,wide=True)
    drawAnnotationsForPlots(canvas,axisHist,fileConfigs,histConfig)
    canvas.RedrawAxis()
    saveNameBase = outPrefix + histConfig['name'] + outSuffix
    canvas.SaveAs(saveNameBase+".png")
    canvas.SaveAs(saveNameBase+".pdf")
    canvas.SetLogy(False)
    canvas.SetLogx(False)

def plotManyFilesOneNMinusOnePlot(fileConfigDatas,fileConfigMCs,cutConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint,weight="1",table=False):
    """
    Similar usage to plotManyFilesOnePlot, just cut instead of cuts

    cutSpans: list of len 2 lists of areas to mark as cut. 
                Use none to have a span go to the edge of the axis

    Optionally, for multiple plots for a single cut, you can just put
        the 'cut' and 'histConfigs', which is a list of dataMCStack-like hist configs
        in each entry of the cutConfigs argument

    table: if true prints out a table of the number of events N-1 cut

    """
    for fileConfig in fileConfigDatas:
      loadTree(fileConfig,treename)
    for fileConfig in fileConfigMCs:
      loadTree(fileConfig,treename)
    nMinusCutEventCounts = []
    for i in range(len(cutConfigs)):
      nMinusCutEventCounts.append([])
      for j in range(len(fileConfigDatas)+1+len(fileConfigMCs)):
        nMinusCutEventCounts[i].append("")
    for iCut in range(len(cutConfigs)):
      cutConfig = cutConfigs[iCut]
      cuts = []
      for jCut in range(len(cutConfigs)):
        if iCut == jCut:
          continue
        cuts.append(cutConfigs[jCut]['cut'])
      cutStr = "("+") && (".join(cuts) + ")"
      cutStr = "("+cutStr +")*"+weight
      histConfigs = [cutConfig]
      if "histConfigs" in cutConfig: histConfigs = cutConfig["histConfigs"]
      for iHistConfig, histConfig in enumerate(histConfigs):
        hists = []
        binning = histConfig['binning']
        var = histConfig['var']
        #if var.count(":") != 0:
        #  raise Exception("No ':' allowed in variable, only 1D hists allowed",var)
        xtitle = ""
        ytitle = "Events/bin"
        if "xtitle" in histConfig: xtitle = histConfig['xtitle']
        if "ytitle" in histConfig: ytitle = histConfig['ytitle']
        xlim = []
        ylim = []
        if "xlim" in histConfig: xlim = histConfig['xlim']
        if "ylim" in histConfig: ylim = histConfig['ylim']
        logy = False
        logx = False
        if "logy" in histConfig: logy = histConfig['logy']
        if "logx" in histConfig: logx = histConfig['logx']
        caption = ""
        captionleft1 = ""
        captionleft2 = ""
        captionleft3 = ""
        captionright1 = ""
        captionright2 = ""
        captionright3 = ""
        preliminaryString = ""
        if "caption" in histConfig: caption = histConfig['caption']
        if "captionleft1" in histConfig: captionleft1 = histConfig['captionleft1']
        if "captionleft2" in histConfig: captionleft2 = histConfig['captionleft2']
        if "captionleft3" in histConfig: captionleft3 = histConfig['captionleft3']
        if "captionright1" in histConfig: captionright1 = histConfig['captionright1']
        if "captionright2" in histConfig: captionright2 = histConfig['captionright2']
        if "captionright3" in histConfig: captionright3 = histConfig['captionright3']
        if "preliminaryString" in histConfig: preliminaryString = histConfig['preliminaryString']
        vlineXs = []
        hlineYs = []
        vlines = []
        hlines = []
        cutSpans = cutStringParser(cutConfig['cut'])
        vspans = []
        if "drawvlines" in histConfig and type(histConfig["drawvlines"]) == list:
          vlineXs = histConfig["drawvlines"]
        if "drawhlines" in histConfig and type(histConfig["drawhlines"]) == list:
          hlineYs = histConfig["drawhlines"]
        if "cutSpans" in histConfig and type(histConfig["cutSpans"]) == list:
          cutSpans = histConfig["cutSpans"]
        printIntegral = False
        if "printIntegral" in histConfig and histConfig["printIntegral"]:
          printIntegral = True
        # now on to the real work
        dataHists = []
        for iFile, fileConfig in enumerate(fileConfigDatas):
          hist = loadHist(histConfig,fileConfig,binning,var,cutStr,nMax,False)
          dataHists.append(hist)
          if table and iHistConfig == 0:
            nMinusCutEventCounts[iCut][iFile] = "{:.0f}".format(getIntegralAll(hist))
          if printIntegral:
            print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],hist.Integral()))
        mcHists = []
        for iFile, fileConfig in enumerate(fileConfigMCs):
          hist = loadHist(histConfig,fileConfig,binning,var,cutStr,nMax,False)
          mcHists.append(hist)
          if table and iHistConfig == 0:
            nMinusCutEventCounts[iCut][len(fileConfigDatas)+1+iFile] = "{:.1f}".format(getIntegralAll(hist))
          if printIntegral:
            print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],hist.Integral()))
        mcSumHist = None
        mcStack = root.THStack()
        if len(mcHists) > 0 :
          mcSumHist = mcHists[0].Clone(mcHists[0].GetName()+"_sumHist")
          mcSumHist.SetFillColor(root.kBlue)
          #mcSumHist.SetFillStyle(3254)
          mcSumHist.SetFillStyle(1)
          mcSumHist.SetMarkerSize(0)
          mcSumHist.Reset()
          for mcHist in reversed(mcHists):
            mcSumHist.Add(mcHist)
            mcStack.Add(mcHist)
        if table and iHistConfig == 0:
          nMinusCutEventCounts[iCut][len(fileConfigDatas)] = "{:.1f}".format(getIntegralAll(mcSumHist))
        if printIntegral and not (mcStack is None):
          print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,"MC Sum",mcSumHist.Integral()))
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)
        axisHist = makeStdAxisHist(dataHists+[mcSumHist],logy=logy,freeTopSpace=0.35,xlim=xlim,ylim=ylim)
        setHistTitles(axisHist,xtitle,ytitle)
        axisHist.Draw()
        for hlineY in hlineYs:
          hlines.append(drawHline(axisHist,hlineY))
        for vlineX in vlineXs:
          vlines.append(drawVline(axisHist,vlineX))
        for cutSpan in cutSpans:
          vspans.append(drawVSpan(axisHist,cutSpan[0],cutSpan[1]))
        #mcSumHist.Draw("histsame")
        mcStack.Draw("histsame")
        for dataHist in dataHists:
          dataHist.Draw("esame")
        labels = [fileConfig['title'] for fileConfig in fileConfigDatas]
        legOptions = ["lep"]*len(fileConfigDatas)
        labelHists = dataHists
        labels += [fileConfig['title'] for fileConfig in fileConfigMCs]
        legOptions += ["F"]*len(fileConfigMCs)
        labelHists += mcHists
        leg = drawNormalLegend(labelHists,labels,legOptions,wide=True)
        drawStandardCaptions(canvas,caption,captionleft1=captionleft1,captionleft2=captionleft2,captionleft3=captionleft3,captionright1=captionright1,captionright2=captionright2,captionright3=captionright3,preliminaryString=preliminaryString)
        canvas.RedrawAxis()
        saveNameBase = outPrefix + histConfig['name'] + outSuffix
        canvas.SaveAs(saveNameBase+".png")
        canvas.SaveAs(saveNameBase+".pdf")
        canvas.SetLogy(False)
        canvas.SetLogx(False)
    if table:
      #rowTitles = []
      #for cutConfig in cutConfigs:
      #  if 'xtitle' in cutConfig:
      #    rowTitles.append(cutConfig['xtitle']+" "+cutConfig['cut'])
      #  else:
      #    for histConfig in histConfigs:
      #      rowTitles.append(histConfig['xtitle']+" "+cutConfig['cut'])
      
      rowTitles = [x['cut'] for x in cutConfigs]
      columnTitles = [x['name'] for x in fileConfigDatas]+["MC Sum"]+[x['name'] for x in fileConfigMCs]
      printTable(nMinusCutEventCounts,rowTitles=rowTitles,columnTitles=columnTitles)

