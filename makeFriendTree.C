
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
const auto MCHARGEDPION = 139.57018; // MeV/c^2
const auto MPROTON = 938.2720813; // MeV/c^2
const auto KINLOSTBEFORETPC = 0.0; //MeV; from LArIAT pion total cross section group
const auto KINLOSTBEFORETPCPROTON = 0.0; //MeV; from LArIAT pion total cross section group


void makeFriendTree (TString inputFileName,TString outputFileName,TString caloCalibFileName, TString sceCalibFileName, TString sceCalibFileNameFLF, unsigned maxEvents, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() << " in file " << outputFileName.Data() <<" using calo calibration file: "<< caloCalibFileName.Data() << " and SCE calib file: "<< sceCalibFileName << " and FLF SCE calib file: "<< sceCalibFileNameFLF<< endl;

  bool isMC;
  std::vector<float>* zWiredEdx=0; TBranch* b_zWiredEdx;
  std::vector<float>* zWirePitch=0; TBranch* b_zWirePitch;
  std::vector<float>* zWireZ=0; TBranch* b_zWireZ;
  std::vector<float>* zWireWireZ=0; TBranch* b_zWireWireZ;
  std::vector<float>* PFBeamPrimdEdxs=0; TBranch* b_PFBeamPrimdEdxs;
  std::vector<Int_t>* PFBeamPrimZWires=0; TBranch* b_PFBeamPrimZWires;
  std::vector<float>* PFBeamPrimPitches=0; TBranch* b_PFBeamPrimPitches;
  std::vector<float>* PFBeamPrimZs=0; TBranch* b_PFBeamPrimZs;
  Float_t PFBeamPrimStartZ;
  Float_t PFBeamPrimEndZ;
  Float_t pWC;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("zWiredEdx",&zWiredEdx,&b_zWiredEdx);
  tree->SetBranchAddress("zWirePitch",&zWirePitch,&b_zWirePitch);
  tree->SetBranchAddress("zWireZ",&zWireZ,&b_zWireZ);
  tree->SetBranchAddress("zWireWireZ",&zWireWireZ,&b_zWireWireZ);
  tree->SetBranchAddress("PFBeamPrimdEdxs",&PFBeamPrimdEdxs,&b_PFBeamPrimdEdxs);
  tree->SetBranchAddress("PFBeamPrimZWires",&PFBeamPrimZWires,&b_PFBeamPrimZWires);
  tree->SetBranchAddress("PFBeamPrimPitches",&PFBeamPrimPitches,&b_PFBeamPrimPitches);
  tree->SetBranchAddress("PFBeamPrimZs",&PFBeamPrimZs,&b_PFBeamPrimZs);
  tree->SetBranchAddress("PFBeamPrimStartZ",&PFBeamPrimStartZ);
  tree->SetBranchAddress("PFBeamPrimEndZ",&PFBeamPrimEndZ);
  tree->SetBranchAddress("pWC",&pWC);
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
  std::vector<float> zWirePartKin_corr(480*3);
  std::vector<float> zWirePartKinProton_corr(480*3);
  std::vector<float> PFBeamPrimdEdxs_corr(480*3);
  std::vector<float> PFBeamPrimKins_corr(480*3);
  std::vector<float> PFBeamPrimKinsProton_corr(480*3);
  std::vector<float> PFBeamPrimZs_corr(480*3);
  std::vector<float> PFBeamPrimZs_corrFLF(480*3);
  Float_t zWireEnergySum_corr;
  Int_t zWireFirstHitWire;
  Int_t zWireLastHitWire;
  Int_t zWireLastContigHitWire;
  Float_t PFBeamPrimStartZ_corr;
  Float_t PFBeamPrimEndZ_corr;
  Float_t PFBeamPrimStartZ_corrFLF;
  Float_t PFBeamPrimEndZ_corrFLF;
  Float_t PFBeamPrimKinInteract_corr;
  Float_t PFBeamPrimKinInteractProton_corr;
  Float_t PFBeamPrimEnergySum_corr;

  friendTree->Branch("zWiredEdx_corr",&zWiredEdx_corr);
  friendTree->Branch("zWireZ_corr",&zWireZ_corr);
  friendTree->Branch("zWireZ_corrFLF",&zWireZ_corrFLF);
  friendTree->Branch("zWirePartKin_corr",&zWirePartKin_corr);
  friendTree->Branch("zWirePartKinProton_corr",&zWirePartKinProton_corr);
  friendTree->Branch("PFBeamPrimdEdxs_corr",&PFBeamPrimdEdxs_corr);
  friendTree->Branch("PFBeamPrimKins_corr",&PFBeamPrimKins_corr);
  friendTree->Branch("PFBeamPrimKinsProton_corr",&PFBeamPrimKinsProton_corr);
  friendTree->Branch("PFBeamPrimZs_corr",&PFBeamPrimZs_corr);
  friendTree->Branch("PFBeamPrimZs_corrFLF",&PFBeamPrimZs_corrFLF);
  friendTree->Branch("zWireEnergySum_corr",&zWireEnergySum_corr,"zWireEnergySum_corr/F");
  friendTree->Branch("zWireFirstHitWire",&zWireFirstHitWire,"zWireFirstHitWire/I");
  friendTree->Branch("zWireLastHitWire",&zWireLastHitWire,"zWireLastHitWire/I");
  friendTree->Branch("zWireLastContigHitWire",&zWireLastContigHitWire,"zWireLastContigHitWire/I");
  friendTree->Branch("PFBeamPrimStartZ_corr",&PFBeamPrimStartZ_corr,"PFBeamPrimStartZ_corr/F");
  friendTree->Branch("PFBeamPrimEndZ_corr",&PFBeamPrimEndZ_corr,"PFBeamPrimEndZ_corr/F");
  friendTree->Branch("PFBeamPrimStartZ_corrFLF",&PFBeamPrimStartZ_corrFLF,"PFBeamPrimStartZ_corrFLF/F");
  friendTree->Branch("PFBeamPrimEndZ_corrFLF",&PFBeamPrimEndZ_corrFLF,"PFBeamPrimEndZ_corrFLF/F");
  friendTree->Branch("PFBeamPrimKinInteract_corr",&PFBeamPrimKinInteract_corr,"PFBeamPrimKinInteract_corr/F");
  friendTree->Branch("PFBeamPrimKinInteractProton_corr",&PFBeamPrimKinInteractProton_corr,"PFBeamPrimKinInteractProton_corr/F");
  friendTree->Branch("PFBeamPrimEnergySum_corr",&PFBeamPrimEnergySum_corr,"PFBeamPrimEnergySum_corr/F");

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
    b_zWirePitch->GetEntry(iEntry);
    b_zWireZ->GetEntry(iEntry);
    b_zWireWireZ->GetEntry(iEntry);
    b_PFBeamPrimdEdxs->GetEntry(iEntry);
    b_PFBeamPrimZWires->GetEntry(iEntry);
    b_PFBeamPrimZs->GetEntry(iEntry);

    for (size_t iZWire=0; iZWire<480*3; iZWire++)
    {
      zWiredEdx_corr[iZWire] = DEFAULTNEG;
      zWireZ_corr[iZWire] = DEFAULTNEG;
      zWireZ_corrFLF[iZWire] = DEFAULTNEG;
      zWirePartKin_corr[iZWire] = DEFAULTNEG;
      zWirePartKinProton_corr[iZWire] = DEFAULTNEG;
    }
    PFBeamPrimdEdxs_corr.clear();
    PFBeamPrimKins_corr.clear();
    PFBeamPrimKinsProton_corr.clear();
    PFBeamPrimZs_corr.clear();
    PFBeamPrimZs_corrFLF.clear();

    zWireEnergySum_corr = DEFAULTNEG;
    zWireFirstHitWire = DEFAULTNEG;
    zWireLastHitWire = DEFAULTNEG;
    zWireLastContigHitWire = DEFAULTNEG;
    PFBeamPrimStartZ_corr = DEFAULTNEG;
    PFBeamPrimEndZ_corr = DEFAULTNEG;
    PFBeamPrimStartZ_corrFLF = DEFAULTNEG;
    PFBeamPrimEndZ_corrFLF = DEFAULTNEG;
    PFBeamPrimKinInteract_corr = DEFAULTNEG;
    PFBeamPrimKinInteractProton_corr = DEFAULTNEG;
    PFBeamPrimEnergySum_corr = DEFAULTNEG;

    // Either got pWC from beam or from primaryParticle, so now is the time to do this
    float eWC = sqrt(pWC*pWC+MCHARGEDPION*MCHARGEDPION); // assume charged pion in MeV
    float kinWC = eWC - MCHARGEDPION; // assume charged pion in MeV
    float kinWCInTPC = kinWC - KINLOSTBEFORETPC;
                   
    // for proton
    float eWCProton = sqrt(pWC*pWC+MPROTON*MPROTON);
    float kinWCProton = eWCProton - MPROTON;
    float kinWCInTPCProton = kinWCProton - KINLOSTBEFORETPCPROTON;

    // Find which wire is the start and end point to correct Z
    if(zWireWireZ)
    {
      const size_t& zWireSize = zWireWireZ->size();
      if(PFBeamPrimStartZ > -10000)
      {
        if (PFBeamPrimStartZ <= zWireWireZ->at(0)) 
        {
          //cout << "Start is < first wire\n";
          PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[0];
          PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[0];
        }
        else if (PFBeamPrimStartZ >= zWireWireZ->at(zWireSize-1)) 
        {
          //cout << "Start is >= last wire\n";
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
      for (size_t iZWire=1; iZWire<zWireSize; iZWire++)
      {
        if(PFBeamPrimStartZ > -10000. && PFBeamPrimStartZ_corr < -10000. && PFBeamPrimStartZ < zWireWireZ->at(iZWire))
        {
          //cout << "Start is < wire: "<<iZWire<<" at "<<zWireWireZ->at(iZWire)<<"\n";
          if(PFBeamPrimStartZ-zWireWireZ->at(iZWire-1) < zWireWireZ->at(iZWire)-PFBeamPrimStartZ)
          {
            //cout << "  Using prev one: wire: "<<iZWire-1<<" at "<<zWireWireZ->at(iZWire-1)
            //        <<" corr: "<<sceCalibMap[iZWire-1]<<"\n";
            PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[iZWire-1];
            PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[iZWire-1];
          }
          else
          {
            //cout << "  Using this one, corr: "<<sceCalibMap[iZWire]<<"\n";
            PFBeamPrimStartZ_corr = PFBeamPrimStartZ+sceCalibMap[iZWire];
            PFBeamPrimStartZ_corrFLF = PFBeamPrimStartZ+sceCalibMapFLF[iZWire];
          }
        }
        if(PFBeamPrimEndZ > -10000. && PFBeamPrimEndZ_corr < -10000. && PFBeamPrimEndZ < zWireWireZ->at(iZWire))
        {
          if(PFBeamPrimEndZ-zWireWireZ->at(iZWire-1) < zWireWireZ->at(iZWire)-PFBeamPrimEndZ)
          {
            PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[iZWire-1];
            PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[iZWire-1];
          }
          else
          {
            PFBeamPrimEndZ_corr = PFBeamPrimEndZ+sceCalibMap[iZWire];
            PFBeamPrimEndZ_corrFLF = PFBeamPrimEndZ+sceCalibMapFLF[iZWire];
          }
        }
      } // for iZWire
    } // if zWireWireZ
    // Now per wire stuff
    //std::cout << "Start, end:     " << PFBeamPrimStartZ << "    " << PFBeamPrimEndZ << std::endl;
    //std::cout << "Start, end: SCE " << PFBeamPrimStartZ_corr << "    " << PFBeamPrimEndZ_corr << std::endl;
    //std::cout << "Start, end: FLF " << PFBeamPrimStartZ_corrFLF << "    " << PFBeamPrimEndZ_corrFLF << std::endl;
    //std::cout << "Start, end: SCE diff to normal: " << PFBeamPrimStartZ_corr - PFBeamPrimStartZ
    //            << "    " << PFBeamPrimEndZ_corr - PFBeamPrimEndZ << std::endl;
    //std::cout << "Start, end: FLF diff to normal: " << PFBeamPrimStartZ_corrFLF - PFBeamPrimStartZ
    //            << "    " << PFBeamPrimEndZ_corrFLF - PFBeamPrimEndZ << std::endl;
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
    // Now redo kin and energy sum and stuff
    if(zWirePitch)
    {
      zWireEnergySum_corr = 0.;
      for (long iZWire=0; iZWire <= zWireLastHitWire; iZWire++)
      {    
        zWirePartKin_corr.at(iZWire) = kinWCInTPC - zWireEnergySum_corr;
        zWirePartKinProton_corr.at(iZWire) = kinWCInTPCProton - zWireEnergySum_corr;
        if(zWiredEdx_corr.at(iZWire) >= 0.)
        {    
          zWireEnergySum_corr += zWiredEdx_corr.at(iZWire) * zWirePitch->at(iZWire);
        }    
      } // for iZWire
    } // if zWiredEdx && zWirePitch

    // Now on to PFBeamPrimdEdxs, etc.
    if(PFBeamPrimdEdxs && PFBeamPrimZWires && PFBeamPrimPitches && PFBeamPrimZs)
    {
      size_t nHits = PFBeamPrimdEdxs->size();
      PFBeamPrimEnergySum_corr = 0.;
      for(size_t iHit=0; iHit < nHits; iHit++)
      {
        long iWire = PFBeamPrimZWires->at(iHit);
        if(iWire >= 0)
        {
          PFBeamPrimKins_corr.push_back(kinWCInTPC-PFBeamPrimEnergySum_corr);
          PFBeamPrimKinsProton_corr.push_back(kinWCInTPCProton-PFBeamPrimEnergySum_corr);
          float dEdx = PFBeamPrimdEdxs->at(iHit);
          //cout << "dEdx: " << dEdx << " iWire: " << iWire;
          if(dEdx > 0.)
          {
            //cout << " calib:  " << caloCalibMap.at(iWire);
            dEdx *= caloCalibMap.at(iWire);
            //cout << " dEdx:  " << dEdx;
            PFBeamPrimEnergySum_corr += dEdx * PFBeamPrimPitches->at(iHit);
          }
          //cout << endl;
          PFBeamPrimdEdxs_corr.push_back(dEdx);
          PFBeamPrimZs_corr.push_back(PFBeamPrimZs->at(iHit)+sceCalibMap.at(iWire));
          PFBeamPrimZs_corrFLF.push_back(PFBeamPrimZs->at(iHit)+sceCalibMapFLF.at(iWire));
        } // if iWire >= 0
        else
        {
          PFBeamPrimKins_corr.push_back(DEFAULTNEG);
          PFBeamPrimKinsProton_corr.push_back(DEFAULTNEG);
          PFBeamPrimdEdxs_corr.push_back(DEFAULTNEG);
          PFBeamPrimZs_corr.push_back(DEFAULTNEG);
          PFBeamPrimZs_corrFLF.push_back(DEFAULTNEG);
        }
        //cout << "Hit: " << iHit << " dEdx: " << PFBeamPrimdEdxs->at(iHit)
        //                << " dEdx_corr: " << PFBeamPrimdEdxs_corr.at(iHit) << endl;
      } // for iHit
      PFBeamPrimKinInteract_corr = kinWCInTPC - PFBeamPrimEnergySum_corr;
      PFBeamPrimKinInteractProton_corr = kinWCInTPCProton - PFBeamPrimEnergySum_corr;
    } // if PFBeamPrimdEdxs and PFBeamPrimZWires and PFBeamPrimPitches

    friendTree->Fill();
  } // for iEvent

  friendTree->Write();
  outFile->Close();

}
