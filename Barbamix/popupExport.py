#! python3.6
# -*- coding: utf-8 -*-

"""

@author: Equipe BARSUKOV

Dernière modification : jeu. 23 avril 2020 17∶20∶16

"""

from threading import Thread
from tkinter import *
import os
from pyo import *
from time import *
from os import path
import wave
import contextlib
import tkinter as tk

class export():
	def __init__(self,serveur):
		self.serveur = serveur
		
	def popupExport(self):
		self.gestionRecord = Toplevel()
		self.gestionRecord.iconbitmap("Images/DJAhled.ico")
		self.gestionRecord.title('Enregistrement')
		self.gestionRecord.geometry('300x400')
		tk.Label(self.gestionRecord, text="Enregistrement libre : ").pack(padx=10, pady=10)
		b1=Button(self.gestionRecord, text='Start', command=self.startRecord,relief='raised',activebackground='#00ff00',bg='#C0B1B1',cursor="hand1")
		self.b1=b1
		b1.pack(padx=10, pady=10)
		b2=Button(self.gestionRecord, text='Stop', command=self.endRecord,activebackground="#ff3300",bg='#C0B1B1',cursor="hand1",state="disabled")
		self.b2=b2
		b2.pack(padx=10, pady=10)
		e4 = tk.Label(self.gestionRecord, text="", state="disabled")
		self.e4=e4
		e4.pack()
		tk.Label(self.gestionRecord, text="Enregistrement pour un temps défini (en secondes) : ").pack(padx=10, pady=10)
		e1 = tk.Entry(self.gestionRecord)
		self.e1=e1
		e1.insert(0, "0")
		e1.pack(padx=10, pady=10)
		b3=Button(self.gestionRecord, text='Enregistrer', command=self.startRecordUser,bg='#C0B1B1',cursor="hand1")
		self.b3=b3
		b3.pack(padx=10, pady=10)
		b4=Button(self.gestionRecord, text='Quitter', command=self.gestionRecord.destroy,bg='#C0B1B1',cursor="hand1")
		self.b4=b4
		b4.pack(padx=10, pady=10)
		e3 = tk.Label(self.gestionRecord, text="", state="disabled")
		self.e3=e3
		e3.pack(padx=10, pady=10)
		self.gestionRecord.grab_set()

	def startRecord(self):
		self.e4['text']="Enregistrement en cours."
		self.e3['text']=""
		self.b2['state']="normal"
		self.b1['state']="disabled"
		self.b3['state']="disabled"
		path = filedialog.asksaveasfilename(title = "Choose a file to save", filetypes=[('wav file','.wav')], initialdir=os.getcwd()+"/lib/")
		if(path):
			if(not(path.endswith(".wav"))):
				path = path + ".wav"
			self.serveur.recordOptions(sampletype=2,quality=1.0)
			self.serveur.recstart(path)
		
	def endRecord(self):
		self.e4['text']="Enregistrement terminé."
		self.e3['text']=""
		self.b1['state']="normal"
		self.b2['state']="disabled"
		self.b3['state']="normal"
		self.serveur.recstop()
		
	def startRecordUser(self):
		threading.Thread( target=self.startRecordUserThread ).start()
		
	def startRecordUserThread(self):
		e2 = self.e1.get()
		if(e2.isdigit()):
			path = filedialog.asksaveasfilename(title = "Choose a file to save", filetypes=[('wav file','.wav')], initialdir=os.getcwd()+"/lib/")
			if(path):
				if(not(path.endswith(".wav"))):
					path = path + ".wav"
				self.serveur.recordOptions(sampletype=2,quality=1.0)
				self.serveur.recstart(path)
				sleep(int(e2))
				if(self.gestionRecord):
					self.serveur.recstop()
					self.e4['text']=""
					self.e3['text']="L'enregistrement de "+e2+" secondes est terminé."	
		else:
			pass