
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

void makeFriendTree (TString inputFileName,TString outputFileName,TString caloCalibFileName, TString sceCalibFileName, TString sceCalibFileNameFLF, unsigned maxEvents, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() << " in file " << outputFileName.Data() <<" using calo calibration file: "<< caloCalibFileName.Data() << " and SCE calib file: "<< sceCalibFileName << " and FLF SCE calib file: "<< sceCalibFileNameFLF<< endl;

  bool isMC;
  std::vector<float>* zWiredEdx=0; TBranch* b_zWiredEdx;
  std::vector<float>* zWireZ=0; TBranch* b_zWireZ;
  std::vector<float>* zWireWireZ=0; TBranch* b_zWireWireZ;
  Float_t PFBeamPrimStartZ;
  Float_t PFBeamPrimEndZ;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("zWiredEdx",&zWiredEdx,&b_zWiredEdx);
  tree->SetBranchAddress("zWireZ",&zWireZ,&b_zWireZ);
  tree->SetBranchAddress("zWireWireZ",&zWireWireZ,&b_zWireWireZ);
  tree->SetBranchAddress("PFBeamPrimStartZ",&PFBeamPrimStartZ);
  tree->SetBranchAddress("PFBeamPrimEndZ",&PFBeamPrimEndZ);
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
  std::vector<float> zWireZ_corrFLF(480*3);
  Int_t zWireFirstHitWire;
  Int_t zWireLastHitWire;
  Int_t zWireLastContigHitWire;
  Float_t PFBeamPrimStartZ_corr;
  Float_t PFBeamPrimEndZ_corr;
  Float_t PFBeamPrimStartZ_corrFLF;
  Float_t PFBeamPrimEndZ_corrFLF;

  friendTree->Branch("zWiredEdx_corr",&zWiredEdx_corr);
  friendTree->Branch("zWireZ_corr",&zWireZ_corr);
  friendTree->Branch("zWireZ_corrFLF",&zWireZ_corrFLF);
  friendTree->Branch("zWireFirstHitWire",&zWireFirstHitWire,"zWireFirstHitWire/I");
  friendTree->Branch("zWireLastHitWire",&zWireLastHitWire,"zWireLastHitWire/I");
  friendTree->Branch("zWireLastContigHitWire",&zWireLastContigHitWire,"zWireLastContigHitWire/I");
  friendTree->Branch("PFBeamPrimStartZ_corr",&PFBeamPrimStartZ_corr,"PFBeamPrimStartZ_corr/F");
  friendTree->Branch("PFBeamPrimEndZ_corr",&PFBeamPrimEndZ_corr,"PFBeamPrimEndZ_corr/F");
  friendTree->Branch("PFBeamPrimStartZ_corrFLF",&PFBeamPrimStartZ_corrFLF,"PFBeamPrimStartZ_corrFLF/F");
  friendTree->Branch("PFBeamPrimEndZ_corrFLF",&PFBeamPrimEndZ_corrFLF,"PFBeamPrimEndZ_corrFLF/F");

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
  std::vector<float> wirePosMap(480*3,1e-20);
  while (sceCalibFile.good())
  {
    std::getline(sceCalibFile,line,'\n');
    if(line.size() == 0) break;
    const size_t commaLoc = line.find(',');
    const size_t commaLoc2 = line.rfind(',');
    if(commaLoc == std::string::npos || commaLoc2 == std::string::npos || commaLoc == commaLoc2)
    {
      std::cerr << "Warning: didn't understand line in sceCalibFile: '"<<line<<"'"<< std::endl;
    }
    else
    {
      const auto iWireStr = line.substr(0,commaLoc);
      const auto wirePosStr = line.substr(commaLoc+1,commaLoc2);
      const auto corrStr = line.substr(commaLoc2+1);
      const unsigned long iWire = std::stoul(iWireStr);
      const float wirePos = std::stof(wirePosStr);
      const float corr = std::stof(corrStr);
      sceCalibMap[iWire] = corr;
      wirePosMap[iWire] = wirePos;
    }
  }

  std::fstream sceCalibFileFLF(sceCalibFileNameFLF.Data(),ios_base::in);
  std::vector<float> sceCalibMapFLF(480*3,0);
  while (sceCalibFileFLF.good())
  {
    std::getline(sceCalibFileFLF,line,'\n');
    if(line.size() == 0) break;
    const size_t commaLoc = line.find(',');
    const size_t commaLoc2 = line.rfind(',');
    if(commaLoc == std::string::npos || commaLoc2 == std::string::npos || commaLoc == commaLoc2)
    {
      std::cerr << "Warning: didn't understand line in sceCalibFileFLF: '"<<line<<"'"<< std::endl;
    }
    else
    {
      const auto iWireStr = line.substr(0,commaLoc);
      const auto corrStr = line.substr(commaLoc2+1);
      const unsigned long iWire = std::stoul(iWireStr);
      const float corr = std::stof(corrStr);
      sceCalibMapFLF[iWire] = corr;
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
    b_zWireZ->GetEntry(iEntry);
    b_zWireWireZ->GetEntry(iEntry);

    for (size_t iZWire=0; iZWire<480*3; iZWire++)
    {
      zWiredEdx_corr[iZWire] = DEFAULTNEG;
      zWireZ_corr[iZWire] = DEFAULTNEG;
      zWireZ_corrFLF[iZWire] = DEFAULTNEG;
    }

    zWireFirstHitWire = DEFAULTNEG;
    zWireLastHitWire = DEFAULTNEG;
    zWireLastContigHitWire = DEFAULTNEG;
    PFBeamPrimStartZ_corr = DEFAULTNEG;
    PFBeamPrimEndZ_corr = DEFAULTNEG;
    PFBeamPrimStartZ_corrFLF = DEFAULTNEG;
    PFBeamPrimEndZ_corrFLF = DEFAULTNEG;
    // Find which wire is the start and end point to correct Z
    if(zWireWireZ)
    {
      const size_t& zWireSize = zWireWireZ->size();
      if(PFBeamPrimStartZ > -10000)
      {
        if (PFBeamPrimStartZ <= zWireWireZ->at(0)) 
        {
          PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[0];
          PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[0];
        }
        else if (PFBeamPrimStartZ >= zWireWireZ->at(zWireSize-1)) 
        {
          PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[zWireSize-1];
          PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[zWireSize-1];
        }
      }
      if(PFBeamPrimEndZ > -10000)
      {
        if (PFBeamPrimEndZ <= zWireWireZ->at(0)) 
        {
          PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[0];
          PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[0];
        }
        else if (PFBeamPrimEndZ >= zWireWireZ->at(zWireSize-1)) 
        {
          PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[zWireSize-1];
          PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[zWireSize-1];
        }
      }
      for (size_t iZWire=0; iZWire<zWireSize-1; iZWire++)
      {
        if(PFBeamPrimStartZ > -10000. && PFBeamPrimStartZ_corr < -10000. && PFBeamPrimStartZ >= zWireWireZ->at(iZWire))
        {
          if(PFBeamPrimStartZ-zWireWireZ->at(iZWire) < zWireWireZ->at(iZWire+1)-PFBeamPrimStartZ)
          {
            PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[iZWire];
            PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[iZWire];
          }
          else
          {
            PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[iZWire+1];
            PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[iZWire+1];
          }
        }
        if(PFBeamPrimEndZ > -10000. && PFBeamPrimEndZ_corr < -10000. && PFBeamPrimEndZ >= zWireWireZ->at(iZWire))
        {
          if(PFBeamPrimEndZ-zWireWireZ->at(iZWire) < zWireWireZ->at(iZWire+1)-PFBeamPrimEndZ)
          {
            PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[iZWire];
            PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[iZWire];
          }
          else
          {
            PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[iZWire+1];
            PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[iZWire+1];
          }
        }
      } // for iZWire
    } // if zWireWireZ
    // Now per wire stuff
    //std::cout << "Start, end:     " << PFBeamPrimStartZ_corr << "    " << PFBeamPrimEndZ_corr << std::endl;
    //std::cout << "Start, end: FLF " << PFBeamPrimStartZ_corrFLF << "    " << PFBeamPrimEndZ_corrFLF << std::endl;
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
          zWireZ_corrFLF[iZWire] = zWireZ->at(iZWire) + sceCalibMapFLF.at(iZWire);
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
