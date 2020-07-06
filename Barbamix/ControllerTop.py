#! python3.6
# -*- coding: utf-8 -*-


"""
Documentation de la classe ControllerTop

    Version : 15/04/2020  Équipe Rocco Corentin BRIAND
    
    Description :
        Gestion globale du Controller
        
    Attributs :
        topPresentation : topPresentation où sera affichée la présentation de la piste
                
    Constructeur :
        ControllerTop(topPresentation)
        
    Méthodes :
        addPiste(self): Ajoute une piste à la table de mixage
        getVolumeGlobal(self): Récupère la valeur du volume global
        setVolumeGlobal(self,volume): Change la valeur du volume global
        isPlaying(self): Retourne vrai si le mixer est en mute général
        setPlaying(self,bool): Change la valeur du mute général
        listenerVolumeGeneral(self,Volume): Attends le changement de volume global
        listenerPlay(self,State): Attends la lecture
        listenerSave(self): Attends la sauvegarde des paramètres
        listenerLoad(self): Attends le chargement des paramètres
        listenerExport(self): Attends l'exportant du son
        listenerMute(self,Mute): Attends la mise enmute
"""
    

import os
from tkinter import *

from AbstractTop import AbstractTop
from ControllerPiste import ControllerPiste
from ControllerBottom import ControllerBottom
from PresentationTop import PresentationTop
from popupExport import export
from ScrollablePistesFrame import ScrollablePistesFrame
from popupAide import popupAide

class ControllerTop():
    """
    """
    def __init__(self,topPresentation,serveur):
        """
        Paramètre(s)
        ----------
        topPresentation : Master
            Zone d'affichage des présentations
        """
        self.master = topPresentation
        self.serveur = serveur
		
        self.topPresentation = topPresentation
        self.controllerPiste = ControllerPiste(self,self.master)
        self.scrollablePistesFrame = ScrollablePistesFrame(self, self.master)
        self.scrollablePistesFrame.pack(side=RIGHT) 
        self.prensentationTop = PresentationTop(self, self.topPresentation)
        self.abstractTop = AbstractTop()
        self.volumeGlobal = 100
        self.controllerPiste.addPistes(6)
        
        
    def addPiste(self):
        self.controllerPiste.addPistes(1)   
		
#=====================================================================================

    def getVolumeGlobal(self):
        return self.volumeGlobal
		
    def setVolumeGlobal(self,volume):
        self.prensentationTop.setVolumeGlobalValue(volume)
        self.listenerVolumeGeneral(volume)
		
		
    def isPlaying(self):
        return self.abstractTop.isMutedGeneral()
		
    def setPlaying(self,bool):
        self.prensentationTop.setPlayPauseState(bool)
        self.abstractTop.setMuteGeneral(bool)
		
#=====================================================================================
    
    def listenerVolumeGeneral(self,Volume):
        self.abstractTop.setVolumeGeneral(Volume)
        self.volumeGlobal = Volume
        if (not(self.abstractTop.isMutedGeneral())):
            self.controllerPiste.updateVolumeGlobal(Volume)
		
    def listenerNouveauFichier(self):
        request = messagebox.askquestion("Réinitialisation","Voulez-vous réinitialiser l'application ?")
        nbP = self.controllerPiste.getPisteCount()
        if(request == 'yes'):
            self.controllerPiste.removePistes(nbP)
            self.setVolumeGlobal(100)
            self.listenerPlay(True)
            self.controllerPiste.addPistes(6)
		
    def listenerPlay(self,State):
        if( self.abstractTop.isMutedGeneral()):
            self.controllerPiste.updateVolumeGlobal(self.abstractTop.getVolumeGeneral())
            self.abstractTop.setMuteGeneral(False)
        else:
            self.controllerPiste.updateVolumeGlobal(0)
            self.abstractTop.setMuteGeneral(True)
        self.prensentationTop.updatePlayButton(State)
            
			
			
    def listenerSave(self):
        ControllerBottom(self,self.controllerPiste).enregistrement_fichier()
        
    def listenerLoad(self):
        ControllerBottom(self,self.controllerPiste).charger_fichier()
        
    def listenerExport(self):
        export(self.serveur).popupExport()      
        
    def listenerMute(self,Mute):
        self.abstractTop.setMute(Mute)
        
    def listenerAide(self):
        popupAide()