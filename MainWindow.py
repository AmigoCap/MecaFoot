# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:19:53 2017

@author: Alfonso
"""

import os
import math
import time 
import matplotlib.pyplot as plt
import tkinter 
    
        
class MainWindow(tkinter.Tk):
    
    def __init__(self):  
        
        
    # Initialize
        tkinter.Tk.__init__(self)         
        self.title('Projet Souris')  
        os.chdir("/Users/marc/Desktop/Studium/ECL/Cloud/UE Pro/PA/Projet Souris")
        
    # Main Buttons
        self.__f1 = tkinter.Frame(self)
        self.__buttonStart = tkinter.Button(self, text ='Start Recording', command = self.StartRecording).grid(row=1,column=2) 
       
        self.__buttonHeatMap = tkinter.Button(self, text ='Show Heat map', command = self.ShowHeatMap).grid(row=2,column=0)
        
        self.__buttonAngles = tkinter.Button(self, text ='Show Angle variation', command = self.ShowAngleVariation).grid(row=2,column=1)
        
        self.__buttonSpeed = tkinter.Button(self, text ='Show Speed histogramm', command = self.ShowSpeedHistogramm).grid(row=2,column=2)

    
    # Label for description
        self.__lDesc1 = tkinter.Label(self)
        self.__lDesc1.grid(row=0,column=0)
        self.__lDesc1.config(text = "Time to record (in seconds) :")
        
        self.__lDesc2 = tkinter.Label(self)
        self.__lDesc2.grid(row=0,column=1)
        self.__lDesc2.config(text = "Frequency of echantillonage (per second):")
        
    # Input values
        self.__Time = tkinter.Entry(self)
        self.__Time.grid(row=1,column=0)
         
        self.__Freq = tkinter.Entry(self)
        self.__Freq.grid(row=1,column=1)
        
    # Variables
        self.__SubdivX=10
        self.__SubdivY=10
         
        self.__ScreenWidth=1280
        self.__ScreenHight=800
    
        self.__ResX = self.__ScreenWidth/self.__SubdivX
        self.__ResY = self.__ScreenHight/self.__SubdivY
        
        self.__Stat = []
        self.__MaxStat = 0
        
        self.__LocalTime=[]
        self.__CoorX=[]
        self.__CoorY=[]
        
        self.__Numer = 10
        
    def StartRecording(self):
        pos=[]
        t=0
        
        MaxTime = int(self.__Time.get())
        delta_t = float(self.__Freq.get())
        
        root=tkinter.Tk()
        
        while t<=MaxTime:
            
            t1=time.clock()
            x=root.winfo_pointerx()
            y=root.winfo_pointery()
            pos.append((t,x,y))
            t+=delta_t
            t2=time.clock()
            time.sleep(delta_t-(t2-t1))
            
        result=open("Data_mouse_"+str(self.__Numer)+".txt","w")
            
        for entry in pos:
            result.write(str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+"\n")
               
        result.close()
        
        file="Data_mouse_"+str(self.__Numer)+".txt"
        
# Lecture des données----------------------------------------------------------
        Data_mouse = open(file,"r")
        data = Data_mouse.readlines()
    
        for l in data:
            dataline = l.split()
            self.__LocalTime.append(float(dataline[0]))
            self.__CoorX.append(int(dataline[1]))
            self.__CoorY.append(int(dataline[2]))
    
        Data_mouse.close()
    
    # Initialisation de la matrice Stat
        for i in range(self.__SubdivX):
            self.__Stat.append([0])
            for j in range(self.__SubdivY-1): 
                self.__Stat[i].append(0)
    
    # Calcule de la matrice Stat
        for i in range(len(self.__CoorX)):
            self.__Stat[int(self.__CoorX[i]/self.__ResX)][int(self.__CoorY[i]/self.__ResY)]=self.__Stat[int(self.__CoorX[i]/self.__ResX)][int(self.__CoorY[i]/self.__ResY)]+1
            if (self.__Stat[int(self.__CoorX[i]/self.__ResX)][int(self.__CoorY[i]/self.__ResY)]>self.__MaxStat):
                self.__MaxStat=self.__Stat[int(self.__CoorX[i]/self.__ResX)][int(self.__CoorY[i]/self.__ResY)]
                
    def ShowHeatMap(self):
        HeatMap = tkinter.Tk()
        HeatMap.title("Heat Map")
        C = tkinter.Canvas(HeatMap, bg="white", height=self.__ScreenHight, width=self.__ScreenWidth)
    
        for i in range (len(self.__Stat)):
            for j in range(len(self.__Stat[i])):
                if (self.__Stat[i][j]>0):
                    aux = int((1-(self.__Stat[i][j]/self.__MaxStat))*255)
                    C.create_rectangle(i*self.__ResX, j*self.__ResY, (i+1)*self.__ResX, (j+1)*self.__ResY, width=0, fill= "#%02x%02x%02x" % (aux, aux, aux))
        C.pack()
        HeatMap.mainloop()
        
    def ShowAngleVariation(self):
        
        IntSeconds = 0.2
        Interval = int(IntSeconds/self.__LocalTime[1])
        Angle=[]
    
        for i in range(len(self.__CoorX)-(2*Interval)):
            u=[self.__CoorX[i+Interval]-self.__CoorX[i],self.__CoorY[i+Interval]-self.__CoorY[i]]
            v=[self.__CoorX[i+2*Interval]-self.__CoorX[i+Interval],self.__CoorY[i+2*Interval]-self.__CoorY[i+Interval]]
            normu= math.sqrt(u[0]*u[0]+u[1]*u[1])
            normv= math.sqrt(v[0]*v[0]+v[1]*v[1])
            if (normu!=0 and normv!=0 and u[0]*v[1]!=u[1]*v[0]):  
                Angle.append(math.degrees(math.acos((u[0]*v[0]+u[1]*v[1])/(normu*normv))))
            
        plt.hist(Angle)
        plt.xlabel('Angle')
        plt.ylabel('Quantité')
        plt.grid(True)
        plt.show()
        plt.savefig("hist_"+str(self.__Numer)+".png")
    
    def ShowSpeedHistogramm(self):
        
        echmoy=3
        Speed=[]
        
    # Calcule de la vitesse de la souris
        for i in range(len(self.__CoorX)-echmoy):
            sumdist = 0
            for j in range (echmoy):
                dist = math.sqrt((self.__CoorX[i+j]-self.__CoorX[i+j+1])*(self.__CoorX[i+j]-self.__CoorX[i+j+1])+(self.__CoorY[i+j]-self.__CoorY[i+j+1])*(self.__CoorY[i+j]-self.__CoorY[i+j+1]))
                sumdist = sumdist + dist 
                Speed.append(sumdist/self.__LocalTime[1])
    
    # Dessin du histogramme de vitesse
        plt.hist(Speed)
        plt.xlabel('Vitesse')
        plt.ylabel('Quantité')
        plt.grid(True)
        plt.show()
        plt.savefig("hist_"+str(self.__Numer)+".png")                       

window = MainWindow() 
window.mainloop() 
         
         
         
         
         
         
         
         
         
         
         
         
         
         