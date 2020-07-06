#! python3.6
# -*- coding: utf-8 -*-

"""
Groupe Fusée

- Allan RUNEGO
- Clément Quere
- Liam Hô
- Pierre-Alexandre Obin
- Martin Boussion

Scripte python de sauvegarde des paramètres de la table de mixeur dans un fichier en format json
"""
import json
import os
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import pathlib
from pydub import AudioSegment

class AbstractBottom:
    def __init__(self):
        self.dico = {}  #Création du dictionnaire
        
    def getDico(self):
        return self.dico
    
    def setDico(self,dico):
        self.dico = dico
        
    def addNbPiste(self,nbP): #nombre de piste
        self.dico['nb_piste'] = []
        self.dico['nb_piste'].append({'nbp': nbP})
    
    def addSavePiste(self,controllerTop,controllerPiste):    #Enregistre une piste$
        nbP = controllerPiste.getPisteCount()
        self.addNbPiste(nbP)
        
        i = 1
        while(i <= nbP):
            self.dico[i] = []
            self.dico[i].append({
                'volume': controllerPiste.getVolume(i),
                'volumeGlobal': controllerPiste.getVolumeGlobal(i),
                'stereo': controllerPiste.getStereo(i),
                'pitch': controllerPiste.getPitch(i),
                'mute': controllerPiste.getMute(i),
                'path': controllerPiste.getTrackPath(i),
                'effet': controllerPiste.getEffet(i),
                'crossFade': controllerPiste.getCrossFade(i),
                'randomState': controllerPiste.getRandomState(i)#,
                #'randomPlay': controllerPiste.getRandomPlay(i)
            })
            i+=1
            
        self.addSaveGlobal(controllerTop)

    def addSaveGlobal(self,controllerTop):   #Enregistre le volume global
        self.dico['global'] = []
        self.dico['global'].append({'volume': controllerTop.getVolumeGlobal(),'pause': controllerTop.isPlaying()})
    
    def getValeur(self,piste,valeur):   #Retourne la valeur de la variable
        for i in self.dico[piste]:      #le numéro de la piste
            return i[valeur]            #Retourne la valeur de la variable

    def loadPiste(self,controllerTop,controllerPiste):       #Initialise le track de la piste
        nbPC = controllerPiste.getPisteCount()      #nombre de piste courante
        nbPL = self.getValeur('nb_piste','nbp')     #nombre de piste enregistrer
        
        controllerTop.setVolumeGlobal(self.loadGlobal())
        controllerTop.setPlaying(self.loadPlayingGlobal())
        
        if(nbPC < nbPL):
            controllerPiste.addPistes(nbPL-nbPC)
        else:
            controllerPiste.removePistes(nbPC-nbPL)
        i = 1
        while(i <= nbPL):
            controllerPiste.setVolume(i,self.getValeur(str(i),'volume'))
            controllerPiste.setVolumeGlobal(i,self.getValeur(str(i),'volumeGlobal'))
            controllerPiste.setStereo(i,self.getValeur(str(i),'stereo'))
            controllerPiste.setPitch(i,self.getValeur(str(i),'pitch'))
            controllerPiste.setMute(i,self.getValeur(str(i),'mute'))
			
			#verifier si le fichier existe
            fichier = self.getValeur(str(i),'path') #TODO verife fichier
            if not(os.path.isfile(fichier)):
                messagebox.showwarning("fichier manquant","Ce fichier n'existe pas: " + os.path.basename(fichier))
                request = messagebox.askquestion("Charger fichier","Voulez-vous charger un nouveau fichier ?")
                if(request == 'yes'):
                    fichier = filedialog.askopenfilename(initialdir = "..\Banque",filetypes=[("wav file","*.wav"),('mp3 file','.mp3')])
                    if (fichier):
                        controllerPiste.setTrackPath(i,fichier)
                    else:
                        controllerPiste.setTrackPath(i,'Banque\silence.wav')
                else:
                    controllerPiste.setTrackPath(i,'Banque\silence.wav')

			
            controllerPiste.setEffet(i,self.getValeur(str(i),'effet'))
            controllerPiste.setCrossFade(i,self.getValeur(str(i),'crossFade'))
            controllerPiste.setRandomState(i,self.getValeur(str(i),'randomState'))
            #controllerPiste.setRandomPlay(i,self.getValeur(str(i),'randomPlay'))
            i+=1
			
    def loadGlobal(self):
        return self.getValeur('global','volume') #Retourne la valeur du volume global enregistré
		
    def loadPlayingGlobal(self):
        return self.getValeur('global','pause') #Retourne le boolean play/pause