
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
#include <fstream>

#ifdef __MAKECINT__
#pragma link C++ class vector<float>+;
#endif

#define pi TMath::Pi()

void makeFriendTree (TString inputFileName,TString outputFileName,TString calibFileName, unsigned maxEvents, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() << " in file " << outputFileName.Data() <<" using calibration file: "<< calibFileName.Data() << endl;

  bool isMC;
  std::vector<float>* zWiredEdx=0; TBranch* b_zWiredEdx;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("zWiredEdx",&zWiredEdx,&b_zWiredEdx);
  //tree->Print();

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Friend Tree

  TFile* outFile = new TFile(outputFileName,"RECREATE");
  outFile->cd();

  TTree* friendTree = new TTree("friend","");
  std::vector<float> zWiredEdx_corr;

  friendTree->Branch("zWiredEdx_corr",&zWiredEdx_corr);

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Calibration data

  std::fstream calibFile(calibFileName.Data(),ios_base::in);
  std::string line;
  std::vector<float> calibMap;
  while (calibFile.good())
  {
    std::getline(calibFile,line,'\n');
    if(line.size() == 0) break;
    float val = std::stof(line);
    calibMap.push_back(val);
  }
  calibFile.close();


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
    const auto& iEntry = tree->LoadTree(iEvent);
    b_zWiredEdx->GetEntry(iEntry);

    if(zWiredEdx)
    {
      const size_t& zWireSize = zWiredEdx->size();
      zWiredEdx_corr.resize(zWireSize);
      for (size_t iZWire=0; iZWire<zWireSize; iZWire++)
      {
        zWiredEdx_corr[iZWire] = calibMap.at(iZWire)*zWiredEdx->at(iZWire);
      }
    }

    friendTree->Fill();
  } // for iEvent

  friendTree->Write();
  outFile->Close();

}