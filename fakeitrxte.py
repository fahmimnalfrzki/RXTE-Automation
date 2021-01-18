#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 00:39:06 2019

@author: fahmi
"""
import os, mmap,glob
import numpy as np

folder='/home/fahmi/rxteotomasi/'
os.chdir(folder+'fakeit_dbb/')
flux_dbb=[[],[],[],[]]
Tin=np.linspace(0.5,3.0,50)

for i in Tin:
    with open("XSPEC","w") as fout:
        fout.write("setplot energy\n")
        fout.write("query yes\n")
        fout.write("mo tbabs*(diskbb)\n")
        fout.write("0.781 -1\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write("energies 3.0 20.0 1000\n")
        fout.write("flux 3.0 20.0")
    os.system("xspec < XSPEC > logfile.xspec")
    
    f = open('logfile.xspec','r')
    flux=f.readlines()
    for j in range(len(flux)):
        if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
            x=float(flux[j].split()[4][1:])
    
    norm=2.47156284298038E-08/x
    with open("XSPEC","w") as fout:
        fout.write('setplot energy\n')
        fout.write('query yes\n')
        fout.write('mo tbabs*(diskbb)\n')
        fout.write('0.781 -1\n')
        fout.write(str(i)+"\n")
        fout.write('1.\n')
        fout.write('energies 3.0 20.0 1000\n')
        fout.write('flux 3.0 20.0\n')
        fout.write('new 3 '+str(norm)+'\n')
        fout.write('energies reset\n')
        fout.write('fakeit none\n')
        fout.write(glob.glob('*.rsp')[0]+'\n')
        fout.write('\n')
        fout.write('y\n')
        fout.write('fake\n')
        fout.write('dbb_'+str(i)+'keV.fak\n')
        fout.write('512\n')
        fout.write('statistic cstat\n')
        fout.write('statistic test pchi\n')
        fout.write('ignore 0.0-3.0,20.0-**\n')
        fout.write('fit\n')
        fout.write('new 1 0\n')
        fout.write('flux 3.0 4.0\n')
        fout.write('flux 4.0 6.4\n')
        fout.write('flux 6.4 9.7\n')
        fout.write('flux 9.7 16.0')
    os.system("xspec < XSPEC > logfile.xspec1")
    
    f = open('logfile.xspec1','r')
    flux=f.readlines()
    for j in range(90,len(flux)):
        if len(flux[j].split())==11 and flux[j].split()[9]=='4.0000':
            flux_dbb[0].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='6.4000':
            flux_dbb[1].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='9.7000':
            flux_dbb[2].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='16.000':
            flux_dbb[3].append(float(flux[j].split()[4][1:]))


os.chdir(folder+'fakeit_po/')
flux_po=[[],[],[],[]]
PhotIndex=np.linspace(1.0,2.5,50)

for i in PhotIndex:
    with open("XSPEC","w") as fout:
        fout.write("setplot energy\n")
        fout.write("query yes\n")
        fout.write("mo tbabs*(po)\n")
        fout.write("0.781 -1\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write("energies 3.0 20.0 1000\n")
        fout.write("flux 3.0 20.0")
    os.system("xspec < XSPEC > logfile.xspec")
    
    f = open('logfile.xspec','r')
    flux=f.readlines()
    for j in range(len(flux)):
        if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
            x=float(flux[j].split()[4][1:])
    
    norm=2.47156284298038E-08/x
    with open("XSPEC","w") as fout:
        fout.write('setplot energy\n')
        fout.write('query yes\n')
        fout.write('mo tbabs*(po)\n')
        fout.write('0.781 -1\n')
        fout.write(str(i)+"\n")
        fout.write('1.\n')
        fout.write('energies 3.0 20.0 1000\n')
        fout.write('flux 3.0 20.0\n')
        fout.write('new 3 '+str(norm)+'\n')
        fout.write('energies reset\n')
        fout.write('fakeit none\n')
        fout.write(glob.glob('*.rsp')[0]+'\n')
        fout.write('\n')
        fout.write('y\n')
        fout.write('fake\n')
        fout.write('po_'+str(i)+'.fak\n')
        fout.write('512\n')
        fout.write('statistic cstat\n')
        fout.write('statistic test pchi\n')
        fout.write('ignore 0.0-3.0,20.0-**\n')
        fout.write('fit\n')
        fout.write('new 1 0\n')
        fout.write('flux 3.0 4.0\n')
        fout.write('flux 4.0 6.4\n')
        fout.write('flux 6.4 9.7\n')
        fout.write('flux 9.7 16.0')
    os.system("xspec < XSPEC > logfile.xspec1")
    
    f = open('logfile.xspec1','r')
    flux=f.readlines()
    for j in range(90,len(flux)):
        if len(flux[j].split())==11 and flux[j].split()[9]=='4.0000':
            flux_po[0].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='6.4000':
            flux_po[1].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='9.7000':
            flux_po[2].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='16.000':
            flux_po[3].append(float(flux[j].split()[4][1:]))


os.chdir(folder+'fakeit_dbb_po/')
flux_bp1=[[],[],[],[]]
tin=1.

for i in PhotIndex:
    with open("XSPEC","w") as fout:
        fout.write("setplot energy\n")
        fout.write("query yes\n")
        fout.write("mo tbabs*(diskbb+po)\n")
        fout.write("0.781 -1\n")
        fout.write(str(tin)+"\n")
        fout.write("1.\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write("energies 3.0 20.0 1000\n")
        fout.write("flux 3.0 20.0")
    os.system("xspec < XSPEC > logfile.xspec")
    
    f = open('logfile.xspec','r')
    flux=f.readlines()
    for j in range(len(flux)):
        if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
            x=float(flux[j].split()[4][1:])
    
    norm=2.47156284298038E-08/x
    with open("XSPEC","w") as fout:
        fout.write('setplot energy\n')
        fout.write('query yes\n')
        fout.write("mo tbabs*(diskbb+po)\n")
        fout.write("0.781 -1\n")
        fout.write(str(tin)+"\n")
        fout.write("1.\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write('energies 3.0 20.0 1000\n')
        fout.write('flux 3.0 20.0\n')
        fout.write('new 3 '+str(norm)+'\n')
        fout.write('energies reset\n')
        fout.write('fakeit none\n')
        fout.write(glob.glob('*.rsp')[0]+'\n')
        fout.write('\n')
        fout.write('y\n')
        fout.write('fake\n')
        fout.write('bp1_'+str(i)+'keV.fak\n')
        fout.write('512\n')
        fout.write('statistic cstat\n')
        fout.write('statistic test pchi\n')
        fout.write('ignore 0.0-3.0,20.0-**\n')
        fout.write('fit\n')
        fout.write('new 1 0\n')
        fout.write('flux 3.0 4.0\n')
        fout.write('flux 4.0 6.4\n')
        fout.write('flux 6.4 9.7\n')
        fout.write('flux 9.7 16.0')
    os.system("xspec < XSPEC > logfile.xspec1")
    
    f = open('logfile.xspec1','r')
    flux=f.readlines()
    for j in range(90,len(flux)):
        if len(flux[j].split())==11 and flux[j].split()[9]=='4.0000':
            flux_bp1[0].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='6.4000':
            flux_bp1[1].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='9.7000':
            flux_bp1[2].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='16.000':
            flux_bp1[3].append(float(flux[j].split()[4][1:]))


flux_bp2=[[],[],[],[]]
pot=1.4

for i in Tin:
    with open("XSPEC","w") as fout:
        fout.write("setplot energy\n")
        fout.write("query yes\n")
        fout.write("mo tbabs*(diskbb+po)\n")
        fout.write("0.781 -1\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write(str(pot)+"\n")
        fout.write("1.\n")
        fout.write("energies 3.0 20.0 1000\n")
        fout.write("flux 3.0 20.0")
    os.system("xspec < XSPEC > logfile.xspec")
    
    f = open('logfile.xspec','r')
    flux=f.readlines()
    for j in range(len(flux)):
        if len(flux[j].split())>5 and flux[j].split()[0]=='Model' and flux[j].split()[1]=='Flux':
            x=float(flux[j].split()[4][1:])
    
    norm=2.47156284298038E-08/x
    with open("XSPEC","w") as fout:
        fout.write('setplot energy\n')
        fout.write('query yes\n')
        fout.write("mo tbabs*(diskbb+po)\n")
        fout.write("0.781 -1\n")
        fout.write(str(i)+"\n")
        fout.write("1.\n")
        fout.write(str(pot)+"\n")
        fout.write("1.\n")
        fout.write('energies 3.0 20.0 1000\n')
        fout.write('flux 3.0 20.0\n')
        fout.write('new 3 '+str(norm)+'\n')
        fout.write('energies reset\n')
        fout.write('fakeit none\n')
        fout.write(glob.glob('*.rsp')[0]+'\n')
        fout.write('\n')
        fout.write('y\n')
        fout.write('fake\n')
        fout.write('bp2_'+str(i)+'keV.fak\n')
        fout.write('512\n')
        fout.write('statistic cstat\n')
        fout.write('statistic test pchi\n')
        fout.write('ignore 0.0-3.0,20.0-**\n')
        fout.write('fit\n')
        fout.write('new 1 0\n')
        fout.write('flux 3.0 4.0\n')
        fout.write('flux 4.0 6.4\n')
        fout.write('flux 6.4 9.7\n')
        fout.write('flux 9.7 16.0')
    os.system("xspec < XSPEC > logfile.xspec1")
    
    f = open('logfile.xspec1','r')
    flux=f.readlines()
    for j in range(90,len(flux)):
        if len(flux[j].split())==11 and flux[j].split()[9]=='4.0000':
            flux_bp2[0].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='6.4000':
            flux_bp2[1].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='9.7000':
            flux_bp2[2].append(float(flux[j].split()[4][1:]))
        if len(flux[j].split())==11 and flux[j].split()[9]=='16.000':
            flux_bp2[3].append(float(flux[j].split()[4][1:]))

soft=[np.array(flux_dbb[1])/np.array(flux_dbb[0]),np.array(flux_po[1])/np.array(flux_po[0]),np.array(flux_bp1[1])/np.array(flux_bp1[0]),np.array(flux_bp2[1])/np.array(flux_bp2[0])]
hard=[np.array(flux_dbb[3])/np.array(flux_dbb[2]),np.array(flux_po[3])/np.array(flux_po[2]),np.array(flux_bp1[3])/np.array(flux_bp1[2]),np.array(flux_bp2[3])/np.array(flux_bp2[2])]

dat=['softbb hardbb softpo hardpo softbp1 hardbp1 softbp2 hardbp2']
for i in range(len(soft[0])):
    dat.append(str(soft[0][i])+' '+str(hard[0][i])+' '+str(soft[1][i])+' '+str(hard[1][i])+' '+str(soft[2][i])+' '+str(hard[2][i])+' '+str(soft[3][i])+' '+str(hard[3][i]))        
np.savetxt(folder+'fakeit_rxte.tsv',dat,fmt='%s')