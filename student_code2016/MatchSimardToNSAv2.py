#!/usr/bin/python
# coding: utf-8

# Goal:  
# Combine the NSAYang catalog with the Simard catalog to include sersic fits
# 
# Required Files:
# * The NASA Sloan Atlas catalog (nsa_v0_1_2.fits) found here http://www.nsatlas.org/data
# * asu.fit
# 
# Obtaining asu.fit:
# 1. http://vizier.cfa.harvard.edu/viz-bin/VizieR?-source=J/ApJS/196/11
# 2. Check all boxes and click "Join selected tables"
# 3. Scroll down and check "ALL col" then uncheck "All", "Sloan", and "DR7"
# 4. Click any of the submit buttons
# 5. On the left in the "Preferences" box change "max" to unlimited, "HTML Table" to "FITS (ascii) table, and then click submit
# 
# Notes:
# * All entries in asu.fit are strings. Can be changed to floats using np.astype(np.float32)


#import csv
import numpy as np
from astropy.io import fits
import fnmatch
import time
import argparse


def findnearest(x1,y1,x2,y2,delta):
    matchflag=1
    nmatch=0
    d=np.sqrt((x1-x2)**2 + (y1-y2)**2)
    index=np.arange(len(d))
    t=index[d<delta]
    matches=t
    if len(matches) > 0:
        nmatch=len(matches)
        if nmatch > 1:
            imatch=index[(d == min(d[t]))]
        else:
            imatch=matches[0]
    else:
        imatch = 0
        matchflag = 0

    return imatch, matchflag,nmatch


parser = argparse.ArgumentParser(description ='Match the NSA catalog with the Simard catalogs')
parser.add_argument('--s', dest = 's', default = False, action = 'store_true', help = 'Use shortened version of NSA catalog (nsa_uat.fits)')
args = parser.parse_args()


asu1 = fits.getdata('asu.fit',1)
asu2 = fits.getdata('asu.fit',2)
asu3 = fits.getdata('asu.fit',3)
if arg.s:
    nsadat = fits.getdata('nsa_uat.fits')
else:
    nsadat = fits.getdata('nsa_v0_1_2.fits')


for i in range(len(asu1._DE)):
    asu1._DE[i] = asu1._DE[i].rstrip("\r").rstrip("+")
    

matchRadius=0.1/3600
start_time = time.time()
imatch=np.zeros(len(nsadat.RA),'i')
matchflag=np.zeros(len(nsadat.RA),'bool')
nmatch=np.zeros(len(nsadat.RA),'i')
RA = asu1._RA.astype(np.float32)
DEC = asu1._DE.astype(np.float32)
for i in range(len(nsadat.RA)):
    t = findnearest(nsadat.RA[i],nsadat.DEC[i],RA,DEC,matchRadius)
    try:
        imatch[i],matchflag[i],nmatch[i]  =  t
    except ValueError:
        print t
        d1 = abs(nsadat.Z[i] - asu1.z[t[0][0]].astype(np.float32))
        d2 = abs(nsadat.Z[i] - asu1.z[t[0][1]].astype(np.float32))
        if d1 < d2:
            imatch[i],matchflag[i],nmatch[i] = t[0][0],t[1],t[2]
        else:
            imatch[i],matchflag[i],nmatch[i] = t[0][1],t[1],t[2]
print "Done matching"  
print("--- %s seconds ---" % (time.time() - start_time))
if arg.s:
    outfile='Simard1ToNSA_uat.fits'
else:
    outfile='Simard1ToNSA.fits'
matchedarray1=np.zeros(len(nsadat),dtype=asu1.dtype)
matchedarray1[matchflag] = asu1[imatch[matchflag]]
new1 = []
for i in range(len(matchedarray1)): # row
    for j in range(len(matchedarray1[0])): #column
        if len(new1)<62:
            new1.append([])
        new1[j].append(matchedarray1[i][j])
headers1 = asu1.names
i = 0
cols = []
for n in headers1:
    colnum = fits.Column(name=n,format='A10',array=new1[i])
    cols.append(colnum)
    i = i+1
newcol = fits.ColDefs(cols)
hdu = fits.BinTableHDU.from_columns(newcol)
hdu.writeto(outfile,clobber=True)

if arg.s:
    outfile='Simard2ToNSA_uat.fits'
else:
    outfile='Simard2ToNSA.fits'
matchedarray2=np.zeros(len(nsadat),dtype=asu2.dtype)
matchedarray2[matchflag] = asu2[imatch[matchflag]]
new2 = []
for i in range(len(matchedarray2)): # row
    for j in range(len(matchedarray2[0])): #column
        if len(new2)<62:
            new2.append([])
        new2[j].append(matchedarray2[i][j])
headers2 = asu2.names
i = 0
cols = []
for n in headers2:
    colnum = fits.Column(name=n,format='A10',array=new2[i])
    cols.append(colnum)
    i = i+1
newcol = fits.ColDefs(cols)
hdu = fits.BinTableHDU.from_columns(newcol)
hdu.writeto(outfile,clobber=True)

if arg.s:
    outfile='Simard3ToNSA_uat.fits'
else:
    outfile='Simard3ToNSA.fits'
matchedarray3=np.zeros(len(nsadat),dtype=asu3.dtype)
matchedarray3[matchflag] = asu3[imatch[matchflag]]
new3 = []
for i in range(len(matchedarray3)): # row
    for j in range(len(matchedarray3[0])): #column
        if len(new3)<62:
            new3.append([])
        new3[j].append(matchedarray3[i][j])
headers3 = asu3.names
i = 0
cols = []
for n in headers3:
    colnum = fits.Column(name=n,format='A10',array=new3[i])
    cols.append(colnum)
    i = i+1
newcol = fits.ColDefs(cols)
hdu = fits.BinTableHDU.from_columns(newcol)
hdu.writeto(outfile,clobber=True)
print "Done"
print("--- %s seconds ---" % (time.time() - start_time))