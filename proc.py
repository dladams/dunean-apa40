import sys
import h5py
from runfiles import runfiles

# Read command line
dbg = 1
maxcha = -1
samRange = "all"
chanoff = 128
myname = sys.argv[0] + ": "
narg = len(sys.argv)
if narg < 3:
  print("Usage: python " + sys.argv[0] + " PROC RUN [MAXSAM] [DBG]")
  print("  PROC = dqm to create DQM plots")
  print("         caltree to create ROI tree at ADC scale")
  print("         calib to create charge calibration histograms")
  exit()

# Import dunetpc components.
import cppyy
from cppyy.gbl import AdcChannelData
from cppyy.gbl import AdcChannelDataMap
from cppyy.gbl import AdcChannelTool
from cppyy.gbl import ArtServiceHelper
from cppyy.gbl import DuneToolManager
from cppyy.gbl import IndexMapTool
from cppyy.gbl import DataMap

def shapingTime(irun):
  if irun == 1004: return 2
  if irun == 1015: return 2
  if irun == 1020: return 2
  return 1

proc = sys.argv[1]
irun = int(sys.argv[2])
isam1 = 0
isam2 = 0
if narg > 3:
  samRange = sys.argv[3]
  lims = samRange.split("-")
  if len(lims) == 1:
    isam1 = 0
    isam2 = int(lims[0])
  elif len(lims) == 2:
    isam1 = int(lims[0])
    isam2 = int(lims[1])
if narg > 4:
  dbg = int(sys.argv[4])
print(myname + "Process: ", proc)
print(myname + "Run: ", irun)
print(myname + "Sample range: ", samRange)
print(myname + "Log level", dbg)

# Find the run data.
try:
  fnam = runfiles[irun]
except:
  print(myname + "ERROR: Run not found:", irun)
  exit()
print(myname + "Run " + str(irun) + ": " + fnam)
if not h5py.is_hdf5(fnam):
  print(myname + "ERROR: Input file is not hd5.")
  exit()

# Load services.
print(myname, "******* Loading services.")
ArtServiceHelper.load("./load.fcl")

# Load tools.
try:
  dtm = DuneToolManager.instance("./load.fcl")
except Exception as e:
  print(e)
  exit(1)
print(myname, "******* Finding tools.")
# DQM plots: channel-tick displaye and metrics vs. channel
scalePos = -1
if proc == "dqm":
  tnams = [
    'adcPedestalFitPlot',
    'femb_adcChannelPedestalPlotter',
    'femb_adcChannelPedestalNoisePlotter',
    'femb_adcChannelPedestalRawRmsPlotter',
    'femb_adcChannelPedestalOrfPlotter',
    'femb_adcChannelPedestalPeakBinExcessPlotter',
    'femb_adcChannelPedestalRawTailPlotter',
    'femb_adcChannelPedestalReducedChiSquarePlotter',
    'rawAdcPlotter'
  ]
# ROI tree at ADC scale for hand calibration.
elif proc == "caltree":
  tnams = [
    'adcPedestalFit',
    'adcSampleFiller',
    'adcThresholdSignalFinder',
    'adcRoiTreeMaker'
  ]
# Run calibration tool to create input for automatic calibration.
elif proc == "calib":
  tnams = [
    'adcPedestalFit',
    'adcSampleFiller',
    'adcCalibSignalFinderPos',
    'adcRoiFitter'
  ]
elif proc == "dftpow":
  tnams = [
    'adcPedestalFit',
    'sampleCalibration',
    'adcSplit1000',
    'adcFFT',
    'adcPlotDftTickPower'
  ]
  scalePos = 2
else:
  print(myname, "ERROR: Invalid proc:", proc)
  exit()
# Add scale factor
if scalePos >= 0:
  if shapingTime(irun) == 2:
      tnams.insert(scalePos, "scale1usTo2us")
tools = { }
for tnam in tnams:
  print(myname + "Fetching tool", tnam)
  tools[tnam] = dtm.getShared[AdcChannelTool](tnam)
  print(myname, "Fetched tool", tnam, ":", tools[tnam], cppyy.addressof(tools[tnam]))
  if not cppyy.addressof(tools[tnam]):
    print(myname, "ERROR: Unable to find tool", tnam)
    sys.exit(2)
chanStatTool = dtm.getShared[IndexMapTool]('channelStatusFromService')

# Build channel data.
df = h5py.File(fnam)
#print(len(df))
#print(df)
acds = AdcChannelDataMap()
ievt = 0
ncha = 0
for sch in df:
  ncha = ncha + 1
  if maxcha >= 0 and ncha > maxcha:
    if dbg > 0: print(myname + "INFO: Skipping channel", icha, "and beyond")
    break
  icha = int(sch[2:])
  if icha < chanoff:
    print(myname + "ERROR: Channel below channel offset:", icha, "<", chanoff)
    exit()
  icha = icha - chanoff
  if isam2 > isam1:
    dat = df[sch][isam1:isam2]
  else:
    dat = df[sch][:]
  #print(" ", sch, len(dat), dat)
  if dbg > 2: print(myname, "  Channel", icha);
  acds[icha].setEventInfo(irun, ievt);
  status = chanStatTool.get(icha)
  acds[icha].setChannelInfo(icha, ievt, icha, status);
  acds[icha].raw = dat
  nsam = acds[icha].raw.size()
  acds[icha].flags.resize(nsam, 0)
  if dbg > 2: print(myname, "    NRaw:", acds[icha].raw.size())
if dbg > 0: print(myname + "Channel count:", acds.size())
# Run tools
for tnam, tool in tools.items():
  if dbg > 1: print(myname, "  Calling tool", tnam)
  ret = tool.updateMap(acds)
  if dbg > 1: print(ret)
# Delete tools.
# If we wait for C++ closeout, then ROOT may delete objects that
# are needed in these dtors.
for tnam, tool in tools.items():
  if dbg > 1: print(myname, "  Deleting tool", tnam)
  dtm.deleteShared(tnam)
  


