from misc import *

def plotHistsSimple(hists,labels,xtitle,ytitle,canvas,outfileprefix,captionArgs=[""],xlim=[],ylim=[],drawOptions="hist",logy=False,colors=None,normalize=False,rebin=None,dontclone=False):
  if len(hists) == 0:
    print "Warning: plotHistsSimple hists is empty for "+outfileprefix
    return
  assert((labels is None) or (len(labels) == len(hists)))
  oldhists = hists
  hists = []
  if labels:
    for hist, label in zip(oldhists,labels):
      try:
        hists.append(hist.Clone(uuid.uuid1().hex))
      except ReferenceError as e:
        print("Hist for label '{}' is a null pointer".format(label))
        raise e
  else:
    for iHist, hist in enumerate(oldhists):
      try:
        hists.append(hist.Clone(uuid.uuid1().hex))
      except ReferenceError as e:
        print("Hist '{}' is a null pointer".format(iHist))
        raise e
  for hist in hists:
    try:
      hist.Sumw2(True)
    except:
      pass
  if colors is None:
    colors = COLORLIST
  freeTopSpace = 0.35
  if labels is None:
    freeTopSpace = 0.05
  if normalize:
    for hist in hists:
      normalizeHist(hist)
  if not (rebin is None):
    for hist in hists:
      hist.Rebin(rebin)
  if not (drawOptions is list):
    drawOptions = [drawOptions]*len(hists)
  assert(len(drawOptions) == len(hists))
  includeErrorBar=False
  for drawOpt in drawOptions:
    if drawOpt == "E":
      includeErrorBar=True
  axisHist = makeStdAxisHist(hists,logy=logy,freeTopSpace=freeTopSpace,xlim=xlim,ylim=ylim,includeErrorBar=includeErrorBar)
  if xtitle is None:
    xtitle = hists[0].GetXaxis().GetTitle()
  if ytitle is None:
    ytitle = hists[0].GetYaxis().GetTitle()
  setHistTitles(axisHist,xtitle,ytitle)
  axisHist.Draw()
  for hist, color, drawOpt in reversed(zip(hists,colors,drawOptions)):
    hist.UseCurrentStyle()
    if normalize:
        normalizeHist(hist)
    if len(hists) > 1:
      hist.SetLineColor(color)
      hist.SetMarkerColor(color)
    drawstr = "same"+drawOpt
    print xtitle, drawstr
    hist.Draw(drawstr)
  leg = None
  if not (labels is None):
    legOptions = ["l"]*len(hists)
    leg = drawNormalLegend(hists,labels,legOptions,wide=True)
  thisCaptionArgs = [canvas] + captionArgs
  drawStandardCaptions(*thisCaptionArgs)
  canvas.SaveAs(outfileprefix+".png")
  canvas.SaveAs(outfileprefix+".pdf")

def plotHist2DSimple(hist,xtitle,ytitle,canvas,outfileprefix,captionArgs=[""],profileX=False,profileY=False,xlims=None,ylims=None,rebin=None):
  setupCOLZFrame(canvas)
  hist = hist.Clone(uuid.uuid1().hex)
  hist.UseCurrentStyle()
  if rebin:
    assert(len(rebin)==2)
    hist.Rebin2D(*rebin)
  if xtitle is None:
    xtitle = hist.GetXaxis().GetTitle()
  if ytitle is None:
    ytitle = hist.GetYaxis().GetTitle()
  setHistTitles(hist,xtitle,ytitle)
  hist.Draw("colz")
  thisCaptionArgs = [canvas] + captionArgs
  drawStandardCaptions(*thisCaptionArgs)
  profX = None
  profY = None
  if profileX:
     profX = hist.ProfileX()
     profX.Draw("Esame")
  if profileY:
     profY = hist.ProfileX()
     profY.Draw("Esame")
  if xlims is None:
    pass
  elif type(xlims) is list and len(xlims) == 2:
    hist.GetXaxis().SetRangeUser(*xlims)
  else:
    raise ValueError("xlims must be list of len 2 "+str(xlims))
  if ylims is None:
    pass
  elif type(ylims) is list and len(ylims) == 2:
    hist.GetYaxis().SetRangeUser(*ylims)
  else:
    raise ValueError("ylims must be list of len 2 "+str(ylims))
  canvas.SaveAs(outfileprefix+".png")
  #c.SaveAs(outfileprefix+".pdf")
  setupCOLZFrame(canvas,True) #reset frame
  return hist

