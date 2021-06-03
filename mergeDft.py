import sys
import glob
import math

myname = "mergeDft:"

if len(sys.argv) < 2:
  print("Usage: python mergeDft.py RUN")
  exit()

irun = sys.argv[1]
srun = str(irun)
sfrun = srun
while len(sfrun) < 6: sfrun = '0' + sfrun
print(myname, "Processing run", irun)

ymax = 1000
if len(sys.argv) > 2:
  ymax = float(sys.argv[2])
symax = str(int(ymax + 0.01))
while len(symax) < 4: symax = '0' + symax

from apa40ChanMap import getApa40ChannelsMap
import cppyy
from cppyy.gbl import TPadManipulator
from cppyy.gbl import TH1F
from cppyy.gbl import ArtServiceHelper
from cppyy.gbl import DuneToolManager
from cppyy.gbl import IndexMapTool
from cppyy.gbl import TLatex

sfrun = srun
while len(sfrun) < 6: sfrun = '0' + sfrun
snsam = '1000000'
dir = 'procrun/dftpow/run' + sfrun + '/maxsam' + snsam;
pat = dir + '/dftpowt_run' + sfrun + '_evt000000_ch*.tpad'
fnams = glob.glob(pat)
if len(fnams) == 0:
  print(myname, "No tpad files match pattern", pat)
  exit()
fout = "dftpow_run" + sfrun + '_ymax' + symax + ".{png,tpad}"
dbg = 3

# Load services.
print(myname, "******* Loading services.")
ArtServiceHelper.load("./load.fcl")

# Load tools.
try:
  dtm = DuneToolManager.instance("./load.fcl")
except Exception as e:
  print(e)
  exit(1)

print(myname, 'Retrieving channel status tool.')
chanStatTool = dtm.getShared[IndexMapTool]('channelStatusFromService')
if False:
  for icha in range(128):
    print(myname, icha, chanStatTool.get(icha))
  exit()

chmap = getApa40ChannelsMap()
phmap = { }
nchmap = { }
for fnam in fnams:
  print(myname)
  print(myname, 'Reading', fnam)
  topman = TPadManipulator.read(fnam);
  if topman == cppyy.nullptr:
    print(myname, "ERROR: Unable to read", fnam)
    exit()
  print(myname, 'Opened tpad file.')
  for iman in range(topman.npad()):
    man = topman.man(iman)
    ph = man.hist()
    if ph == cppyy.nullptr:
      print(myname, "WARNING: No histogram found")
    else:
      hnam = ph.GetName()
      sfcha = hnam[len(hnam)-5:]
      while len(sfcha) > 1 and sfcha[0] == '0': sfcha = sfcha[1:]
      icha = int(sfcha)
      chstat = chanStatTool.get(icha)
      chori = ''
      if chstat:
        print(myname, "Keeping channel", icha, " with status ", chstat)
        chori = 'o'
      else:
        for sori in ['x', 'u', 'v']:
          if icha in chmap[sori]: chori = sori
      if len(chori) != 1:
        print(myname, "Orientation not found for channel", icha)
        for sori in ['x', 'u', 'v']:
          print(sori, ":", chmap[sori], "len:", len(chmap[sori]))
        exit()
      print(myname, "Using histogram", hnam, "for channel", icha)
      if not chori in phmap:
        hnam = hnam[0:len(hnam)-7] + chori
        print(myname, "Creating histogram", hnam)
        phmap[chori] = ph.Clone(hnam)
        nchmap[chori] = 1
      else:
        phmap[chori].Add(ph)
        nchmap[chori] += 1
for sori in phmap:
  print(myname, " ", phmap[sori].GetName(), nchmap[sori])
  phmap[sori].Scale(1.0e6/nchmap[sori])
  phmap[sori].GetYaxis().SetTitle('Power/tick/channel [e^{2}]')
      
man = TPadManipulator(1400, 1000)
manhists = { 0:'x', 1:'u', 2:'o', 3:'v' }
man.split(2,2)
lapa40 = 2800
lib = 952
#ymax = lapa40/lib*300
font = 42
tsiz = 0.05
for iman in manhists:
  sori = manhists[iman]
  pwr = phmap[sori].Integral()
  snoi = str(int(math.sqrt(pwr)+0.499))
  print(myname, "noise for", sori+":", snoi, "e")
  man.man(iman).add(phmap[sori], "hist")
  man.man(iman).setRangeY(0, ymax)
  man.man(iman).setRangeX(0, 1000)
  xlab = 0.7
  ylab = 0.73
  txt = TLatex(xlab, ylab, "#sqrt{#Sigma} = " + snoi + " e")
  txt.SetNDC()
  txt.SetTextFont(font)
  man.man(iman).add(txt)
  txt.Print()
  ylab = 0.55
  txt = TLatex(xlab, ylab, "BNL 40% APA")
  txt.SetNDC()
  txt.SetTextFont(font)
  man.man(iman).add(txt)
  ylab -= 0.06
  if sori == 'o':
    txt = TLatex(xlab, ylab, "Open wires")
  else:
    txt = TLatex(xlab, ylab, sori.capitalize() + " wires")
  txt.SetNDC()
  txt.SetTextFont(font)
  man.man(iman).add(txt)
  ylab -= 0.06
  txt = TLatex(xlab, ylab, "Run " + srun)
  txt.SetNDC()
  txt.SetTextFont(font)
  man.man(iman).add(txt)
  man.man(iman).addAxis()
  man.man(iman).setLabelSizeX(tsiz)
  man.man(iman).setLabelSizeY(tsiz)
  man.man(iman).setTitleSize(tsiz)
  man.man(iman).setMarginLeft(0.14)
  man.man(iman).setMarginTop(0.05)
  man.man(iman).setMarginBottom(0.12)
  man.man(iman).centerAxisTitles()
  man.man(iman).hist().SetLineWidth(2)
#h = TH1F("h1", "My histo", 10, 0, 10)
#padin = TPadManipulator.read("dftin.tpad")
#h = padin.hist()
#print(myname, h.GetName());
#man.add(h)
print(myname, "Printing", fout)
man.print(fout)
