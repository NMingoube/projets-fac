#! python3.6
# -*- coding: utf-8 -*-

"""
Cree le mardi 27/04/2020

@author: L'Equipe Rocco // Corentin BRIAND // Thibaud BARON
"""

from ControllerEffet import ControllerEffet

class AbstractPiste ():
    """
    Classe abstraite de piste


    attributs
    ----------
    VolumeLocal : float
        VolumeLocal de la piste, valeur comprise en 0 et 100
    VolumeGlobal : float
        VolumeGlobal de la piste après application du volume global, valeur comprise en 0 et 100
    Stereo : float
        Valeur de la stereo de la piste, doit être comprise en -100 et 100
    Pitch : float
        Valeur du Pitch de la piste, doit être comprise en 0 et 200
    Mute : bool
        Si la piste est mute (true) ou non (false)
    Precedent : AbstractPiste
        Channel précédent
    Suivant : AbstractPiste
        Channel suivant
    IdChannel : int
        ID de la piste
    Track : Track
        track de la piste pour sauvegarder le fichier en cours
    Effet : ???
        Les effets de la piste
    CrossFade : int
        Le CrossFade de la piste
    RandomState : bool
        Si le random est actif (true) ou non (false)
    RandomPlay : int
        Nombre de fois que le son devra être joué en ??? secondes


    Methodes
    -------
    remove()
        Détruit l'AbstractPiste
        
    getID() : int
        Retourne l'ID de la piste
        
    setID(int ID)
        Change l'ID de la piste
        
    getSuivant() : AbstractPiste
        Retourne la piste suivante
    
    setSuivant(AbstractPiste Suivant)
        Change la piste suivant
        
    getPrecedent() : AbstractPiste
        Retourne la piste precedente
        
    setPrecedent(AbstractPiste Precedent)
        Change le channel precédént de la piste
            
    getVolume() : float
        Retourne le volume de la piste
        
    setVolume(float Volume)
        Change le volume de la piste
        
    getStereo() : float
        Retourne la stéréo de la piste
    
    setStereo(float Stereo)
        Change la stéréo de la piste
        
    getPitch() : float
        Retourne le pitch de la piste
    
    setPitch(float Pitch)
        Change le pitch de la piste
        
    getMute() : boolean
        Retourne l'état du mute de la piste
    
    setMute(boolean Mute)
        Change l'état du mute de la piste

    getEffet(self) : ???
        Retourne les effets de la piste
    
    setEffet(??? Effet)
        Change les effets de la piste
        
    getCrossFade(self) : int
        Retourne le CrossFade de la piste
    
    setCrossFade(int CrossFade)
        Change le CrossFade de la piste
        
    getRandomState() : boolean
        Retourne l'état du random de la piste
    
    setRandomState(boolean RandomState)
        Change l'état du random de la piste
        
    getRandomNbRep() : int
        Retourne le nombre de fois que le son doit être joué
    
    setRandomNbRep(int RandomNbRep)
        Change le nombre de fois que le son doit être joué
    """
    
    def __init__(self,controllerPiste,ID):
        """
        Constructeur de piste
        
        Paramètre(s)
        ----------
        ID : int
            L'ID de la piste
        """
        self.VolumeLocal=100  #Pour max c'est le volume de la piste
        self.VolumeGlobal=100 #Pour max c'est le volume de la piste apres avoir appliquer le volume global
        self.Stereo=0
        self.Pitch=1
        self.Mute = False
        self.Precedent = None
        self.Suivant = None
        self.IdChannel = ID
        self.Effet = None
        self.CrossFade = 0
        self.RandomState = False
        self.RandomNbRep = 0
        self.RandomTemp = 0
        self.controllerEffet = ControllerEffet(controllerPiste,self.IdChannel)

        #   Attribut pour empécher d'activer les fonctionnaltiés de se superposer.
        #   0 : Aucune des fonctionnalités est activé
        #   1 : Crossfade est activé
        #   2 : Random est activé
        self.securityState = 0
        
    def remove(self):
        del(self)

		
    def getControllerEffet(self):
        """
        Return
        ----------
        ControllerEffet : Le ControllerEffet de la piste
        """
        return self.controllerEffet
		
    def getID(self):
        """
        Return
        ----------
        int : L'ID de la piste
        """
        return self.IdChannel
    
    def setID(self,ID):
        """
        Paramètre(s)
        ----------
        ID : int
            Le nouvel ID de la piste
        """
        self.IdChannel=ID
    
    def getSuivant(self):
        """
        Return
        ----------
        AbstractPiste : La piste suivante
        """
        return self.Suivant
    
    def setSuivant(self,Suivant):
        """
        Paramètre(s)
        ----------
        Suivant : AbstractPiste
            La nouvelle piste suivante
        """
        self.Suivant=Suivant
            
    def getPrecedent(self):
        """
        Return
        ----------
        AbstractPiste : La piste précédente
        """
        return self.Precedent
    
    def setPrecedent(self,Precedent):
        """
        Paramètre(s)
        ----------
        Precedent : AbstractPiste
            La nouvelle piste précédente
        """
        self.Precedent=Precedent
            
    def getVolume(self):
        """
        Return
        ----------
        float : Le VolumeLocal de la piste
        """
        return self.VolumeLocal
    
    def setVolume(self,VolumeLocal):
        """
        Paramètre(s)
        ----------
        VolumeLocal : float
            Le nouveau VolumeLocal de la piste
        """
        self.VolumeLocal=VolumeLocal
		            
    def getVolumeGlobal(self):
        """
        Return
        ----------
        float : Le VolumeGlobal de la piste
        """
        return self.VolumeGlobal
    
    def setVolumeGlobal(self,VolumeGlobal):
        """
        Paramètre(s)
        ----------
        VolumeGlobal : float
            Le nouveau VolumeGlobal de la piste
        """
        self.VolumeGlobal=VolumeGlobal
		
    def getStereo(self):
        """
        Return
        ----------
        float : la valeur du stéréo de la piste
        """
        return self.Stereo
    
    def setStereo(self,Stereo):
        """
        Paramètre(s)
        ----------
        Stereo : float
            La nouvelle Stereo de la piste
        """
        self.Stereo=Stereo
        
    def getPitch(self):
        """
        Return
        ----------
        float : La valeur du pitch de la piste
        """
        return self.Pitch
    
    def setPitch(self,Pitch):
        """
        Paramètre(s)
        ----------
        Pitch : float
            La nouvelle valeur du pitch de la piste
        """
        self.Pitch=Pitch
        
    def getMute(self):
        """
        Return
        ----------
        bool : l'état de la piste
        """
        return self.Mute
    
    def setMute(self,Mute):
        """
        Paramètre(s)
        ----------
        Mute : bool
            Le nouvel état du mute de la piste
        """
        self.Mute=Mute
        
    def getEffet(self):
        """
        Return
        ----------
        ??? : Les effets de la piste
        """
        return self.Effet
    
    def setEffet(self,Effet):
        """
        Paramètre(s)
        ----------
        Effet : ???
            Les nouveaux effets de la piste
        """
        self.Effet=Effet
        
    def getCrossFade(self):
        """
        Return
        ----------
        int : La valeur du crossfade de la piste
        """
        return self.CrossFade
    
    def setCrossFade(self,CrossFade):
        """
        Paramètre(s)
        ----------
        CrossFade : int
            La nouvelle valeur du crossfade de la piste
        """
        self.CrossFade=CrossFade
        
    def getRandomState(self):
        """
        Return
        ----------
        bool : L'état du random de la piste
        """
        return self.RandomState
    
    def setRandomState(self,RandomState):
        """
        Paramètre(s)
        ----------
        RandomState : bool
            Le nouvel état du random de la piste
        """
        self.RandomState=RandomState
        
    def getRandomNbRep(self):
        """
        Return
        ----------
        int : Le nombre de fois que le son doit être joué
        """
        return self.RandomNbRep
    
    def setRandomNbRep(self,RandomNbRep):
        """
        Parametres
        ----------
        RandomNbRep : int
            Le nouveau nombre de fois que le son doit être joué
        """
        self.RandomNbRep=RandomNbRep

    def getRandomTime(self):
        """
        Return
        ----------
        int : Le nombre de fois que le son doit être joué
        """
        return self.RandomTime
    
    def setRandomTime(self,time):
        """
        Parametres
        ----------
        RandomTime : int
            l'intervalle de temps où le son se répète.
        """
        self.RandomTime=time

    def getSecurityState(self):
        """
        Return
        ----------
        int : état de la piste selon la fonctionnalité spéciale activé
        """
        return self.securityState

    def setSecurityState(self,value):
        """
        Parametres
        ----------
        value : int
            l'état de la piste si une fonctionnalité spéciale a été activé 
        """
        self.securityState = value
