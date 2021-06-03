THis is data taken January 2021 with the 40% APA at BNL using
the 3-ASIC FEMBs later used in Iceberg 5.

Post DQM plots.
> ./proc dqm 1010 200000

Calibration
> ./doCalib DST FIT
DST is the dataset name. See ./makeFembCalibData.C.
FIT is the fit flag. See doCalib.

Conclusion is fit varying pedestal is best.
This requires two or more DAC settings which we only have
for g2s1b2.
There is more spread in gains (3.3% vs 2.1%) if all three DAC
settings (4, 8, 12) are are used instead of just two.
Adopt the latter for calibration: 
  tools.areaGain_apa40_202101g2s1b2lo_v03

To make DFT power plots for each channel:
> ./proc dftpow 1013 1000000

To construct a summary DFT power plot
python mergeDft.py 1013
