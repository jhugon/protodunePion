#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import os.path

def printEvents(infilename,treename,variableNames,cuts={},printFullFilename=False,printFileBasename=True,nMax=100):
  tree = root.TChain(treename)
  try:
    if type(infilename) is str:
        tree.AddFile(infilename)
    elif type(infilename) is list:
        for fn in infilename:
            tree.AddFile(fn)
    else:
        raise Exception("")
  except KeyError:
    return
  nEvents = tree.GetEntries()
  nEvents = min(nEvents,nMax)
  allVals = []
  filenames = []
  for iEvent in range(nEvents):
    tree.GetEntry(iEvent)
    failedCuts = False
    for cutVar in cuts:
      cutOp = cuts[cutVar][0]
      cutVal = cuts[cutVar][1]
      if cutOp == "==" or cutOp == "=":
        if getattr(tree,cutVar) != cutVal:
          failedCuts = True
          break
      elif cutOp == "!=":
        if getattr(tree,cutVar) == cutVal:
          failedCuts = True
          break
      elif cutOp == ">":
        if getattr(tree,cutVar) <= cutVal:
          failedCuts = True
          break
      elif cutOp == "<":
        if getattr(tree,cutVar) >= cutVal:
          failedCuts = True
          break
      elif cutOp == ">=":
        if getattr(tree,cutVar) < cutVal:
          failedCuts = True
          break
      elif cutOp == "<=":
        if getattr(tree,cutVar) > cutVal:
          failedCuts = True
          break
      else:
        raise Exception("Unknown cut op: ",cutOp)
    if failedCuts:
      continue
    runNumber = tree.runNumber
    eventNumber = tree.eventNumber
    try:
        filenames.append(str(tree.infilename))
    except:
        filenames.append("No filename")
    vals = []
    vals.append("{:>5}:{:>5}".format(runNumber,eventNumber))
    for variableName in variableNames:
      try:
        val = getattr(tree,variableName)
      except:
        val = "Error"
      finally:
        if type(val) == root.string:
            val = str(val)
        if type(val) != str:
          try:
              val = val[0]
          except TypeError:
              pass
          except IndexError:
              val = "Empty"
        if type(val) == float:
          val = "{:g}".format(val)
        else:
          val = "{}".format(val)
        vals.append(val)
    allVals.append(vals)
  nLines = len(allVals)
  nPerLine = len(variableNames)
  valLengths = []
  for i in range(nPerLine+1):
    maxLen = 0
    for vals in allVals:
      maxLen = max(maxLen,len(vals[i]))
    valLengths.append(maxLen)
  for iLine in range(nLines):
    outStr = ("{:"+str(valLengths[0])+"}").format(allVals[iLine][0])
    for i in range(1,nPerLine+1):
      outStr += " {}: ".format(variableNames[i-1])
      outStr += ("{:"+str(valLengths[i])+"}").format(allVals[iLine][i])
    print outStr
    if printFullFilename:
        print "  ",filenames[iLine]
    elif printFileBasename:
        print "  ",os.path.basename(filenames[iLine])
        

if __name__ == "__main__":

  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status","BITrigger","BITriggerMatched","BIActiveTrigger","triggerIsBeam"]
  varNames = ["beamMom","TOF","CKov0Status","CKov1Status"]
  cuts = {
    #"triggerIsBeam": ["=",1],
    #"BITrigger": [">",0],
    "BITriggerMatched": ["==",1],
  }

  #print "Run 5145, 7 GeV/c"
  #printEvents("piAbsSelector_run5145.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  print "Run 5766, 6 GeV/c"
  printEvents("piAbsSelector_run5766.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  print "Run 5780, 3 GeV/c"
  printEvents("piAbsSelector_run5780.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)

