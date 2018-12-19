from misc import *

def dataMCStack(self,fileConfigDatas,fileConfigMCs,histConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint):
    """
    fileConfigDatas is a list of dictionaries configuring the data
    fileConfigMCs is a list of dictionaries configuring the MC files
    histConfigs is a list of dictionaries configuring the histograms. It is a
      list so you can do multiple plots.
    canvas is a root TCanvas
    treename is where to find the tree in each file
  
    fileConfig options:
      fn: filename str or list of str for a chain. REQUIRED
      title: title of sample: will be used for legends REQUIRED
      color: will be used for line/marker color
      scaleFactor: scale histograms by this much after filling
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
      integral: if True, makes each bin content Nevents for X >= bin low edge
      title: (unused)
      color: (unused)
      drawhlines: list of y locations to draw horizontal lines
      drawvlines: list of x locations to draw vertical lines
      printIntegral: if True, print integral after all scaling
    """
    #print("plotManyFilesOnePlot")
    for fileConfig in fileConfigDatas:
      loadTree(fileConfig,treename)    
    for fileConfig in fileConfigMCs:
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
      if "drawvlines" in histConfig and type(histConfig["drawvlines"]) == list:
        vlineXs = histConfig["drawvlines"]
      if "drawhlines" in histConfig and type(histConfig["drawhlines"]) == list:
        hlineYs = histConfig["drawhlines"]
      printIntegral = False
      if "printIntegral" in histConfig and histConfig["printIntegral"]:
        printIntegral = True
      # now on to the real work
      dataHists = []
      for fileConfig in fileConfigDatas:
        hist = loadHist(histConfig,fileConfig,binning,var,cuts,nMax,False)
        dataHists.append(hist)
        if printIntegral:
          print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],hist.Integral()))
      mcHists = []
      for fileConfig in fileConfigMCs:
        hist = loadHist(histConfig,fileConfig,binning,var,cuts,nMax,False)
        mcHists.append(hist)
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
      #mcSumHist.Draw("histsame")
      mcStack.Draw("histsame")
      for dataHist in dataHists:
        dataHist.Draw("esame")
      labels = [fileConfig['title'] for fileConfig in fileConfigDatas] + [fileConfig['title'] for fileConfig in fileConfigMCs]
      legOptions = ["lep"]*len(fileConfigDatas)+["F"]*len(fileConfigMCs)
      leg = drawNormalLegend(dataHists+mcHists,labels,legOptions,wide=True)
      drawStandardCaptions(canvas,caption,captionleft1=captionleft1,captionleft2=captionleft2,captionleft3=captionleft3,captionright1=captionright1,captionright2=captionright2,captionright3=captionright3,preliminaryString=preliminaryString)
      canvas.RedrawAxis()
      saveNameBase = outPrefix + histConfig['name'] + outSuffix
      canvas.SaveAs(saveNameBase+".png")
      canvas.SaveAs(saveNameBase+".pdf")
      canvas.SetLogy(False)
      canvas.SetLogx(False)

def dataMCStackNMinusOne(self,fileConfigDatas,fileConfigMCs,cutConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint,weight="1",table=False):
    """
    Similar usage to dataMCStack, just cut instead of cuts

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

def dataMCCategoryStack(self,fileConfigDatas,fileConfigMCs,histConfigs,canvas,treename,outPrefix="",outSuffix="Hist",nMax=sys.maxint,catConfigs=[]):
    """
    fileConfigDatas is a list of dictionary configuring the data
    fileConfigMCs is a list of dictionaries configuring the MC files
    histConfigs is a list of dictionaries configuring the histograms. It is a
      list so you can do multiple plots.
    canvas is a root TCanvas
    treename is where to find the tree in each file
  
    fileConfig options:
      fn: filename str or list of str for a chain. REQUIRED
      title: title of sample: will be used for legends REQUIRED
      color: will be used for line/marker color
      scaleFactor: scale histograms by this much after filling
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
      integral: if True, makes each bin content Nevents for X >= bin low edge
      title: (unused)
      color: (unused)
      drawhlines: list of y locations to draw horizontal lines
      drawvlines: list of x locations to draw vertical lines
      printIntegral: if True, print integral after all scaling
    catConfig options:
      title: Title to display in legend REQUIRED
      cuts: Cuts to define the category, each one should be independent REQUIRED
      color: Color for this category REQUIRED
    """
    for fileConfig in fileConfigDatas:
      loadTree(fileConfig,treename)
    for fileConfig in fileConfigMCs:
      loadTree(fileConfig,treename)

    for histConfig in histConfigs:
      hists = []
      binning = histConfig['binning']
      var = histConfig['var']
      cuts = histConfig['cuts']
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
      if "drawvlines" in histConfig and type(histConfig["drawvlines"]) == list:
        vlineXs = histConfig["drawvlines"]
      if "drawhlines" in histConfig and type(histConfig["drawhlines"]) == list:
        hlineYs = histConfig["drawhlines"]
      printIntegral = False
      if "printIntegral" in histConfig and histConfig["printIntegral"]:
        printIntegral = True
      # now on to the real work
      dataHists = []
      for fileConfig in fileConfigDatas:
        dataHist = loadHist(histConfig,fileConfig,binning,var,cuts,nMax,False)
        dataHists.append(dataHist)
        if printIntegral:
          print("{} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],dataHist.Integral()))
      catHists = []
      for catConfig in catConfigs:
        thisCuts = cuts + "*(" + catConfig["cuts"] + ")"
        catHist = None
        for fileConfig in fileConfigMCs:
          hist = loadHist(histConfig,fileConfig,binning,var,thisCuts,nMax,False)
          if catHist is None:
            catHist = hist
          else:
            catHist.Add(hist)
        catHist.SetFillColor(catConfig['color'])
        catHist.SetLineColor(catConfig['color'])
        catHists.append(catHist)
        if printIntegral:
          print("{} {} {} Integral: {}".format(outPrefix+histConfig['name']+outSuffix,fileConfig['title'],catConfig['title'],catHist.Integral()))
      mcSumHist = None
      mcStack = root.THStack()
      if len(catHists) > 0 :
        mcSumHist = catHists[0].Clone(catHists[0].GetName()+"_sumHist")
        mcSumHist.SetFillColor(root.kBlue)
        #mcSumHist.SetFillStyle(3254)
        mcSumHist.SetFillStyle(1)
        mcSumHist.SetMarkerSize(0)
        mcSumHist.Reset()
        for mcHist in reversed(catHists):
          mcSumHist.Add(mcHist)
          mcStack.Add(mcHist)
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
      #mcSumHist.Draw("histsame")
      mcStack.Draw("histsame")
      for dataHist in dataHists:
        dataHist.Draw("esame")

      labels = [fileConfig['title'] for fileConfig in fileConfigDatas] + [catConfig['title'] for catConfig in catConfigs]
      legOptions = ["lep"]*len(dataHists)+["F"]*len(catConfigs)
      leg = drawNormalLegend(dataHists+catHists,labels,legOptions,wide=True)
      drawStandardCaptions(canvas,caption,captionleft1=captionleft1,captionleft2=captionleft2,captionleft3=captionleft3,captionright1=captionright1,captionright2=captionright2,captionright3=captionright3,preliminaryString=preliminaryString)
      canvas.RedrawAxis()
      saveNameBase = outPrefix + histConfig['name'] + outSuffix
      canvas.SaveAs(saveNameBase+".png")
      canvas.SaveAs(saveNameBase+".pdf")
      canvas.SetLogy(False)
      canvas.SetLogx(False)

