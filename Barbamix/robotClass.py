import getopt
import numpy as np
import scipy.io.wavfile as wavfile
import math
import sys
from waveshaper import Waveshaper
# Diode constants (must be below 1; paper uses 0.2 and 0.4)
VB = 0.2
VL = 0.4

# Controls distortion
H = 4

# Controls N samples in lookup table; probably leave this alone
LOOKUP_SAMPLES = 1024

# Frequency (in Hz) of modulating frequency
MOD_F = 50

class Robot:
    def __init__(self,path,piste):
        self.fichierOrig=path
        self.nPiste=piste
        #print(self.fichierOrig)
        rate, data = wavfile.read(self.fichierOrig)
	   
        if(data.ndim>1):
            data = data[:,1]

        # get max value to scale to original volume at the end
        scaler = np.max(np.abs(data))

        # Normalize to floats in range -1.0 < data < 1.0
        data = data.astype(np.float)/scaler

        # Length of array (number of samples)
        n_samples = data.shape[0]

        # Create the lookup table for simulating the diode.
        d_lookup = self.diode_lookup(LOOKUP_SAMPLES)
        diode = Waveshaper(d_lookup)

        # Simulate sine wave of frequency MOD_F (in Hz)
        tone = np.arange(n_samples)
        tone = np.sin(2*np.pi*tone*MOD_F/rate)

        # Gain tone by 1/2
        tone = tone * 0.5

        # Junctions here
        tone2 = tone.copy() # to top path
        data2 = data.copy() # to bottom path

        # Invert tone, sum paths
        tone = -tone + data2 # bottom path
        data = data + tone2 #top path

        #top
        data = diode.transform(data) + diode.transform(-data)

        #bottom
        tone = diode.transform(tone) + diode.transform(-tone)

        result = data - tone

        #scale to +-1.0
        result /= np.max(np.abs(result))
        #now scale to max value of input file.
        result *= scaler
        # wavfile.write wants ints between +-5000; hence the cast
        wavfile.write("Banque\\BarbaMixGenatedSound_effetRobot"+str(self.nPiste)+"_"+str(id(self))+".wav", rate, result.astype(np.int16))
        self.newWavEffet="Banque\\BarbaMixGenatedSound_effetRobot"+str(self.nPiste)+"_"+str(id(self))+".wav"
        

    def diode_lookup(self, n_samples):
        result = np.zeros((n_samples,))
        for i in range(0, n_samples):
            v = float(i - float(n_samples)/2)/(n_samples/2)
            v = abs(v)
            if v < VB:
                result[i] = 0
            elif VB < v <= VL:
                result[i] = H * ((v - VB)**2)/(2*VL - 2*VB)
            else:
                result[i] = H*v - H*VL + (H*(VL-VB)**2)/(2*VL-2*VB)

        return result

    def raw_diode(self,signal):
        result = np.zeros(signal.shape)
        for i in range(0, signal.shape[0]):
            v = signal[i]
            if v < VB:
                result[i] = 0
            elif VB < v <= VL:
                result[i] = H * ((v - VB)**2)/(2*VL - 2*VB)
        else:
            result[i] = H*v - H*VL + (H*(VL-VB)**2)/(2*VL-2*VB)
        return result
    def getNewPath(self):
        return self.newWavEffet
