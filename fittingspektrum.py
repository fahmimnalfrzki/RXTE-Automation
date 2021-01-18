#!/usr/bin/env python3
'''
#=============================================================================

Otomasi Fitting Spektrum Xspec

#=============================================================================
'''

from xspec import*
import os,glob,shutil,sys
import numpy as np
from astropy.io import fits
from matplotlib.pyplot import*

nama_obj='CirX-1'
NH=1.49

home='/home/fahmi/rxteotomasi'
folder='/home/fahmi/Documents/data/'+nama_obj+'/RXTE/'

data=os.listdir(folder)
os.chdir(folder)
obs_id=os.listdir()

file=[]
Tin=[]
norm_dbb=[]
PhotIn=[]
norm_po=[]
rcs=[]
flux=[[],[],[],[]]
fluxall=[]
fluxbb=[]
ctr=[[],[]]

for i in range(len(obs_id)):
    os.chdir(obs_id[i])
    for j in range(len(glob.glob(obs_id[i]+'_16_*'+'*_grp.pha'))):
        file.append(obs_id[i]+'_16_'+str(j))
        spek=Spectrum(obs_id[i]+'_16_'+str(j)+'_grp.pha')
        spek.ignore('0.0-3.0,20.0-**')
        ctr[0].append(spek.rate[0])
        ctr[1].append(spek.rate[1])

        mod=Model('TBabs*smedge*(diskbb+po+gauss)')
        c1=mod.TBabs
        c2=mod.smedge
        c3=mod.diskbb
        c4=mod.powerlaw
        c5=mod.gaussian

        c1.nH.values=NH
        c2.edgeE.values=7.1
        c5.LineE.values=6.4

        c1.nH.frozen=True
        c2.edgeE.frozen=True
        c5.LineE.frozen=True

        Fit.query='yes'
        Fit.perform()

        Fit.steppar('6 0.0 1.5 50')
        Fit.steppar('8 0.5 2. 50')
        Fit.show()
        
        Tin.append(c3.Tin.values[0])
        norm_dbb.append(c3.norm.values[0])
        PhotIn.append(c4.PhoIndex.values[0])
        norm_po.append(c4.norm.values[0])
        rcs.append(Fit.statistic/Fit.dof)
        
        c1.nH.values=0
        
        AllModels.calcFlux("3.0 4.0")
        flux[0].append(spek.flux[0])
        AllModels.calcFlux("4.0 6.4")
        flux[1].append(spek.flux[0])
        AllModels.calcFlux("6.4 9.7")
        flux[2].append(spek.flux[0])
        AllModels.calcFlux("9.7 16.0")
        flux[3].append(spek.flux[0])
        AllModels.calcFlux("3.0 20.0")
        fluxall.append(spek.flux[0])
        
        c4.norm.values=0
        
        AllModels.calcFlux("3.0 20.0")
        fluxbb.append(spek.flux[0])
        
        AllModels.clear()
        AllData.clear()
        
    os.chdir('..')


err=np.array([np.array(ctr[1])/np.array(ctr[0])*np.array(flux[0]),
             np.array(ctr[1])/np.array(ctr[0])*np.array(flux[1]),
             np.array(ctr[1])/np.array(ctr[0])*np.array(flux[2]),
             np.array(ctr[1])/np.array(ctr[0])*np.array(flux[3]),
             np.array(ctr[1])/np.array(ctr[0])*np.array(fluxall),
             np.array(ctr[1])/np.array(ctr[0])*np.array(fluxbb)])

soft=np.array(flux[1])/np.array(flux[0])
hard=np.array(flux[3])/np.array(flux[2])

soft_err=np.sqrt((1/np.array(flux[0]) *np.array(err[0]))**2 
             +(-np.array(flux[1])/(np.array(flux[0])**2)*np.array(err[0]))**2)
hard_err=np.sqrt((1/np.array(flux[2]) *np.array(err[2]))**2 
             +(-np.array(flux[3])/(np.array(flux[2])**2)*np.array(err[2]))**2)

fig=figure(0)
f=fig.add_subplot(111)
f.scatter(soft,hard)
f.errorbar(x=soft,y=hard,xerr=soft_err,yerr=hard_err,fmt='o'
           ,color='black', ecolor='lightgray',capsize=0)
#f.set_ylim(0.0,1.0)
#f.set_xlim(4.0,5.5)
f.set_xlabel('Soft Color')
f.set_ylabel('Hard Color')
f.set_title('Diagram Color-Color (Flux) '+nama_obj)
savefig(home+'/Diagram Color-Color (Flux) '+nama_obj+'.png')

dat=['File Tin Norm_Diskbb PhoIndex_Powerlaw Norm_Powerlaw 
     ReducedChiSq Flux3-4 err Flux4-6.4 err Flux6.4-9.7 err 
     Flux9.7-16 err Flux3-20 err Fluxbb err CountRate err 
     SoftColor err HardColor err']
for i in range(len(Tin)):
    dat.append(str(file[i])+' '+str(Tin[i])+' '+str(norm_dbb[i])
    +' '+str(PhotIn[i])+' '+str(norm_po[i])+' '+str(rcs[i])
    +' '+str(flux[0][i])+' '+str(err[0][i])+' '+str(flux[1][i])
    +' '+str(err[1][i])+' '+str(flux[2][i])+' '+str(err[2][i])
    +' '+str(flux[3][i])+' '+str(err[3][i])+' '+str(fluxall[i])
    +' '+str(err[4][i])+' '+str(fluxbb[i])+' '+str(err[5][i])
    +' '+str(ctr[0][i])+' '+str(ctr[1][i])+' '+str(soft[i])
    +' '+str(soft_err[i])+' '+str(hard[i])+' '+str(hard_err[i]))        
np.savetxt('/home/fahmi/Documents/data/'+nama_obj+'/'
           +nama_obj+'.tsv',dat,fmt='%s')