from tkinter import *
import os
from pyo import *
from time import *
from os import path
import wave
import contextlib
import tkinter.font as tkFont

class popupAide():
        def __init__(self):
            gestion = Toplevel()
            gestion.title('Aide')
            gestion.geometry('920x720')
            gestion.resizable(False,False)
            gestion.iconbitmap("Images/DJAhled.ico")

            titre = Message(gestion, text="Aide de l'application BarbaMix")
            fontStyle = tkFont.Font(family="Arial")
            titre.configure(width=920, font=(fontStyle, 20))
            titre.pack()

            instruction1 = Label(gestion, text="Gestion de la piste général :", font=("Arial", 14))
            instruction1.place(x=0, y=60)
            
            text = Label(gestion, text="Dans un premier temps vous pouvez lancer ou mettre en pause la piste générale grâce au bouton Play/Pause.", font=(None, 10))
            text.place(x=0, y=90)
            text = Label(gestion, text="Dans un deuxième temps vous pouvez regler le son générale grâce au bouton scroll et affiche le volume en cours.", font=(None, 10))
            text.place(x=0, y=110)
            text = Label(gestion, text="Pour ajouter une piste cliquer sur le bouton \"Add Chanel\".", font=(None, 10))
            text.place(x=0, y=130)
            text = Label(gestion, text="Vous pouvez sauvegarder vos paramètres, charger des paramètres et exporter vos propres paramètres.", font=(None, 10))
            text.place(x=0, y=150)

            instruction2 = Label(gestion, text="Gestion des pistes :", font=("Arial", 14))
            instruction2.place(x=0, y=180)
            text = Label(gestion, text="Vous pouvez charger un son via le bouton \"Charger\".", font=(None, 10))
            text.place(x=0, y=210)
            text = Label(gestion, text="Vous pouvez supprimer la piste actuelle grâce au bouton \"Supprimer\".", font=(None, 10))
            text.place(x=0, y=230)
            text = Label(gestion, text="Vous pouvez jouer sur le Stéréo et le Pitch.", font=(None, 10))
            text.place(x=0, y=250)
            text = Label(gestion, text="Régler le son de la piste grâce au bonton scroll et affiche le son de la piste.", font=(None, 10))
            text.place(x=0, y=270)
            text = Label(gestion, text="Muter le son grâce au bonton haut-parleur !", font=(None, 10))
            text.place(x=0, y=290)
            text = Label(gestion, text="Vous pouvez ajouter un effet à la piste, jouer sur le crossfade et le random.", font=(None, 10))
            text.place(x=0, y=310)
            text = Label(gestion, text="Vous ne pouvez malheureusement pas utiliser le crossfade et le random en même temps donc vous pouvez jouer que l'un ou l'autre !", font=(None, 10))
            text.place(x=0, y=330)

            instruction3 = Label(gestion, text="La gestion du fichier :", font=("Arial", 14))
            instruction3.place(x=0, y=360)
            text = Label(gestion, text="Vous pouvez creer un nouveau fichier dans le menu bar !", font=(None, 10))
            text.place(x=0, y=390)
            text = Label(gestion, text="Vous pouvez sauvegarder vos propre paramètre.", font=(None, 10))
            text.place(x=0, y=410)
            text = Label(gestion, text="Enfin vous pouvez charger vos paramètres que vous avez initialement sauvegarder ou les exporter !", font=(None, 10))
            text.place(x=0, y=430)
