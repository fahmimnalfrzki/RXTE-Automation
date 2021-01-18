#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 14:57:09 2019

@author: fahmi
"""

from xspec import*
import os
from matplotlib import*

tin=np.linspace(0.25,3.0,20)

os.chdir('/home/fahmi/Documents/data/CygX-1/RXTE/90414-03-03-00/')
soft=[]
hard=[]

for i in range(len(tin)):
    mod=Model('TBabs*diskbb')
    c1=mod.TBabs
    c2=mod.diskbb
    
    c1.nH.values=0.781
    c1.nH.frozen=True
    c2.Tin.values=tin[i]
    
    AllModels.setEnergies('3.0 20.0 1000')
    
    AllModels.calcFlux('3.0 20.0')
    f=AllModels(1).flux[0]
    norma=8.568e-9/f
    
    c2.norm.values=norma
    
    AllModels.setEnergies('reset')
    fs1 = FakeitSettings(response="res_90414-03-03-00.rsp", exposure = 512.0,fileName='fakebb_'+str(tin[i])+'.fak')
    AllData.fakeit(1,fs1)
    
    Fit.statMethod = "cstat"
    Fit.statTest="pchi"
    AllData.ignore('0.0-3.0,20.0-**')
    Fit.query='yes'
    Fit.perform()
    
    c1.nH.values=0
    
    AllModels.calcFlux('3.0 4.0')
    f1=AllModels(1).flux[0]
    AllModels.calcFlux('4.0 6.4')
    f2=AllModels(1).flux[0]
    AllModels.calcFlux('6.4 9.7')
    f3=AllModels(1).flux[0]
    AllModels.calcFlux('9.7 16.0')
    f4=AllModels(1).flux[0]
    
    soft.append(f2/f1)
    hard.append(f4/f3)
    
    AllModels.clear()
    AllData.clear()