{
  gROOT->ProcessLine(".L makeFriendTree.C++");

  unsigned maxEvents = 100000000;
  //unsigned maxEvents = 100;

  TString calibrationFn = "CalibrationFactors_run5145.txt";

  makeFriendTree("piAbsSelector_run5145_v4.10.root","friendTree_piAbsSelector_run5145_v4.10.root",calibrationFn,maxEvents);
  makeFriendTree("piAbsSelector_run5387_v4.10.root","friendTree_piAbsSelector_run5387_v4.10.root",calibrationFn,maxEvents);
  makeFriendTree("piAbsSelector_run5432_1kevts_v4.10.root","friendTree_piAbsSelector_run5432_1kevts_v4.10.root",calibrationFn,maxEvents);

}
