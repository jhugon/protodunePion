#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import os.path

def runNoArgs():

  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status","BITrigger","BITriggerMatched","BIActiveTrigger","triggerIsBeam"]
  #varNames = ["beamMom","TOF","CKov0Status","CKov1Status"]
  varNames = [#"beamMom",
                "TOF",
                #"primTrkStartX","primTrkStartY","primTrkStartZ","primTrkLength",
                #"PFBeamPrimStartX","PFBeamPrimStartY","PFBeamPrimStartZ","PFBeamPrimTrkLen",
                #"PFBeamPrimIsTracklike"
            ]
  cuts = {
    "triggerIsBeam": ["=",1],
    "BITrigger": [">",0],
    "BITriggerMatched": [">",0],
    #"CKov1Status":["=",0],
    #"CKov0Status":["=",1],
    "TOF":[">",180.], # should be ~191 raw TOF for Deuterons at 2 GeV, 172 at 3GeV so maybe cut 168 at 2 GeV
  }

  #print "Run 5145, 7 GeV/c"
  #printEvents("piAbsSelector_run5145_v4.4.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=1000,printFileBasename=True)
  #print "Run 5432, 2 GeV/c @ LSU, Deuteron Cut"
  #printEvents("piAbsSelector_run5432_v4.4.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100,printFileBasename=True)
  #print "Run 5432, 2 GeV/c @ Fermilab, Deuteron Cut"
  #printEvents("piAbsSelector_run5432_v3.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  #print "Run 5758, 6 GeV/c"
  #printEvents("piAbsSelector_run5758.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)
  #print "Run 5780, 3 GeV/c"
  #printEvents("piAbsSelector_run5780.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100)

  varNames = ["trueStartMom","trueEndMom","trueSecondToEndMom","truePrimaryTrackID","PFBeamPrimTrueTrackID","trueEndZ","PFBeamPrimStartZ","PFBeamPrimEndZ"]
  #varNames = ["trueStartMom","trueEndZ","PFBeamPrimStartZ","PFBeamPrimStartZ_corr","PFBeamPrimStartZ_corrFLF","PFBeamPrimEndZ","PFBeamPrimEndZ_corr","PFBeamPrimEndZ_corrFLF"]
  cuts = {
    #"truePrimaryPDG": ["==",-13],
    "truePrimaryPDG": ["==",2212],
    "PFNBeamSlices": ["==",1],
    "PFBeamPrimIsTracklike": ["==",1],
    "PFBeamPrimStartZ": ["<",50],
    "PFBeamPrimEndZ": ["<",650],
  }
  #print "MCC11 FLF 2 GeV v4.11 -- Protons"
  #printEvents("piAbsSelector_mcc11_flf_2p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=10000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.11.root")
  print "MCC11 FLF 1 GeV v4.11 -- Protons"
  printEvents("piAbsSelector_mcc11_flf_1p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=10000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_flf_1p0GeV_v4.11.root",printFileBasename=True)

#  print "Run 5387 v4.10"
#  varNames = ["PFBeamPrimStartX","PFBeamPrimStartY","PFBeamPrimStartZ","PFBeamPrimEndX","PFBeamPrimEndY","PFBeamPrimEndZ","PFBeamPrimTrkLen","beamMom"]
#  varNames = ["PFBeamPrimStartX","PFBeamPrimStartY","PFBeamPrimStartZ","PFBeamPrimEndX","PFBeamPrimEndY","PFBeamPrimEndZ","beamMom"]
#  cuts = {
#    "triggerIsBeam": ["=",1],
#    "BITrigger": [">",0],
#    "BITriggerMatched": [">",0],
#    "nBeamTracks": ["=",1],
#    "nBeamMom": ["=",1],
#    "CKov1Status":["=",0],
#    "TOF":["<",170.],
#    "PFNBeamSlices": ["==",1],
#    "PFBeamPrimIsTracklike": ["==",1],
#    "PFBeamPrimStartZ": ["<",50],
#    "PFBeamPrimEndZ": [">",650],
#  }
#  printEvents("piAbsSelector_run5387_v4.10.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=10000,printFileBasename=True)

  # want something like PFBeamPrimEndZ-zWireWireZ[zWireLastHitWire] > 50.

  #varNames = ["trueStartMom","trueEndZ","PFBeamPrimEndZ","PFBeamPrimEndZ_corr","PFBeamPrimEndZ_corrFLF","zWireLastHitWire","zWireLastHitWireTrue"]
  #cuts = {
  #  "truePrimaryPDG": ["==",211],
  #  #"truePrimaryPDG": ["==",2212],
  #  "PFNBeamSlices": ["==",1],
  #  "PFBeamPrimIsTracklike": ["==",1],
  #  "PFBeamPrimStartZ": ["<",50],
  #  "PFBeamPrimEndZ": ["<",650],
  #}
  #print "MCC11 FLF 2 GeV v4.11 -- Pions"
  #printEvents("piAbsSelector_mcc11_flf_2p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.11.root")

  varNames = ["trueStartMom","truePrimaryPDG","trueEndProcess","trueSecondToEndMom"]
  cuts = {
    "trueCategory": ["==",0],
  }
  print "MCC11 FLF 1 GeV v4.11 -- True Unknown"
  printEvents("piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",printFileBasename=True)

  varNames = ["trueStartMom","truePrimaryPDG","trueEndProcess","trueSecondToEndMom"]
  cuts = {
    "trueCategory": ["==",15],
  }
  print "MCC11 FLF 1 GeV v4.11 -- True Primary Other non-Pion"
  printEvents("piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",printFileBasename=True)

  varNames = ["trueStartMom","truePrimaryPDG","trueEndProcess","trueSecondToEndMom"]
  cuts = {
    "trueCategory": ["==",16],
  }
  print "MCC11 FLF 1 GeV v4.11 -- True Other Stopping"
  printEvents("piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root","PiAbsSelector/tree",varNames,cuts=cuts,nMax=100000,friendTreeName="friend",friendTreeFileName="friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root",printFileBasename=True)

if __name__ == "__main__":
  import argparse

  print "start"
  parser = argparse.ArgumentParser(description='Print ROOT TTree info')
  parser.add_argument('-f','--file',
                      help='file name tree is in')
  parser.add_argument('-t','--treeName',
                      default="PiAbsSelector/tree",
                      help='tree name within file, default: "PiAbsSelector/tree"')
  parser.add_argument('-v','--variables',
                      help='variable string for ROOT TTree::Scan')
  parser.add_argument('-c','--cuts',
                      default="",
                      help='cut string for ROOT TTree::Scan, default: ""')
  parser.add_argument('--friendFile',
                      help='filename friend tree is in')
  parser.add_argument('--friendTreeName',
                      default="friend",
                      help='friend tree name within file, default: "friend"')

  
  args = parser.parse_args()
  print args
  if bool(args.file) ^ bool(args.variables):
    print "Error: You must either use none of or both of: --file and --variables"
    sys.exit(1)
  doingArgs = False
  if args.file:
    cuts = ""
    if args.cuts:
      cuts = args.cuts
    f = root.TFile(args.file)
    tree = f.Get(args.treeName)
    if args.friendFile:
      tree.AddFriend(args.friendTreeName,args.friendFile)
    tree.Scan(args.variables,args.cuts)
  else:
    #runNoArgs()
    print "would run normal stuff"

  print "end"
