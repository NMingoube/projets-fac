#! python3.6
# -*- coding: utf-8 -*-

"""
Created on Thu Mar  5 08:45:28 2020

@author: Equipe Rocco

Dernière modification : 15/04/2020 18h36  par Thibaud BARON

En cas de soucis: Merci de vous référez à l'équipe Rocco :)

"""

from tkinter import *
import tkinter.font as tkFont
from math import sqrt,pi,acos,cos,sin

"""
    Classe Knob 
        Attributs:
            #Consernant la valeur
            minValue : Valeur minimale
            maxValue : Valeur maximale

            #Consernant l'affichage

            canvas : canvas où le bouton tournant est dessiné

            background : le cercle représentant le bouton tournant
            point : point sur le bouton tournant pour voir l'angle actuelle du bouton
            textArea : Espace texte pour afficher la valeur actuelle


            radius : le rayon du bouton tournant
            pointRadius : le rayon du point sur le bouton tournant
            radiusDiff : l'écart le plus petit entre le périmètre du bouton tournant et celui du point

            margin : la marge entre le périmètre du canvas et le bouton tournant

            heigthTextArea : hauteur pour la zone de texte


        Méthodes:
            
            update : méthode appelée pour toutes modifications suite à un évènement avec une 

            checkNewPointCoordonates : Renvoie des nouvelles coordonnées pour le point

            calculNewValeur : Recalcule la valeur associé au bouton tournant et l'affiche dans la zone de texte

            setValue : Mutateur de la valeur attribuée au bouton tournant, et applique les modifications visuelles demandées
            
            getValue : Récupère la valeur attribuée
            
            pack : permet de pack le canvas du bouton tournant




"""



class Knob():

    #Constructeur
    #param master master à attribuer pour le canvas du Knob où sera dessiné le bouton tournant
    #param minValue Valeur minimale à ne pas dépasser pour le Knob
    #param maxValue Valeur maximale à ne pas dépasser pour le Knob
    #param func nom de la fonction associée au bouton lors d'un changement de valeur

    def __init__(self,master,minValue,maxValue,func):
        self.minValue = minValue
        self.maxValue = maxValue

        self.radius = 28
        self.pointRadius = 8
        self.radiusDiff = 4

        self.margin = 10
        self.heigthTextArea = 15
        
        self.canvas = Canvas(master,background='#FFFFFF',height=(self.radius+self.margin)*2+self.heigthTextArea , width = (self.radius+self.margin)*2 , borderwidth = 0 , confine = True , cursor="hand2" , highlightthickness=0 )

        self.background = self.canvas.create_oval(self.margin, self.margin , self.radius*2+self.margin, self.radius*2 +self.margin,fill='#BBBBBB')
        self.point = self.canvas.create_oval(self.radius- self.pointRadius +self.margin , self.radiusDiff +self.margin, self.radius + self.pointRadius +self.margin , self.radiusDiff + self.pointRadius*2 +self.margin , fill='#333333' )
        
        #Les deux petites lignes
        self.canvas.create_line( (self.margin + self.radius)*(1-sqrt(3)/2) , (self.margin + self.radius)/2 + self.margin + self.radius , self.margin + self.radius*(1-sqrt(3)/2) , self.margin + 3*self.radius/2 , width = 3 )
        self.canvas.create_line( (self.margin + self.radius)*(1+sqrt(3)/2) , (self.margin + self.radius)/2 + self.margin + self.radius , self.margin + self.radius*(1+sqrt(3)/2) , self.margin + 3*self.radius/2 , width = 3 )

        self.textArea = self.canvas.create_text( self.margin + self.radius , self.margin * 2 + self.radius * 2  , font = tkFont.Font(size=-(int(self.heigthTextArea)) ) )

        self.value = (self.maxValue+self.minValue)/2
        
        strValue = "%3.2f" % self.value

        self.canvas.itemconfigure( self.textArea , text = strValue )

        self.canvas.bind("<B1-Motion>",self.update)

        self.actionByUpdate = func


    #-------------------------------------------------------------------------------------------


    def update(self,event):

        X = self.canvas.coords(self.background)[0]+self.radius
        Y = self.canvas.coords(self.background)[1]+self.radius

        xPoint = self.canvas.coords(self.point)[0]+self.pointRadius
        yPoint = self.canvas.coords(self.point)[1]+self.pointRadius

        pointDistance = self.radius-self.radiusDiff-self.pointRadius
        mouseDistance = sqrt(pow((self.radius+self.margin)-event.x,2) +pow((self.radius+self.margin)-event.y,2))

        if( mouseDistance != 0 ):
            newXPoint = X + (event.x-X)*(pointDistance/mouseDistance)
            newYPoint = Y + (event.y-Y)*(pointDistance/mouseDistance)

            newXPoint , newYPoint = self.checkNewPointCoordonates( newXPoint , newYPoint )

            self.canvas.move(self.point , newXPoint - xPoint , newYPoint - yPoint )
            self.calculNewValeur(newXPoint , newYPoint)
            self.actionByUpdate()

    #---------------------------------------------------------------------------

    def checkNewPointCoordonates(self,XPoint,YPoint):

        marginToCenter = 1

        if( YPoint > ( (self.radius-self.radiusDiff-self.pointRadius)/2 + self.radius + self.margin ) ):
            YPoint = (self.radius-self.radiusDiff-self.pointRadius)/2 + self.radius +self.margin
            if( XPoint < self.radius + self.margin  ):
                XPoint = self.radius + self.margin - (self.radius - self.radiusDiff-self.pointRadius) *sqrt(3)/2
            elif( XPoint >= self.radius + self.margin ):
                XPoint = self.radius + self.margin + (self.radius - self.radiusDiff-self.pointRadius) *sqrt(3)/2 
        elif ( YPoint < (self.margin + self.radiusDiff + self.pointRadius + marginToCenter) ):
            YPoint = self.margin + self.radiusDiff + self.pointRadius
            XPoint = self.margin + self.radius
        return XPoint , YPoint


    #-------------------------------------------------------------------------------------------

    def calculNewValeur( self , Xpoint, YPoint):
        valueInAcos = (Xpoint - self.radius - self.margin) / (self.radius - self.radiusDiff-self.pointRadius)

        angle = acos( valueInAcos )
        
        if( YPoint > (self.radius+self.margin) ):
            if( Xpoint > (self.radius+self.margin) ):
                angle = pi/6 - angle
            else:
                angle = 2*pi - angle
                angle = angle + pi / 6
        else :
            angle = angle + pi / 6

        self.value = ((4/3*pi - angle)/(4/3*pi))*(self.maxValue - self.minValue) +self.minValue

        strValue = "%3.2f" % self.value

        self.canvas.itemconfigure( self.textArea , text = strValue )


    #--------------------------------------------------------------------------------------------


    def setValue(self,newValue):
        if (newValue < self.minValue or newValue > self.maxValue):
            print("La valeur que vous souhaitez attribuer au Knob est en dehors de l'intervalle admis")
        else:
            self.value = newValue

            angleTemp = (self.maxValue - self.value) / (3*(self.maxValue-self.minValue)/(4*pi))
            newangle =angleTemp - pi/6


            xPoint = self.canvas.coords(self.point)[0]+self.pointRadius
            yPoint = self.canvas.coords(self.point)[1]+self.pointRadius

            newXPoint = (self.radius - self.pointRadius - self.radiusDiff)*cos(newangle) + self.canvas.coords(self.background)[0]+self.radius
            newYPoint = -(self.radius - self.pointRadius - self.radiusDiff)*sin(newangle) + self.canvas.coords(self.background)[1]+self.radius

            self.canvas.move(self.point , newXPoint - xPoint , newYPoint - yPoint )
            strValue = "%3.2f" % self.value
            self.canvas.itemconfigure( self.textArea , text = strValue )
        self.actionByUpdate()


    #-------------------------------------------------------------------------------------


    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------------

    def pack(self):
        self.canvas.pack()

