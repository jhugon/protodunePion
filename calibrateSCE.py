#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys

cutGoodBeamline = "*(triggerIsBeam == 1 && BITrigger > 0 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom == 1)"
cutGoodFEMBs = "*(isMC || (nGoodFEMBs[0]==20 && nGoodFEMBs[2]==20 && nGoodFEMBs[4]==20))"

deltaXTrackBICut = "*(isMC && ((PFBeamPrimXFrontTPC-xWC) > -10) && ((PFBeamPrimXFrontTPC-xWC) < 10)) || ((!isMC) && ((PFBeamPrimXFrontTPC-xWC) > 10) && ((PFBeamPrimXFrontTPC-xWC) < 30))"
deltaYTrackBICut = "*(isMC && ((PFBeamPrimYFrontTPC-yWC) > -10) && ((PFBeamPrimYFrontTPC-yWC) < 10)) || ((!isMC) && ((PFBeamPrimYFrontTPC-yWC) > 7) && ((PFBeamPrimYFrontTPC-yWC) < 27))"
primaryTrackCuts = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ < 650.)"+deltaXTrackBICut+deltaYTrackBICut
primaryTrackCutsMu = "*(PFNBeamSlices == 1 && PFBeamPrimIsTracklike && PFBeamPrimStartZ < 50. && PFBeamPrimEndZ > 650.)"+deltaXTrackBICut+deltaYTrackBICut

primaryTrackCutsData = cutGoodFEMBs+cutGoodBeamline+primaryTrackCutsMu
cutsMC = "(truePrimaryPDG == 211 || truePrimaryPDG == -13)"+primaryTrackCutsMu

if __name__ == "__main__":

  makeHists=False
  getWireLocs=False

  histConfigs = [
  ]
  c = root.TCanvas()
  NMAX=10000000000
  #NMAX=100

  fileConfigsMC = [
    {
      'fn': "piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 No SCE 1 GeV/c",
      'caption': "MCC11 No SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_1p0GeV_v4.11.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 SCE 1 GeV/c",
      'caption': "MCC11 SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_1p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 FLF SCE 1 GeV/c",
      'caption': "MCC11 FLF SCE 1 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root",
      'name': "mcc11_3ms_2GeV",
      'title': "MCC11 No SCE 2 GeV/c",
      'caption': "MCC11 No SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_2p0GeV_v4.11.root",
      'name': "mcc11_sce_2GeV",
      'title': "MCC11 SCE 2 GeV/c",
      'caption': "MCC11 SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.11.root",
      'name': "mcc11_flf_2GeV",
      'title': "MCC11 FLF SCE 2 GeV/c",
      'caption': "MCC11 FLF SCE 2 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root",
      'name': "mcc11_3ms_7GeV",
      'title': "MCC11 No SCE SCE 7 GeV/c",
      'caption': "MCC11 No SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_sce_7p0GeV_v4.11.root",
      'name': "mcc11_sce_7GeV",
      'title': "MCC11 SCE 7 GeV/c",
      'caption': "MCC11 SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
    {
      'fn': "piAbsSelector_mcc11_flf_7p0GeV_v4.11.root",
      'name': "mcc11_flf_7GeV",
      'title': "MCC11 FLF SCE 7 GeV/c",
      'caption': "MCC11 FLF SCE 7 GeV/c",
      'isData': False,
      "cuts": "*"+cutsMC
    },
  ]

  if makeHists:
    for histConfig in histConfigs:
      histConfig["caption"] = caption
      histConfig["normalize"] = True
      histConfig["ytitle"] = "Normalized Events / Bin"

    plotManyFilesOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",outSuffix="Hist",nMax=NMAX)
    for histConfig in histConfigs:
      histConfig['logy'] = True
      histConfig["normalize"] = False
      histConfig["ytitle"] = "Events / Bin"
    plotManyFilesOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",outSuffix="_logyHist",nMax=NMAX)

  wireBinning = [480*3,0,480*3]
  #wireBinning = [100,0,100]

  histConfigs= [
    {
      'name': "zWireZVzWireWireZ",
      'xtitle': "Z Wire Z-Position [cm]",
      'ytitle': "Reco Hit Z-Position [cm]",
      'binning': 2*[710,-5.,705.],
      'var': "zWireZ:zWireWireZ",
      'cuts': "1",
      'logz': True,
    },
    {
      'name': "zWireZVzWireWireZ",
      'xtitle': "Z Wire Z-Position [cm]",
      'ytitle': "True Hit Z-Position [cm]",
      'binning': 2*[710,-5.,705.],
      'var': "zWireTrueZ:zWireWireZ",
      'cuts': "1",
      'logz': True,
    },
    #{
    #  'name': "deltaRecoWireZVWireNum",
    #  'xtitle': "Z Wire Number",
    #  'ytitle': "Reco Hit-Wire Z-Position [cm]",
    #  'binning': wireBinning+[300,-30,30],
    #  'var': "zWireZ-zWireWireZ:Iteration$",
    #  'cuts': "1",
    #  'logz': True,
    #},
    {
      'name': "deltaWireTrueZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Wire-True Hit Z-Position [cm]",
      'binning': wireBinning+[300,-20,20],
      'var': "zWireWireZ-zWireTrueZ:Iteration$",
      'cuts': "1",
      'logz': True,
      'profileXtoo': True,
    },
    {
      'name': "deltaRecoTrueZVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco-True Hit Z-Position [cm]",
      'binning': wireBinning+[300,-20,20],
      'var': "zWireZ-zWireTrueZ:Iteration$",
      'cuts': "1",
      'logz': True,
      'profileXtoo': True,
    },
    {
      'name': "deltaPitchTrueHitSpacingVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "Reco Pitch-True Hit Spacing [cm]",
      'binning': wireBinning+[200,-5,5],
      'var': "zWirePitch-zWireTruedR:Iteration$",
      'cuts': "1",
      'logz': True,
    },
  ]
  if makeHists:
    plotOneHistOnePlot(fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="WireZ_",nMax=NMAX,saveHistsRootName="WireHistsSCE.root")

  if getWireLocs:
    ### Getting True Z-wire locations
    for fileConfig in fileConfigsMC:
      tfile = root.TFile(fileConfig['fn'])
      tree = tfile.Get("PiAbsSelector/tree")
      tree.GetEntry(0)
      with open("WireZPositions.txt",'w') as outfile:
        for iWire in range(tree.zWireWireZ.size()):
          outstr = "{},{}\n".format(iWire,tree.zWireWireZ[iWire])
          outfile.write(outstr)
      del tree
      tfile.Close()
      break

  wireLocs = [0.]*480*3
  with open("WireZPositions.txt") as wireLocFile:
    for line in wireLocFile:
      record = line.replace("\n","").split(",")
      wireNum = int(record[0])
      pos = float(record[1])
      wireLocs[wireNum] = pos

  histFileName = "WireHistsSCE.root"
  histname = "dEdxVWireNum"
  hf = HistFile(histFileName)
  root.gStyle.SetMarkerSize(0)
  for histConfig in histConfigs:
    histName = histConfig['name']
    if "PitchTrueHitSpacing" in histName or not ("delta" in histName):
      continue
    profs = []
    projs = []
    labels = []
    goodWireIs = []
    derivFuncs = []
    graphs = []
    lists = []
    for iFileConfig,fileConfig in enumerate(fileConfigsMC):
      fileName = fileConfig['name']
      if "3ms" in fileName:
        continue
      if not ("deltaWireTrue" in histName):
        continue
      name = histName+"_"+fileName
      hist = hf[name]
      print "justin",name,hist
      if not hist:
        continue
      #hist.RebinX(240)
      #hist.RebinY(50)
      nWires = hist.GetNbinsX()
      proj = hist.ProjectionX(hist.GetName()+"_proj",1,hist.GetNbinsY())
      #plotHistsSimple([proj],None,histConfig['xtitle'],"N Hits",c,"WireZ_proj_"+histName+"_"+fileName)
      prof = hist.ProfileX(hist.GetName()+"_pfxAgain")
      prof.SetMarkerSize(0)
      profs.append(prof)
      projs.append(proj)
      labels.append(fileConfig['title'])
      try:
        import numpy
        from scipy import interpolate
        import matplotlib.pyplot as mpl
      except ImportError:
        graph = root.TGraph()
        iPoint = 0
        for iWire in range(nWires):
          if iWire < 30 or iWire > 480*3 - 30:
              continue
          nHits = proj.GetBinContent(iWire+1)
          if nHits < 20:
            continue
          y = prof.GetBinContent(iWire+1)
          graph.SetPoint(iPoint,iWire,y)
          iPoint+= 1
        graphs.append(graph)
        c.Clear()
        print name, graph.GetN()
        if graph.GetN() == 0:
          continue
        smoother = root.TGraphSmooth("smoother_"+name)
        smooth = smoother.SmoothKern(graph,"normal",20)
        smooth.SetLineColor(root.kBlue+1)
        #axisHist = drawGraphs(c,[graph,smooth],histConfig['xtitle'],"Profile of "+histConfig['ytitle'],yStartZero=False,drawOptions="l")
        axisHist = drawGraphs(c,[smooth],histConfig['xtitle'],"Profile of "+histConfig['ytitle'],yStartZero=False,drawOptions="l")
        drawStandardCaptions(c,fileConfig["title"])
        c.SaveAs("WireZ_smooth_"+histName+"_"+fileName+".png")
        c.SaveAs("WireZ_smooth_"+histName+"_"+fileName+".pdf")
        l = [0]*480*3
        xs = smooth.GetX()
        ys = smooth.GetY()
        for iPoint in range(smooth.GetN()):
          l[int(xs[iPoint])] = ys[iPoint]
        with open("CalibrationSCE_RootSmooth_"+name+".txt",'w') as outfile:
          for iWire in range(len(l)):
            line = "{},{}".format(iWire,l[iWire])
            outfile.write(line+"\n")
      else:
        wires = []
        ys = []
        yErrs = []
        print "made it here"
        for iWire in range(nWires):
          if iWire < 30 or iWire > 480*3 - 30 or (iWire >= 957 and iWire <= 960) or (iWire >= 479 and iWire <= 481):
            continue
          if "sce_2GeV" in fileName and iWire < 38:
            continue
          nHits = proj.GetBinContent(iWire+1)
          #if nHits < 20:
          if nHits < 10 or ((not ("sce_7GeV" in fileName)) and nHits < 20):
            continue
          yErr = prof.GetBinError(iWire+1)
          if yErr == 0.:
            continue
          wires.append(iWire)
          ys.append(prof.GetBinContent(iWire+1))
          yErrs.append(yErr)
        if len(wires) == 0:
          continue
        wires = numpy.array(wires)
        ys = numpy.array(ys)
        yErrs = numpy.array(yErrs)
        yWeights = 1./yErrs
        smoothFactor=0.8
        if "deltaWireTrueZVWireNum" in histName:
          smoothFactor=1.
          if "sce_7GeV" in fileName:
            smoothFactor=1.1
          if "sce_2GeV" in fileName:
            smoothFactor=0.9
          if "flf_2GeV" in fileName:
            smoothFactor=1.
        spline = interpolate.UnivariateSpline(wires,ys,yWeights,s=float(len(wires))*smoothFactor,check_finite=True)
        ysSmoothed = spline(numpy.arange(480*3))
        derivSmoothed = spline.derivative(1)(numpy.arange(480*3))
        goodWireIs.append(wires)
        derivFuncs.append(spline.derivative(1))
        fig, ax = mpl.subplots()
        ax.fill_between(wires,ys-yErrs,ys+yErrs,color='c',label="Profile Error-band")
        ax.plot(wires,ys,"-b",label="Profile Mean")
        ax.plot(numpy.arange(480*3),ysSmoothed,"-r",label="Smoothed")
        ax.set_xlabel(histConfig["xtitle"])
        ax.set_ylabel(histConfig["ytitle"])
        ax.set_title(fileConfig["title"])
        ax.set_xlim(0,480*3)
        #ax.set_xlim(460,500)
        #ax.set_ylim(1,3)
        ax.grid()
        leg = ax.legend()
        fig.savefig("WireZ_pysmooth_"+histName+"_"+fileName+".png")
        fig.savefig("WireZ_pysmooth_"+histName+"_"+fileName+".pdf")
        mpl.close()
        fig, ax = mpl.subplots()
        ax.fill_between(wires,-yErrs,yErrs,color='c')
        ax.plot(wires,spline(wires)-ys,"-b")
        ax.set_xlabel(histConfig["xtitle"])
        ax.set_ylabel("Smooth-Profile for "+histConfig["ytitle"])
        ax.set_title(fileConfig["title"])
        ax.set_xlim(0,480*3)
        #ax.set_xlim(800,1000)
        #ax.set_xlim(460,500)
        ax.grid()
        fig.savefig("WireZ_pysmooth_diff_"+histName+"_"+fileName+".png")
        fig.savefig("WireZ_pysmooth_diff_"+histName+"_"+fileName+".pdf")
        mpl.close()
        fig, ax = mpl.subplots()
        mpl.subplots_adjust(left=0.16) # 0.14 is the default
        iWiresForDeriv=numpy.arange(wires[0],wires[-1])
        ax.plot(iWiresForDeriv,spline.derivative(1)(iWiresForDeriv),"-b")
        ax.set_xlabel(histConfig["xtitle"])
        ax.set_ylabel("Derivative of Smoothed "+histConfig["ytitle"])
        ax.set_title(fileConfig["title"])
        ax.set_xlim(0,480*3)
        #ax.set_xlim(800,1000)
        #ax.set_xlim(460,500)
        ax.grid()
        fig.savefig("WireZ_pysmooth_deriv_"+histName+"_"+fileName+".png")
        fig.savefig("WireZ_pysmooth_deriv_"+histName+"_"+fileName+".pdf")
        mpl.close()
        with open("CalibrationSCE_PythonSmooth_"+name+".txt",'w') as outfile:
          for iWire,offset in zip(numpy.arange(480*3),ysSmoothed):
            line = "{},{},{}".format(iWire,wireLocs[iWire],-offset)
            outfile.write(line+"\n")
    plotHistsSimple(profs,labels,histConfig['xtitle'],"Profile of "+histConfig['ytitle'],c,"WireZ_prof_"+histName,drawOptions="",ylim=[-10,25])
    c.SetLogy(True)
    plotHistsSimple(projs,labels,histConfig['xtitle'],"N Hits / bin",c,"WireZ_proj_"+histName,drawOptions="",logy=True)
    c.SetLogy(False)
    try:
      import numpy
      from scipy import interpolate
      import matplotlib.pyplot as mpl
    except ImportError:
      pass
    else:
      fig, ax = mpl.subplots()
      mpl.subplots_adjust(left=0.16) # 0.14 is the default
      for wires, deriv, label in zip(goodWireIs,derivFuncs,labels):
        if "1 GeV" in label:
          continue
        iWiresForDeriv=numpy.arange(wires[0],wires[-1])
        ax.plot(iWiresForDeriv,(deriv(iWiresForDeriv)/0.5792+1)*100,label=label)
      ax.set_xlabel(histConfig["xtitle"])
      ax.set_ylabel("Slice Width Scale Factor from SCE [%]")
      ax.set_xlim(0,480*3)
      ax.grid()
      leg = ax.legend(loc="best")
      fig.savefig("WireZ_pysmooth_allderiv_"+histName+".png")
      fig.savefig("WireZ_pysmooth_allderiv_"+histName+".pdf")
      mpl.close()
      fig, ax = mpl.subplots()
      mpl.subplots_adjust(left=0.16) # 0.14 is the default
      for wires, deriv, label in zip(goodWireIs,derivFuncs,labels):
        if "1 GeV" in label:
          continue
        iWiresForDeriv=numpy.arange(wires[0],wires[-1])
        ax.plot([wireLocs[iWire] for iWire in iWiresForDeriv],(deriv(iWiresForDeriv)/0.5792+1)*100.,label=label)
      ax.set_xlabel("Wire Z Position [cm]")
      ax.set_ylabel("Slice Width Scale Factor from SCE [%]")
      ax.set_xlim(wireLocs[0],wireLocs[-1])
      ax.grid()
      leg = ax.legend(loc="best")
      fig.savefig("WireZ_pysmooth_allderiv_wireZ_"+histName+".png")
      fig.savefig("WireZ_pysmooth_allderiv_wireZ_"+histName+".pdf")
      mpl.close()

  firstWire = 67
  firstWirePosShouldBe = wireLocs[0]
  for calibFn in glob.glob("CalibrationSCE_*Smooth*.txt"):
    if "scaleData" in calibFn:
      continue
    scaleDataFn = calibFn.replace(".txt","_scaleData.txt")
    corrs = [0.]*480*3
    with open(calibFn) as infile:
      for line in infile:
        record = line.replace("\n","").split(",")
        wireNum = int(record[0])
        corr = float(record[2])
        corrs[wireNum] = corr
    sf = (wireLocs[0]-wireLocs[firstWire])/corrs[firstWire]
    corrsScaleData = [0.]*480*3
    for iWire in range(480*3):
      corrsScaleData[iWire] = corrs[iWire]*sf
    with open(scaleDataFn,'w') as outfile:
      for iWire in range(480*3):
        # wire num, wire z (no correction), correction
        outline = "{},{},{}\n".format(iWire,wireLocs[iWire],corrs[iWire]*sf)
        outfile.write(outline)
    if "deltaWireTrue" in calibFn:
      try:
        import numpy
        import matplotlib.pyplot as mpl
      except ImportError:
        pass
      else:
        corrs = numpy.array(corrs)
        corrsScaleData = numpy.array(corrsScaleData)
        rawPos = numpy.array(wireLocs)
        mcCorPos = rawPos+corrs
        dataCorPos = rawPos+corrsScaleData
        fig, ax = mpl.subplots()
        ax.plot(rawPos,dataCorPos,"-b",label="MC Scaled to Data")
        ax.plot(rawPos,mcCorPos,"-r",label="MC")
        ax.plot(rawPos,rawPos,":k",label="Identity")
        ax.set_xlabel("Raw Reconstructed Z Position [cm]")
        ax.set_ylabel("Corrected Reconstructed Z Position [cm]")
        #ax.set_title(fileConfig["title"])
        #ax.set_xlim(0,480*3)
        ax.set_xlim(0,700)
        ax.set_ylim(0,700)
        #ax.set_xlim(460,500)
        leg = ax.legend()

        fig.savefig(calibFn.replace(".txt",".png"))
        fig.savefig(calibFn.replace(".txt",".pdf"))
        mpl.close()
