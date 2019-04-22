{
  gROOT->ProcessLine(".L makeFriendTree.C++");

  unsigned maxEvents = 100000000;
  //maxEvents = 10;

  TString caloCalibFn = "CalibrationFactors_run5145.txt";
  TString sceCalibFn = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_sce_2GeV_scaleData.txt";
  TString sceCalibFnFLF = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_flf_7GeV_scaleData.txt";
  TString sceCalibFnMC = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_sce_2GeV.txt";
  TString sceCalibFnMCFLF = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_flf_7GeV.txt";

  TString ajib3msFn = "/cshare/vol2/users/jhugon/apaudel_calib/v080100/mcc11_sceoff_1-5/sceoff_1-5gev_Xcalibration.root";
  TString ajibsceFn = "/cshare/vol2/users/jhugon/apaudel_calib/v080100/mcc11_SCE_5-7/sce_5-7gev_Xcalibration.root";
  TString ajibflfFn = "/cshare/vol2/users/jhugon/apaudel_calib/v080100/mcc11_FLF_5-7/sce_5-7gev_Xcalibration.root";

  double ajib3msCalibConst = 4.79e-3;
  double ajibsceCalibConst = 4.71e-3;
  double ajibflfCalibConst = 4.73e-3;

  double ajib3msNormFact = 1.6925;
  double ajibsceNormFact = 1.639;
  double ajibflfNormFact = 1.656;

  makeFriendTree("piAbsSelector_run5432_v8.0_64cf7360_local.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_run5432_oldCalo_oldBIPos_v7.4_5a76d2fe.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("PiAbsSelector_run5145_50evt_v7.4_5a76d2fe.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("PiAbsSelector_run5145_50evt_oldPos_v7.4_5a76d2fe.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);

  //makeFriendTree("piAbsSelector_run5145_v7_55712ad_local.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_run5432_v7_55712ad_local.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_run5387_v7_55712ad_local.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);

//  makeFriendTree("piAbsSelector_data_run5432_v7a2_faaca6ad.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
//  makeFriendTree("piAbsSelector_data_run5786_v7a2_faaca6ad.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_data_run5204_v7a2_faaca6ad.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_data_run5387_v7a2_faaca6ad.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  //makeFriendTree("piAbsSelector_data_run5770_v7a2_faaca6ad.root","",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);

  //makeFriendTree("piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);

  //makeFriendTree("piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);

  //makeFriendTree("piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_1p0GeV_v6.1_08b55104.root","friendTree_piAbsSelector_mcc11_sce_1p0GeV_v6.1_08b55104.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_1p0GeV_v7.0_55712adf_local.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_2p0GeV_v7.0_55712adf_local.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_7p0GeV_v7.0_55712adf_local.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);

  //makeFriendTree("piAbsSelector_mcc11_sce_1GeV_histats_part1_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_1GeV_histats_part2_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_1GeV_histats_part3_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_1GeV_histats_part4_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_2GeV_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_3ms_2GeV_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_3GeV_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_6GeV_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  //makeFriendTree("piAbsSelector_mcc11_sce_7GeV_v7a1_55712adf.root","","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
}
