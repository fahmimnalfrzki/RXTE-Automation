#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 23:57:00 2019

Fitting Simultan RXTE dan Swift

@author: fahmi
"""

from xspec import*
import os,glob,shutil,sys
import numpy as np
from astropy.io import fits
from matplotlib.pyplot import*

nama_obj='CygX-1'
NH=0.781

home='/home/fahmi/Documents/data/'+nama_obj
rxte='/home/fahmi/Documents/data/'+nama_obj+'/RXTE/'
swift='/home/fahmi/Documents/data/'+nama_obj+'/Swift/'
simul='/home/fahmi/Documents/data/'+nama_obj+'/simultan/'
robsid=os.listdir(rxte)
sobsid=os.listdir(swift)

for i in range(len(robsid)):
    for j in range(len(glob.glob(rxte+robsid[i]+'/'
                                 +robsid[i]+'_16_*_grp.pha'))):
        shutil.copy2(rxte+robsid[i]+'/'+robsid[i]+'_16_'
                     +str(j)+'_grp.pha',simul)
        shutil.copy2(rxte+robsid[i]+'/'+'bkg_'+robsid[i]
        +'_16_'+str(j)+'_rbn_grp.pha',simul)
    shutil.copy2(rxte+robsid[i]+'/'+'res_'+robsid[i]+'.rsp',simul)

for i in range(len(sobsid)):
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'+sobsid[i]
    +'_wt_20_grp.pha',simul)
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'
                 +'bkg'+sobsid[i]+'_wt_20_grp.pha',simul)
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'+sobsid[i]+'_wt_exp.arf',simul)
    shutil.copy2(glob.glob(swift+sobsid[i]+'/xrt/event/'+'*.rmf')[0],simul)


os.chdir(simul)
irisan=[[],[],[],[]]
ctr1=[[],[]]
ctr2=[[],[]]
Tin=[]
norm_dbb=[]
PhotIn=[[],[]]
norm_po=[[],[]]
rcs=[]
flux=[[],[],[],[]]
fluxall=[]
fluxbb=[]

for i in range(len(robsid)):
    for k in range(len(sobsid)):
        pca=fits.open(robsid[i]+'_16_0_grp.pha')
        xrt=fits.open(sobsid[k]+'_wt_20_grp.pha')
        t1=pca[1].header['DATE-OBS']
        t2=xrt[1].header['DATE-OBS']
        if t1.split('T')[0]==t2.split('T')[0]:
            irisan[0].append(robsid[i])
            irisan[1].append(sobsid[k])
            irisan[2].append(t1)
            irisan[3].append(t2)

for i in range(len(irisan[0])):
    for k in range(len(glob.glob(irisan[0][i]+'*_grp.pha'))):
        s1=Spectrum(irisan[1][i]+'_wt_20_grp.pha')
        s2=Spectrum(irisan[0][i]+'_16_'+str(k)+'_grp.pha')
        s1.ignore('0.0-0.3,10.0-**')
        s2.ignore('0.0-3.0,20.0-**')
        ctr1[0].append(s1.rate[0])
        ctr1[1].append(s1.rate[1])
        ctr2[0].append(s2.rate[0])
        ctr2[1].append(s2.rate[1])
    
        m1=Model('TBabs*const*smedge*(diskbb+po+gauss)')
        AllData('1:1 '+irisan[1][i]+'_wt_20_grp.pha'+' 2:1 '+irisan[0][i]
        +'_16_'+str(k)+'_grp.pha')
        m2=AllModels(2)
        c1_1=m1.TBabs
        c2_1=m1.constant
        c3_1=m1.smedge
        c4_1=m1.diskbb
        c5_1=m1.powerlaw
        c6_1=m1.gaussian
        
        c2_2=m2.TBabs
        c2_2=m2.constant
        c3_2=m2.smedge
        c4_2=m2.diskbb
        c5_2=m2.powerlaw
        c6_2=m2.gaussian
        
        c1_1.nH.values=NH
        c2_1.factor=1.
        c3_1.edgeE.values=7.1
        c6_1.LineE.values=6.4

        c1_1.nH.frozen=True
        c2_1.factor.frozen=True
        c3_1.edgeE.frozen=True
        c6_1.LineE.frozen=True

        c2_2.factor=1.
        c5_2.PhoIndex=1.4
        c5_2.norm=1.
        Fit.query='yes'
        Fit.perform()
        Fit.show()
        
        Fit.steppar('7 0.0 1.5 50')
        Fit.steppar('9 0.5 2. 50')
        Fit.steppar('22 0.5 2. 50')
        
        Tin.append(c4_1.Tin.values[0])
        norm_dbb.append(c4_1.norm.values[0])
        PhotIn[0].append(c5_1.PhoIndex.values[0])
        norm_po[0].append(c5_1.norm.values[0])
        PhotIn[1].append(c5_2.PhoIndex.values[0])
        norm_po[1].append(c5_2.norm.values[0])
        rcs.append(Fit.statistic/Fit.dof)
        
        c1_1.nH.values=0
        
        AllModels.calcFlux("3.0 4.0")
        flux[0].append(Spectrum.flux[0])
        AllModels.calcFlux("4.0 6.4")
        flux[1].append(Spectrum.flux[0])
        AllModels.calcFlux("6.4 9.7")
        flux[2].append(Spectrum.flux[0])
        AllModels.calcFlux("9.7 16.0")
        flux[3].append(Spectrum.flux[0])
        AllModels.calcFlux("3.0 20.0")
        fluxall.append(Spectrum.flux[0])
        
        c5_1.norm.values=0
        c5_2.norm.values=0
        
        AllModels.calcFlux("3.0 20.0")
        fluxbb.append(Spectrum.flux[0])
        
        AllModels.clear()
        AllData.clear()
        
        print(irisan[1][i]+'_wt_20_grp.pha'+' dan '+irisan[0][i]+'_16_'
              +str(k)+'_grp.pha berhasil difitting')