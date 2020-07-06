#! python3.6
# -*- coding: utf-8 -*-

"""
Cree le mardi 10/04/2020

@author: L'Equipe Rocco // Jordan AGARD aka SosoLeBG
"""

class AbstractTop():
    """
    Classe abstraite de Top


    Attributs
    ----------
    VolumeGeneral : float
        Volume général du mixer, doit être comprise en 0 et 100
    Mute : booleen
        Si la piste est mute (true) ou non (false)
    ( Config : string
        Chemin du fichier de sauvegarde du mixer ) # A garder ou pas mais je pense pas
    
    Methodes
    -------
    getVolumeGeneral() : float
        Retourne le volume général
        
    setVolumeGeneral(float Volume)
        Change le volume général
        
    isMutedGeneral() : boolean
        Retourne l'état du mute du mixer
    
    setMuteGeneral(boolean Mute)
        Change l'état du mute du mixer
    """
    
    def __init__(self):
        """
        Constructeur de Top
        
        """
        self.VolumeGeneral=100
        self.MuteGeneral=False
        
    def getVolumeGeneral(self):
        """
        Retourne le volume général
        
        
        Return
        ----------
        float : Le volume général
        """
        return self.VolumeGeneral
    
    def setVolumeGeneral(self,Volume):
        """
        Change le volume général
        
        
        Parametres
        ----------
        Volume : float
            Le nouveau volume général
        """
        self.VolumeGeneral=Volume
    
    def isMutedGeneral(self):
        """
        Retourne l'état du mute du mixer
        
        
        Return
        ----------
        boolean : l'état du mute du mixer
        """
        return self.MuteGeneral
    
    def setMuteGeneral(self,Mute):
        """
        Change l'état du mute du mixer
        
        
        Parametres
        ----------
        Mute : boolean
            Le nouvel état du mute du mixer
        """
        self.MuteGeneral=Mute