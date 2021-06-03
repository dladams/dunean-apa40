{
  string loadfcl = "load.fcl";
  if ( gSystem->Getenv("ROOTFCL") != nullptr ) {
    loadfcl = gSystem->Getenv("ROOTFCL");
  }
  cout << "Fcl loaded from " << loadfcl << endl;
  gROOT->ProcessLine("ArtServiceHelper::load(loadfcl)");
  gROOT->ProcessLine("DuneToolManager* ptm = DuneToolManager::instance(loadfcl)");
  gROOT->ProcessLine(".L makeFembCalibData.C");
  gROOT->ProcessLine(".L $DUNECECALIB_DIR/root/calib.C");
  gROOT->ProcessLine(".L $DUNECECALIB_DIR/root/doCalib.C");
  gROOT->ProcessLine(".L $DUNECECALIB_DIR/root/calplots.C");
  gROOT->ProcessLine(".L $DUNECECALIB_DIR/root/drawGainDist.C");
}
