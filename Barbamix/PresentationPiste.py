#! python3.6
# -*- coding: utf-8 -*-

from tkinter import *
from knob import Knob
import sys
import os.path


"""
Documentation de la classe Presentation pour une piste

	Version : 23/04/2020 Thibaud BARON Equipe ROCCO

	Participant : Thibaud BARON

	Description :

		Présentation est une classe concrète qui va permettre d'afficher les boutons, les informations ,... à l'utilisateur pour une seule piste associée.
		Présentation connait la présentation de la piste suivante et la présentation de la piste précédente, ce qui permet former une liste chainée.

	Attribut :

		canvas : canvas où sera affichée la présentation de la piste
		idPiste : Numéro de la piste
		controller : Controller de la piste

		suivant : Presentation de la piste suivant  
		precedent : Presentation de la piste precedent
		
		window : Fenêtre qui contient la piste, permettant de la déplacer dans le canvas géré par la scrollbar
		idLabel : Texte affichant le numéro de la piste
		nameLabel : Texte affichant le nom du son
		loadButton : Bouton pour charger un son
		stereoLabel : Texte affichant "Stéréo"
		stereoKnob : bouton tournant pour sélectionner la valeur de la stéréo
		volumeLabel : Texte affichant "Volume"
		soundSlider : curseur pour sélectionner la valeur du volume
		speedLabel : Texte affichant "Pitch"
		speedKnob : Knob pour sélectionner la valeur de vitesse
		muteLabel : Texte pour afficher le "Mute"
		muteButtonState : Boolean pour si le son est mise en sourdine
		muteButton : Bouton pour mettre en sourdine
		effectButton : Bouton pour les effets
		crossFadeButtonState : Boolean pour si le son est mise en crossfade
		crossFadeButton : Bouton pour activer le crossFade
		randomButton : Button pour activer le random

	Constructeur:
		PresentationPiste(controller, canvas , idPiste)

	Methode :
		open_file(self) : Méthode qui signale l'importation d'un son.
		setName(self, name) : Change le nom à afficher
		remove(self) : Méthode qui détruit la présentation
		setId(self,id) : Méthode qui change le numéro d'identité
		getId(self) : Méthode qui renvoie le numéro d'identité
		getSuivant(self) : Méthode qui renvoie la présentation de la piste suivante
		setSuivant(self,suivant) : Méthode qui change la présentation de la piste suivante
		getPrecedent(self) : Méthode qui renvoie la présentation de la piste précédente
		setPrecedent(self) : Méthode qui renvoie la présentation de la piste précédente
		isMuted(self) : Méthode qui renvoie le boolean de si le son est mute ou pas, c'est à dire si le bouton mute est enfoncé.
		refreshMuteState(self,muteState) : Méthode qui met à jour l'état du bouton mute
		setVolumeValue(self,volumeValue) : Méthode qui change la valeur du VolumeSlider.
		setStereoValue(self,stereoValue) : Méthode qui change la valeur du StéréoKnob.
		setSpeedValue( self,SpeedValue ) : Méthode qui change la valeur du SpeedValue.


			--- Méthodes associées aux boutons ---

		modifyStereoValue(self) : Méthode qui signale de modifier la valeur du Stéréo
		modifySpeedValue(self) : Méthode qui signale modifier la valeur de la vitesse
		modifyVolumeValue(self) : Méthode qui signale modifier la valeur du volume
		modifyEffect(self) : Méthode qui signale une demande de modifier l'effet. #TODO : A faire 
		modifyCrossFade(self) : Méthode qui signale une demande de CrossFade.
		modifyRandom(self) : Méthode qui signale une demande de Random. #TODO : A faire
		askRemovePiste(self) : Méthode qui signale une demande de retirer la piste.

"""


class PresentationPiste (Frame):

	"""
		Constructeur
		
		Paramètres
		------------------
			Presentation        self : Objet créé
			Controller          controller : Controller de la piste
			Canvas              canvas : Canvas où sera affichée Presentation de la piste. # MODIF scrollbar
			int                 idPiste : Numéro attribué à la piste pour se repérer
	"""   
	
	def __init__( self ,controller, canvas , idPiste):
		super().__init__(canvas)
		
		self.canvas = canvas
		self.controller = controller
		self.window = None
		
		self.idPiste = idPiste
		self.suivant = None
		self.precedent = None

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1' , height = 2)
		self.spacerLabel.pack()

		self.removeButton = Button( self , text="Supprimer" , command = self.askRemovePiste, width=8 ,cursor="hand2", background='red',font="Helvetica 8 bold" , foreground = "white" , activebackground = "#EA0000" , activeforeground="#EAEAEA" )
		self.removeButton.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 2' , height = 1)
		self.spacerLabel.pack()

		self.idLabel = Label( self , text = "CH " + str( self.idPiste ),background="white",font='Helvetica 16 bold', foreground = "#A0A0A0")
		self.idLabel.pack()

		self.nameLabel = Label( self , text="Veuillez charger un son",background="white",font='Helvetica 8 ' , width = 19, height = 1)
		self.nameLabel.pack()
	

		self.LoadButton = Button( self , text="Charger" , command = self.open_file,width=14,cursor="hand2" ,background='#C8C8C8',font="Helvetica 12 bold" , activebackground = "#B9B9B9" , height = 1 )
		self.LoadButton.pack()

		
		
		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 3', height = 1 )
		self.spacerLabel.pack()

		self.stereoLabel = Label(self,text="Stéréo",background="white",font="Helvetica 11 bold")
		self.stereoLabel.pack()

		self.stereoKnob = Knob(self, -1 , 1 , self.modifyStereoValue )
		self.stereoKnob.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1 , )
		self.spacerLabel.pack()

		self.volumeLabel = Label(self,text="Volume",background="white" , font="Helvetica 11 bold")
		self.volumeLabel.pack()

		self.volumeSlider = Scale(self , orient=VERTICAL, command = self.modifyVolumeValue,background="white", troughcolor='#C8C8C8' ,activebackground="#D9D9D9",font='Helvetica 10 bold' , width = 20, length = 125 , cursor="hand2" , highlightthickness=0 )
		self.volumeSlider.config(from_ = 150, to = 0)
		self.setVolumeValue(100)
		self.volumeSlider.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1)
		self.spacerLabel.pack()

		self.speedLabel = Label(self, text="Pitch",background="white" , font="Helvetica 11 bold")
		self.speedLabel.pack()

		self.speedKnob = Knob( self , 0 , 2 , self.modifySpeedValue)
		self.speedKnob.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1)
		self.spacerLabel.pack()

		self.muteLabel = Label( self , text = "Mute",background="white" , font="Helvetica 11 bold")
		self.muteLabel.pack()

		self.muteButtonState = False
		soundOn=PhotoImage(file="Images/unMute.png",master=self.canvas)
		self.muteButton = Button(self,image=soundOn, command = self.modifyMuteState, cursor="hand2" )
		self.muteButton.image = soundOn
		self.muteButton.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 5', height = 1)
		self.spacerLabel.pack()
		
		self.effectButton = Button(self,text="Effet",width=14, background='#C8C8C8',font="Helvetica 11 bold",cursor="hand2" , command = self.modifyEffet , activebackground = "#B9B9B9")
		self.effectButton.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1)
		self.spacerLabel.pack()

		self.crossFadeButtonState = False
		self.crossFadeButton = Button(self,text="CrossFade",width=14,cursor="hand2", background='#C8C8C8',font="Helvetica 11 bold", command = self.modifyCrossFade , activebackground = "#B9B9B9" )
		self.crossFadeButton.pack()

		self.spacerLabel = Label(self,text="",background='#FFFFFF', font='Helvetica 1', height = 1)
		self.spacerLabel.pack()

		self.randomNbRepFrame = Frame(self)
		self.nbRepText = Text( self.randomNbRepFrame , height = 1 , width = 4 )
		self.nbRepText.insert(INSERT,"0")
		self.nbRepText.pack( side = LEFT )
		self.nbRepLabel = Label( self.randomNbRepFrame, text="apparitions" , height = 1 , width = 13 , background='#C8C8C8' )
		self.nbRepLabel.pack(side = RIGHT )
		self.randomNbRepFrame.pack(  )

		self.randomTimeFrame = Frame(self)
		self.timeText = Text( self.randomTimeFrame , height = 1 , width = 4)
		self.timeText.insert(INSERT,"0")
		self.timeText.pack( side = LEFT )
		self.timeLabel = Label ( self.randomTimeFrame , text="secondes", height = 1 , width = 13 , background='#C8C8C8' )
		self.timeLabel.pack( side = RIGHT )
		self.randomTimeFrame.pack(  )

		self.randomButton = Button(self,text="Random",width=14,cursor="hand2",background='#C8C8C8',font="Helvetica 11 bold", command = self.modifyRandom , activebackground = "#B0B0B0")
		self.randomButton.pack()

		self.configure(background="#FFF")
		self.pack(side = LEFT)
		
	def open_file(self):
		"""
		Méthode qui signale l'importation d'un son.
		"""
		self.controller.listenerLoadTrack ( self.idPiste )

	
	def setName(self, name):
		"""
		Méthode qui change le nom affiché du son

		Paramètre
		-----------
		name : String nom à afficher

		"""
		self.nameLabel.config(text = name)

	
	def remove(self):
		"""
		Méthode qui détruit la presentation.
		"""
		self.destroy()
	

	def setID(self,id):
		"""
		Méthode qui attribut le numéro d'identifiant de la piste

		Paramètre
		----------
		id : int numéro d'identification de la piste
		"""
		self.idPiste = id
		self.idLabel.configure(text ="CH "+ str(self.idPiste))
	

	def getID(self):
		"""
		Méthode qui renvoie le numéro d'identifiant de la piste

		Return
		------------
		int numéro d'identification de la piste
		"""
		return self.idPiste
	

	def getSuivant(self):
		"""

		Méthode qui renvoie la Presentation de la piste suivante

		Return
		--------------
		Presentation Presentation de la piste suivante

		"""
		return self.suivant

	
	def setSuivant(self,suivant):
		"""
		Méthode qui attribut la Presentation de la piste suivante

		Parametres
		------------------
		suivant : Presentation de la piste suivante
		"""
		self.suivant=suivant

	
	def getPrecedent(self):
		"""
		Méthode qui renvoie la Presentation de la piste précédente

		Return
		--------------
		Presentation Presentation de la piste précédente

		"""
		return self.precedent

	
	def setPrecedent(self,precedent):
		"""
		Méthode qui attribut la Presentation de la piste précédente
		
		Parametres
		------------
		precedent : Presentation de la piste précédente

		"""
		self.precedent=precedent

	
	def isMuted(self):
		"""
		Méthode qui retourne le boolean de si ça a été mise en sourdine

		Return
		------------
		boolean : si le son est en sourdine
		"""
		return self.muteButtonState

	def isInCrossFade(self):
		"""
		Méthode qui retourne le boolean de si ça a été mise en crossfade

		Return
		------------
		boolean : si le son est en crossfade
		"""
		return self.crossFadeButtonState
	
	
	def refreshMuteState(self,muteState):
		"""
		Méthode qui met à jour l'état du bouton mute

		Parametres
		------------
		muteState : boolean nouvelle état du bouton mute
		"""
		if muteState:
			soundOff=PhotoImage(file="Images/mute.png",master=self.canvas)
			self.muteButton.config(image=soundOff)
			self.muteButton.image = soundOff
		else:
			soundOn=PhotoImage(file="Images/unMute.png",master=self.canvas)
			self.muteButton.config(image=soundOn)
			self.muteButton.image = soundOn
		self.muteButtonState = muteState

	def refreshCrossFadeState( self , crossfade ):
		self.crossFadeButtonState = crossfade


	def setVolumeValue(self,volumeValue) : 
		"""

		Méthode qui change la valeur du VolumeSlider.

		Parametres
		-------------
		volumeValue : float Valeur du volume de la piste.

		"""
		self.volumeSlider.set(volumeValue)


	def setStereoValue(self,stereoValue) :
		"""

		Méthode qui change la valeur du StéréoKnob.

		Parametres
		------------
		stereoValue : float Valeur du stéréo de la piste.

		"""
		self.stereoKnob.setValue(stereoValue)


	def setSpeedValue( self,SpeedValue ) : 
		"""

		Méthode qui change la valeur du SpeedValue.

		Parametres
		------------
		SpeedValue : float Valeur du speed de la piste.
		
		"""
		self.speedKnob.setValue( SpeedValue )

	def resetRandomTexts( self ):
		"""
		Méthode qui met à zero les textes pour le random.

		"""
		self.nbRepText.delete( "1.0" , 'end-1c' )
		self.timeText.delete( "1.0" , 'end-1c' )
		self.nbRepText.insert( "1.0" , "0")
		self.timeText.insert( "1.0" , "0" )


	"""
	--- Méthodes associées aux boutons ---
	"""


	def modifyStereoValue(self):
		"""
		Méthode qui signale au contoller de modifier (si possible) la valeur du stéreo de la piste.
		"""
		self.controller.listenerStereo( self.stereoKnob.getValue() , self.idPiste )

	
	def modifySpeedValue(self):
		"""
		Méthode qui signale au contoller de modifier (si possible) la valeur de la vitesse de la piste.
		"""
		self.controller.listenerPitch( self.speedKnob.getValue() , self.idPiste )

	def modifyVolumeValue(self,vol):
		"""
		Méthode qui signale au contoller de modifier (si possible) la valeur du volume de la piste.
		"""
		self.controller.listenerVolume( int(vol) , self.idPiste )

	def askRemovePiste(self):
		"""
		Méthode qui signale au contoller d'activer ou de désactiver le Random.
		"""
		self.controller.removeChannelID( self.idPiste )
		self.controller.controllerTop.scrollablePistesFrame.sortPresentation()
		self.controller.controllerTop.scrollablePistesFrame.updateScrollregion()

	
	def modifyMuteState(self):
		"""
		Méthode qui signale au contoller d'activer ou désactiver la mise en sourdine.
		"""
		self.controller.listenerMute(not(self.isMuted()), self.getID())

	def modifyCrossFade(self): 
		"""

		Méthode qui signale une demande de CrossFade.

		"""
		self.controller.listenerCrossFade( not(self.isInCrossFade()) , self.getID() )
		

	def modifyRandom(self): 
		"""

		Méthode qui signale une demande de Random.

		"""
		try:
			nbRep = (int)(self.nbRepText.get( "1.0" , 'end-1c' ))
			timeRandom = (int)(self.timeText.get("1.0" , 'end-1c'))

			self.controller.listenerRandom(nbRep , timeRandom , self.getID() )
		except ValueError:
			self.resetRandomTexts()

	def modifyEffet( self ):
		"""
			Méthode qui signale une demande d'appliquer un effet
		"""
		self.controller.listenerEffet(self.getID())