#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 13:20:21 2019

@author: fahmi
"""
import numpy as np
from matplotlib.pyplot import*
import pandas as pd

nama_obj=np.array(['4U1608-522','XTEJ1752-223','CirX-1','4U1608-522'])
a=np.array(['navy','gold','black','green'])
b=np.array(['orange','blue','gray','black'])

i=3
dat=np.genfromtxt('E:/data/'+nama_obj[i]+'/'+nama_obj[i]+'.tsv',skip_header=1,delimiter=' ')
dat=np.transpose(dat)
'''
fig=figure(0)
f=fig.add_subplot(111)
for i in range(1):
    dat=np.genfromtxt('E:/data/'+nama_obj[i]+'/'+nama_obj[i]+'.tsv',skip_header=1,delimiter=' ')
    dat=np.transpose(dat)
    f.errorbar(x=dat[20],y=dat[22],xerr=dat[21],yerr=dat[23],fmt='o',c=a[i], ecolor=b[i],capsize=0,label=nama_obj[i])

data=np.genfromtxt('fakeit_rxte.tsv',skip_header=1,delimiter=' ')
data=np.transpose(data)
f.plot(data[0],data[1])
f.plot(data[2]*0.8,data[3]+0.25)
f.set_ylim(0.0,2.5)
f.set_xlim(0.0,2.5)
f.set_xlabel('Soft Color')
f.set_ylabel('Hard Color')
#f.legend(loc='upper left',bbox_to_anchor=(1, 1))
f.set_title('Diagram Color-Color 4U1608-522 (Flux) ')
savefig('Diagram Color-Color 4U1608-522 (Flux).png')
'''
par=['rcs','Tin','norm_Tin','photind','norm_po','f34','f46','f69','f916','ft','kompbb','soft','hard']
col=[5,1,2,3,4,6,8,10,12,14,16,20,22]
for j in range(len(par)):
    if j!=10:
        print(par[j])
        print(np.mean(dat[col[j]]))
        print(np.median(dat[col[j]]))
        print(np.min(dat[col[j]]))
        print(np.max(dat[col[j]]))
        print(np.std(dat[col[j]]))
    else:
        persen=(dat[col[j]]/dat[14])*100
        print(par[j])
        print(np.mean(persen))
        print(np.median(persen))
        print(np.min(persen))
        print(np.max(persen))
        print(np.std(persen))

print('')

a=0
b=0
c=0
d=0
print('rcs')
for i in range(len(persen)):
    if dat[5][i]<=1.5:
        a+=1
    elif dat[5][i]>1.5 and dat[5][i]<=2.0:
        b+=1
    elif dat[5][i]>2.0 and dat[5][i]<=2.5:
        c+=1
    elif dat[5][i]>1.5:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('Tin')
for i in range(len(persen)):
    if dat[1][i]<=0.5:
        a+=1
    elif dat[1][i]>0.5 and dat[1][i]<=0.75:
        b+=1
    elif dat[1][i]>0.75 and dat[1][i]<=1.0:
        c+=1
    elif dat[1][i]>1.0:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('normbb')
for i in range(len(persen)):
    if dat[2][i]<=1000:
        a+=1
    elif dat[2][i]>1000 and dat[2][i]<=5000:
        b+=1
    elif dat[2][i]>5000 and dat[2][i]<=10000:
        c+=1
    elif dat[2][i]>10000:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('po')
for i in range(len(persen)):
    if dat[3][i]<=0.5:
        a+=1
    elif dat[3][i]>0.5 and dat[3][i]<=1.5:
        b+=1
    elif dat[3][i]>1.5 and dat[3][i]<=2.5:
        c+=1
    elif dat[3][i]>2.5:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('normpo')
for i in range(len(persen)):
    if dat[4][i]<=1:
        a+=1
    elif dat[4][i]>1 and dat[4][i]<=5:
        b+=1
    elif dat[4][i]>5 and dat[4][i]<=10:
        c+=1
    elif dat[4][i]>10:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('f34')
for i in range(len(persen)):
    if dat[6][i]<=1.5E-9:
        a+=1
    elif dat[6][i]>1.5E-9 and dat[6][i]<=2.5E-9:
        b+=1
    elif dat[6][i]>2.5E-9 and dat[6][i]<=3.5E-9:
        c+=1
    elif dat[6][i]>3.5E-9:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('f46')
for i in range(len(persen)):
    if dat[8][i]<=1.5E-9:
        a+=1
    elif dat[8][i]>1.5E-9 and dat[8][i]<=2.5E-9:
        b+=1
    elif dat[8][i]>2.5E-9 and dat[8][i]<=3.5E-9:
        c+=1
    elif dat[8][i]>3.5E-9:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('f69')
for i in range(len(persen)):
    if dat[10][i]<=1.5E-9:
        a+=1
    elif dat[10][i]>1.5E-9 and dat[10][i]<=2.5E-9:
        b+=1
    elif dat[10][i]>2.5E-9 and dat[10][i]<=3.5E-9:
        c+=1
    elif dat[10][i]>3.5E-9:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('f916')
for i in range(len(persen)):
    if dat[12][i]<=1.5E-9:
        a+=1
    elif dat[12][i]>1.5E-9 and dat[12][i]<=2.5E-9:
        b+=1
    elif dat[12][i]>2.5E-9 and dat[12][i]<=3.5E-9:
        c+=1
    elif dat[12][i]>3.5E-9:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('ft')
for i in range(len(persen)):
    if dat[14][i]<=1.5E-9:
        a+=1
    elif dat[14][i]>1.5E-9 and dat[14][i]<=2.5E-9:
        b+=1
    elif dat[14][i]>2.5E-9 and dat[14][i]<=3.5E-9:
        c+=1
    elif dat[14][i]>3.5E-9:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('kompbb')
for i in range(len(persen)):
    if persen[i]<=25:
        a+=1
    elif persen[i]>25 and persen[i]<=50:
        b+=1
    elif persen[i]>50 and persen[i]<=75:
        c+=1
    elif persen[i]>75 and persen[i]<=100:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('soft')
for i in range(len(persen)):
    if dat[20][i]<=1:
        a+=1
    elif dat[20][i]>1 or dat[20][i]<=1.5:
        b+=1
    elif dat[20][i]>1.5 or dat[20][i]<=2.0:
        c+=1
    elif dat[20][i]>2:
        d+=1

print(a)
print(b)
print(c)
print(d)

a=0
b=0
c=0
d=0
print('ft')
for i in range(len(persen)):
    if dat[22][i]<=1:
        a+=1
    elif dat[22][i]>1 or dat[22][i]<=1.5:
        b+=1
    elif dat[22][i]>1.5 or dat[22][i]<=2.0:
        c+=1
    elif dat[22][i]>2:
        d+=1

print(a)
print(b)
print(c)
print(d)