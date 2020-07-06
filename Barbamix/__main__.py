#! python3.6
# -*- coding: utf-8 -*-

import sys
import os
from tkinter import *
from tkinter import messagebox
from pyo import *

from ControllerTop import ControllerTop

s = Server(duplex = 0).boot()                          #Starts audio engine
s.start()

class test ( Frame ):
    def __init__( self , master):
        super().__init__(master)
        self.master = master
        self.controller = ControllerTop(self.master,s)
		
		#Creation du menu
        monMenu = Menu(self.master)
        self.master.config(menu=monMenu)
        fichier = Menu(monMenu, tearoff=0)
        fichier.add_command(label="Nouveau Fichier",command=self.controller.listenerNouveauFichier)
        fichier.add_command(label="Sauvegarder",command=self.controller.listenerSave)
        fichier.add_command(label="Charger",command=self.controller.listenerLoad)
        fichier.add_command(label="Exporter",command=self.controller.listenerExport)
        fichier.add_separator()
        fichier.add_command(label="Quitter", command=on_closing)
		
        help = Menu(monMenu, tearoff=0)
        help.add_command(label="Aide de barbamix",command=self.controller.listenerAide)
        monMenu.add_cascade(label="Fichier",menu=fichier)
        monMenu.add_cascade(label="Aide",menu=help)
		



def on_closing():
    if messagebox.askokcancel("Quitter ?", "Voulez-vous vraiment quitter ?\n(Ce qui n'est pas sauvegardé sera perdu ! )"):
        app.controller.controllerPiste.endRandom()
        cp = app.controller.controllerPiste
        cp.endRandom()
        while(cp.getPisteCount()>0):
            cp.getThread(cp.getPisteCount()).remove()
            cp.removePistes(1)
        s.stop()
        root.destroy()


# Construction de la fenêtre principale «root»
root = Tk()
root.title("BarbaMix")
root.geometry("1080x800")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)
app = test(root)
root.iconbitmap("Images/DJAhled.ico")
root.configure(background='#FFF')

# Lancement de la «boucle principale»
root.mainloop()
