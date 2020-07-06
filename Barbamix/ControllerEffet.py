from tkinter import *
import os
from pyo import *
from time import *
from os import path
import wave
import contextlib
import tkinter.font as tkFont
from robotClass import Robot
from Inverted import Inverted
from Swapped import Swapped
from SmoothingEffect import SmoothingEffect

class ControllerEffet():
    def __init__(self, ControllerPiste, ID):
        self.file = "Banque/silence.wav"
        self.sonRobot = None #TODO: ajouter effet
        self.sonInverted = None
        self.sonSwapped = None
        self.sonSmooth = None
        self.controller = ControllerPiste
        self.ident = ID
       
    def setID(self,ID):
        self.ident=ID
	
    def getOriginalPath(self):
        return self.file
		
    def remove(self):
        if(self.sonRobot != None): #TODO: ajouter effet
            os.remove(self.sonRobot)
            self.sonRobot = None
        if(self.sonInverted != None):
            os.remove(self.sonInverted)
            self.sonInverted = None
        if(self.sonSwapped != None):
            os.remove(self.sonSwapped)
            self.sonSwapped = None
        if(self.sonSmooth != None):
            os.remove(self.sonSmooth)
            self.sonSmooth = None
	
    def setPath(self,path):
        self.file = path
        self.remove()

    def start(self):
        self.gestion = Toplevel()
        self.gestion.title('Effet')
        self.gestion.geometry('920x720')
        self.gestion.resizable(False,False)
        self.gestion.iconbitmap("Images/DJAhled.ico")
        
        titre = Message(self.gestion, text="Application de l'effet sur le son")
        fontStyle = tkFont.Font(family="Arial")
        titre.configure(width=920, font=(fontStyle, 20))
        titre.pack()
        
        ListeEffet = ["Sans Effet","Robot","Inverse","Swap","Smooth"] #TODO: ajouter effet
        self.liste = Listbox(self.gestion)
        self.liste.insert(0, *ListeEffet)
        self.liste.selection_set(0)
        self.liste.pack()
        
        btn = Button(self.gestion, text="Chargement du choix", command=self.btnAction)
        btn.pack()
        
        instruction1 = Label(self.gestion, text="La génération du nouveau fichier Wav prends un peu de temps veuiller attendre, Merci !", font=("Arial", 14))
        instruction1.place(x=0, y=650)
        
        exit = Button(self.gestion, text='Quitter', command=self.gestion.destroy)
        exit.place(x=400, y=680)
        
        self.gestion.grab_set()          # Interaction avec fenetre barbamix impossible
	
    def btnAction(self): #TODO: ajouter effet
        if(self.liste.get(self.liste.curselection()) == 'Sans Effet'):
            self.controller.setTrackPath(self.ident, self.file)
        elif(self.liste.get(self.liste.curselection()) == 'Robot'):
            if(self.sonRobot == None):
                self.sonRobot = Robot(self.file,self.ident).getNewPath()
            self.controller.setTrackPath(self.ident, self.sonRobot)
        elif(self.liste.get(self.liste.curselection()) == 'Inverse'):
            if(self.sonInverted == None):
                self.sonInverted = Inverted(self.file,self.ident).getNewPath()
            self.controller.setTrackPath(self.ident, self.sonInverted)
        elif(self.liste.get(self.liste.curselection()) == 'Swap'):
            if(self.sonSwapped == None):
                self.sonSwapped = Swapped(self.file,self.ident).getNewPath()
            self.controller.setTrackPath(self.ident, self.sonSwapped)
        elif(self.liste.get(self.liste.curselection()) == 'Smooth'):
            if(self.sonSmooth == None):
                self.sonSmooth = SmoothingEffect(self.file,self.ident).getNewPath()
            self.controller.setTrackPath(self.ident, self.sonSmooth)
