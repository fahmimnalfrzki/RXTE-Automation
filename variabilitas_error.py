#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:26:58 2019

@author: fahmi
"""

import numpy as np
import matplotlib.pyplot as pl
import os,glob
import string,random
from astropy.io import fits
from astropy.time import Time

nama_obj='CygX-1'
folder='E:/data/'+nama_obj+'/'
data=np.genfromtxt(folder+nama_obj+'_swift.tsv',skip_header=1,dtype=str)
data=np.transpose(data)
t=[]
soft=[]
hard=[]
allf=[]
bb=[]
Tin=[]
po=[]
kombb=[]
errs=[]
errh=[]
errall=[]
errk=[]
errbb=[]
#rxte=data[0][i][:-5]

for i in range(len(data[0])):
    os.chdir(folder+'Swift/'+data[0][i]+'/xrt/event/')
    pca=fits.open(data[0][i]+'_wt_grp.pha')
    t.append(pca[1].header['DATE-OBS'])
    time=Time(t,format='isot')
    mjdt=time.mjd
    soft.append(float(data[20][i]))
    hard.append(float(data[22][i]))
    allf.append(float(data[14][i]))
    Tin.append(float(data[1][i]))
    po.append(float(data[3][i]))
    kombb.append((float(data[16][i])/float(data[14][i]))*100)
    errs.append(float(data[21][i]))
    errh.append(float(data[23][i]))
    errall.append(float(data[15][i]))
    errbb.append(float(data[17][i]))
    bb.append(float(data[16][i]))

err=np.sqrt(100*(1/np.array(allf) *np.array(errbb))**2 +100*(-np.array(bb)/(np.array(allf)**2) *np.array(errall))**2)
    
f,ax=pl.subplots(3,sharex=True)
f1,ax1=pl.subplots(3,sharex=True)
ax[0].errorbar(mjdt,soft,yerr=errs,fmt='.')
ax[1].errorbar(mjdt,hard,yerr=errh,fmt='.')
ax[2].errorbar(mjdt,allf,yerr=errall,fmt='.')
ax1[0].scatter(mjdt,Tin,marker='.')
ax1[1].scatter(mjdt,po,marker='.')
ax1[2].errorbar(mjdt,kombb,yerr=err,fmt='.')
ax[0].set_ylabel('soft')
ax[1].set_ylabel('hard')
ax[2].set_ylabel('flux (3.0-20.0 keV)')
ax1[0].set_ylabel('Tin (keV)')
ax1[1].set_ylabel('Photon Index')
ax1[2].set_ylabel('Komponen Termal (%)')
ax1[2].set_xlabel('MJD')
ax[0].set_title('Variabilitas Obs id RXTE '+nama_obj)
#ax[2].set_ylim(1e-12,2e-8)

os.chdir('E:/swiftomasi')
pl.savefig('variabilitas '+nama_obj)