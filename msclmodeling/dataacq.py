# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import time
from datetime import datetime as dt
import matplotlib.pyplot as plt

def timecon(stringl):
    '''This function converts Unix Time stamp data to human readable format'''
    newtime = dt.utcfromtimestamp(int(stringl)).strftime('%Y-%m-%d %H:%M:%S')
    return newtime


def plotter(df):

    # Plotting the data
    fig,ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(df.SmO2,'g')
    ax2.plot(df.Speed,'-k')

    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel('SmO2', color='g')
    ax2.set_ylabel('Speed (mi/hr)', color='k')
    return (df,fig)
    #return {'DataTable':df,'Plot':fig}
    

def twinplot(df,ex='SmO2',wy='Speed'):
    ex = df[ex]
    wy = df[wy]
    plt.figure()
    fig,ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(np.linspace(1,len(df),len(df)),ex,'g',lw=0.6)
    ax2.plot(np.linspace(1,len(df),len(df)),wy,'-k',lw=0.3)
    ax2.plot(np.linspace(1,len(df),len(df)),pd.Series(wy).rolling(10).mean(),'-k')
    #ax2.plot(np.linspace(1,len(df),len(df)),df.SpeedGuide,'-k')
    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel(ex.name, color='g')
    ax2.set_ylabel(wy.name, color='k')
    plt.title(ex.name + ' and ' + wy.name)

def multiplot(df):
    colors = list('rgbymck')
    # op4 = df.resample('10S').mean() 
    params = df.columns
    plt.figure()
    for i in range(1,len(params)):
        plt.subplot(320+i)
        plt.plot(df.iloc[:,[i]],colors[i])
        plt.title(params[i])
    

def exporter (df,filename):
    '''This function exports the dataframe ONE to a filename given by the user. 
     The file is stored with the CSV extension in the current working directory. '''
    export = df[['SpO2','SmO2','Speed']] 
    export.to_csv(filename+'.csv',sep = '\t', header = None, index = False)
    print 'data exported as CSV to', filename
    

def norm (data):
    data= np.array(data)
    for col in (np.arange(0,data.shape[1])):
        for row in (np.arange(1,data.shape[0])):
            data[row,col] = (data[row,col]-data[0,col])/(data[0,col])
        data[0,col] = data[0,col]/data[0,col]
    return data

def normdf (data):
    for col in (np.arange(0,data.shape[1])):
        for row in (np.arange(1,data.shape[0])):
            data.ix[row,col] = (data.ix[row,col]-data.ix[0,col])/(data.ix[0,col])
        data.ix[0,col] = data.ix[0,col]/data.ix[0,col]
    return data

def twinplotset(data,save='n'):
    ''' This function generates four separate plots for the given 'data'frame. 
    Also, if save=='y', the function will save plots as PDF in the working directory.
    save option is set to 'n' by default.'''
    dt=time.strftime('%Y%m%d%H%M')
    twinplot(data,'pwr_instpwr','HeartRate')
    if (save=='y'):
        plt.savefig('pwrHR-'+dt+'.pdf')
    else:
        pass
    twinplot(data,'pwr_instpwr','SmO2')
    if (save=='y'):
        plt.savefig('pwrSmO-'+dt+'.pdf')
    else:
        pass
    twinplot(data,'pwr_instpwr','SpO2')
    if (save=='y'):
        plt.savefig('pwrSpO-'+dt+'.pdf')
    else:
        pass
    twinplot(data,'pwr_instpwr','cad_cadence')
    if (save=='y'):
        plt.savefig('pwrCad-'+dt+'.pdf')
    else:
        pass

def bsxreader(bsxfile,etype='biking'):
    '''This function reads the BSX CSV data file, cleans it and converts it 
    into useful data table, etype could be "biking" or "running (default)"'''
    fields = ['Value 1','Value 2','Value 3','Value 4']
    bsx = pd.read_csv(bsxfile, sep=',',skiprows=np.linspace(1,13,13),usecols=fields)
    bsx.columns = ['TimeStamp','HeartRate','SmO2','Speed']
    bsx.Speed = 2.24 * bsx.Speed  # Convert from meters per second to mi/hr
    if (etype=='biking'):
        bsx.columns = ['TimeStamp','HeartRate','SmO2','Power']
        bsx.Power = bsx.Power/2.24  # Convert from meters per second to mi/hr
    
    #bsx['SpeedGuide'] = speedsetter(bsx)
    bsx.insert(1,'TrueTime',bsx.TimeStamp.apply(timecon))
    bsx.TrueTime = pd.DatetimeIndex (bsx.TrueTime)
#    bsx.insert(1,'SpeedGuide',speedsetter(bsx))
    bsx['IDX'] = pd.DatetimeIndex(bsx['TrueTime']) #Convert TrueTime to TimeSeries format
    bsx.set_index('IDX',inplace=True)
    bsx.index.name=None
    return bsx

def poxconverter(pulseoxfile,strtime):
    pulseox = pd.read_csv(pulseoxfile,delimiter=',')
    if (pulseox.shape[1]==2):
        index = pd.date_range(strtime, freq='S', periods=len(pulseox))
        pulseox.index = index
        pulseox.insert(0,'TrueTime',pulseox.index.values)
        pulseox.to_csv(pulseoxfile+'ss.csv',index = False)
    else:
        print "The file has already been converted to include timestamp."
        return pulseox

def poxreader(pulseoxfile):
    pox = pd.read_csv(pulseoxfile,delimiter=',',header=0)
    pox.TrueTime = pd.DatetimeIndex(pox.TrueTime)
    return pox

def wfconverter (wf_file,strtime):
    wahoo = pd.read_csv(wf_file,sep=',')
    wahoo = wahoo[['pwr_accdist','pwr_speed','pwr_instpwr','cad_cadence']]
    index = pd.date_range(strtime,freq='S',periods=len(wahoo))
    wahoo.index = index
    wahoo.insert(0,'TrueTime',wahoo.index.values)
    wahoo.to_csv(wf_file+'ss.csv',index=False)
    return wahoo

def wahooreader(wf_file):
    wf = pd.read_csv(wf_file,delimiter=',',header=0)
    wf.TrueTime = pd.DatetimeIndex(wf.TrueTime)
    return wf

def curving (data):
    data2 = data.select_dtypes(include=['float','int64','int','double'])
    data2 = data2/data2.max()
    data3 = data.select_dtypes(exclude=['float','int64','int','double'])
    data4 = pd.concat([data3,data2],axis=1)
    return data4
    

if __name__=="__main__":
    
    print "This is a library of functions that may be used for \
processing data files related to the muscle metabolism project. Import \
as >>> import msclib as ml\n\
>>>dir(msclib)\n to learn more about the available functions."