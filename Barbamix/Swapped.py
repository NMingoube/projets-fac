import getopt
import numpy as np
import scipy.io.wavfile as wavfile
import math
import sys


class Swapped:
    def __init__(self,path,piste):
        self.fichierOrig=path
        self.nPiste=piste
        rate, data = wavfile.read(self.fichierOrig)
       
        if(data.ndim>1):
            data = data[:,1]
        tempData = data.copy()
        tempData.setflags(write=1)
        for k in range (0,data.size-1,2):
            tempData.put(k,data.item(k+1))
            tempData.put(k+1,data.item(k))
		
        wavfile.write("Banque\\BarbaMixGenatedSound_effetSwapped"+str(self.nPiste)+"_"+str(id(self))+".wav", rate, tempData.astype(np.int16))
        self.newWavEffet="Banque\\BarbaMixGenatedSound_effetSwapped"+str(self.nPiste)+"_"+str(id(self))+".wav"
        
    def getNewPath(self):
        return self.newWavEffet
