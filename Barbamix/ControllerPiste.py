#! python3.6
# -*- coding: utf-8 -*-

"""
Documentation de la classe Controller pour une piste

    Version : 23/04/2020 Équipe Rocco - Thibaud BARON

    Description : 
        Controller est une classe concrète qui va permettre de gérer les différentes pistes ainsi que leurs composantes.
        
    Attributs :
        topPresentation topPresentation où sera affichée la présentation de la piste
        
        Thread : thread pour un canal
        VolumeGlobal : volume global
        
    Méthodes :
        removeChannelID(self,ID): Supprimer la piste, la présentation et le thread ayant l'ID en paramètre
        updateID(self): Mise à jour des ID des pistes, threads et présentations
        getPiste(self,ID): Retourne la piste ayant l'ID corespondant au paramètre
        getPresentation(self,ID): Retourne la présentation ayant l'ID corespondant au paramètre
        getThread(self,ID): Retourne le thread ayant l'ID corespondant au paramètre
        addPistes(self,nbSupplementaire): Ajout de piste(s) à la liste chaînée
        removePistes(self,nbSupprimer): Supprime des piste(s) de la liste chaînée
        getPisteCount(self): Récupère le nombre de pistes
        
        listenerVolume(self,Volume,ID): Attends le changement de la valeur du volume
        updateVolumeGlobal(self,Volume): Mets à jour le volume global
        listenerStereo(self,Stereo,ID): Attends le changement de la valeur du stéréo
        listenerPitch(self,Pitch,ID): Attends le changement de la valeur du pitch
        listenerMute(self,Mute,ID): Attends l'état du Mute
        listenerLoadTrack(self,ID): Attends l'ouverture d'un fichier de type wav ou mp3 et de le charger en tant que "track"
        
        getVolume(self,ID): Récupère la valeur du volume
        setVolume(self,ID,volume): Change la valeur du volume
        getStereo(self,ID): Récupère la valeur du stéréo
        setStereo(self,ID,stereo): Change la valeur du stéréo
        getPitch(self,ID): Récupère la valeur du pitch
        setPitch(self,ID,pitch): Change la valeur du pitch
        getMute(self,ID): Récupère l'état du Mute
        setMute(self,ID,mute): Change l'état du Mute
        getTrack(self,ID): Récupère la piste avec l'ID associé
        getTrackPath(self,ID): Récupère le chemin correspondant à la piste
        setTrackPath(self,ID,path): Change me chemin correspondant à la piste
        getEffet(self,ID): Récupère l'effet associé à la piste
        setEffet(self,ID,effet): Change l'effet associé à la piste
        getCrossFade(self,ID): Récupère la valeur du Crossfade
        setCrossFade(self,ID,crossFade): Change la valeur du Crossfade
        getRandomState(self,ID): Récupère l'état de la lecture aléatoire
        setRandomState(self,ID,randomState): Change l'état de la lecture aléatoire
        getRandomPlay(self,ID): Récupère la valeur de la lecture aléatoire
        setRandomPlay(self,ID,randomPlay): Change la valeur de la lecture aléatoire
"""

import os

from AbstractPiste import AbstractPiste
from PresentationPiste import PresentationPiste
from ThreadChannel import ThreadChannel
from ControllerEffet import ControllerEffet

from tkinter import filedialog
from tkinter import Canvas

class ControllerPiste():
		
    def __init__(self,controllerTop,masterPiste):
        """
        Paramètre(s)
        ----------
        masterPiste : Master
            Zone d'affichage des présentations
        """
        self.controllerTop = controllerTop
        self.masterPiste=masterPiste
        self.Thread = None
        self.Prese = None
        self.Piste = None
        self.Count = 1
        
    def removeChannelID(self,ID):
        """
        Paramètre(s)
        ----------
        ID : int
            L'ID de la piste à supprimer
        """
        deletedPrese = self.getPresentation(ID)
        deletedPiste = self.getPiste(ID)
        deletedThread = self.getThread(ID)
        if(deletedPiste != None):
            if(ID == 1):
                self.Piste=deletedPiste.getSuivant()
                self.Prese=deletedPrese.getSuivant()
                self.Thread=deletedThread.getSuivant()
            else:
                deletedPiste.getPrecedent().setSuivant(deletedPiste.getSuivant())
                deletedPrese.getPrecedent().setSuivant(deletedPrese.getSuivant())
                deletedThread.getPrecedent().setSuivant(deletedThread.getSuivant())
            if(deletedPiste.getSuivant() != None):
                deletedPiste.getSuivant().setPrecedent(deletedPiste.getPrecedent())
                deletedPrese.getSuivant().setPrecedent(deletedPrese.getPrecedent())
                deletedThread.getSuivant().setPrecedent(deletedThread.getPrecedent())
            deletedPiste.getControllerEffet().remove()
            deletedPiste.remove()
            deletedPrese.remove()
            deletedThread.remove()
            self.Count -= 1
            self.updateID()
        
    def updateID(self):
        """
        Mise à jour des ID des pistes, threads et présentations
        """
        id = 1
        changedPrese=self.Prese
        changedPiste=self.Piste
        changedThread=self.Thread
        while(changedPiste != None):
            changedPiste.getControllerEffet().setID(id)
            changedPrese.setID(id)
            changedPiste.setID(id)
            changedThread.setID(id)
            changedPiste = changedPiste.getSuivant()
            changedPrese = changedPrese.getSuivant()
            changedThread = changedThread.getSuivant()
            id += 1

    def getPiste(self,ID):
        """
        Paramètre(s)
        ----------
        ID : int
            L'ID de la piste à trouver
        
        Return
        ----------
        AbstractPiste : La piste ayant l'ID demandé ou None
        """
        getPiste = self.Piste
        while(getPiste != None and getPiste.getID() != ID):
            getPiste=getPiste.getSuivant()
            
        return getPiste
        
    def getPresentation(self,ID):
        """
        Paramètre(s)
        ----------
        ID : int
            L'ID de la présentation à trouver
        
        Return
        ----------
        Presentation : La présentation ayant l'ID demandé ou None
        """
        getPrese = self.Prese
        while(getPrese != None and getPrese.getID() != ID):
            getPrese=getPrese.getSuivant()
        return getPrese
        
        
    def getThread(self,ID):
        """
        Paramètre(s)
        ----------
        ID : int
            L'Id du thread a trouver
        
        Return
        ----------
        Thread : Le thread ayant l'ID demandé ou None
        """
        getThread = self.Thread
        while(getThread != None and getThread.getID() != ID):
            getThread=getThread.getSuivant()
        return getThread
        
        
        
    def addPistes(self,nbSupplementaire):
        """
        Paramètre(s)
        ----------
        nbSupplementaire : int
            Le nombre de channel(s) à ajouter
            
        """
        lastPrese = self.getPresentation(self.Count-1)
        lastPiste = self.getPiste(self.Count-1)
        lastThread = self.getThread(self.Count-1)
        count = 0
        if(self.Count == 1 and nbSupplementaire > 0):
            preCanvas = Canvas(self.controllerTop.scrollablePistesFrame)
            self.Prese = PresentationPiste(self, preCanvas , self.Count)
            self.Piste = AbstractPiste(self,self.Count)
            self.Thread = ThreadChannel(self.Count,self)
            lastPrese = self.Prese
            lastPiste = self.Piste
            lastThread = self.Thread
            count = 1
            self.Count = 2
            self.controllerTop.scrollablePistesFrame.addPresentation(self.Prese)
            
        while(count < nbSupplementaire):
            newPreCanvas = Canvas(self.controllerTop.scrollablePistesFrame)
            newPrese = PresentationPiste(self, newPreCanvas , self.Count)
            newPiste = AbstractPiste(self,self.Count)
            newThread = ThreadChannel(self.Count,self)
            lastPrese.setSuivant(newPrese)
            lastPiste.setSuivant(newPiste)
            lastThread.setSuivant(newThread)
            newPrese.setPrecedent(lastPrese)
            newPiste.setPrecedent(lastPiste)
            newThread.setPrecedent(lastThread)
            lastPrese = newPrese
            lastPiste = newPiste
            lastThread = newThread
            count += 1
            self.Count += 1
            self.controllerTop.scrollablePistesFrame.addPresentation(newPrese)
                
    def removePistes(self,nbSupprimer):
        """
        Paramètre(s)
        ----------
        nbSupprimer : int
            Le nombre de channel(s) à supprimer
            
        """
        lastPrese = self.getPresentation(self.Count-1)
        lastPiste = self.getPiste(self.Count-1)
        lastThread = self.getThread(self.Count-1)
        count = 0
        while(lastPiste != None and count < nbSupprimer):
            deletePrese = lastPrese
            deletePiste = lastPiste
            deleteThread = lastThread
            if(deletePrese.getPrecedent() == None):
                self.Prese=None
                self.Piste=None
                self.Thread=None
            else:
                lastPrese = deletePrese.getPrecedent()
                lastPiste = deletePiste.getPrecedent()
                lastThread = deleteThread.getPrecedent()
                lastPrese.setSuivant(None)
                lastPiste.setSuivant(None)
                lastThread.setSuivant(None)
            deletePiste.remove()
            deletePrese.remove()
            deleteThread.remove()
            count += 1
            self.Count -= 1
			
    def getPisteCount(self):
        return self.Count-1
		
    def endRandom(self):
        id = 1
        while(id < self.Count):
            self.getThread(id).track.random(0,0)
            id = id +1
			
            
#=====================================================================================

    def listenerVolume(self,Volume,ID):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            changedPiste.setVolume(Volume)
            changedPiste.setVolumeGlobal(Volume*(self.controllerTop.getVolumeGlobal()/100))
            if(not(changedPiste.getMute())):
                changedThread.setAttribute("volume",Volume*(self.controllerTop.getVolumeGlobal()/100))
                
    def updateVolumeGlobal(self,Volume):
        changedPiste = self.Piste
        changedThread = self.Thread
        while(changedPiste != None):
            changedPiste.setVolumeGlobal(changedPiste.getVolume()*(Volume/100))
            if(not(changedPiste.getMute())):
                changedThread.setAttribute("volume",changedPiste.getVolumeGlobal())
            changedPiste=changedPiste.getSuivant()
            changedThread=changedThread.getSuivant()
            
    def listenerStereo(self,Stereo,ID):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            changedPiste.setStereo(Stereo)
            changedThread.setAttribute("stereo",-Stereo)
            
    def listenerPitch(self,Pitch,ID):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            changedPiste.setPitch(Pitch)
            changedThread.setAttribute("pitch",Pitch)
            
    def listenerMute(self,Mute,ID):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            changedPiste.setMute(Mute)
            if(Mute):
                changedThread.setAttribute("mute",0)
            else:
                changedThread.setAttribute("mute",changedPiste.getVolumeGlobal())
            self.getPresentation( ID ).refreshMuteState( Mute )
            
    def listenerLoadTrack(self,ID):  #Methode permettant d'ouvrir un fichier de type wav ou mp3 et de le charger en tant que "track"
        changedPiste = self.getPiste(ID)
        changedPrese = self.getPresentation(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            newTrackName = filedialog.askopenfile(filetypes=[('wav file','.wav'),('mp3 file','.mp3')],title='Choose a file', initialdir=os.getcwd()+"/lib/")
            if(newTrackName != None):
                changedThread.setSound(newTrackName.name)
                changedPrese.setName(os.path.basename(newTrackName.name))
                changedPiste.getControllerEffet().setPath(newTrackName.name)
				


    def listenerCrossFade( self , crossFade , ID ):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            if(crossFade):
                changedPiste.setCrossFade( 20 )
                changedPiste.setSecurityState( 1 )
            else:
                changedPiste.setCrossFade( 0 )
                changedPiste.setSecurityState( 0 )
            changedPiste.setRandomState( False )

            changedThread.setAttribute("crossfade",changedPiste.getCrossFade())
            
            changedPresentation = self.getPresentation( ID )
            changedPresentation.refreshCrossFadeState( crossFade )
            changedPresentation.resetRandomTexts()

    def listenerRandom(self , nbRep, timeInt , ID):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        if(changedPiste != None):
            changedPiste.setRandomState( nbRep != 0 and timeInt != 0 )
            changedPiste.setRandomNbRep( nbRep )
            changedPiste.setRandomTime( timeInt )
            changedThread.setAttribute( "random" , [ nbRep , timeInt ] )
            changedPiste.setSecurityState( 2 )
            changedPiste.setCrossFade(0)
            self.getPresentation( ID ).refreshCrossFadeState( False )

    def listenerEffet( self , ID ):
        changedPiste = self.getPiste(ID)
        changedThread = self.getThread(ID)
        path = self.getTrackPath(ID)
        if(changedPiste != None):
            changedPiste.getControllerEffet().start()

#=====================================================================================

    def getVolume(self,ID):
        return self.getPiste(ID).getVolume()
    
    def setVolume(self,ID,volume):
        self.getPresentation(ID).setVolumeValue(volume)
        self.listenerVolume(volume,ID)
        
    def setVolumeGlobal(self,ID,VolumeGlobal):
        self.getPiste(ID).setVolumeGlobal(VolumeGlobal)
		
    def getVolumeGlobal(self,ID):
        return self.getPiste(ID).getVolumeGlobal()
        
    def getStereo(self,ID):
        return self.getPiste(ID).getStereo()
    
    def setStereo(self,ID,stereo):
        self.getPresentation(ID).setStereoValue(stereo)
        self.listenerStereo(stereo,ID)
        
    def getPitch(self,ID):
        return self.getPiste(ID).getPitch()
    
    def setPitch(self,ID,pitch):
        self.getPresentation(ID).setSpeedValue(pitch)
        self.listenerPitch(pitch,ID)
        
    def getMute(self,ID):
        return self.getPiste(ID).getMute()
    
    def setMute(self,ID,mute):
        self.getPresentation(ID).refreshMuteState(mute)
        self.listenerMute(mute,ID)
        
    def getTrack(self,ID):
        return self.getThread(ID).getTrack()
		
    def getTrackPath(self,ID):
        return self.getThread(ID).getTrack().getSource()
    
    def setTrackPath(self,ID,path):
        if(os.path.basename(path).startswith("BarbaMixGenatedSound_")):
             self.getPresentation(ID).setName(os.path.basename(self.getPiste(ID).getControllerEffet().getOriginalPath()))
        elif(os.path.basename(path) != "silence.wav"):
             self.getPresentation(ID).setName(os.path.basename(path))
        else:
             self.getPresentation(ID).setName("Veuillez charger un son")
        self.getThread(ID).setSound(path)
        
    def getEffet(self,ID):
        return self.getPiste(ID).getEffet()
    
    def setEffet(self,ID,effet):
        self.getPiste(ID).setEffet(effet)
        
    def getCrossFade(self,ID):
        return self.getPiste(ID).getCrossFade()
    
    def setCrossFade(self,ID,crossFade):
        self.getPiste(ID).setCrossFade(crossFade)
        
        
    def getRandomState(self,ID):
        return self.getPiste(ID).getRandomState()
    
    def setRandomState(self,ID,randomState):
        self.getPiste(ID).setRandomState(randomState)
        
    def getRandomTime(self,ID):
        return self.getPiste(ID).getRandomTime()
    
    def setRandomTime(self,ID,randomTime):
        self.getPiste(ID).setRandomTime(randomTime)

    def getRandomNbRep(self,ID):
        return self.getPiste(ID).getRandomTime()
    
    def setRandomNbRep(self,ID,randomNbRep):
        self.getPiste(ID).setRandomNbRep(randomNbRep)





