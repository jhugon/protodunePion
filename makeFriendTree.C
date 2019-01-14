
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
const auto DEFAULTNEG = -99999999;

void makeFriendTree (TString inputFileName,TString outputFileName,TString caloCalibFileName, TString sceCalibFileName, unsigned maxEvents, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() << " in file " << outputFileName.Data() <<" using calo calibration file: "<< caloCalibFileName.Data() << " and SCE calib file: "<< sceCalibFileName<< endl;

  bool isMC;
  std::vector<float>* zWiredEdx=0; TBranch* b_zWiredEdx;
  std::vector<float>* zWireZ=0; TBranch* b_zWireZ;
  //Float_t PFBeamPrimStartZ;
  //Float_t PFBeamPrimEndZ;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("zWiredEdx",&zWiredEdx,&b_zWiredEdx);
  tree->SetBranchAddress("zWireZ",&zWireZ,&b_zWireZ);
  //tree->Print();

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Friend Tree

  TFile* outFile = new TFile(outputFileName,"RECREATE");
  outFile->cd();

  TTree* friendTree = new TTree("friend","");
  std::vector<float> zWiredEdx_corr(480*3);
  std::vector<float> zWireZ_corr(480*3);
  Int_t zWireFirstHitWire;
  Int_t zWireLastHitWire;
  Int_t zWireLastContigHitWire;
  //Float_t PFBeamPrimStartZ_corr;
  //Float_t PFBeamPrimEndZ_corr;

  friendTree->Branch("zWiredEdx_corr",&zWiredEdx_corr);
  friendTree->Branch("zWireZ_corr",&zWireZ_corr);
  friendTree->Branch("zWireFirstHitWire",&zWireFirstHitWire,"zWireFirstHitWire/I");
  friendTree->Branch("zWireLastHitWire",&zWireLastHitWire,"zWireLastHitWire/I");
  friendTree->Branch("zWireLastContigHitWire",&zWireLastContigHitWire,"zWireLastContigHitWire/I");
  //friendTree->Branch("PFBeamPrimStartZ_corr",&PFBeamPrimStartZ_corr,"PFBeamPrimStartZ_corr/F");
  //friendTree->Branch("PFBeamPrimEndZ_corr",&PFBeamPrimEndZ_corr,"PFBeamPrimEndZ_corr/F");

  ///////////////////////////////
  ///////////////////////////////
  ///////////////////////////////
  // Calibration data
  std::string line;

  std::fstream caloCalibFile(caloCalibFileName.Data(),ios_base::in);
  std::vector<float> caloCalibMap;
  while (caloCalibFile.good())
  {
    std::getline(caloCalibFile,line,'\n');
    if(line.size() == 0) break;
    float val = std::stof(line);
    caloCalibMap.push_back(val);
  }
  caloCalibFile.close();
  if(caloCalibMap.size() == 0)
  {
    caloCalibMap.resize(480*3,1.);
  }

  std::fstream sceCalibFile(sceCalibFileName.Data(),ios_base::in);
  std::vector<float> sceCalibMap(480*3,0);
  while (sceCalibFile.good())
  {
    std::getline(sceCalibFile,line,'\n');
    if(line.size() == 0) break;
    size_t commaLoc = line.find(',');
    if(commaLoc == std::string::npos)
    {
      std::cerr << "Warning: didn't understand line in sceCalibFile: '"<<line<<"'"<< std::endl;
    }
    else
    {
      auto iWireStr = line.substr(0,commaLoc);
      auto corrStr = line.substr(commaLoc+1);
      unsigned long iWire = std::stoul(iWireStr);
      float corr = std::stof(corrStr);
      sceCalibMap[iWire] = corr;
    }
  }

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

    for (size_t iZWire=0; iZWire<480*3; iZWire++)
    {
      zWiredEdx_corr[iZWire] = DEFAULTNEG;
      zWireZ_corr[iZWire] = DEFAULTNEG;
    }

    zWireFirstHitWire = DEFAULTNEG;
    zWireLastHitWire = DEFAULTNEG;
    zWireLastContigHitWire = DEFAULTNEG;
    bool lastZWireGood=false;
    if(zWiredEdx)
    {
      const size_t& zWireSize = zWiredEdx->size();
      for (size_t iZWire=0; iZWire<zWireSize; iZWire++)
      {
        const auto& dEdx = zWiredEdx->at(iZWire);
        if(dEdx >= 0)
        {
          zWiredEdx_corr[iZWire] = caloCalibMap.at(iZWire)*dEdx;
          zWireZ_corr[iZWire] = zWireZ->at(iZWire) + sceCalibMap.at(iZWire);
          zWireLastHitWire = iZWire;
          if(lastZWireGood)
          {
            zWireLastContigHitWire = iZWire;
          }
          if(zWireFirstHitWire < 0.)
          {
            zWireFirstHitWire = iZWire;
            zWireLastContigHitWire = iZWire;
            lastZWireGood = true;
          }
        }
        else
        {
          lastZWireGood = false;
        }
      } // for iZWire
    } // if zWiredEdx

    friendTree->Fill();
  } // for iEvent

  friendTree->Write();
  outFile->Close();

}
