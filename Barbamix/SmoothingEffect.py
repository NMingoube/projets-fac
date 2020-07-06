# -*- coding: utf-8 -*-

import getopt
import numpy as np
import scipy.io.wavfile as wavfile
import math
import sys

class SmoothingEffect():
    def __init__(self,path,piste):
        self.fichierOrig=path
        self.nPiste=piste

        self.radiusSmoothing = 5

        #print(self.fichierOrig)
        rate, data = wavfile.read(self.fichierOrig)
       
        if(data.ndim>1):
            data = data[:,1]
			
        tempData = data.copy()
        tempData.setflags(write=1)

        for k in range ( 0 , data.size ):
            self.doSmoothing( data , k , tempData )

        

        result = tempData
        # wavfile.write wants ints between +-5000; hence the cast
        wavfile.write("Banque\\BarbaMixGenatedSound_effetSmoothing"+str(self.nPiste)+"_"+str(id(self))+".wav", rate, result.astype(np.int16))
        self.newWavEffet="Banque\\BarbaMixGenatedSound_effetSmoothing"+str(self.nPiste)+"_"+str(id(self))+".wav"
    
    def doSmoothing( self , OriginalData , index , TargetData ):

        diff = 1
        proportion = 1
        total = 0
        result = 0
        for k in range( index - self.radiusSmoothing  , index + self.radiusSmoothing + 1 ):
            if( k > 0 and k < OriginalData.size ):
                result = result + OriginalData.take(k) * proportion 
            total = total + proportion
            if( k < index ):
                proportion = proportion + diff
            else :
                proportion = proportion - diff
        TargetData.put( index , (int)(result/total) )

    def getNewPath(self):
        return self.newWavEffet