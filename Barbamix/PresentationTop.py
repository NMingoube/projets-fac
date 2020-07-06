#! python3.6
# -*- coding: utf-8 -*-

"""
Documentation de la classe PresentationTop

    Version : 17/04/2020  Équipe ROCCO

	Participant:	Maxence CONAN
					Thibaud BARON

    Description :
        Présentation globale de la table de mixage.
        
    Attributs :
        controller : controller de la piste
        topPresentation : topPresentation où sera affichée la présentation de la piste
        
        volumeGlobalSlider : gestion du volume global à l'aide d'un slider
        soundButton : bouton gérant la pause du son
        addChannel : bouton gérant l'ajout de pistes
        saveButton : bouton gérant la sauvegarde les paramètres
        loadButton : bouton gérant le chargement des paramètres
        exportButton : bouton gérant l'exportation d'un fichier
        
    Constructeur :
        PresentationTop(controller, topPresentation)
        
    Méthodes :
        setVolumeGlobalValue(self,volumeValue) : Change la valeur du volume global
        setPlayPauseState(self,playState) : Change l'image du bouton
        modifyVolumeGlobalValue(self,val): Signale le changement de la valeur du volume global
        save_file(self): Signale le début d'une sauvegarde
        load_file(self): Signale le début d'une restauration
        export_file(self): Signale le début d'une exportation
        clickedSoundButton(self): Signale au controller de mute/unmute la piste et met à jour le bouton
"""

import tkinter
import os.path
from tkinter import *

class PresentationTop (Frame):
	def __init__(self, controller, topPresentation):
		super().__init__(topPresentation)
		self.topPresentation = topPresentation
		self.controller = controller
		
		
		soundOff=tkinter.PhotoImage(file="Images/pause.png",master=self.topPresentation)
		self.soundButton = Button(self,image=soundOff, command = self.clickedSoundButton )
		self.soundButton.image = soundOff
		self.soundButtonState = False
		
		self.soundButton.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 2', height = 1 )
		self.spacerLabel.pack()
		
		self.volumeGlobalSlider = Scale(self , orient=VERTICAL, command = self.modifyVolumeGlobalValue,background="white", troughcolor='#C8C8C8' , activebackground="#D9D9D9",font='Helvetica 12 bold',borderwidth=1 , cursor="hand2" , highlightthickness=0 ,  width = 20, length = 150 , sliderlength = 40)
		self.volumeGlobalSlider.config(from_ = 100, to = 0)
		self.setVolumeGlobalValue(100)
		self.volumeGlobalSlider.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 8', height = 1 )
		self.spacerLabel.pack()
		
		self.addChannel = Button(self,text= "Ajouter une piste", command=self.controller.addPiste,width=22, height = 2,cursor="hand2", background='#C8C8C8',font="Helvetica 12 bold", activebackground = "#B9B9B9")
		self.addChannel.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 6', height = 1 )
		self.spacerLabel.pack()
		
		self.saveButton = Button(self,text= "Sauvegarder les\nparamètres",command=self.save_file,width=22 , height = 2 ,cursor="hand2", background='#C8C8C8',font="Helvetica 12 bold", activebackground = "#B9B9B9")
		self.saveButton.pack()
		
		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1 )
		self.spacerLabel.pack()

		self.loadButton = Button(self,text= "Charger de\nparamètres",command=self.load_file,width=22 , height = 2 , cursor="hand2", background='#C8C8C8',font="Helvetica 12 bold", activebackground = "#B9B9B9")
		self.loadButton.pack()
		
		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 6', height = 1 )
		self.spacerLabel.pack()

		self.exportButton = Button(self,text = "Exporter",command=self.export_file,width=22 , height = 2,cursor="hand2", background='#C8C8C8',font="Helvetica 12 bold", activebackground = "#B9B9B9")
		self.exportButton.pack()
		
		self.configure(background="#FFF")
		self.pack(side = LEFT)
		
		
	def setVolumeGlobalValue(self,volumeValue) : 
		"""
      Paramètre(s)
		-------------
		volumeValue : float Valeur du volume de la piste.

		"""
		self.volumeGlobalSlider.set(volumeValue)
		
		
	def setPlayPauseState(self,playState) : 
		"""
      Paramètre(s)
		-------------
		playState : boolean état de l'image

		"""
		if playState:
			soundOn=tkinter.PhotoImage(file="Images/play.png",master=self.topPresentation)
			self.soundButton.config(image=soundOn)
			self.soundButton.image = soundOn
			self.soundButtonState = True
		else:
			soundOff=tkinter.PhotoImage(file="Images/pause.png",master=self.topPresentation)
			self.soundButton.config(image=soundOff)
			self.soundButton.image = soundOff
			self.soundButtonState = False
		
	"""
	----------------------------Signal-----------------------------------------
	"""
	
	def modifyVolumeGlobalValue(self,val):
		self.controller.listenerVolumeGeneral(int(val))
		
	def save_file(self):
		self.controller.listenerSave()

	def load_file(self):
		self.controller.listenerLoad()

	def export_file(self):
		self.controller.listenerExport()

	def clickedSoundButton(self):
		if self.soundButtonState:
			soundOff=tkinter.PhotoImage(file="Images/pause.png",master=self.topPresentation)
			self.soundButton.config(image=soundOff)
			self.soundButton.image = soundOff
			self.soundButtonState = False
		else:
			soundOn=tkinter.PhotoImage(file="Images/play.png",master=self.topPresentation)
			self.soundButton.config(image=soundOn)
			self.soundButton.image = soundOn
			self.soundButtonState = True
		self.controller.listenerPlay(self.soundButtonState)
