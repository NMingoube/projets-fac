# -*- coding: utf-8 -*-
"""
Documentation de la classe ScrollablePistesFrame

	Version : 24/04/2020 Jordan AGARD Equipe ROCCO

	Participant : Jordan AGARD

	Description :

		ScrollablePistesFrame est une classe concrète qui va permettre d'accueillir
        les pistes dans un canvas et de les faire défiler horizontalement.

	Attribut :

		height : Hauteur de la fenêtre contenant les pistes, modifiable.
        width : Largeur de la fenêtre contenant les pistes, modifiable.
		pisteWidth : Largeur d'une piste. Utile pour créer le décalage à chaque ajout de piste ou déterminer un padding
        scrollRegionWidth : Met à jour la largeur scrollable du presentationCanvas quand une piste est ajoutée ou retirée
        controllerTop : Référence au controllerTop auquel il appartient
        pisteScrollbar : Scrollbar qui permet le défilement horizontal du canvas lié aux pistes
        presentationCanvas : Canvas qui accueille les pistes (Presentation)

	Constructeur:
        
		ScrollablePistesFrame(controllerTop, master)
        
        controllerTop : Référence au controllerTop auquel il appartient
        master : Référence à la Frame ou au Canvas auquel il appartient
        
    Methode :
		addPresentation(self, newPrese) : Ajoute une Presentation au canvas géré par la scrollbar
		updateScrollRegion(self) : Met à jour la region scrollable du canvas pour qu'elle se limite aux Presentations présentes
        sortPresentation(self) : Réarrange la disposition des Presentation, lors de la suppression de l'une d'entre elles

"""

from tkinter import *
from tkinter import Button
from tkinter import Scale
from tkinter import Label
from tkinter import Frame

class ScrollablePistesFrame (Frame):
    """
		Constructeur
		
		Paramètres
		------------------
			ScrollablePistesFrame		self : Objet créé
			ControllerTop			    controllerTop : Controller de la Frame scrollable
	"""	
    def __init__(self, controllerTop, master):
        super().__init__(master)
        
        self.pisteWidth = 140
        
        self.height = 825
        self.width = 6*self.pisteWidth # Se base sur le nombre de pistes voulues au départ et de la largeur d'une piste
        
        self.scrollRegionWidth = 0
      
        self.controllerTop = controllerTop
        
        self.pistesScrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.pistesScrollbar.pack(side=BOTTOM, fill=X)
        
        self.presentationsCanvas = Canvas(self, xscrollcommand=self.pistesScrollbar.set, height=self.height, width=self.width, background='#FFF', highlightthickness  = 0)
        self.pistesScrollbar.config(command=self.presentationsCanvas.xview)
        self.presentationsCanvas.pack(side=RIGHT)
    
    def addPresentation(self, newPrese):
        """
        

        Paramètres
        ----------
        newPrese : Presentation
            Presentation qui sera ajoutée au canvas géré par la scrollbar.

        Returns
        -------
        None.

        """
        offsetX = (newPrese.getID()-1) * self.pisteWidth
        self.scrollRegionWidth = self.pisteWidth*newPrese.getID()
        newPrese.window = self.presentationsCanvas.create_window(offsetX , 0 , window = newPrese.canvas, anchor="nw" )
        self.presentationsCanvas.configure(scrollregion=(0,0,self.scrollRegionWidth,0))
    
    def updateScrollregion(self):
        """
        

        Returns
        -------
        None.

        """
        nbPistes = self.controllerTop.controllerPiste.getPisteCount()
        self.scrollRegionWidth = self.pisteWidth * nbPistes
        self.presentationsCanvas.configure(scrollregion=(0,0,self.scrollRegionWidth,0))

    def sortPresentation(self):
        """
        

        Returns
        -------
        None.

        """
        prese = self.controllerTop.controllerPiste.getPresentation(1)
        while (prese != None):
            self.presentationsCanvas.coords(prese.window, (prese.getID()-1)*self.pisteWidth, 0)
            prese = prese.getSuivant()
        