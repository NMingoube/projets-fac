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

import os
import json
import tkinter
from tkinter import filedialog
from tkinter import messagebox

from AbstractBottom import AbstractBottom

class ControllerBottom:
    def __init__(self,controllerTop,controllerPiste):
        self.data = AbstractBottom()
        self.controllerTop = controllerTop
        self.controllerPiste = controllerPiste

    def enregistrement_fichier(self): #Enregistre le dictionnaire dans un fichier
        self.data.addSavePiste(self.controllerTop,self.controllerPiste)
        filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if(filename):
            if(not(filename.endswith(".json"))):
                filename = filename + ".json"
            with open(filename,'w') as f:
                json.dump(self.data.dico,f,indent=3)

    def charger_fichier(self):    #Charge les données d'un fichier .json dans un dictionnaire
        request = messagebox.askyesnocancel("Charger fichier","Voulez-vous charger un fichier sans sauvegarder vos paramètres actuelle ?") #TODO verife fichier
        if(request == False):
            self.enregistrement_fichier()
            
        if(request != None):
            filename = filedialog.askopenfilename(title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
            if(filename):
                if(not(filename.endswith(".json"))):
                    filename = filename + ".json"
                with open(filename,'r') as f:
                    self.data.setDico(json.load(f))
            
            self.data.loadPiste(self.controllerTop,self.controllerPiste)
            
        