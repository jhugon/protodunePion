
#include <TSystem.h>
#include <TROOT.h>
#include <TFile.h>
#include <TChain.h>
#include <TTree.h>
#include <TH2F.h>
#include <TH1F.h>
#include <TGraph.h>
#include <TCanvas.h>
#include <TMath.h>
#include <Math/Interpolator.h>
//#include <TF1.h>
//#include <TRandom3.h>

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <cctype>

#ifdef __MAKECINT__
#pragma link C++ class vector<float>+;
#endif

#define pi TMath::Pi()
const auto DEFAULTNEG = -99999999;
const auto MCHARGEDPION = 139.57018; // MeV/c^2
const auto MPROTON = 938.2720813; // MeV/c^2
const auto KINLOSTBEFORETPC = 0.0; //MeV; from LArIAT pion total cross section group
const auto KINLOSTBEFORETPCPROTON = 0.0; //MeV; from LArIAT pion total cross section group

class ChargeCorrectorAjib
{
  public:
    ChargeCorrectorAjib(TString calibFn, double calibConst, double normFact);
    // Get calibrated dE/dx for dQ/dx and position
    float calibrateddEdx(float dqdx, float x, float y, float z);
    // Given a dQ/dx returns a dE/dx corrected using modified box model
    float boxChargeToEnergy(float dqdx);
    // Calibrate the dqdx based on the position in the detector
    float calibrateCharge(float dqdx, float x, float y, float z);
  private:
    const double Rho = 1.383;//g/cm^3 (liquid argon density at a pressure 18.0 psia)      
    const double betap = 0.212;//(kV/cm)(g/cm^2)/MeV                                      
    const double alpha = 0.93;//parameter from ArgoNeuT experiment at 0.481kV/cm          
    const double Wion = 23.6e-6;//parameter from ArgoNeuT experiment at 0.481kV/cm        
    const double Efield = 0.50;//kV/cm protoDUNE electric filed      

    const double calibration_constant;
    const double normalisation_factor;
    TFile calibFile;
    TH1F* X_correction_hist;
};

class MuonTable
{
  public:
    MuonTable() {};
    MuonTable(TString infilename,float rho=1.396 /*g/cm^3*/);
    float dEdx(float ke /*MeV*/); // returns MeV/cm
    float range(float ke /*MeV*/); // returns cm
    float keFromRange(float r /*cm*/); // returns MeV
  protected:
    float minKin;
    float maxKin;
    float minRange;
    float maxRange;
    std::vector<double> kins;
    std::vector<double> dEdxs;
    std::vector<double> ranges;
    ROOT::Math::Interpolator dEdxInterp;
    ROOT::Math::Interpolator rangeInterp;
    ROOT::Math::Interpolator keFromRangeInterp;
};

class PStarTable : public MuonTable
{
  public:
    PStarTable(TString infilename,float rho=1.396 /*g/cm^3*/);
};

void makeFriendTree (TString inputFileName,TString outputFileName,TString caloCalibFileName, TString sceCalibFileName, TString sceCalibFileNameFLF, unsigned maxEvents, TString ajibCorrFn="/cshare/vol2/users/jhugon/apaudel_calib/v71100/run_5387_Xcalibration.root", double ajibCalibConst=6.155e-3, double ajibNormFact=0.983, TString inputTreeName="PiAbsSelector/tree")
{
  using namespace std;

  cout << "makeFriendTree for "<< inputFileName.Data() 
        << endl
        << " in file " << outputFileName.Data() 
        << endl
        <<" using calo calibration file: "<< caloCalibFileName.Data() 
        << endl
        << " SCE calib file: "<< sceCalibFileName 
        << endl
        << " FLF SCE calib file: "<< sceCalibFileNameFLF
        << endl
        << " Ajib correction file: "<< ajibCorrFn
        << endl
        << " Ajib calibration const: "<< ajibCalibConst
        << " Ajib normfactor: "<< ajibNormFact
        << endl;

  ChargeCorrectorAjib ajibCorrector(ajibCorrFn,ajibCalibConst,ajibNormFact);
  MuonTable muonTable("muE_liquid_argon.txt");
  PStarTable protonTable("pstar_argon.txt");

  bool isMC;
  std::vector<float>* zWiredEdx=0; TBranch* b_zWiredEdx;
  std::vector<float>* zWiredQdx=0; TBranch* b_zWiredQdx;
  std::vector<float>* zWirePitch=0; TBranch* b_zWirePitch;
  std::vector<float>* zWireX=0; TBranch* b_zWireX;
  std::vector<float>* zWireY=0; TBranch* b_zWireY;
  std::vector<float>* zWireZ=0; TBranch* b_zWireZ;
  std::vector<float>* zWireWireZ=0; TBranch* b_zWireWireZ;
  std::vector<float>* zWireTrueEnergy=0; TBranch* b_zWireTrueEnergy;
  std::vector<float>* PFBeamPrimdEdxs=0; TBranch* b_PFBeamPrimdEdxs;
  std::vector<Int_t>* PFBeamPrimZWires=0; TBranch* b_PFBeamPrimZWires;
  std::vector<float>* PFBeamPrimPitches=0; TBranch* b_PFBeamPrimPitches;
  std::vector<float>* PFBeamPrimXs=0; TBranch* b_PFBeamPrimXs;
  std::vector<float>* PFBeamPrimYs=0; TBranch* b_PFBeamPrimYs;
  std::vector<float>* PFBeamPrimZs=0; TBranch* b_PFBeamPrimZs;
  Float_t PFBeamPrimStartZ;
  Float_t PFBeamPrimEndZ;
  Float_t PFBeamPrimTrkLen;
  Float_t pWC;

  // infile chain
  TChain * tree = new TChain(inputTreeName);
  tree->Add(inputFileName);
  tree->SetBranchAddress("isMC",&isMC);
  tree->SetBranchAddress("zWiredEdx",&zWiredEdx,&b_zWiredEdx);
  tree->SetBranchAddress("zWiredQdx",&zWiredQdx,&b_zWiredQdx);
  tree->SetBranchAddress("zWirePitch",&zWirePitch,&b_zWirePitch);
  tree->SetBranchAddress("zWireX",&zWireX,&b_zWireX);
  tree->SetBranchAddress("zWireY",&zWireY,&b_zWireY);
  tree->SetBranchAddress("zWireZ",&zWireZ,&b_zWireZ);
  tree->SetBranchAddress("zWireWireZ",&zWireWireZ,&b_zWireWireZ);
  tree->SetBranchAddress("zWireTrueEnergy",&zWireTrueEnergy,&b_zWireTrueEnergy);
  tree->SetBranchAddress("PFBeamPrimdEdxs",&PFBeamPrimdEdxs,&b_PFBeamPrimdEdxs);
  tree->SetBranchAddress("PFBeamPrimZWires",&PFBeamPrimZWires,&b_PFBeamPrimZWires);
  tree->SetBranchAddress("PFBeamPrimPitches",&PFBeamPrimPitches,&b_PFBeamPrimPitches);
  tree->SetBranchAddress("PFBeamPrimXs",&PFBeamPrimXs,&b_PFBeamPrimXs);
  tree->SetBranchAddress("PFBeamPrimYs",&PFBeamPrimYs,&b_PFBeamPrimYs);
  tree->SetBranchAddress("PFBeamPrimZs",&PFBeamPrimZs,&b_PFBeamPrimZs);
  tree->SetBranchAddress("PFBeamPrimStartZ",&PFBeamPrimStartZ);
  tree->SetBranchAddress("PFBeamPrimEndZ",&PFBeamPrimEndZ);
  tree->SetBranchAddress("PFBeamPrimTrkLen",&PFBeamPrimTrkLen);
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
  std::vector<float> zWiredEdx_ajib(480*3);
  std::vector<float> zWiredEdx_caloScaleUp(480*3);
  std::vector<float> zWiredEdx_caloScaleDown(480*3);
  std::vector<float> zWiredQdx_ajib(480*3);
  std::vector<float> zWireZ_corr(480*3);
  std::vector<float> zWireZ_corrFLF(480*3);
  std::vector<float> zWirePartKin_corr(480*3);
  std::vector<float> zWirePartKinProton_corr(480*3);
  std::vector<float> zWirePartKin_ajib(480*3);
  std::vector<float> zWirePartKinProton_ajib(480*3);
  std::vector<float> zWirePartKin_caloScaleUp(480*3);
  std::vector<float> zWirePartKin_caloScaleDown(480*3);
  std::vector<float> zWirePartKin_beamScaleUp(480*3);
  std::vector<float> zWirePartKin_beamScaleDown(480*3);
  std::vector<float> PFBeamPrimdEdxs_corr(480*3);
  std::vector<float> PFBeamPrimdEdxs_ajib(480*3);
  std::vector<float> PFBeamPrimdQdxs_ajib(480*3);
  std::vector<float> PFBeamPrimKins_corr(480*3);
  std::vector<float> PFBeamPrimKinsProton_corr(480*3);
  std::vector<float> PFBeamPrimZs_corr(480*3);
  std::vector<float> PFBeamPrimZs_corrFLF(480*3);
  Float_t zWireEnergySum;
  Float_t zWireEnergySum_corr;
  Float_t zWireEnergySum_ajib;
  Float_t zWireEnergySum_caloScaleUp;
  Float_t zWireEnergySum_caloScaleDown;
  Int_t zWireFirstHitWire;
  Int_t zWireLastHitWire;
  Int_t zWireLastContigHitWire;
  Int_t zWireFirstHitWireTrue;
  Int_t zWireLastHitWireTrue;
  Float_t PFBeamPrimStartZ_corr;
  Float_t PFBeamPrimEndZ_corr;
  Float_t PFBeamPrimStartZ_corrFLF;
  Float_t PFBeamPrimEndZ_corrFLF;
  Float_t PFBeamPrimKinInteract_corr;
  Float_t PFBeamPrimKinInteractProton_corr;
  Float_t PFBeamPrimEnergySum_corr;
  Float_t PFBeamPrimEnergySumCSDAMu; // MeV kinetic energy
  Float_t PFBeamPrimEnergySumCSDAProton; // MeV kinetic energy
  Float_t pWCCSDARangeMu; // cm
  Float_t pWCCSDARangeProton; // cm

  friendTree->Branch("zWiredEdx_corr",&zWiredEdx_corr);
  friendTree->Branch("zWiredEdx_ajib",&zWiredEdx_ajib);
  friendTree->Branch("zWiredEdx_caloScaleUp",&zWiredEdx_caloScaleUp);
  friendTree->Branch("zWiredEdx_caloScaleDown",&zWiredEdx_caloScaleDown);
  friendTree->Branch("zWiredQdx_ajib",&zWiredQdx_ajib);
  friendTree->Branch("zWireZ_corr",&zWireZ_corr);
  friendTree->Branch("zWireZ_corrFLF",&zWireZ_corrFLF);
  friendTree->Branch("zWirePartKin_corr",&zWirePartKin_corr);
  friendTree->Branch("zWirePartKinProton_corr",&zWirePartKinProton_corr);
  friendTree->Branch("zWirePartKin_ajib",&zWirePartKin_ajib);
  friendTree->Branch("zWirePartKinProton_ajib",&zWirePartKinProton_ajib);
  friendTree->Branch("zWirePartKin_caloScaleUp",&zWirePartKin_caloScaleUp);
  friendTree->Branch("zWirePartKin_caloScaleDown",&zWirePartKin_caloScaleDown);
  friendTree->Branch("zWirePartKin_beamScaleUp",&zWirePartKin_beamScaleUp);
  friendTree->Branch("zWirePartKin_beamScaleDown",&zWirePartKin_beamScaleDown);
  friendTree->Branch("PFBeamPrimdEdxs_corr",&PFBeamPrimdEdxs_corr);
  friendTree->Branch("PFBeamPrimdEdxs_ajib",&PFBeamPrimdEdxs_ajib);
  friendTree->Branch("PFBeamPrimdQdxs_ajib",&PFBeamPrimdQdxs_ajib);
  friendTree->Branch("PFBeamPrimKins_corr",&PFBeamPrimKins_corr);
  friendTree->Branch("PFBeamPrimKinsProton_corr",&PFBeamPrimKinsProton_corr);
  friendTree->Branch("PFBeamPrimZs_corr",&PFBeamPrimZs_corr);
  friendTree->Branch("PFBeamPrimZs_corrFLF",&PFBeamPrimZs_corrFLF);
  friendTree->Branch("zWireEnergySum",&zWireEnergySum,"zWireEnergySum/F");
  friendTree->Branch("zWireEnergySum_corr",&zWireEnergySum_corr,"zWireEnergySum_corr/F");
  friendTree->Branch("zWireEnergySum_ajib",&zWireEnergySum_ajib,"zWireEnergySum_ajib/F");
  friendTree->Branch("zWireEnergySum_caloScaleUp",&zWireEnergySum_caloScaleUp,"zWireEnergySum_caloScaleUp/F");
  friendTree->Branch("zWireEnergySum_caloScaleDown",&zWireEnergySum_caloScaleDown,"zWireEnergySum_caloScaleDown/F");
  friendTree->Branch("zWireFirstHitWire",&zWireFirstHitWire,"zWireFirstHitWire/I");
  friendTree->Branch("zWireLastHitWire",&zWireLastHitWire,"zWireLastHitWire/I");
  friendTree->Branch("zWireLastContigHitWire",&zWireLastContigHitWire,"zWireLastContigHitWire/I");
  friendTree->Branch("zWireFirstHitWireTrue",&zWireFirstHitWireTrue,"zWireFirstHitWireTrue/I");
  friendTree->Branch("zWireLastHitWireTrue",&zWireLastHitWireTrue,"zWireLastHitWireTrue/I");
  friendTree->Branch("PFBeamPrimStartZ_corr",&PFBeamPrimStartZ_corr,"PFBeamPrimStartZ_corr/F");
  friendTree->Branch("PFBeamPrimEndZ_corr",&PFBeamPrimEndZ_corr,"PFBeamPrimEndZ_corr/F");
  friendTree->Branch("PFBeamPrimStartZ_corrFLF",&PFBeamPrimStartZ_corrFLF,"PFBeamPrimStartZ_corrFLF/F");
  friendTree->Branch("PFBeamPrimEndZ_corrFLF",&PFBeamPrimEndZ_corrFLF,"PFBeamPrimEndZ_corrFLF/F");
  friendTree->Branch("PFBeamPrimKinInteract_corr",&PFBeamPrimKinInteract_corr,"PFBeamPrimKinInteract_corr/F");
  friendTree->Branch("PFBeamPrimKinInteractProton_corr",&PFBeamPrimKinInteractProton_corr,"PFBeamPrimKinInteractProton_corr/F");
  friendTree->Branch("PFBeamPrimEnergySum_corr",&PFBeamPrimEnergySum_corr,"PFBeamPrimEnergySum_corr/F");
  friendTree->Branch("PFBeamPrimEnergySumCSDAMu",&PFBeamPrimEnergySumCSDAMu,"PFBeamPrimEnergySumCSDAMu/F");
  friendTree->Branch("PFBeamPrimEnergySumCSDAProton",&PFBeamPrimEnergySumCSDAProton,"PFBeamPrimEnergySumCSDAProton/F");
  friendTree->Branch("pWCCSDARangeMu",&pWCCSDARangeMu,"pWCCSDARangeMu/F");
  friendTree->Branch("pWCCSDARangeProton",&pWCCSDARangeProton,"pWCCSDARangeProton/F");

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
    b_zWireTrueEnergy->GetEntry(iEntry);
    b_PFBeamPrimdEdxs->GetEntry(iEntry);
    b_PFBeamPrimZWires->GetEntry(iEntry);
    b_PFBeamPrimZs->GetEntry(iEntry);

    for (size_t iZWire=0; iZWire<480*3; iZWire++)
    {
      zWiredEdx_corr[iZWire] = DEFAULTNEG;
      zWiredEdx_ajib[iZWire] = DEFAULTNEG;
      zWiredEdx_caloScaleUp[iZWire] = DEFAULTNEG;
      zWiredEdx_caloScaleDown[iZWire] = DEFAULTNEG;
      zWiredQdx_ajib[iZWire] = DEFAULTNEG;
      zWireZ_corr[iZWire] = DEFAULTNEG;
      zWireZ_corrFLF[iZWire] = DEFAULTNEG;
      zWirePartKin_corr[iZWire] = DEFAULTNEG;
      zWirePartKinProton_corr[iZWire] = DEFAULTNEG;
      zWirePartKin_ajib[iZWire] = DEFAULTNEG;
      zWirePartKinProton_ajib[iZWire] = DEFAULTNEG;
      zWirePartKin_caloScaleUp[iZWire] = DEFAULTNEG;
      zWirePartKin_caloScaleDown[iZWire] = DEFAULTNEG;
      zWirePartKin_beamScaleUp[iZWire] = DEFAULTNEG;
      zWirePartKin_beamScaleDown[iZWire] = DEFAULTNEG;
    }
    PFBeamPrimdEdxs_corr.clear();
    PFBeamPrimdEdxs_ajib.clear();
    PFBeamPrimdQdxs_ajib.clear();
    PFBeamPrimKins_corr.clear();
    PFBeamPrimKinsProton_corr.clear();
    PFBeamPrimZs_corr.clear();
    PFBeamPrimZs_corrFLF.clear();

    zWireEnergySum = DEFAULTNEG;
    zWireEnergySum_corr = DEFAULTNEG;
    zWireEnergySum_ajib = DEFAULTNEG;
    zWireEnergySum_caloScaleUp = DEFAULTNEG;
    zWireEnergySum_caloScaleDown = DEFAULTNEG;
    zWireFirstHitWire = DEFAULTNEG;
    zWireLastHitWire = DEFAULTNEG;
    zWireLastContigHitWire = DEFAULTNEG;
    zWireFirstHitWireTrue = DEFAULTNEG;
    zWireLastHitWireTrue = DEFAULTNEG;
    PFBeamPrimStartZ_corr = DEFAULTNEG;
    PFBeamPrimEndZ_corr = DEFAULTNEG;
    PFBeamPrimStartZ_corrFLF = DEFAULTNEG;
    PFBeamPrimEndZ_corrFLF = DEFAULTNEG;
    PFBeamPrimKinInteract_corr = DEFAULTNEG;
    PFBeamPrimKinInteractProton_corr = DEFAULTNEG;
    PFBeamPrimEnergySum_corr = DEFAULTNEG;
    PFBeamPrimEnergySumCSDAMu = DEFAULTNEG;
    PFBeamPrimEnergySumCSDAProton = DEFAULTNEG;
    pWCCSDARangeMu = DEFAULTNEG;
    pWCCSDARangeProton = DEFAULTNEG;

    // Either got pWC from beam or from primaryParticle, so now is the time to do this
    float eWC = sqrt(pWC*pWC+MCHARGEDPION*MCHARGEDPION); // assume charged pion in MeV
    float kinWC = eWC - MCHARGEDPION; // assume charged pion in MeV
    float kinWCInTPC = kinWC - KINLOSTBEFORETPC;
                   
    // for proton
    float eWCProton = sqrt(pWC*pWC+MPROTON*MPROTON);
    float kinWCProton = eWCProton - MPROTON;
    float kinWCInTPCProton = kinWCProton - KINLOSTBEFORETPCPROTON;

    if (pWC > 0.)
    {
      pWCCSDARangeMu = muonTable.range(kinWC);
      pWCCSDARangeProton = protonTable.range(kinWCProton);
    }

    if (PFBeamPrimTrkLen > 0.)
    {
      PFBeamPrimEnergySumCSDAMu = muonTable.keFromRange(PFBeamPrimTrkLen);
      PFBeamPrimEnergySumCSDAProton = protonTable.keFromRange(PFBeamPrimTrkLen);
    }

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
          zWiredEdx_caloScaleUp[iZWire] = 1.1*dEdx;
          zWiredEdx_caloScaleDown[iZWire] = 0.9*dEdx;
          const float dQdx_ajib = ajibCorrector.calibrateCharge(zWiredQdx->at(iZWire),
                                                    zWireX->at(iZWire),
                                                    zWireY->at(iZWire),
                                                    zWireZ->at(iZWire)
                                                        );
          const float dEdx_ajib = ajibCorrector.boxChargeToEnergy(dQdx_ajib);
          zWiredEdx_ajib[iZWire] = dEdx_ajib;
          zWiredQdx_ajib[iZWire] = dQdx_ajib;
          //std::cout << "iZWire: " << iZWire << " dQdx: " << zWiredQdx->at(iZWire) << " dQdx_ajib: " << dQdx_ajib 
          //          << " dEdx: " << zWiredEdx->at(iZWire) << " dEdx_ajib: " << dEdx_ajib << std::endl;
          zWireZ_corr[iZWire] = zWireZ->at(iZWire) + sceCalibMap.at(iZWire);
          zWireZ_corrFLF[iZWire] = zWireZ->at(iZWire) + sceCalibMapFLF.at(iZWire);
          zWireLastHitWire = iZWire;
          if(lastZWireGood)
          {
            zWireLastContigHitWire = iZWire;
          }
          if(zWireFirstHitWire < 0)
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
    if(zWirePitch && zWireFirstHitWire >= 0)
    {
      zWireEnergySum = 0.;
      zWireEnergySum_corr = 0.;
      zWireEnergySum_ajib = 0.;
      zWireEnergySum_caloScaleUp = 0.;
      zWireEnergySum_caloScaleDown = 0.;
      for (long iZWire=0; iZWire <= zWireLastHitWire; iZWire++)
      {    
        zWirePartKin_corr.at(iZWire) = kinWCInTPC - zWireEnergySum_corr;
        zWirePartKinProton_corr.at(iZWire) = kinWCInTPCProton - zWireEnergySum_corr;
        zWirePartKin_ajib.at(iZWire) = kinWCInTPC - zWireEnergySum_ajib;
        zWirePartKinProton_ajib.at(iZWire) = kinWCInTPCProton - zWireEnergySum_ajib;
        zWirePartKin_caloScaleUp.at(iZWire) = kinWCInTPC - zWireEnergySum_caloScaleUp;
        zWirePartKin_caloScaleDown.at(iZWire) = kinWCInTPC - zWireEnergySum_caloScaleDown;
        zWirePartKin_beamScaleUp.at(iZWire) = kinWCInTPC*1.1 - zWireEnergySum;
        zWirePartKin_beamScaleDown.at(iZWire) = kinWCInTPC*0.9 - zWireEnergySum;
        const auto pitch = zWirePitch->at(iZWire);
        if(zWiredEdx_corr.at(iZWire) >= 0.)
        {    
          zWireEnergySum_corr += zWiredEdx_corr.at(iZWire) * pitch;
        }    
        if(zWiredEdx_ajib.at(iZWire) >= 0.)
        {    
          zWireEnergySum_ajib += zWiredEdx_ajib.at(iZWire) * pitch;
        }    
        if(zWiredEdx->at(iZWire) >= 0.)
        {    
          const auto& dEdx = zWiredEdx->at(iZWire);
          zWireEnergySum += dEdx * pitch;
          zWireEnergySum_caloScaleUp += dEdx * pitch * 1.1;
          zWireEnergySum_caloScaleDown += dEdx * pitch * 0.9;
        }    
      } // for iZWire
    } // if zWiredEdx && zWirePitch
    // Now true wires
    if(zWireTrueEnergy)
    {
      const size_t& zWireSize = zWireTrueEnergy->size();
      for (size_t iZWire=0; iZWire<zWireSize; iZWire++)
      {
        const auto& trueE = zWireTrueEnergy->at(iZWire);
        if(trueE >= 0)
        {
          zWireLastHitWireTrue = iZWire;
          if(zWireFirstHitWireTrue < 0)
          {
            zWireFirstHitWireTrue = iZWire;
          }
        }
      } // for iZWire
    } // if zWireTrueEnergy

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
          const float dEdx = PFBeamPrimdEdxs->at(iHit);
          const float dQdx_ajib = ajibCorrector.calibrateCharge(dEdx,
                                                    PFBeamPrimXs->at(iHit),
                                                    PFBeamPrimYs->at(iHit),
                                                    PFBeamPrimZs->at(iHit)
                                                        );
          const float dEdx_ajib = ajibCorrector.boxChargeToEnergy(dQdx_ajib);
          float dEdx_corr = DEFAULTNEG;
          //cout << "dEdx: " << dEdx << " iWire: " << iWire;
          if(dEdx > 0.)
          {
            //cout << " calib:  " << caloCalibMap.at(iWire);
            dEdx_corr = dEdx * caloCalibMap.at(iWire);
            //cout << " dEdx_corr:  " << dEdx_corr;
            PFBeamPrimEnergySum_corr += dEdx_corr * PFBeamPrimPitches->at(iHit);
          }
          //cout << endl;
          PFBeamPrimdEdxs_corr.push_back(dEdx_corr);
          PFBeamPrimdEdxs_ajib.push_back(dEdx_ajib);
          PFBeamPrimdQdxs_ajib.push_back(dQdx_ajib);
          PFBeamPrimZs_corr.push_back(PFBeamPrimZs->at(iHit)+sceCalibMap.at(iWire));
          PFBeamPrimZs_corrFLF.push_back(PFBeamPrimZs->at(iHit)+sceCalibMapFLF.at(iWire));
          PFBeamPrimdQdxs_ajib.push_back(dQdx_ajib);
        } // if iWire >= 0
        else
        {
          PFBeamPrimKins_corr.push_back(DEFAULTNEG);
          PFBeamPrimKinsProton_corr.push_back(DEFAULTNEG);
          PFBeamPrimdEdxs_corr.push_back(DEFAULTNEG);
          PFBeamPrimdEdxs_ajib.push_back(DEFAULTNEG);
          PFBeamPrimdQdxs_ajib.push_back(DEFAULTNEG);
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

////////////////////////////////////////
////////////////////////////////////////
////////////////////////////////////////

ChargeCorrectorAjib::ChargeCorrectorAjib(TString calibFn, double calibConst, double normFact)
    : calibFile(calibFn), calibration_constant(calibConst), normalisation_factor(normFact)
{
     X_correction_hist = (TH1F*) calibFile.Get("dqdx_X_correction_hist");
}

float ChargeCorrectorAjib::boxChargeToEnergy(float dqdx)
{
    return (exp(dqdx*(betap/(Rho*Efield)*Wion))-alpha)/(betap/(Rho*Efield)); 
}

float ChargeCorrectorAjib::calibrateCharge(float dqdx,float x, float /*y*/, float /*z*/)
{
    size_t iBin = X_correction_hist->FindBin(x);
    float result = dqdx*normalisation_factor*X_correction_hist->GetBinContent(iBin);
    result /= calibration_constant;
    return result;
}

float ChargeCorrectorAjib::calibrateddEdx(float dqdx, float x, float y, float z)
{
    float calibQ = calibrateCharge(dqdx,x,y,z);
    float result = boxChargeToEnergy(calibQ);
    return result;
}

MuonTable::MuonTable(TString infilename, float rho /*g/cm^3*/)
{
  std::string line;

  std::fstream inFile(infilename.Data(),ios_base::in);
  while (inFile.good())
  {
    std::getline(inFile,line,'\n');
    if(line.size() < 110) continue;
    if(!std::isdigit(line[2])) continue; // ensure a data line
    if(!std::isdigit(line[86])) continue; // to catch muon critical energy line
    if(line.size() < (10*8+11)) 
    {
        std::cerr << "Error: mu table file line too short\n";
        return;
    }
    //std::cout << line.substr(10*0+1,10*0+11) << std::endl;
    //std::cout << line.substr(10*7+1,10*7+11) << std::endl;
    //std::cout << line.substr(10*8+1,10*8+11) << std::endl;
    const auto& T = std::stod(line.substr(10*0+1,10*0+11));
    if (T < 1.1) continue;
    const auto& dEdx = std::stod(line.substr(10*7+1,10*7+11));
    const auto& r = std::stod(line.substr(10*8+1,10*8+11));
    
    kins.push_back(T);
    dEdxs.push_back(dEdx*rho);
    ranges.push_back(r/rho);
  }
  inFile.close();

  dEdxInterp.SetData(kins,dEdxs);
  rangeInterp.SetData(kins,ranges);
  keFromRangeInterp.SetData(ranges,kins);

  // Graph
  if (false)
  {
    TGraph dEdxsGraph;
    TGraph rangesGraph;
    TGraph keFromRangesGraph;
    dEdxsGraph.SetMarkerStyle(20);
    rangesGraph.SetMarkerStyle(20);
    keFromRangesGraph.SetMarkerStyle(20);
    dEdxsGraph.SetMarkerSize(1);
    rangesGraph.SetMarkerSize(1);
    keFromRangesGraph.SetMarkerSize(1);
    for(size_t iPoint = 0; iPoint < kins.size(); iPoint++)
    {
      const auto& T = kins.at(iPoint);
      dEdxsGraph.SetPoint(iPoint,T,dEdxs.at(iPoint));
      rangesGraph.SetPoint(iPoint,T,ranges.at(iPoint));
      keFromRangesGraph.SetPoint(iPoint,ranges.at(iPoint),T);
      //std::cout << "    " << T
      //          << "    " << dEdxs.at(iPoint)
      //          << "    " << ranges.at(iPoint)
      //          << std::endl;
    }
    TGraph dEdxsInterpGraph;
    TGraph rangesInterpGraph;
    TGraph keFromRangesInterpGraph;
    dEdxsInterpGraph.SetLineColor(kBlue);
    rangesInterpGraph.SetLineColor(kBlue);
    keFromRangesInterpGraph.SetLineColor(kBlue);
    for(size_t iPoint = 0; iPoint < 4000; iPoint++)
    {
      const double& T = iPoint;
      dEdxsInterpGraph.SetPoint(iPoint,T,dEdx(T));
      rangesInterpGraph.SetPoint(iPoint,T,range(T));
      const double& csdaRange = ((double) iPoint)*0.25;
      keFromRangesInterpGraph.SetPoint(iPoint,csdaRange,keFromRange(csdaRange));
    }
    TCanvas c("c");
    //TH2F axisHist("axisHist","",1,0.01,4e3,1,0.01,30);
    TH2F axisHist("axisHist","",1,0.01,30,1,0.01,100);
    axisHist.GetXaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist.GetYaxis()->SetTitle("Average dE/dx [MeV/cm]");
    axisHist.Draw();
    dEdxsInterpGraph.Draw("L");
    dEdxsGraph.Draw("P");
    c.SaveAs("dEdxInterp.png");
    c.SaveAs("dEdxInterp.pdf");
    c.Clear();
    //TH2F axisHist2("axisHist2","",1,0.01,2e3,1,0.01,1e3);
    TH2F axisHist2("axisHist2","",1,0.01,30,1,0.01,30);
    axisHist2.GetXaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist2.GetYaxis()->SetTitle("CSDA Range [cm]");
    axisHist2.Draw();
    rangesInterpGraph.Draw("L");
    rangesGraph.Draw("P");
    c.SaveAs("rangeInterp.png");
    c.SaveAs("rangeInterp.pdf");
    c.Clear();
    //TH2F axisHist3("axisHist3","",1,0.01,1e3,1,0.01,2e3);
    TH2F axisHist3("axisHist3","",1,0.01,8,1,0.01,100);
    axisHist3.GetXaxis()->SetTitle("CSDA Range [cm]");
    axisHist3.GetYaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist3.Draw();
    keFromRangesInterpGraph.Draw("L");
    keFromRangesGraph.Draw("P");
    c.SaveAs("keFromRangeInterp.png");
    c.SaveAs("keFromRangeInterp.pdf");
    c.Clear();
  }
}

float MuonTable::dEdx(float kin /*MeV*/) // returns MeV/cm
{
  if (kin <= kins.front())
    return dEdxs.front();
  else if (kin >= kins.back())
    return dEdxs.back();
  else
    return dEdxInterp.Eval(kin);
}

float MuonTable::range(float kin /*MeV*/) // returns cm
{
  if (kin <= kins.front())
    return ranges.front();
  else if (kin >= kins.back())
    return ranges.back();
  else
    return rangeInterp.Eval(kin);
}
float MuonTable::keFromRange(float r /*cm*/) // returns MeV
{
  if (r <= ranges.front())
    return kins.front();
  else if (r >= ranges.back())
    return kins.back();
  else
    return keFromRangeInterp.Eval(r);
}

PStarTable::PStarTable(TString infilename, float rho /*g/cm^3*/)
{
  std::string line;

  std::fstream inFile(infilename.Data(),ios_base::in);
  while (inFile.good())
  {
    std::getline(inFile,line,'\n');
    //std::cout << line << std::endl;
    if(line.size() < 74) continue;
    if(!std::isdigit(line[2])) continue; // ensure a data line
    //std::cout << line.substr(11*0+2,11) << std::endl;
    //std::cout << line.substr(11*3+2,11) << std::endl;
    //std::cout << line.substr(11*4+2,11) << std::endl;
    const auto& T = std::stod(line.substr(11*0+2,11));
    if (T < 1) continue;
    const auto& dEdx = std::stod(line.substr(11*3+2,11));
    const auto& r = std::stod(line.substr(11*4+2,11));
    
    kins.push_back(T);
    dEdxs.push_back(dEdx*rho);
    ranges.push_back(r/rho);
  }
  inFile.close();

  dEdxInterp.SetData(kins,dEdxs);
  rangeInterp.SetData(kins,ranges);
  keFromRangeInterp.SetData(ranges,kins);

  // Graph
  if (false)
  {
    TGraph dEdxsGraph;
    TGraph rangesGraph;
    TGraph keFromRangesGraph;
    dEdxsGraph.SetMarkerStyle(20);
    rangesGraph.SetMarkerStyle(20);
    keFromRangesGraph.SetMarkerStyle(20);
    dEdxsGraph.SetMarkerSize(1);
    rangesGraph.SetMarkerSize(1);
    keFromRangesGraph.SetMarkerSize(1);
    for(size_t iPoint = 0; iPoint < kins.size(); iPoint++)
    {
      const auto& T = kins.at(iPoint);
      dEdxsGraph.SetPoint(iPoint,T,dEdxs.at(iPoint));
      rangesGraph.SetPoint(iPoint,T,ranges.at(iPoint));
      keFromRangesGraph.SetPoint(iPoint,ranges.at(iPoint),T);
      //std::cout << "    " << T
      //          << "    " << dEdxs.at(iPoint)
      //          << "    " << ranges.at(iPoint)
      //          << std::endl;
    }
    TGraph dEdxsInterpGraph;
    TGraph rangesInterpGraph;
    TGraph keFromRangesInterpGraph;
    dEdxsInterpGraph.SetLineColor(kBlue);
    rangesInterpGraph.SetLineColor(kBlue);
    keFromRangesInterpGraph.SetLineColor(kBlue);
    for(size_t iPoint = 0; iPoint < 4000; iPoint++)
    {
      const double& T = iPoint;
      dEdxsInterpGraph.SetPoint(iPoint,T,dEdx(T));
      rangesInterpGraph.SetPoint(iPoint,T,range(T));
      const double& csdaRange = ((double) iPoint)*0.25;
      keFromRangesInterpGraph.SetPoint(iPoint,csdaRange,keFromRange(csdaRange));
    }
    TCanvas c("c");
    //TH2F axisHist("axisHistP","",1,0.01,4e3,1,0.01,30);
    TH2F axisHist("axisHistP","",1,0.01,3,1,0.01,1000);
    axisHist.GetXaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist.GetYaxis()->SetTitle("Average dE/dx [MeV/cm]");
    axisHist.Draw();
    dEdxsInterpGraph.Draw("L");
    dEdxsGraph.Draw("P");
    c.SaveAs("dEdxInterpProton.png");
    c.SaveAs("dEdxInterpProton.pdf");
    c.Clear();
    //TH2F axisHist2("axisHist2P","",1,0.01,2e3,1,0.01,1e3);
    TH2F axisHist2("axisHist2","",1,0.01,4,1,0.001,0.06);
    axisHist2.GetXaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist2.GetYaxis()->SetTitle("CSDA Range [cm]");
    axisHist2.Draw();
    rangesInterpGraph.Draw("L");
    rangesGraph.Draw("P");
    c.SaveAs("rangeInterpProton.png");
    c.SaveAs("rangeInterpProton.pdf");
    c.Clear();
    //TH2F axisHist3("axisHist3P","",1,0.01,1e3,1,0.01,2e3);
    //TH2F axisHist3("axisHist3","",1,0.001,0.2,1,0.01,15);
    TH2F axisHist3("axisHist3","",1,0.001,2,1,0.01,100);
    axisHist3.GetXaxis()->SetTitle("CSDA Range [cm]");
    axisHist3.GetYaxis()->SetTitle("Kinetic Energy [MeV]");
    axisHist3.Draw();
    keFromRangesInterpGraph.Draw("L");
    keFromRangesGraph.Draw("P");
    c.SaveAs("keFromRangeInterpProton.png");
    c.SaveAs("keFromRangeInterpProton.pdf");
    c.Clear();
  }
}

