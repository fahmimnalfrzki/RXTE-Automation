#!/usr/bin/python
'''
===============================================================

Pengolahan Data RXTE PCA (PCU2-Top layer only)
Dibuat oleh: Fahmi Iman Alfarizki (fahmimn21@gmail.com)

===============================================================
'''

import os,glob,shutil,sys
import subprocess as sub
from astropy.io import fits
import numpy as np
from astropy.coordinates import SkyCoord

nama_obj='CygX-1'
cor=SkyCoord.from_name('Cyg X-1')

home='/home/fahmi/rxteotomasi'
folder='/home/fahmi/Documents/data/'+nama_obj+'/ff/'

lisfile=os.listdir(folder)
os.chdir(folder)
obs_id=os.listdir()


def src_file(i,k):
    return(obs_id[i]+'_16_'+str(k))
def bkg_file(i,k):
    return('bkg_'+obs_id[i]+'_16_'+str(k))
def resp_file(i):
    return('res_'+obs_id[i]+'.rsp')




#============= <Definisi Fungsi-Fungsi> =======================#
def skrip(call,filelog):
        with sub.Popen(call, stdout=sub.PIPE, stderr=sub.STDOUT,
                       bufsize=1) as p, \
            open(filelog, 'ab') as file:
                for line in p.stdout: # b'\n'-separated lines
                    sys.stdout.write(line) # pass bytes as is
                    file.write(line)

def STD1(call,file_log):
        with sub.Popen(call, stdout=sub.PIPE, stderr=sub.STDOUT,
                       bufsize=1) as p, \
            open(file_log, 'ab') as file:
                for line in p.stdout: # b'\n'-separated lines
                    sys.stdout.write(line) # pass bytes as is
                    file.write(line)

def extsalc(infile,gtiorfile,gtiandfile,outroot,accumulate,
            timecol,columns,binsz,printmode,lcmode,smode,timemin,
            timemax,timeint,chmin,chmax,
            chint,chbin):
        sextrct=['saextrct',
             infile,
             gtiorfile,
             gtiandfile,
             outroot,
             accumulate,
             timecol,
             columns,
             binsz,
             printmode,
             lcmode,
             smode,
             timemin,
             timemax,
             timeint,
             chmin,
             chmax,
             chint,
             chbin]
        skrip(sextrct,'spek'+outroot+'.log')

def extsastd1(infile,gtiorfile,gtiandfile,outroot,accumulate,
              timecol,columns,binsz,printmode,lcmode,smode,
              timemin,timemax,timeint,chmin,chmax,
              chint,chbin):
        sextrctstd1=['saextrct',
             infile,
             gtiorfile,
             gtiandfile,
             outroot,
             accumulate,
             timecol,
             columns,
             binsz,
             printmode,
             lcmode,
             smode,
             timemin,
             timemax,
             timeint,
             chmin,
             chmax,
             chint,
             chbin]
               file.write(line)

def deadtimecorr(Non_VLE_cr,VLE_cr): 
    num_pcu_on=5
    DTF=(Non_VLE_cr* 10**-5 / num_pcu_on 
         + (VLE_cr * 10**-4 / num_pcu_on)

    return(1/(1-DTF)) 
#===========================================================#    

for i in range(len(obs_id)):
    os.chdir(home)
    ob=folder+obs_id[i]
    os.chdir(ob)
    os.chdir('pca/')

#Membuat Standar List 1 dan 2
    fstd1=os.open(ob+'/std1.list',os.O_RDWR|os.O_CREAT)
    for j in range(len(glob.glob('FS46*'))):
        std1='pca/'+glob.glob('FS46*')[j]
        os.write(fstd1,str.encode(std1+'\n'))
    os.close(fstd1)
    fstd2=os.open(ob+'/std2.list',os.O_RDWR|os.O_CREAT)
    for j in range(len(glob.glob('FS4a*'))):
        std2='pca/'+glob.glob('FS4a*')[j]
        os.write(fstd2,str.encode(std2+'\n'))
    os.close(fstd2)
    os.chdir("..")

    shutil.copy2(home+'/pcu2.col', ob)
    shutil.copy2(home+'/col_deadtime.col', ob)

#Membuat Filter File Baru    
    filtfile=['xtefilt', '-c', '-a', home
              +'/appidlist', '-o', obs_id[i], '-p',
              ob, '-f', 'filter_new', '-t', '16', '-b', 'CALDB']
    skrip(filtfile,'filtfile.log')

#Membuat Good File Interval    
    gti=['maketime', ob+'/filter_new.xfl', 'good_ti.gti',
    'elv.gt.10.and.offset.lt.0.02.and.pcu2_on.eq.1.and.num_pcu_on.gt.0.'+
    'and.time_since_saa.gt.30.or.time_since_saa.lt.0.and.electron2.lt.'+
    '0.1.and.time_since_brk.lt.-150.or.time_since_brk.gt.600', 'NAME',
    'VALUES', 'TIME', 'no']
    skrip(gti,'gti.log')

#Ekstrak Kurva Cahaya dan Spektrum Tanpa Seleksi Interval Waktu
    extsalc('@std2.list','APPLY','good_ti.gti','int_'
            +obs_id[i]+'_16','ONE',
            'TIME','@pcu2.col','16','BOTH',
            'RATE','SUM','INDEF','INDEF',
             'INDEF','INDEF','INDEF','INDEF','INDEF')

#Mengekstrak Interval Waktu Dari 
#STDGTI Kurva Cahaya untuk Ekstrak Spektrum    
    hdul=fits.open('int_'+obs_id[i]+'_16.lc')
    dat=hdul[2].data
    
    ttimes=[]
    intv=0
    for j in range(len(dat)):
        for k in range(int((dat[j][1]-dat[j][0])/512)+1):
            if (dat[j][1]-dat[j][0])>=512.0:
                ttimes.append(dat[j][0]+intv)
                if ttimes[k]+intv<=dat[j][1]:
                    intv=k*intv+512
                else:
                    break
    a=np.sort(ttimes)
    b=set(a)
    b=list(b)
    if (dat[j][1]-dat[j][0])>=512.0:
        if b[-1]>dat[j][1]:
            rm=b[len(b)-1]
            b.remove(rm)
    ttime=np.sort(b)
    

#Ekstrak Spektrum Utama dan Untuk Keperluan Deadtime Corrextion    
    for k in range(len(ttime)-1):
        extsalc('@std2.list','APPLY','good_ti.gti',src_file(i,k),
                'ONE','TIME','@pcu2.col','16',
                'SPECTRUM','RATE','SUM',
                str(ttime[k]),str(ttime[k+1]),
                'INDEF','INDEF','INDEF','INDEF',
                'INDEF')
        extsalc('@std1.list','APPLY','good_ti.gti',
                  'non_VLCstd1_'+src_file(i,k),'ONE','TIME',
                  '@col_deadtime.col','16',
                  'SPECTRUM','RATE','SUM',
                  str(ttime[k]),str(ttime[k+1]),
                  'INDEF','INDEF','INDEF',
                  'INDEF','INDEF')
        extsalc('@std1.list','APPLY','good_ti.gti',
                  'VLCstd1_'+src_file(i,k),'ONE',
                  'TIME','VLECnt','16',
                  'SPECTRUM','RATE','SUM',
                  str(ttime[k]),str(ttime[k+1]),
                  'INDEF','INDEF','INDEF','INDEF','INDEF')

#Deadtime Correction   
    for k in glob.glob(obs_id[i]+'_16_*'+'*.pha'):
        hdusa=fits.open(k)
        exp=hdusa[1].header['EXPOSURE']
        l=k.replace('.pha','')
        file1=open('speknon_VLCstd1_'+l+'.log','r')
        file2=open('spekVLCstd1_'+l+'.log','r')
        data1=file1.readlines()
        data2=file2.readlines()

        for j in range (0,len(data1)-1):
            if len(data1[j].split())==6 :
                if data1[j].split()[1]=='Counts/Time' 
                and data1[j].split()[5]!='Not':
                    Non_VLE_cr=float(data1[j].split()[5])
                else:
                    pass

        for j in range (0,len(data2)-1):
            if len(data2[j].split())==6 :
                if data2[j].split()[1]=='Counts/Time' 
                and data2[j].split()[5]!='Not':
                    VLE_cr=float(data2[j].split()[5])
                else:
                    pass

        new_exp=exp/deadtimecorr(Non_VLE_cr,VLE_cr)
        hdusa[1].header['EXPOSURE']=new_exp

#Membuat File Background    
    os.chdir('pca/')
    for k in range(len(glob.glob('FS4a*'))):
        bkg_name='bkg_'+glob.glob('FS4a*')[k]
        pbkg=['pcabackest',
              glob.glob('FS4a*')[k],
              bkg_name,
              home+'/pca_bkgd_cmbrightvle_eMv20051128.mdl',
              ob+'/filter_new.xfl',
              '16',
              'yes',
              'no',
              'fullspec='+'yes',
              'saahfile='+home+'/pca_saa_history.gz']
        skrip(pbkg,'pcabackest.log')
        shutil.move(ob+'/pca/'+bkg_name,ob)
    os.chdir('..')

#Membuat List File Background
    backfile=os.open(ob+'/bkg.list',os.O_RDWR|os.O_CREAT)
    for j in range(len(glob.glob('*bkg_FS4a*'))):
        bkgf=glob.glob('bkg_FS4a*')[j]
        os.write(backfile,str.encode(bkgf+'\n'))
    os.close(backfile)
    
#Ekstrak Spektrum Background dan Spektrum Background Deadtime Correction
    for k in range(len(ttime)-1):
        extsalc('@bkg.list','APPLY','good_ti.gti',
                bkg_file(i,k),'ONE','TIME',
                '@pcu2.col','16','SPECTRUM','RATE',
                'SUM',str(ttime[k]),
                 str(ttime[k+1]),'INDEF','INDEF',
                 'INDEF','INDEF','INDEF')
        extsalc('@std1.list','APPLY','good_ti.gti',
                  'non_VLCstd1_'+bkg_file(i,k),
                  'ONE','TIME',
                  '@col_deadtime.col','16',
                  'SPECTRUM','RATE','SUM',
                  str(ttime[k]),str(ttime[k+1]),
                  'INDEF','INDEF','INDEF',
                  'INDEF','INDEF')
        extsalc('@std1.list','APPLY','good_ti.gti',
                  'VLCstd1_'+bkg_file(i,k),'ONE',
                  'TIME','VLECnt','16',
                  'SPECTRUM','RATE','SUM',
                  str(ttime[k]),str(ttime[k+1]),
                  'INDEF','INDEF','INDEF','INDEF','INDEF')

#Deadtime Correction Background
    for k in glob.glob('bkg_'+obs_id[i]+'_16_*'+'*.pha'):
        hdusa=fits.open(k)
        exp=hdusa[1].header['EXPOSURE']
        l=k.replace('.pha','')
        file1=open('speknon_VLCstd1_'+l+'.log','r')
        file2=open('spekVLCstd1_'+l+'.log','r')
        data1=file1.readlines()
        data2=file2.readlines()

        for j in range (0,len(data1)-1):
            if len(data1[j].split())==6 :
                if data1[j].split()[1]=='Counts/Time' 
                and data1[j].split()[5]!='Not':
                    Non_VLE_cr=float(data1[j].split()[5])
                else:
                    pass

        for j in range (0,len(data2)-1):
            if len(data2[j].split())==6 :
                if data2[j].split()[1]=='Counts/Time' 
                and data2[j].split()[5]!='Not':
                    VLE_cr=float(data2[j].split()[5])
                else:
                    pass
    
    new_exp_bkg=exp/deadtimecorr(Non_VLE_cr,VLE_cr)

    for k in glob.glob('bkg_'+obs_id[i]+'_16_*'):
        hdusa=fits.open(k)
        hdusa[1].header['EXPOSURE']=new_exp_bkg

#Mengubah Nilai RA dan Dec ke Header Spektrum        
    for j in range(len(glob.glob(obs_id[i]+'_16_*'+'*.pha'))):
        sa=fits.open(src_file(i,j)+'.pha')
        sa[1].header['RA_OBJ']=cor.ra.deg
        sa[1].header['DEC_OBJ']=cor.ra.deg
        bck=fits.open(bkg_file(i,j)+'.pha')
        bck[1].header['RA_OBJ']=cor.ra.deg
        bck[1].header['DEC_OBJ']=cor.ra.deg

#Membuat File Response

    
#Rebin PHA dan GRPPHA

    resp=['pcarsp',
          '-f', 'int_'+obs_id[i]+'_16.pha',
           '-a', str(glob.glob('acs/FH0e_*')[0]),
           '-l', 'L1,R1',
           '-w', '1,1,1,1,1',
           '-j', 'y',
           '-p', '2',
           '-m', 'y', 
           '-n', resp_file(i)]
    skrip(resp,'resp'+str(k)+'.log')
    for k in range(len(glob.glob(obs_id[i]+'_16_*'+'*.pha'))):
        rds=['rddescr', src_file(i,k)+'.pha', 'chan.txt']
        skrip(rds,'rds'+str(k)+'.log')
        rbn=['rbnpha',
             'binfile=chan.txt',
             'infile='+bkg_file(i,k)+'.pha',
             'outfile='+bkg_file(i,k)+'_rbn.pha']
        skrip(rbn,'rbn'+str(k)+'.log')
        os.remove('chan.txt')
        grpbkg=['grppha',
                bkg_file(i,k)+'_rbn.pha',
                bkg_file(i,k)+'_rbn_grp.pha',
                'chatter=0',
                'comm=sys_err 0.01& group min 20&chkey respfile '
                +resp_file(i)+'&exit']
        skrip(grpbkg,'grpbkg'+str(k)+'.log')
        grp=['grppha',
             obs_id[i]+'_16_'+str(k)+'.pha',
             obs_id[i]+'_16_'+str(k)+'_grp.pha',
             'chatter=0',
             'comm=sys_err 0.01& group min 20&chkey respfile '
             +resp_file(i)+'&chkey backfile '
             +bkg_file(i,k)+'_rbn_grp.pha'+'&exit']
        skrip(grp,'grpspek'+str(k)+'.log')