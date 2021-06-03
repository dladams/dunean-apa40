// makeFembCalibData.C
//
// David Adams
// May 2021
//
// Define the default function that defines femb datasets.

const AdcCalibData* makeAdcCalibData(string samName, string crNameIn, bool checkFile) {
  using Name = std::string;
  using Index = unsigned int;
  using IndexVector = vector<Index>;
  Name myname = "makeAdcCalibData: ";
  Name crName = crNameIn;
  const AdcCalibData* pcad = AdcCalibData::get(samName, crNameIn);
  if ( pcad != nullptr ) return pcad;
  using RunMap = std::map<int, IndexVector>;   // Runs indexed by pulser gain
  RunMap runMap;
  string basedir = "data";
  bool skipMissingFiles = false;
  Name crNameDefault = "all";
  StringManipulator sman(samName, false);
  vector<string> fields = sman.split("-");
  if ( fields.size() > 2 ) {
    cout << "Invalid sample name: " << samName << endl;
    return nullptr;
  }
  string dstName = fields[0];
  Name dirName = dstName.substr(0,12);
  vector<string> subdsts;
  if ( dstName == "XXX" ) {
    subdsts.push_back("XXX12");
    subdsts.push_back("XXXX2");
  } else {
    subdsts.push_back(dstName);
  }
  vector<string> ssgns = {"pos"};
  for ( string subName : subdsts ) {
    // 14 mV/fC, 1.0 us, 200 mV, ? pA
    if ( subName == "apa40_202101g2s1b2" ) {
      runMap[ 8].push_back(1010);
      runMap[ 4].push_back(1011);
      runMap[12].push_back(1012);
      runMap[ 8].push_back(1018);
    } else if ( subName == "apa40_202101g2s1b2lo" ) {
      runMap[ 8].push_back(1010);
      runMap[ 4].push_back(1011);
      runMap[ 8].push_back(1018);
    } else if ( subName == "apa40_202101g2s1b2one" ) {
      runMap[ 8].push_back(1010);
      runMap[ 8].push_back(1018);
    }
  }
  if ( runMap.size() == 0 ) {
    cout << myname << "Dataset not found: " << dstName << endl;
    return pcad;
  }
  if ( crName == "" || crName == "." ) crName = crNameDefault;
  AdcCalibData* pcadMut = AdcCalibData::create(dstName, crName);
  pcad = pcadMut;
  if ( pcad == nullptr ) {
    cout << myname << "Unable to create calib data: " << samName << " " << crName << endl;
    return pcad;
  }
  for ( RunMap::value_type arun : runMap ) {
    int ia = arun.first;
    for ( unsigned int run : arun.second ) {
      string srun = to_string(run);
      while ( srun.size() < 6 ) srun = "0" + srun;
      string fnamBase = basedir + "/" + dirName + "/" + crName + "/roicha" + srun;
      for ( string ssgn : ssgns ) {
        int isign = ssgn == "pos" ? 1 : -1;
        string fnam = fnamBase + ssgn + ".root";
        bool addFile = true;
        if ( checkFile ) {
          bool fileExists = ! gSystem->AccessPathName(fnam.c_str());
          addFile = fileExists;
        }
        if ( addFile ) pcadMut->add(isign*ia, run, fnam);
        else if ( skipMissingFiles ) cout << myname << "Skipping missing file: " << fnam <<endl;
        else {
          cout << myname << "Unable to find " << fnam << endl;
          return nullptr;
        }
      }
    }
  }
  pcad->print();
  return pcad;
}
