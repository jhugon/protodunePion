{
  gROOT->ProcessLine(".L makeFriendTree.C++");

  unsigned maxEvents = 100000000;
  //maxEvents = 10;

  TString caloCalibFn = "CalibrationFactors_run5145.txt";
  TString sceCalibFn = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_sce_2GeV_scaleData.txt";
  TString sceCalibFnFLF = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_flf_7GeV_scaleData.txt";
  TString sceCalibFnMC = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_sce_2GeV.txt";
  TString sceCalibFnMCFLF = "CalibrationSCE_PythonSmooth_deltaWireTrueZVWireNum_mcc11_flf_7GeV.txt";

  makeFriendTree("piAbsSelector_run5145_d9d59922.root","friendTree_piAbsSelector_run5145_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  makeFriendTree("piAbsSelector_run5387_d9d59922.root","friendTree_piAbsSelector_run5387_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);
  makeFriendTree("piAbsSelector_run5432_d9d59922.root","friendTree_piAbsSelector_run5432_d9d59922.root",caloCalibFn,sceCalibFn,sceCalibFnFLF,maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_7p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_7p0GeV_v4.12.root","","","",maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_2p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_2p0GeV_v4.12.root","","","",maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_flf_1p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_sce_1p0GeV_v4.12.root","",sceCalibFnMC,sceCalibFnMCFLF,maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.12.root","","","",maxEvents);
}
