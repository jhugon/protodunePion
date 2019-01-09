{
  gROOT->ProcessLine(".L makeFriendTree.C++");

  //unsigned maxEvents = 100000000;
  unsigned maxEvents = 100;

  TString calibrationFn = "Calibration_Data.txt";

  makeFriendTree("piAbsSelector_mcc11_3ms_2p0GeV_v4.10.root","friendTree_piAbsSelector_mcc11_3ms_2p0GeV_v4.10.root",calibrationFn,maxEvents);

}
