from dataacq import *
__version__ = '0.7'

def timecon(stringl):
    '''This function converts Unix Time stamp data to human readable format'''
    newtime = dt.utcfromtimestamp(int(stringl)).strftime('%Y-%m-%d %H:%M:%S')
    return newtime