{
  gROOT->ProcessLine(".L makeFriendTree.C++");

  unsigned maxEvents = 100000000;
  //unsigned maxEvents = 100;

  TString calibrationFn = "CalibrationFactors_run5145.txt";

  makeFriendTree("piAbsSelector_run5145_v4.10.root","friendTree_piAbsSelector_run5145_v4.10.root",calibrationFn,maxEvents);
  makeFriendTree("piAbsSelector_run5387_v4.10.root","friendTree_piAbsSelector_run5387_v4.10.root",calibrationFn,maxEvents);
  makeFriendTree("piAbsSelector_run5432_v4.10.root","friendTree_piAbsSelector_run5432_v4.10.root",calibrationFn,maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_7p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_flf_7p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_7p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_sce_7p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_3ms_7p0GeV_v4.11.root","",maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_2p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_flf_2p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_2p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_sce_2p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_3ms_2p0GeV_v4.11.root","",maxEvents);

  makeFriendTree("piAbsSelector_mcc11_flf_1p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_flf_1p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_sce_1p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_sce_1p0GeV_v4.11.root","",maxEvents);
  makeFriendTree("piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root","friendTree_piAbsSelector_mcc11_3ms_1p0GeV_v4.11.root","",maxEvents);

}
