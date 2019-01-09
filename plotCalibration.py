#!/usr/bin/env python

from plotWires import *
import glob


class CaloCalibrationFactors(object):

  def __init__(self,fn,expectedMPV=1.74):
    self.fn = fn
    # wire, mpv, mpv err, nEvents
    self.entries = []
    with open(fn) as f:
      for row in f:
        row = row[:-1].split(",")
        entry = [int(row[0])]+ [float(i) for i in row[1:]]
        self.entries.append(entry)

    self.dataMPV = [expectedMPV]*3*480
    for entry in self.entries:
      self.dataMPV[entry[0]] = entry[1]
    self.sf = [expectedMPV/x for x in self.dataMPV]
    self.sfStr = ""
    for i in range(len(self.sf)):
      self.sfStr += "*((Iteration$ == {0}) * {1})".format(i,self.sf[i])

  def get_zWiredEdx(self):
    return "zWiredEdx"+self.sfStr

if __name__ == "__main__":

  EXPECTEDMPV = 1.74

  caloCalib = CaloCalibrationFactors("Calibration_run5145.txt",EXPECTEDMPV)

  histConfigs = [
  ]
  c = root.TCanvas()
  NMAX=10000000000
  NMAX=100
  #fn = "piAbsSelector_protodune_beam_p2GeV_cosmics_3ms_sce_mcc10_100evts.root"
  #caption = "MCC10, 2 GeV SCE"
  #fn = "piAbsSelector_mcc11_protoDUNE_reco_100evts.root"
  #fn = "PiAbs_mcc11.root"
  fn = "PiAbsSelector.root"
  name = "mcc11"
  #caption = "ProtoDUNE-SP Internal"# & MCC11"
  caption = ""
  scaleFactor= 1.
  #fn = "PiAbs_mcc10_2and7GeV_3ms_sce.root"
  #caption = "MCC10 2 & 7 GeV 3m SCE"

  fileConfigsData = [
    {
      'fn': "piAbsSelector_run5387_v4.10.root",
      'name': "run5387",
      'title': "Run 5387: 1 GeV/c",
      'caption': "Run 5387: 1 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 0 && TOF < 170.)*"+primaryTrackCutsData, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 170.)*"+primaryTrackCutsData, # for protons
    },
    {
      'fn': "piAbsSelector_run5432_v4.10.root",
      'name': "run5432",
      'title': "Run 5432: 2 GeV/c",
      'caption': "Run 5432: 2 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 0 && TOF < 160.)*"+primaryTrackCutsData, # for pions
      #'cuts': "*(CKov1Status == 0 && TOF > 160.)*"+primaryTrackCutsData, # for protons
    },
    {
      'fn': "piAbsSelector_run5145_v4.10.root",
      'name': "run5145",
      'title': "Run 5145: 7 GeV/c",
      'caption': "Run 5145: 7 GeV/c",
      'isData': True,
      'cuts': "*(CKov1Status == 1 && CKov0Status == 1)*"+primaryTrackCutsData, # for pions/electrons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 1)*"+primaryTrackCutsData, # for kaons
      #'cuts': "*(CKov1Status == 0 && CKov0Status == 0)*"+primaryTrackCutsData, # for protons
    },
  ]
  for i, fileConfig in enumerate(fileConfigsData):
    fileConfig['color'] = COLORLIST[i]
  fileConfigsAllData = [
    {
      'fn': [
                "piAbsSelector_run5145_v4.10.root",
                #"piAbsSelector_run5387.root",
                #"piAbsSelector_run5430.root",
                #"piAbsSelector_run5758.root",
                #"piAbsSelector_run5777.root",
                #"piAbsSelector_run5826.root",
                #"piAbsSelector_run5834.root",
                #"piAbsSelector_run5145_v3.root",
                #"piAbsSelector_run5387_v3.root",
                #"piAbsSelector_run5432_v3.root",
            ],
      'name': "runMany",
      'title': "Runs 5145, 5387, 5432",
      'caption': "Runs 5145, 5387, 5432",
      'color': root.kBlack,
      #'cuts': "*"+cutGoodBeamline,
    },
  ]
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

  for histConfig in histConfigs:
    histConfig["caption"] = caption
    histConfig["normalize"] = True
    histConfig["ytitle"] = "Normalized Events / Bin"

  plotManyFilesOnePlot(fileConfigsData,histConfigs,c,"PiAbsSelector/tree",outPrefix="PostCalibration_",outSuffix="Hist",nMax=NMAX)
  for histConfig in histConfigs:
    histConfig['logy'] = True
    histConfig["normalize"] = False
    histConfig["ytitle"] = "Events / Bin"
  plotManyFilesOnePlot(fileConfigsData,histConfigs,c,"PiAbsSelector/tree",outPrefix="PostCalibration_",outSuffix="_logyHist",nMax=NMAX)

  wireBinning = [480*3,0,480*3]
  #wireBinning = [100,0,100]

  histConfigs= [
    {
      'name': "dEdxVWireNum",
      'xtitle': "Z Wire Number",
      'ytitle': "dE/dx [MeV/cm]",
      'binning': wireBinning+[100,0,10],
      'var': caloCalib.get_zWiredEdx()+":Iteration$",
      'cuts': "1",
      'logz': True,
      'drawhlines': [EXPECTEDMPV],
    },
  ]
  hists = plotOneHistOnePlot(fileConfigsData,histConfigs,c,"PiAbsSelector/tree",outPrefix="PostCalibration_",nMax=NMAX)

