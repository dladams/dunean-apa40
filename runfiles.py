import os

runfiles = {}

finnams = ['/nashome/d/dladams/data/dune/apa40/2021-01-05/femb1/hd5/runs.dat']
for finnam in finnams:
  sdir = os.path.split(finnam)[0]
  fin = open(finnam, 'r')
  while True:
    line = fin.readline()
    if len(line) == 0: break
    line = line[0:len(line)-1]
    words = line.split()
    irun = int(words[0])
    fnam = words[1]
    runfiles[irun] = sdir + "/" + fnam
  
if __name__ == '__main__':
  import sys
  if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == 'html':
      fnam = "/nashome/d/dladams/wwwdune/protodune/femb/apa40/2021-01/runs/index.html"
      out = open(fnam, 'w')
      out.write('<html>\n');
      out.write('<style>\n');
      out.write('th { text-align: left; }\n');
      out.write('</style>\n');
      out.write('<table>\n')
      out.write('<caption>BNL APA40 data, Jan 2021</caption>\n')
      out.write('<tr><th>Run</th><th>File</th></tr>\n')
      for run in runfiles.keys():
        fil = runfiles[run]
        out.write('<tr><td>'+str(run)+'</td><td>'+fil+'</td></tr>\n')
      out.write('</table>\n')
      out.write('</html>\n');
      print("Wrote", fnam)
    elif arg == 'print':
      for run in runfiles.keys():
        print(str(run) + ": " + runfiles[run])
    else:
      irun = int(sys.argv[1])
      if irun in runfiles.keys():
        print(runfiles[irun])
