#!/usr/bin/env python

import ROOT as root
from helpers import *
root.gROOT.SetBatch(True)
import copy
import sys
import signal
import multiprocessing

def doPlots(NMAX,mcfn,caption,scaleFactor,fileConfigsData,sillystr):
  doNMinusOne = True
  doNoCuts = True
  doSCE = False
  doLogy = True

  cutConfigs = [
    {
      'histConfigs':
        [
          #{
          #  'name': "nGoodFEMBs",
          #  'xtitle': "N Good FEMBs for Beam-side APAs",
          #  'ytitle': "Events / bin",
          #  'binning': [61,-0.5,60.5],
          #  'var': "nGoodFEMBs[0] + nGoodFEMBs[2] + nGoodFEMBs[4]",
          #},
       ],
      'cut': "isMC || (nGoodFEMBs[0] == 20 && nGoodFEMBs[2] == 20 && nGoodFEMBs[4] == 20)",
    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "pBI_low",
#            'xtitle': "Beamline Momentum [GeV/c]",
#            'ytitle': "Events / bin",
#            'binning': [80,0,4],
#            'var': "pWC/1000.",
#            'printIntegral': True,
#          },
#          {
#            'name': "pBI_wide",
#            'xtitle': "Beamline Momentum [GeV/c]",
#            'ytitle': "Events / bin",
#            'binning': [100,0,10],
#            'var': "pWC/1000.",
#            'printIntegral': True,
#          },
#        ],
#      'cut': "1",
#    },
    {
      'histConfigs':
        [
          #{
          #  'name': "PFNBeamSlices",
          #  'xtitle': "Number of PF Beam Slices",
          #  'ytitle': "Events / bin",
          #  'binning': [9,-0.5,8.5],
          #  'var': "PFNBeamSlices",
          #  'printIntegral': True,
          #},
        ],
      'cut': "PFNBeamSlices == 1",
    },
    {
      'histConfigs':
        [
          #{
          #  'name': "PFBeamPrimIsTracklike",
          #  'xtitle': "PF Beam Primary is Track-like",
          #  'ytitle': "Tracks / bin",
          #  'binning': [2,-0.5,1.5],
          #  'var': "PFBeamPrimIsTracklike",
          #},
        ],
      'cut': "PFBeamPrimIsTracklike == 1",
    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "DeltaXPFBeamPrimBI",
#            'xtitle': "#Delta X PF Track & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-25,50],
#            'var': "PFBeamPrimXFrontTPC - xWC",
#          },
#          {
#            'name': "DeltaXPFBeamPrimBI_wide",
#            'xtitle': "#Delta X PF Track & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-100,100],
#            'var': "PFBeamPrimXFrontTPC - xWC",
#          },
#       ],
#      #'cut': "(isMC && ((PFBeamPrimXFrontTPC-xWC) > -10) && ((PFBeamPrimXFrontTPC-xWC) < 10)) || ((!isMC) && ((PFBeamPrimXFrontTPC-xWC) > 10) && ((PFBeamPrimXFrontTPC-xWC) < 30))",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "DeltaYPFBeamPrimBI",
#            'xtitle': "#Delta Y PF Track & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-25,50],
#            'var': "PFBeamPrimYFrontTPC - yWC",
#          },
#          {
#            'name': "DeltaYPFBeamPrimBI_wide",
#            'xtitle': "#Delta Y PF Track & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-100,100],
#            'var': "PFBeamPrimYFrontTPC - yWC",
#          },
#       ],
#      #'cut': "(isMC && ((PFBeamPrimYFrontTPC-yWC) > -10) && ((PFBeamPrimYFrontTPC-yWC) < 10)) || ((!isMC) && ((PFBeamPrimYFrontTPC-yWC) > 7) && ((PFBeamPrimYFrontTPC-yWC) < 27))",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "DeltaXPFBeamPrimBI_fromTrackEnd",
#            'xtitle': "#Delta X PF Track End & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-25,50],
#            'var': "PFBeamPrimXFrontTPCTrackEnd - xWC",
#          },
#          {
#            'name': "DeltaXPFBeamPrimBI_fromTrackEnd_wide",
#            'xtitle': "#Delta X PF Track End & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-100,100],
#            'var': "PFBeamPrimXFrontTPCTrackEnd - xWC",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "DeltaYPFBeamPrimBI_fromTrackEnd",
#            'xtitle': "#Delta Y PF Track End & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-25,50],
#            'var': "PFBeamPrimYFrontTPCTrackEnd - yWC",
#          },
#          {
#            'name': "DeltaYPFBeamPrimBI_fromTrackEnd_wide",
#            'xtitle': "#Delta Y PF Track End & BI Track at TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-100,100],
#            'var': "PFBeamPrimYFrontTPCTrackEnd - yWC",
#          },
#       ],
#      'cut': "1",
#    },
    {
      'histConfigs':
        [
          #{
          #  'name': "DeltaXPFBeamPrimStartBI",
          #  'xtitle': "#Delta X PF Track Start & BI Track [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [150,-25,50],
          #  'var': "PFBeamPrimStartX - xWC",
          #},
          #{
          #  'name': "DeltaXPFBeamPrimStartBI_wide",
          #  'xtitle': "#Delta X PF Track Start & BI Track [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [100,-100,100],
          #  'var': "PFBeamPrimStartX - xWC",
          #},
       ],
      'cut': "(isMC && ((PFBeamPrimStartX-xWC) > -5) && ((PFBeamPrimStartX-xWC) < 5)) || ((!isMC) && ((PFBeamPrimStartX-xWC) > 0) && ((PFBeamPrimStartX-xWC) < 20))",
    },
    {
      'histConfigs':
        [
          #{
          #  'name': "DeltaYPFBeamPrimStartBI",
          #  'xtitle': "#Delta Y PF Track Start & BI Track [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [150,-25,50],
          #  'var': "PFBeamPrimStartY - yWC",
          #},
          #{
          #  'name': "DeltaYPFBeamPrimStartBI_wide",
          #  'xtitle': "#Delta Y PF Track Start & BI Track [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [100,-100,100],
          #  'var': "PFBeamPrimStartY - yWC",
          #},
       ],
      'cut': "(isMC && ((PFBeamPrimStartY-yWC) > 0) && ((PFBeamPrimStartY-yWC) < 10)) || ((!isMC) && ((PFBeamPrimStartY-yWC) > 10) && ((PFBeamPrimStartY-yWC) < 30))",
    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimAngleToBeamTrk",
#            'xtitle': "Angle Between BI & Primary PF Track [Deg]",
#            'ytitle': "Events / bin",
#            'binning': [80,0,40],
#            'var': "PFBeamPrimAngleToBeamTrk*180/pi",
#            #'cutSpans': [[30.,None]],
#          },
#          {
#            'name': "PFBeamPrimAngleToBeamTrk_wide",
#            'xtitle': "Angle Between BI & Primary PF Track [Deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,0,180],
#            'var': "PFBeamPrimAngleToBeamTrk*180/pi",
#            #'cutSpans': [[30.,None]],
#          },
#       ],
#      #'cut': "PFBeamPrimAngleToBeamTrk < 30.*pi/180.",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndAngleToBeamTrk",
#            'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
#            'ytitle': "Events / bin",
#            'binning': [80,0,40],
#            'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
#            #'cutSpans': [[30.,None]],
#          },
#          {
#            'name': "PFBeamPrimEndAngleToBeamTrk_wide",
#            'xtitle': "Angle Between BI & Primary PF Track End [Deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,0,180],
#            'var': "PFBeamPrimEndAngleToBeamTrk*180/pi",
#            #'cutSpans': [[30.,None]],
#          },
#       ],
#      #'cut': "PFBeamPrimEndAngleToBeamTrk < 30.*pi/180.",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimBeamCosmicScore",
#            'xtitle': "Pandora Beam / Cosmic BDT Score",
#            'ytitle': "Events / bin",
#            'binning': [100,-0.5,0.5],
#            'var': "PFBeamPrimBeamCosmicScore",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartX",
#            'xtitle': "Track Start X Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-100,50],
#            'var': "PFBeamPrimStartX",
#          },
#          {
#            'name': "PFBeamPrimStartX_wide",
#            'xtitle': "Track Start X Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-500,500],
#            'var': "PFBeamPrimStartX",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartY",
#            'xtitle': "Track Start Y Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,350,450],
#            'var': "PFBeamPrimStartY",
#          },
#          {
#            'name': "PFBeamPrimStartY_wide",
#            'xtitle': "Track Start Y Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [315,-10,620],
#            'var': "PFBeamPrimStartY",
#          },
#       ],
#      'cut': "1"
#    },
    {
      'histConfigs':
        [
          #{
          #  'name': "PFBeamPrimStartZ",
          #  'xtitle': "TPC Track Start Z [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [100,-5,60],
          #  'var': "PFBeamPrimStartZ",
          #},
          #{
          #  'name': "PFBeamPrimStartZ_wide",
          #  'xtitle': "TPC Track Start Z [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [400,-10,705],
          #  'var': "PFBeamPrimStartZ",
          #},
       ],
      'cut': "PFBeamPrimStartZ<50",
    },
    #{
    #  'histConfigs':
    #    [
    #      {
    #        'name': "PFBeamPrimStartZ_corr",
    #        'xtitle': "TPC Track Start Z (SCE Corrected) [cm]",
    #        'ytitle': "Events / bin",
    #        'binning': [100,-5,60],
    #        'var': "PFBeamPrimStartZ_corr",
    #      },
    #      {
    #        'name': "PFBeamPrimStartZ_corr_wide",
    #        'xtitle': "TPC Track Start Z (SCE Corrected) [cm]",
    #        'ytitle': "Events / bin",
    #        'binning': [400,-10,705],
    #        'var': "PFBeamPrimStartZ_corr",
    #      },
    #   ],
    #  'cut': "1",
    #},
    #{
    #  'histConfigs':
    #    [
    #      {
    #        'name': "PFBeamPrimStartZ_corrFLF",
    #        'xtitle': "TPC Track Start Z (FLF SCE Corrected) [cm]",
    #        'ytitle': "Events / bin",
    #        'binning': [100,-5,60],
    #        'var': "PFBeamPrimStartZ_corrFLF",
    #      },
    #      {
    #        'name': "PFBeamPrimStartZ_corrFLF_wide",
    #        'xtitle': "TPC Track Start Z (FLF SCE Corrected) [cm]",
    #        'ytitle': "Events / bin",
    #        'binning': [400,-10,705],
    #        'var': "PFBeamPrimStartZ_corrFLF",
    #      },
    #   ],
    #  'cut': "1",
    #},
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndX",
#            'xtitle': "Track End X Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-150,50],
#            'var': "PFBeamPrimEndX",
#          },
#          {
#            'name': "PFBeamPrimEndX_wide",
#            'xtitle': "Track End X Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [100,-500,500],
#            'var': "PFBeamPrimEndX",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndY",
#            'xtitle': "Track End Y Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [125,250,500],
#            'var': "PFBeamPrimEndY",
#          },
#          {
#            'name': "PFBeamPrimEndY_wide",
#            'xtitle': "Track End Y Position [cm]",
#            'ytitle': "Events / bin",
#            'binning': [63,-10,620],
#            'var': "PFBeamPrimEndY",
#          },
#       ],
#      'cut': "1"
#    },
    {
      'histConfigs':
        [
          #{
          #  'name': "PFBeamPrimEndZ_end",
          #  'xtitle': "TPC Track End Z [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [55,600,710],
          #  'var': "PFBeamPrimEndZ",
          #},
          #{
          #  'name': "PFBeamPrimEndZ_start",
          #  'xtitle': "TPC Track End Z [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [55,-10,100],
          #  'var': "PFBeamPrimEndZ",
          #},
          #{
          #  'name': "PFBeamPrimEndZ_wide",
          #  'xtitle': "TPC Track End Z [cm]",
          #  'ytitle': "Events / bin",
          #  'binning': [143,-10,705],
          #  'var': "PFBeamPrimEndZ",
          #},
       ],
      'cut': "PFBeamPrimEndZ<650",
    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "lastHitWireMod480",
#            'xtitle': "Last Hit Z Wire Number Mod 480",
#            'ytitle': "Events / bin",
#            'binning': [30,450,480],
#            'var': "zWireLastHitWire % 480",
#          },
#          {
#            'name': "lastHitWireMod480_wide",
#            'xtitle': "Last Hit Z Wire Number Mod 480",
#            'ytitle': "Events / bin",
#            'binning': [96,0,480],
#            'var': "zWireLastHitWire % 480",
#          },
#       ],
#      #'cut': "(zWireLastHitWire % 480) <= 485",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndZ_corrFLF",
#            'xtitle': "TPC Track End Z (FLF SCE Corrected) [cm]",
#            'ytitle': "Events / bin",
#            'binning': [55,600,705],
#            'var': "PFBeamPrimEndZ_corrFLF",
#          },
#          {
#            'name': "PFBeamPrimEndZ_corrFLF_wide",
#            'xtitle': "TPC Track End Z (FLF SCE Corrected) [cm]",
#            'ytitle': "Events / bin",
#            'binning': [143,-10,705],
#            'var': "PFBeamPrimEndZ_corrFLF",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndZ_corr",
#            'xtitle': "TPC Track End Z (SCE Corrected) [cm]",
#            'ytitle': "Events / bin",
#            'binning': [55,600,705],
#            'var': "PFBeamPrimEndZ_corr",
#          },
#          {
#            'name': "PFBeamPrimEndZ_corr_wide",
#            'xtitle': "TPC Track End Z (SCE Corrected) [cm]",
#            'ytitle': "Events / bin",
#            'binning': [143,-10,705],
#            'var': "PFBeamPrimEndZ_corr",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartTheta",
#            'xtitle': "TPC Track Start #theta [deg]",
#            'ytitle': "Events / bin",
#            'binning': [50,0,50],
#            'var': "PFBeamPrimStartTheta*180/pi",
#          },
#          {
#            'name': "PFBeamPrimStartTheta_wide",
#            'xtitle': "TPC Track Start #theta [deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,0,180],
#            'var': "PFBeamPrimStartTheta*180/pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartPhi",
#            'xtitle': "TPC Track Start #phi [deg]",
#            'ytitle': "Events / bin",
#            'binning': [60,-160,-100],
#            'var': "PFBeamPrimStartPhi*180/pi",
#          },
#          {
#            'name': "PFBeamPrimStartPhi_wide",
#            'xtitle': "TPC Track Start #phi [deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,-180,180],
#            'var': "PFBeamPrimStartPhi*180/pi",
#            'printIntegral': True,
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartThetaXZ",
#            'xtitle': "TPC Track Start #theta_{xz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [50,-25,0],
#            #'var': "(atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#          },
#          {
#            'name': "PFBeamPrimStartThetaXZ_wide",
#            'xtitle': "TPC Track Start #theta_{xz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,-90,90],
#            #'var': "(atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartThetaYZ",
#            'xtitle': "TPC Track Start #theta_{yz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [80,-40,0],
#            #'var': "(atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#          },
#          {
#            'name': "PFBeamPrimStartThetaYZ_wide",
#            'xtitle': "TPC Track Start #theta_{yz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,-90,90],
#            #'var': "(atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180/pi)*(PFBeamPrimStartTheta > -100.)+(PFBeamPrimStartTheta <= -100.)*-999999",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndThetaXZ",
#            'xtitle': "TPC Track End #theta_{xz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [50,-25,0],
#            #'var': "(atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#          },
#          {
#            'name': "PFBeamPrimEndThetaXZ_wide",
#            'xtitle': "TPC Track End #theta_{xz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,-90,90],
#            #'var': "(atan2(sin(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimEndTheta)*cos(PFBeamPrimEndPhi))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimEndThetaYZ",
#            'xtitle': "TPC Track End #theta_{yz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [80,-40,0],
#            #'var': "(atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#          },
#          {
#            'name': "PFBeamPrimEndThetaYZ_wide",
#            'xtitle': "TPC Track End #theta_{yz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,-90,90],
#            #'var': "(atan2(sin(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi),cos(PFBeamPrimEndTheta))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#            'var': "(atan(tan(PFBeamPrimEndTheta)*sin(PFBeamPrimEndPhi))*180/pi)*(PFBeamPrimEndTheta > -100.)+(PFBeamPrimEndTheta <= -100.)*-999999",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartThetaY",
#            'xtitle': "TPC Track #theta_{y} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,0,180],
#            'var': "acos(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi))*180./pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartPhiZX",
#            'xtitle': "TPC Track #phi_{zx} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,-180,180],
#            'var': "atan2(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180./pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimStartThetaX",
#            'xtitle': "TPC Track #theta_{x} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [180,0,180],
#            'var': "acos(sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi))*180./pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#              'name': "trackStartCosThetaX",
#              'xtitle': "TPC Track cos(#theta_{x})",
#              'ytitle': "Events / bin",
#              'binning': [100,0,1],
#              'var': "sin(PFBeamPrimStartTheta)*cos(PFBeamPrimStartPhi)",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#              'name': "PFBeamPrimStartPhiZY",
#              'xtitle': "TPC Track #phi_{zy} [deg]",
#              'ytitle': "Events / bin",
#              'binning': [180,-180,180],
#              'var': "atan2(sin(PFBeamPrimStartTheta)*sin(PFBeamPrimStartPhi),cos(PFBeamPrimStartTheta))*180./pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'name': "PFBeamPrimTrkLen",
#      'xtitle': "TPC Track Length [cm]",
#      'ytitle': "Events / bin",
#      'binning': [200,0,800],
#      'var': "PFBeamPrimTrkLen",
#      'cut': "1",
#    },
#    {
#      'name': "PFBeamPrimNDaughters",
#      'xtitle': "Number of PF Secondaries",
#      'ytitle': "Events / bin",
#      'binning': [9,-0.5,8.5],
#      'var': "PFBeamPrimNDaughters",
#      'cut': "1",
#    },
#    {
#      'name': "kinBI",
#      'xtitle': "Beamline Kinetic Energy (assume #pi^{+}) [MeV]",
#      'ytitle': "Events / bin",
#      'binning': [100,0,10],
#      'var': "kinWC/1000.",
#      'cut': "1",
#    },
#    {
#      'name': "PFBeamPrimKinInteract",
#      'xtitle': "PF Track Interaction KE [GeV]",
#      'ytitle': "Events / bin",
#      'binning': [100,0,10],
#      'var': "PFBeamPrimKinInteract/1000.",
#      'cut': "1",
#    },
#    {
#      'name': "trueSecondToEndKin",
#      'xtitle': "True Particle Interaction KE [GeV]",
#      'ytitle': "Events / bin",
#      'binning': [100,0,10],
#      'var': "trueSecondToEndKin/1000.",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimYFrontTPC",
#            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [50,300,600],
#            'var': "PFBeamPrimYFrontTPC",
#          },
#          {
#            'name': "PFBeamPrimYFrontTPC_wide",
#            'xtitle': "Y of TPC Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [300,-500,1500],
#            'var': "PFBeamPrimYFrontTPC",
#          },
#       ],
#      #'cut': "PFBeamPrimYFrontTPC > 400 && PFBeamPrimYFrontTPC < 470"
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimXFrontTPC",
#            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [50,-100,100],
#            'var': "PFBeamPrimXFrontTPC",
#          },
#          {
#            'name': "PFBeamPrimXFrontTPC_wide",
#            'xtitle': "X of TPC Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-600,600],
#            'var': "PFBeamPrimXFrontTPC",
#          },
#       ],
#      #'cut': "PFBeamPrimXFrontTPC > -40 && PFBeamPrimXFrontTPC < 20",
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "yWC",
#            'xtitle': "Y of BI Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [50,300,600],
#            'var': "yWC",
#          },
#          {
#            'name': "yWC_wide",
#            'xtitle': "Y of BI Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [300,-500,1500],
#            'var': "yWC",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "xWC",
#            'xtitle': "X of BI Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [50,-100,100],
#            'var': "xWC",
#          },
#          {
#            'name': "xWC_wide",
#            'xtitle': "X of BI Track Projection to TPC Front [cm]",
#            'ytitle': "Events / bin",
#            'binning': [150,-600,600],
#            'var': "xWC",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "thetaWCXZ",
#            'xtitle': "BI Track #theta_{xz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [50,-25,0],
#            #'var': "(atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#            'var': "(atan(tan(thetaWC)*cos(phiWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          },
#          #{
#          #  'name': "thetaWCXZ_wide",
#          #  'xtitle': "BI Track #theta_{xz} [deg]",
#          #  'ytitle': "Events / bin",
#          #  'binning': [90,-90,90],
#          #  #'var': "(atan2(sin(thetaWC)*cos(phiWC),cos(thetaWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          #  'var': "(atan(tan(thetaWC)*cos(phiWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          #},
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "thetaWCYZ",
#            'xtitle': "BI Track #theta_{yz} [deg]",
#            'ytitle': "Events / bin",
#            'binning': [50,-25,0],
#            #'var': "(atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#            'var': "(atan(tan(thetaWC)*sin(phiWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          },
#          #{
#          #  'name': "thetaWCYZ_wide",
#          #  'xtitle': "BI Track #theta_{yz} [deg]",
#          #  'ytitle': "Events / bin",
#          #  'binning': [90,-90,90],
#          #  #'var': "(atan2(sin(thetaWC)*sin(phiWC),cos(thetaWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          #  'var': "(atan(tan(thetaWC)*sin(phiWC))*180/pi)*(thetaWC > -100.)+(thetaWC <= -100.)*-999999",
#          #},
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimTrkStartEndDirAngle",
#            'xtitle': "TPC Track Angle Between Start & End [deg]",
#            'ytitle': "Events / bin",
#            'binning': [30,0,30],
#            'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
#          },
#          {
#            'name': "PFBeamPrimTrkStartEndDirAngle_wide",
#            'xtitle': "TPC Track Angle Between Start & End [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,0,180],
#            'var': "PFBeamPrimTrkStartEndDirAngle*180/pi",
#          },
#       ],
#      'cut': "1",
#    },
#    {
#      'histConfigs':
#        [
#          {
#            'name': "PFBeamPrimTrkMaxKink",
#            'xtitle': "TPC Track Max Kink Angle [deg]",
#            'ytitle': "Events / bin",
#            'binning': [40,0,20],
#            'var': "PFBeamPrimTrkMaxKink*180/pi",
#          },
#          {
#            'name': "PFBeamPrimTrkMaxKink_wide",
#            'xtitle': "TPC Track Max Kink Angle [deg]",
#            'ytitle': "Events / bin",
#            'binning': [90,0,180],
#            'var': "PFBeamPrimTrkMaxKink*180/pi",
#          },
#       ],
#      'cut': "1",
#    },
  ]

  fileConfigsMC = [
    #{
    #  'fn': mcfn,
    #  'name': "mcc11_piInel",
    #  'title': "MCC11 #pi Inelastic",
    #  'caption': "MCC11 #pi Inelastic",
    #  'cuts': "*(trueCategory>=1 && trueCategory <=4)",
    #  'color': root.kBlue-7,
    #  'scaleFactor': scaleFactor,
    #},
    {
      'fn': mcfn,
      'name': "mcc11_piInel_good",
      'title': "MCC11 #pi Inelastic--Good Reco",
      'caption': "MCC11 #pi Inelastic--Good Reco",
      'cuts':"*(trueCategory>=1 && trueCategory <=4)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))<20)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': mcfn,
      'name': "mcc11_piInel_badIntMatch",
      'title': "MCC11 #pi Inelastic--Bad Reco/True Interaction Match",
      'caption': "MCC11 #pi Inelastic--Bad Reco/True Interaction Match",
      'cuts':"*(trueCategory>=1 && trueCategory <=4)*(PFBeamPrimTrueTrackID == truePrimaryTrackID)*(sqrt(pow(PFBeamPrimEndX-trueEndX,2)+pow(PFBeamPrimEndY-trueEndY,2)+pow(PFBeamPrimEndZ-trueEndZ,2))>=20)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': mcfn,
      'name': "mcc11_piInel_badTrkMatch",
      'title': "MCC11 #pi Inelastic--Bad Track/True Primary Match",
      'caption': "MCC11 #pi Inelastic--Bad Track/True Primary Match",
      'cuts':"*(trueCategory>=1 && trueCategory <=4)*(PFBeamPrimTrueTrackID != truePrimaryTrackID)",
      'color': root.kBlue-7,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': mcfn,
      'name': "mcc11_piDecay",
      'title': "MCC11 #pi Decay",
      'caption': "MCC11 #pi Decay",
      'cuts': "*(trueCategory==9 || trueCategory ==10)",
      'color': root.kRed-4,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': mcfn,
      'name': "mcc11_piOutsideTPC",
      'title': "MCC11 #pi Interacted Outside TPC",
      'caption': "MCC11 #pi Interacted Outside TPC",
      'cuts': "*(trueCategory==6 || trueCategory ==7 || trueCategory==8)",
      'color': root.kGreen+3,
      'scaleFactor': scaleFactor,
    },
    {
      'fn': mcfn,
      'name': "mcc11_mu",
      'title': "MCC11 Primary Muon",
      'caption': "MCC11 Primary Muon",
      'cuts': "*(trueCategory==13)",
      'color': root.kAzure+10,
      'scaleFactor': scaleFactor,
    },
    #{
    #  'fn': mcfn,
    #  'name': "mcc11_other",
    #  'title': "MCC11 Unknown",
    #  'caption': "MCC11 Unknown",
    #  'cuts': "*(trueCategory==5)",
    #  'color': root.kAzure+10,
    #  'scaleFactor': scaleFactor,
    #},
  ]
  if ('6GeV' in sillystr) or ('7GeV' in sillystr):
    fileConfigsMC.append({
      'fn': mcfn,
      'name': "mcc11_e",
      'title': "MCC11 Primary Electron",
      'caption': "MCC11 Primary Electron",
      'cuts': "*(trueCategory==11)",
      'color': root.kAzure+10,
      'scaleFactor': scaleFactor,
    })
  #fileConfigsMC = [
  #  {
  #    'fn': mcfn,
  #    'name': "mcc11",
  #    'title': "MCC11",
  #    'caption': "MCC11",
  #    'cuts': "*((trueCategory == 13 || trueCategory < 11) && trueCategory > 0 )",
  #    'color': root.kBlue-7,
  #    'scaleFactor': scaleFactor,
  #  },
  #]

  fileConfigsData = copy.deepcopy(fileConfigsData)
  print "fileConfigsMC"
  print fileConfigsMC
  print "fileConfigsData"
  print fileConfigsData

  for iFC, fc in enumerate(fileConfigsData):
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
  for iFC, fc in enumerate(fileConfigsMC):
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]
    fc["color"] = COLORLIST[iFC]

  mcscecuts = "*((trueCategory == 13 || trueCategory < 11) && trueCategory > 0 )"
  #mcscecuts = "*((trueCategory == 13 || trueCategory <= 11) && trueCategory > 0 )"
  fileConfigsSCEMC = [
    {
      'fn': "piAbsSelector_mcc11_3ms_2p0GeV_v4.4.root",
      'name': "mcc11_noSCE",
      'title': "MCC11 No SCE",
      'caption': "MCC11 No SCE",
      'cuts': mcscecuts,
      'scaleFactor': 1.,
      'color': root.kBlue-7,
    },
    {
      'fn': "piAbsSelector_mcc11_sce_2p0GeV_v4.4.root",
      'name': "mcc11_SCE",
      'title': "MCC11 SCE",
      'caption': "MCC11 SCE",
      'cuts': mcscecuts,
      'scaleFactor': 1.,
      'color': root.kRed-7,
    },
    {
    'fn': "piAbsSelector_mcc11_flf_2p0GeV_v4.4.root",
      'name': "mcc11_FLF",
      'title': "MCC11 SCE FLF",
      'caption': "MCC11 SCE FLF",
      'cuts': mcscecuts,
      'scaleFactor': 1.,
      'color': root.kGreen+3,
    },
  ]
  for fc in fileConfigsSCEMC:
    fc["addFriend"] = ["friend","friendTree_"+fc["fn"]]

  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        histConfig["caption"] = "N-1 Cut, "+caption
    else: 
      cutConfig["caption"] = "N-1 Cut, "+caption

  histConfigs = []
  for cutConfig in cutConfigs:
    if "histConfigs" in cutConfig:
      for histConfig in cutConfig["histConfigs"]:
        config = copy.deepcopy(histConfig)
        config["caption"] = caption
        config["cuts"] = "1"
        histConfigs.append(config)
    else: 
      config = copy.deepcopy(cutConfig)
      config["caption"] = caption
      del config["cut"]
      config["cuts"] = "1"
      histConfigs.append(config)
  try:
    histConfigs[0]["printIntegral"] = True
    histConfigs[-1]["printIntegral"] = True
  except IndexError:
    pass

  c = root.TCanvas()

  if doNMinusOne:
    dataMCStackNMinusOne(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_NM1_"+sillystr,nMax=NMAX,table=True)
  if doNoCuts:
    dataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_"+sillystr,nMax=NMAX)
  if doSCE:
    plotManyFilesOneNMinusOnePlot(fileConfigsData+fileConfigsSCEMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="InelasticSCE_",outSuffix="_NM1_"+sillystr,nMax=NMAX,table=True)
  if doLogy:
    for cutConfig in cutConfigs:
      if "histConfigs" in cutConfig:
        for histConfig in cutConfig["histConfigs"]:
          histConfig['logy'] = True
      else: 
        cutConfig['logy'] = True
    logHistConfigs = []
    for histConfig in histConfigs:
      histConfig['logy'] = True
    if doNMinusOne:
      dataMCStackNMinusOne(fileConfigsData,fileConfigsMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_NM1_logy_"+sillystr,nMax=NMAX)
    if doNoCuts:
      dataMCStack(fileConfigsData,fileConfigsMC,histConfigs,c,"PiAbsSelector/tree",outPrefix="Inelastic_",outSuffix="_logy_"+sillystr,nMax=NMAX)
    if doSCE:
      plotManyFilesOneNMinusOnePlot(fileConfigsData+fileConfigsSCEMC,cutConfigs,c,"PiAbsSelector/tree",outPrefix="InelasticSCE_",outSuffix="_NM1_logy_"+sillystr,nMax=NMAX)

  del c

if __name__ == "__main__":

  NMAX=10000000000
  #NMAX=100
  
  #cutGoodBeamline = "(triggerIsBeam == 1 && BITriggerMatched > 0 && nBeamTracks > 0 && nBeamMom  > 0)"
  cutGoodBeamline = "(triggerIsBeam == 1 && BITriggerMatched > 0 && nBeamTracks == 1 && nBeamMom  == 1)"

  stuff = []

  stuff.append(
    (
      [{
        #'fn': "piAbsSelector_run5387_v7_55712ad_local.root",
        'fn': "piAbsSelector_data_run5387_v7a2_faaca6ad.root",
        'name': "run5387",
        'title': "Run 5387: 1 GeV/c",
        'caption': "Run 5387: 1 GeV/c",
        'cuts': "*(BIPion1GeV)*"+cutGoodBeamline,
      }],
      #"piAbsSelector_mcc11_sce_1p0GeV_v7.0_55712adf_local.root",
      "piAbsSelector_mcc11_sce_1GeV_histats_partAll_v7a1_55712adf.root",
      "Run 5387: 1 GeV/c & MCC11 SCE",
      1.185506241331484,
      "run5387_1GeV",
    )
  )

  stuff.append(
    (
      [{
        'fn': "piAbsSelector_run5432_v7_55712ad_local.root",
        'name': "run5432",
        'title': "Run 5432: 2 GeV/c",
        'caption': "Run 5432: 2 GeV/c",
        'cuts': "*(BIPion2GeV)*"+cutGoodBeamline,
      }],
      #"piAbsSelector_mcc11_sce_2p0GeV_v7.0_55712adf_local.root",
      "piAbsSelector_mcc11_sce_2GeV_v7a1_55712adf.root",
      "Run 5432: 2 GeV/c & MCC11 SCE",
      9.196239717978848,
      "run5432_2GeV",
    )
  )

  stuff.append(
    (
      [{
        'fn': "piAbsSelector_data_run5786_v7a2_faaca6ad.root",
        'name': "run5786",
        'title': "Run 5786: 3 GeV/c",
        'caption': "Run 5786: 3 GeV/c",
        'cuts': "*(BIPion3GeV)*"+cutGoodBeamline,
      }],
      "piAbsSelector_mcc11_sce_3GeV_v7a1_55712adf.root",
      "Run 5786: 3 GeV/c & MCC11 SCE",
      29.92072072072072,
      "run5786_3GeV",
    )
  )


  stuff.append(
    (
      [{
        'fn': "piAbsSelector_data_run5770_v7a2_faaca6ad.root",
        'name': "run5770",
        'title': "Run 5770: 6 GeV/c",
        'caption': "Run 5770: 6 GeV/c",
        'cuts': "*(BIPion6GeV)*"+cutGoodBeamline,
      }],
      "piAbsSelector_mcc11_sce_6GeV_v7a1_55712adf.root",
      "Run 5770: 6 GeV/c & MCC11 SCE",
      5.037104557640751,
      "run5770_6GeV",
    )
  )

  #stuff.append(
  #  (
  #    [{
  #      'fn': "piAbsSelector_run5145_v7_55712ad_local.root",
  #      'name': "run5145",
  #      'title': "Run 5145: 7 GeV/c",
  #      'caption': "Run 5145: 7 GeV/c",
  #      'cuts': "*(BIPion7GeV)*"+cutGoodBeamline,
  #    }],
  #    "piAbsSelector_mcc11_sce_7p0GeV_v7.0_55712adf_local.root",
  #    "Run 5145: 7 GeV/c & MCC11 SCE",
  #    1.,
  #    "run5145_7GeV",
  #  )
  #)

  stuff.append(
    (
      [{
        'fn': "piAbsSelector_data_run5204_v7a2_faaca6ad.root",
        'name': "run5204",
        'title': "Run 5204: 7 GeV/c",
        'caption': "Run 5204: 7 GeV/c",
        'cuts': "*(BIPion7GeV)*"+cutGoodBeamline,
      }],
      "piAbsSelector_mcc11_sce_7GeV_v7a1_55712adf.root",
      "Run 5204: 7 GeV/c & MCC11 SCE",
      0.3204933416748592,
      "run5204_7GeV",
    )
  )

  doMP = True
  pool = None
  if doMP:
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool()
    signal.signal(signal.SIGINT, original_sigint_handler)
  for fc in stuff:
    print stuff
    if doMP:
      pool.apply_async(doPlots,(NMAX,fc[1],fc[2],fc[3],fc[0],fc[4]))
    else:
      doPlots(NMAX,fc[1],fc[2],fc[3],fc[0],fc[4])
  if doMP:
    try:
      pool.close()
      pool.join()
    except KeyboardInterrupt:
      print "Caught KeyBoardInterrupt, terminating processes"
      pool.terminate()
      pool.join()
