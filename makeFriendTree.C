
#include <TSystem.h>
#include <TROOT.h>
#include <TFile.h>
#include <TChain.h>
#include <TTree.h>
#include <TH2F.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TMath.h>
//#include <TF1.h>
//#include <TRandom3.h>

#include <iostream>
#include <vector>
#include <cmath>

#define pi TMath::Pi()

void makeFriendTree (TString inputFileName,TString outputFileName,TString calibFileName, unsigned maxEvents, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() << " in file " << outputFileName.Data() <<" using calibration file: "<< calibFileName.Data() << endl;

  bool isMC;
  Float_t pzWC;
  Float_t trueStartMom;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("pzWC",&pzWC);
  tree->SetBranchAddress("trueStartMom",&trueStartMom);

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Friend Tree

  TFile* outFile = new TFile(outputFileName,"RECREATE");
  outFile->cd();

  TTree* friendTree = new TTree("friend","");
  float allWeight, pzWeight;

  friendTree->Branch("allWeight",&allWeight,"allWeight/F");
  friendTree->Branch("pzWeight",&pzWeight,"pzWeight/F");

  Double_t pzWeightSum=0;
  Double_t nEventsSum=0;

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Event Loop

  unsigned nEvents = tree->GetEntries();
  unsigned reportEach=1000;
  cout << "nEvents in tree: " << nEvents << endl;
  cout << "Stopping at " << maxEvents << endl;

  for(unsigned iEvent=0; iEvent<nEvents;iEvent++)
  {
    if(iEvent >= maxEvents)
      break;
    tree->GetEntry(iEvent);

    friendTree->Fill();
  } // for iEvent

  friendTree->Write();
  outFile->Close();

}
