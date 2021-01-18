#!/usr/bin/env python3
'''
#=============================================================================

Otomasi Fitting Spektrum Simultan

#=============================================================================
'''

from xspec import*
import os,glob,shutil,sys
import numpy as np
from astropy.io import fits
from matplotlib.pyplot import*

nama_obj='XTEJ1752-223'
NH=0.781

home='/home/fahmi/Documents/data/'+nama_obj
rxte='/home/fahmi/Documents/data/'+nama_obj+'/RXTE/'
swift='/home/fahmi/Documents/data/'+nama_obj+'/Swift/'
simul='/home/fahmi/Documents/data/'+nama_obj+'/simultan/'
robsid=os.listdir(rxte)
sobsid=os.listdir(swift)

for i in range(len(robsid)):
    for j in range(len(glob.glob(rxte+robsid[i]+'/'+robsid[i]+'_16_*_grp.pha'))):
        shutil.copy2(rxte+robsid[i]+'/'+robsid[i]+'_16_'+str(j)+'_grp.pha',simul)
        shutil.copy2(rxte+robsid[i]+'/'+'bkg_'+robsid[i]+'_16_'+str(j)+'_rbn_grp.pha',simul)
    shutil.copy2(rxte+robsid[i]+'/'+'res_'+robsid[i]+'.rsp',simul)

for i in range(len(sobsid)):
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'+sobsid[i]+'_wt_20_grp.pha',simul)
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'+'bkg'+sobsid[i]+'_wt_20_grp.pha',simul)
    shutil.copy2(swift+sobsid[i]+'/xrt/event/'+sobsid[i]+'_wt_exp.arf',simul)
    shutil.copy2(glob.glob(swift+sobsid[i]+'/xrt/event/'+'*.rmf')[0],simul)

os.chdir(simul)
irisan=[[],[],[],[]]
#robsid=[]
#sobsid=['00031651015']

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
'''
os.chdir(simul)
for i in range(len(irisan[0])):
    for j in range(len(glob.glob(irisan[0][i]+'_16_*_grp.pha'))):
        with open('XSPEC','w') as fout:
            fout.write('query yes\n')
            fout.write('setplot energy\n')
            fout.write('data 1: '+irisan[0][i]+'_16_'+str(j)+'_grp.pha 2: '+irisan[1][i]+'_wt_20_grp.pha'+'\n')
            fout.write('ign 1:0.0-3.0,20.0-**\n')
            fout.write('ign 2:0.0-0.3,10.0-**\n')
            
            fout.write('mo tbabs*const*(diskbb)\n')
            #Data group 1 - RXTE
            fout.write(str(NH)+' -1\n')
            fout.write('1. -1\n')
            fout.write('1.\n')
            fout.write('1.\n')
            #Data group 2 - Swift
            fout.write('\n')
            fout.write('1.\n')
            fout.write('\n')
            fout.write('\n')
            fout.write('thaw 6\n')
            fout.write('fit\n')
            fout.write('steppar 3 0.5 1. 200\n')
            
            fout.write('editmo tbabs*const*(diskbb+po)\n')
            #Data group 1 - RXTE
            fout.write('1.\n')
            fout.write('1.\n')
            #Data group 2 - Swift
            fout.write('\n')
            fout.write('\n')
            fout.write('fit\n')
            fout.write('steppar 5 0.5 2.5 300\n')
            
            fout.write('editmo tbabs*const*(diskbb+po+gauss)\n')
            #Data group 1 - RXTE
            fout.write('6.4 -1\n')
            fout.write('1e-3\n')
            fout.write('1.\n')
            #Data group 2 - Swift
            fout.write('\n')
            fout.write('\n')
            fout.write('\n')
            fout.write('fit\n')
            
            fout.write('editmo tbabs*const*smedge*(diskbb+po+gauss)\n')
            #Data group 1 - RXTE
            fout.write('7.1\n')
            fout.write('\n')
            fout.write('\n')
            fout.write('1.\n')
            #Data group 2 - Swift
            fout.write('\n')
            fout.write('\n')
            fout.write('\n')
            fout.write('\n')
            fout.write('fit\n')
            fout.write('show all\n')
            fout.write('save all '+irisan[0][i]+'_'+str(j)+'.xcm')
        os.system('xspec < XSPEC > '+irisan[0][i]+'_'+str(j)+'.log')
'''