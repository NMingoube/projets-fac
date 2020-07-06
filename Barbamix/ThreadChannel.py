#! python3.6
# -*- coding: utf-8 -*-

from threading import Thread
from Track import Track
import pathlib
from pyo import *
from time import *

import pydub

class ThreadChannel(Thread):
    
    """
    Thread pour un canal 
    (1 canal = 1 ThreadChannel)
    """
    
    def __init__(self, id, controller):
        Thread.__init__(self)
        self.controller = controller
        self.precedentPiste = None
        self.suivantPiste = None
        self.id = id
        self.track = Track("Banque/silence.wav")
        #Creation du thread pour la lecture du son
        self.thPlaySound = ThreadPlaySound(self.track)
        #Creation du thread pour la modification du son
        self.thModifySound = ThreadModifySound(self.thPlaySound, self.track, self)
        
    def run(self):
        #Lancement des threads
        self.thPlaySound.start()
        self.thModifySound.start()
        
    def getThPlaySound(self):
        """
        Retourne le thPlaySound, le thread qui s'occupe de jouer/mettre en pause le son
        
        
        Return
        ----------
        ThreadModifySound : Le thread de modification du son
        """
        return self.thPlaySound
    
    def getThModifySound(self):
        """
        Retourne le thModifySound, le thread qui s'occupe de la modification du son
        
        
        Return
        ----------
        ThreadModifySound : Le thread de modification du son
        """
        return self.thModifySound
    
    def getID(self):
        """
        Retourne l'ID de la piste
        
        
        Return
        ----------
        int : L'ID de la piste
        """
        return self.id
    
    def setID(self,id):
        """
        Change l'ID de la piste
        
        
        Parametres
        ----------
        id : int
            Le nouvel ID de la piste
        """
        self.id = id

    def getSuivant(self):
        """
        Retourne la piste suivante
        
        
        Return
        ----------
        AbstractPiste : La piste suivante
        """
        return self.suivantPiste
    
    def setSuivant(self,suivant):
        """
        Change la piste suivant
        
        
        Parametres
        ----------
        suivant : AbstractPiste
            La nouvelle piste suivante
        """
        self.suivantPiste=suivant
            
    def getPrecedent(self):
        """
        Retourne la piste précédente
        
        
        Return
        ----------
        AbstractPiste : La piste précédente
        """
        return self.precedentPiste
    
    def setPrecedent(self,precedent):
        """
        Change le channel précédent de la piste
        
        
        Parametres
        ----------
        precedent : AbstractPiste
            La nouvelle piste précédent
        """
        self.precedentPiste=precedent
    
    def getTrack(self):
        return self.track

    def setAttribute(self, attr, val):
        self.thModifySound.setAttribute(attr, val)
    
    def play(self):
        self.thPlaySound.play()
    
    def pause(self):
        self.thPlaySound.pause()

    def setSound(self, pth):
        if pathlib.Path(pth).suffix == '.mp3':
            fichier = (str(pathlib.Path(pth).parent) + "\\" + pathlib.Path(pth).stem + ".wav").replace("\\","/")
            pydub.AudioSegment.from_file(pth,"mp3").export(fichier, format="wav")
            self.thPlaySound.setSound(fichier)
        else:
            self.thPlaySound.setSound(pth)
    def remove(self):
        self.track.pause()
        del(self)

class ThreadPlaySound(Thread):
    
    """
    Thread pour la lecture du son 
    """
    
    def __init__(self, trck):
        Thread.__init__(self)
        self.__track__ = trck
    
    def run(self):
        self.__track__.playSound()                      #Lancement du son
    
    def play(self):
        self.__track__.playSound()                      #Lancement du son

    def pause(self):
        self.__track__.pause()
    
    def setSound(self, pth):
        self.__track__.setSource(pth)
        self.__track__.playSound() 
   
        
class ThreadModifySound(Thread):
    
    """
    Thread pour la modification du son
    """
    
    def __init__(self, thPlaySound, trck, threadChannel):
        Thread.__init__(self)
        self.threadChannel = threadChannel
        self.__track__=trck
        self.__sound__=thPlaySound
        self.controlValue = 0

    def run(self):
        temp=0

    def setAttribute(self, attr, val):
        """
        Modifie un attribut de la track
        pause
        
        Parametres
        ----------
        attr : l'attribut à modifier
        val : la valeur à donner à l'attribut
        """

        #boolean pour indiquer si un son a été relancé
        replayed = False
        self.controlValue = self.controlValue + 1
        if attr == 'volume':
            self.__track__.setLevel(val/50)
        elif attr == 'stereo':
            self.__track__.setPan(val)
        elif attr == 'pitch':
            self.__track__.setPitch(val)
        elif attr == 'random':
            self.__track__.setXFade(0)
            self.__track__.random(val[0],val[1])
        elif attr == 'crossfade':
            self.__track__.random(0,0)
            self.__track__.setXFade(val)
            self.__track__.restartSound()
            replayed = True
        elif attr == 'mute':
            if(val == 0):
                self.__track__.setLevel(0)
                self.__track__.resetLooper()
                self.__track__.playSound()
                replayed = True
            else:
                self.__track__.setLevel(val/100)
				
        if( not(replayed) ):
            if(not(self.threadChannel.controller.getRandomState(self.threadChannel.id))):
                if( self.__track__.getXFade() == 0 ):
                    self.reLoad()
                else:

                    self.__track__.restartSound()

                
    def reLoad(self):
        self.remaining = (self.__track__.getSoundDuration() - self.__track__.getPause()) * ( 100-self.__track__.getXFade() )/100
        self.restart = threading.Thread( target=self.restartTrack )
        self.__track__.playSound()
        self.restart.start()
        
    def restartTrack(self):
        control = self.controlValue
        sleep( self.remaining )
        if( control == self.controlValue ):
            self.__track__.resetLooper()
            self.__track__.playSound()
