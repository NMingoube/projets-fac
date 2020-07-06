#! python3.6
# -*- coding: utf-8 -*-

"""
@author: Nathan Mingoube & Ferragu Thomas
"""

# importe le module graphique TK


from tkinter import *
import os
import tkinter as tk
import tkinter.filedialog
from pyo import *
from time import *
from os import path
import wave
import contextlib
from random import randint

# @Author: Nathan Mingoube & Ferragu Thomas, Groupe trébuchet
# @Name: Track class
# @Date: 02/02/2020
# @Version: 1.0.0
# @Dependencies: pyo librairies


class Track:

    def __init__(self, pth):  # Constructor, overrides setSource()

        self.__pitch = 1.0  # Pitch (highness) of the sound
        self.__xfade = 0  # Crossfade (in % of total duration)
        self.__mul = 1  # Multiplicator of sound speed OVERRIDEN
        self.__start = 0  # Offset to start
        self.__level = 1  # Sound level modifier
        self.__gain = 0  # Gain modifier
        self.__pan = 0.0  # PAN of the sound [-1.0;1.0]. Set to -1.0 to have the sound 100% to the right or 1.0 to have the sound 100% to the left (may be the other way around)
        self.__path = pth  # Absolute path to sound file
        with contextlib.closing(wave.open(self.__path,'r')) as f:
            self.__soundDuration = f.getnframes() / f.getframerate()
        self.__srcTable = SndTable(self.__path)  # Sound file
        self.__looper = Looper(self.__srcTable)  # Instance of the sound
        self.__timePause = 0;
        self.__timeStart = 0;
        self.controlValue = 0;

    def setPitch(self, pitch):  # Sets pitch of the sound
        self.__pitch = pitch

    def getPitch(self):  # Return pitch of the sound
        return self.__pitch

    def setXFade(self, xFade):  # Sets xFade of the sound
        self.__xfade = xFade

    def getXFade(self):  # Return xFade of the sound
        return self.__xfade

    def setMul(self, mul):  # Sets Mul of the sound
        self.__mul = mul

    def getMul(self):  # Return Mul of the sound
        return self.__mul

    def setStart(self, start):  # Sets start point of the sound
        self.__start = start

    def getStart(self):  # Return start point of the sound
        return self.__start

    def setLevel(self, lv):  # Sets relative level of the sound in dB
        self.__srcTable.mul = lv
        self.__level = lv

    def getLevel(self):  # Returns level of the sound in dB
        return self.__level

    def setGain(self, gain):  # Sets gain of the sound
        self.__gain = gain

    def getGain(self):  # Return gain of the sound
        return self.__gain

    def setPan(self, pn):  # Sets the pan (stereo)
        self.__pan = pn

    def getPan(self):  # Returns the pan (stereo)
        return self.__pan

    def setSource(self, path):  # Sets source to the audio file
        self.__path = path
        self.__srcTable = SndTable(path)
        self.__looper = Looper(self.__srcTable)
        self.resetLooper()
        with contextlib.closing(wave.open(self.__path,'r')) as f:
            self.__soundDuration = f.getnframes() / f.getframerate()

    def getSource(self):  # Returns source file
        return self.__path
		
    def restartSound( self ):
        """
            Méthode pour redémarrer le son
            Contrairement au initSound, il joue le son à partir de self.__start
        """
        self.__initSound( time = self.__start )
        self.__looper = self.__looper.mix(2).out()
        self.__timeStart = time()
        self.__timePause = time()
		
    def getSoundDuration(self):  # Returns the duration of the sound file
        return self.__soundDuration

    def __initSound(self, time=0):  # Initiates the looper class and summons its controls
        self.__srcTable = SndTable(path=self.__path, start=time)
        self.__looper = Looper(table=self.__srcTable, pitch=self.__pitch, dur=self.getSoundDuration(), xfade=self.__xfade, autosmooth=True, mul=[self.__level * (1 + self.__pan), self.__level * (1 - self.__pan)])

    def playSound(self):  # Plays the sound
        if (self.__timePause != 0) :
            self.__initSound( time = ( self.__timePause - self.__timeStart ) % self.getSoundDuration())
            self.__timeStart = self.__timePause - ( self.__timePause - self.__timeStart ) % self.getSoundDuration()
        else:
            self.__initSound()
            self.__timeStart = time()
        self.__looper = self.__looper.mix(2).out()
        self.__timePause = time()
		

    def pause(self):
        self.__looper = self.__looper.stop()
        self.__timePause = time()

    def getPause(self):
        self.__timePause = time()
        return (self.__timePause - self.__timeStart) % self.getSoundDuration()
		
    def resetLooper(self):
        self.__timePause = time()
        self.__timeStart = time()

    def export(self):
        res={
                "level" : self.__level,
                "gain" : self.__gain,
                "pan" : self.__pan,
                "pitch" : self.__pitch,
                "xfade" : self.__xfade,
                "start" : self.__start,
                "path" : self.__path
            }
        return res
		
    def random(self, nbRep, timeInt):
        self.controlValue = self.controlValue + 1;
        self.__looper = self.__looper.stop()
        self.nbRep = nbRep
        self.timeInt = timeInt
        if (nbRep != 0 and timeInt != 0):
            sd = self.getSoundDuration()
            if((self.nbRep*sd) > self.timeInt):
                tkinter.messagebox.showerror(title="Erreur de valeur", message="Un son de " + str(round(sd, 2)) +" seconde(s) ne peut pas être lu " + str(self.nbRep) +" fois sur " + str(self.timeInt) + " seconde(s) !")
            else:
                threading.Thread(target=self.launchRandom).start()
				
	
    def launchRandom(self):
        control = self.controlValue
        threading.Thread(target=self.privateRandom).start()
        sleep(self.timeInt)
        if(self.controlValue == control):
            self.launchRandom()
	
    def privateRandom(self): 
    #nbRep : le nombre de fois que l'on veut que le son se répète dans timeInt l'interval de temps
        control = self.controlValue
        sd = self.getSoundDuration()
        nombreRep = self.nbRep
        nbMax = int(self.timeInt / sd)
        while(nombreRep > 0 and nbMax > 0):
            luck = randint(0,100) - ((nbMax-nombreRep)*10)
            if(luck < 0):
                luck = 0
            alea = randint(luck,100)
            if(alea >= 50 or nombreRep == nbMax):
                if(self.controlValue == control):
                    self.playSound()
                nombreRep = nombreRep - 1
            sleep(sd)
            self.__looper = self.__looper.stop()
            self.resetLooper()
            nbMax = nbMax - 1	
