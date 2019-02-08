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

  makeFriendTree("piAbsSelector_run5145_d9d59922.root","friendTree_piAbsSelector_run5145_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  makeFriendTree("piAbsSelector_run5387_d9d59922.root","friendTree_piAbsSelector_run5387_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  makeFriendTree("piAbsSelector_run5432_d9d59922.root","friendTree_piAbsSelector_run5432_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  makeFriendTree("piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  makeFriendTree("piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);

  makeFriendTree("piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  makeFriendTree("piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  makeFriendTree("piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);

  makeFriendTree("piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibflfFn,ajibflfCalibConst,ajibflfNormFact);
  makeFriendTree("piAbsSelector_mcc11_sce_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_1p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents,ajibsceFn,ajibsceCalibConst,ajibsceNormFact);
  makeFriendTree("piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","","","",maxEvents,ajib3msFn,ajib3msCalibConst,ajib3msNormFact);
}
