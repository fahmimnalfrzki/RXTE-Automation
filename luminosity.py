#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 18:35:47 2019

@author: fahmi
"""
import numpy as np
from matplotlib.pyplot import*
from scipy import stats
import astropy.units as u
import astropy.constants as co
import pandas as pd

nama_obj='CygX-1'

home='/home/fahmi/rxteotomasi'
folder='/home/fahmi/Documents/data/'+nama_obj+'/RXTE/'

dat=np.genfromtxt('/home/fahmi/Documents/data/'+nama_obj+'/'+nama_obj+'.tsv',skip_header=1,delimiter=' ')
dat=np.transpose(dat)

flux=dat[14]
Tin=dat[1]*u.keV
b=Tin.to(u.K,equivalencies=u.temperature_energy())
d=1.86*u.kpc.to(u.cm)
lum=(flux*4*np.pi* d**2)

tbl=pd.DataFrame({'Tin':Tin,'Luminositas':lum,'logT':np.log(Tin.value),'logL':np.log(lum)})
loglum=tbl[(tbl.logT >-1) & (tbl.logL > 82.75)].logL
logtin=tbl[(tbl.logT > -1) & (tbl.logL > 82.75)].logT
sb=co.sigma_sb.decompose(u.cgs.bases)
Rin=np.sqrt(lum/(4*np.pi*sb* (b.value)**4))
gradient,intercept,r_value,p_value,std_err=stats.linregress(logtin,loglum)

R=np.sqrt((10**intercept)/(4*np.pi*sb))

fig=figure(0)
f=fig.add_subplot(111)
f.scatter(logtin,loglum)
f.plot(logtin,gradient*logtin+intercept,color='red')
#f.errorbar(x=soft,y=hard,xerr=soft_err,yerr=hard_err,fmt='o',color='black', ecolor='lightgray',capsize=0)
#f.set_ylim(82.5,83)
#f.set_xlim(-0.7,0.7)
f.set_xlabel('log(Tin) (keV)')
f.set_ylabel('log(L)')
f.set_title('Diagram Tin vs Luminositas '+nama_obj)

