# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 5/3/2021 11:19:13 AM
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl
import numpy as np
import struct
import os
#import file
import h5py

class RAW_CONV():
    def raw_conv_feedloc(self, raw_data):
        myname = 'raw_conv_feedloc: '
        smps = int(len(raw_data) //2)
        dataNtuple =struct.unpack_from(">%dH"%(smps),raw_data)
        if (self.jumbo_flag == True):
            pkg_len = int(0x1E06/2)
        else:
            pkg_len = int(0x406/2)

        feed_loc=[]
        pkg_index  = []
        datalength = int( (len(dataNtuple) // pkg_len) -3) * (pkg_len)
        data_rest = raw_data[(datalength + pkg_len)*2:]
        i = int(0)
        k = []
        j = int(0)
        smps_num = 0
        chn_data=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
        countBad = int(0)
        while (i <= datalength ):
            #print (''.join('{:04x} '.format(x) for x in dataNtuple[i:i+pkg_len]) )
            data_a =  ((dataNtuple[i+0]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1]& 0x00FFFFFFFF) + 0x0000000001
            data_b =  ((dataNtuple[i+0+pkg_len]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1+pkg_len]& 0x00FFFFFFFF)
            acc_flg = ( data_a  == data_b )
            face_flg = ((dataNtuple[i+2+6] == 0xface) or (dataNtuple[i+2+6] == 0xfeed))
            #exit()

            if (face_flg == True ) and ( acc_flg == True ) :
                pkg_index.append(i)
                pkg_start = i
                i = i + pkg_len
                onepkgdata = dataNtuple[pkg_start : pkg_start + pkg_len]
                j = 8
                peak_len = 100
                while j < len(onepkgdata) :
                    if (onepkgdata[j] == 0xface ) or (onepkgdata[j] == 0xfeed ):
                        if  (onepkgdata[j] == 0xfeed ):
                            trg_flg = 0x1000 
                        else:
                            trg_flg = 0x0000 
                        chn_data[0].append( trg_flg + ((onepkgdata[j+1] & 0XFFF0)>>4) )
                        chn_data[1].append( trg_flg + ((onepkgdata[j+1] & 0XF)<<8) + ((onepkgdata[j+2] & 0XFF00)>>8) )
                        chn_data[2].append( trg_flg + ((onepkgdata[j+2] & 0XFF)<<4) + ((onepkgdata[j+3] & 0XF000)>>12) )
                        chn_data[3].append( trg_flg + ((onepkgdata[j+3] & 0XFFF)) )

                        chn_data[4].append( trg_flg + ((onepkgdata[j+4] & 0XFFF0)>>4) )
                        chn_data[5].append( trg_flg + ((onepkgdata[j+4] & 0XF)<<8) + ((onepkgdata[j+5] & 0XFF00)>>8) )
                        chn_data[6].append( trg_flg + ((onepkgdata[j+5] & 0XFF)<<4) + ((onepkgdata[j+6] & 0XF000)>>12) )
                        chn_data[7].append( trg_flg + ((onepkgdata[j+6] & 0XFFF)) )

                        chn_data[8].append( trg_flg + ((onepkgdata[j+7] & 0XFFF0)>>4) )
                        chn_data[9].append( trg_flg + ((onepkgdata[j+7] & 0XF)<<8) + ((onepkgdata[j+8] & 0XFF00)>>8) )
                        chn_data[10].append( trg_flg + ((onepkgdata[j+8] & 0XFF)<<4) + ((onepkgdata[j+9] & 0XF000)>>12) )
                        chn_data[11].append( trg_flg + ((onepkgdata[j+9] & 0XFFF)) )

                        chn_data[12].append( trg_flg + ((onepkgdata[j+10] & 0XFFF0)>>4) )
                        chn_data[13].append( trg_flg + ((onepkgdata[j+10] & 0XF)<<8) + ((onepkgdata[j+11] & 0XFF00)>>8) )
                        chn_data[14].append( trg_flg + ((onepkgdata[j+11] & 0XFF)<<4) + ((onepkgdata[j+12] & 0XF000)>>12) )
                        chn_data[15].append( trg_flg + ((onepkgdata[j+12] & 0XFFF)) )

#                        chn_data[7].append( trg_flg + ((onepkgdata[j+1] & 0X0FFF)<<0 ))
#                        chn_data[6].append( trg_flg + ((onepkgdata[j+2] & 0X00FF)<<4)+ ((onepkgdata[j+1] & 0XF000) >> 12))
#                        chn_data[5].append( trg_flg + ((onepkgdata[j+3] & 0X000F)<<8) +((onepkgdata[j+2] & 0XFF00) >> 8 ))
#                        chn_data[4].append( trg_flg + ((onepkgdata[j+3] & 0XFFF0)>>4 ))
#
#                        chn_data[3].append( trg_flg + (onepkgdata[ j+3+1] & 0X0FFF)<<0 )
#                        chn_data[2].append( trg_flg + ((onepkgdata[j+3+2] & 0X00FF)<<4) + ((onepkgdata[j+3+1] & 0XF000) >> 12))
#                        chn_data[1].append( trg_flg + ((onepkgdata[j+3+3] & 0X000F)<<8) + ((onepkgdata[j+3+2] & 0XFF00) >> 8 ))
#                        chn_data[0].append( trg_flg + ((onepkgdata[j+3+3] & 0XFFF0)>>4) )
#
#                        chn_data[15].append(trg_flg +  ((onepkgdata[j+6+1] & 0X0FFF)<<0 ))
#                        chn_data[14].append(trg_flg +  ((onepkgdata[j+6+2] & 0X00FF)<<4 )+ ((onepkgdata[j+6+1] & 0XF000) >> 12))
#                        chn_data[13].append(trg_flg +  ((onepkgdata[j+6+3] & 0X000F)<<8 )+ ((onepkgdata[j+6+2] & 0XFF00) >> 8 ))
#                        chn_data[12].append(trg_flg +  ((onepkgdata[j+6+3] & 0XFFF0)>>4 ))
#
#                        chn_data[11].append(trg_flg +  ((onepkgdata[j+9+1] & 0X0FFF)<<0 ))
#                        chn_data[10].append(trg_flg +  ((onepkgdata[j+9+2] & 0X00FF)<<4 )+ ((onepkgdata[j+9+1] & 0XF000) >> 12))
#                        chn_data[9].append( trg_flg +  ((onepkgdata[j+9+3] & 0X000F)<<8 )+ ((onepkgdata[j+9+2] & 0XFF00) >> 8 ))
#                        chn_data[8].append( trg_flg +  ((onepkgdata[j+9+3] & 0XFFF0)>>4 ))
                        if (onepkgdata[j] == 0xfeed ):
                            feed_loc.append(smps_num)
                        smps_num = smps_num + 1
                    else:
                        pass
                    j = j + 13
            else:
                #pass
                countBad = countBad + 1
                i = i + 1
                if countBad < 10:
                  print("Wrong data at addr = {}".format(i))

        if countBad:
          print(myname, "WARNING: Wrong data error count:", countBad)
        return data_rest, chn_data

    def __init__(self):
        self.jumbo_flag = False

import sys

if __name__ == '__main__':
  myname = sys.argv[0] + ': '
  COV = RAW_CONV ()
  #ifdir = "APA_FEMB1_rawdata/"
  #ofdir = $HOME/data/dune/apa40/2021-01-05/femb1/hd5
  #pattern = "Rawdata_01_15_2021_12_06_18_RT"
  if len(sys.argv) < 3:
    print("Usage: python sys.argv[0] INDIR/BASE OUTDIR")
    sys.exit()
  dirbase = os.path.split(sys.argv[1])
  pattern = dirbase[1]
  ifdir = dirbase[0] + '/'
  for root, dirs, files in os.walk(ifdir):
    break
  ofdir = sys.argv[2] + '/'


  hdfsav=''
  for afile in files:
    #print(myname, "Checking", afile)
    if (pattern in afile)  and (".bin" in afile):
        fn = ifdir + afile
        fembno = int( afile[afile.find("FEMB")+4] )
        asicno = int( afile[afile.find("ASIC")+4] )
        fsize = (os.path.getsize(fn))
        slice_n = 100000
        tmp1 = afile.find(pattern)
        tmp2 = afile.find("_FEMB")
        hdf = ofdir + afile[tmp1:tmp2] + ".h5"
        if len(hdfsav):
          if hdf != hdfsav:
            print(myname, "ERROR: Output file name mismatch:", hdf)
            sys.exit()
        else:
          hdfsav = hdf
          print(myname, "Output file:", hdf)
        print(myname, "Converting", fn)
        with h5py.File(hdf, "a") as f:
            with open(fn, "rb") as fp:
                for i in range((fsize//slice_n)-2):
                    if i == 0:
                        Rawdata = fp.read(slice_n)
                    else:
                        Rawdata = fp.read(slice_n)
                        Rawdata = data_rest + Rawdata

                    data_rest, chn_data= COV.raw_conv_feedloc(Rawdata)

                    if i == 0:
                        dset = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
                        for j in range(16):
                            dset[j] = f.create_dataset('CH{}'.format(fembno*128 + asicno*16 + j), (len(chn_data[j]),), maxshape=(None,), dtype='u2', chunks=True)
                            dset[j][:] = chn_data[j]
                    else:
                        for j in range(16):
                            ll = len(chn_data[j])
                            dset[j].resize(dset[j].shape[0]+ll, axis=0)
                            dset[j][-ll:] = chn_data[j]



