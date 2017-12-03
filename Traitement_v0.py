# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
import tkinter

   
class MainWindow(tkinter.Tk):
    
    
    def __init__(self):
         
    # Initialize
        tkinter.Tk.__init__(self)         
        self.title('Traitement Donnée Sportives')  
        tkinter.Grid.rowconfigure(self, 0, weight=1)
        tkinter.Grid.rowconfigure(self, 1, weight=1)
        tkinter.Grid.rowconfigure(self, 2, weight=1)
        tkinter.Grid.rowconfigure(self, 3, weight=1)
        tkinter.Grid.rowconfigure(self, 4, weight=1)
        tkinter.Grid.columnconfigure(self, 0, weight=1)
        tkinter.Grid.columnconfigure(self, 1, weight=6)
        #os.chdir("/Users/marc/Desktop/Studium/ECL/Cloud/UE Pro/PA/Projet Souris")
        
        self.__C_active = False
        self.__M_active = False
        self.__H_active = False
        
        self.__H_Start_Time_aux  = 0
        self.__H_End_Time_aux    = 0
        self.__H_Duration_aux    = 0
      
    # Main Panels
    
        self.__C_Panel      = tkinter.LabelFrame(self, text="Affichage de courbes :")
        self.__M_Panel      = tkinter.LabelFrame(self, text="Visualisation du mouvement :")
        self.__H_Panel      = tkinter.LabelFrame(self, text="Affichage du HeatMap :")
        self.__I_Panel      = tkinter.LabelFrame(self, text="Information :")
        self.__Canvas_Panel = tkinter.LabelFrame(self, text="Affichage du terrain :")

    # Courbe_Panel elements
    

        self.__C_MenuButton          = tkinter.Menubutton(self.__C_Panel, text = "Choisir Courbe", relief = "raised")
        self.__C_Init_Time_Scale     = tkinter.Scale(self.__C_Panel,from_=0, to=100, orient="horizontal", label = "Temps Initial (%)")
        self.__C_Final_Time_Scale    = tkinter.Scale(self.__C_Panel,from_=0, to=100, orient="horizontal", label = "Temps Final (%)")
        self.__C_Duration_Time_Scale = tkinter.Scale(self.__C_Panel,from_=0, to=100, orient="horizontal", label = "Duration (%)")
        self.__C_ShowButton          = tkinter.Button(self.__C_Panel, text = "Afficher", relief = "raised", command = self.ShowC)
        
        
        self.__C_MenuButton.pack(expand="true")
        self.__C_Init_Time_Scale.pack(expand="true")
        self.__C_Final_Time_Scale.pack(expand="true")
        self.__C_Duration_Time_Scale.pack(expand="true")
        self.__C_ShowButton.pack(expand="true")
        
        self.__C_Panel.grid(row=0, column=0,sticky='NSEW')
        
    # MouvmentVisualitation_Panel elements
        
        self.__M_Percent_Speed_Scal   = tkinter.Scale(self.__M_Panel,from_=1, to=100, orient="horizontal", label = "Vitesse (%)")
        self.__M_Duration_Trace_Scale = tkinter.Scale(self.__M_Panel,from_=1, to=100, orient="horizontal", label = "Duration Trace (%)")
        self.__M_ShowButton           = tkinter.Button(self.__M_Panel, text = "Afficher", relief = "raised", command = self.ShowM)
        
        self.__M_Percent_Speed_Scal.pack(expand="true")
        self.__M_Duration_Trace_Scale.pack(expand="true")
        self.__M_ShowButton.pack(expand="true")
        
        self.__M_Panel.grid(row=1, column=0,sticky='NSEW')
        
    # HeatMap_Panel elements
    
        self.__H_Divisions_Scale     = tkinter.Scale(self.__H_Panel,from_=1, to=100, orient="horizontal", label = "Nb de division")
        self.__H_Init_Time_Scale     = tkinter.Scale(self.__H_Panel,from_=0, to=100, orient="horizontal", label = "Temps Initial (%)")
        self.__H_Final_Time_Scale    = tkinter.Scale(self.__H_Panel,from_=0, to=100, orient="horizontal", label = "Temps Final (%)")
        self.__H_Duration_Time_Scale = tkinter.Scale(self.__H_Panel,from_=0, to=100, orient="horizontal", label = "Duration (%)")
        self.__H_ShowButton          = tkinter.Button(self.__H_Panel, text = "Afficher", relief = "raised", command = self.ShowH)
        
        self.__H_Divisions_Scale.pack(expand="true")
        self.__H_Init_Time_Scale.pack(expand="true")
        self.__H_Final_Time_Scale.pack(expand="true")
        self.__H_Duration_Time_Scale.pack(expand="true")
        self.__H_ShowButton.pack(expand="true")
        
        self.__H_Panel.grid(row=2, column=0,sticky='NSEW')
    
    # Information_Panel elements
    
        self.__I_Data_Duration       = tkinter.Label(self.__I_Panel)
        self.__I_Data_Duration.pack(expand="true")
        #self.__I_Data_test           = tkinter.Text(self.__I_Panel, text="test").pack(expand="true")
        
        self.__I_Panel.grid(row=3, column=0,sticky='NSEW')
        
    # Canvas Panel
        
        self.__Rugby_W=70     #meters
        self.__Rugby_H=140    #meters
        
        self.__Margin = 10    #pixe
        
        self.__Scale = 6
        
        self.__W_Canvas = self.__Rugby_W*self.__Scale
        self.__H_Canvas = self.__Rugby_H*self.__Scale
    
        self.__Canvas = tkinter.Canvas(self.__Canvas_Panel,width = self.__W_Canvas+self.__Margin, height = self.__H_Canvas+self.__Margin, bg="white")
        self.__Canvas_C = tkinter.Canvas(self.__Canvas_Panel,bg="blue")
        self.__Canvas.grid(row=0,column=1,columnspan=1,rowspan=4,sticky='NSEW')
        self.__Canvas_C.grid(row=0,column=2,columnspan=1,rowspan=4,sticky='NSEW')
        
        self.DrawTerrain()
        
        self.__Canvas_Panel.grid(row=0, column=1, columnspan=1, rowspan=4,sticky='NSEW')

        # Data opening
        
        file = "Rugby_Data.txt"
        self.__DataFile = open(file,"r")
        self.__Data = self.__DataFile.readlines()
        
        self.__Time=[]
        self.__Velocity=[]
        self.__Acceleration=[]
        self.__Odometer=[]
        self.__Y=[]
        self.__X=[]
    
        for l in self.__Data:
            dataline = l.split()
            self.__Time.append(float(dataline[0]))
            self.__Velocity.append(float(dataline[1])/3.6)
            self.__Acceleration.append(float(dataline[2]))
            self.__Odometer.append(float(dataline[3]))
            self.__Y.append(float(dataline[5]))
            self.__X.append(float(dataline[4]))
            
        
        self.__DataFile.close()
        
        X_mid = 43.482162
        Y_mid = -1.536879
        self.__PI = 3.14159
        self.__R_Earth = 6378000.0
        
        for i in range(len(self.__X)):
            self.__X[i] = abs(X_mid-self.__X[i])*self.__PI/180*self.__R_Earth
            
        for i in range(len(self.__Y)):
            self.__Y[i] = abs(Y_mid-self.__Y[i])*self.__PI/180*self.__R_Earth
             
        X_max = max(self.__X)
        Y_max = max(self.__Y)
        
        for i in range(len(self.__X)):
            self.__X[i] = self.__X[i]/X_max*self.__W_Canvas
            
        for i in range(len(self.__Y)):
            self.__Y[i] = self.__Y[i]/Y_max*self.__H_Canvas
        
            
    def DrawTerrain(self):
        
        self.__Canvas.create_rectangle(self.__Margin,self.__Margin,self.__W_Canvas,self.__H_Canvas, fill = "#38CB3F")
        self.__Canvas.create_rectangle(self.__Margin,self.__Margin+20*self.__Scale,self.__W_Canvas,self.__H_Canvas-20*self.__Scale, fill = "#27CF2E")
        self.__Canvas.create_line(self.__Margin,self.__Margin+self.__H_Canvas*0.5,self.__W_Canvas,self.__Margin+self.__H_Canvas*0.5)
        self.__Canvas.create_rectangle(self.__Margin+self.__W_Canvas*0.5-20,self.__Margin+20*self.__Scale-5,self.__Margin+self.__W_Canvas*0.5+20,self.__Margin+20*self.__Scale+5, fill = "#000000")
        self.__Canvas.create_rectangle(self.__Margin+self.__W_Canvas*0.5-20,self.__Margin+118*self.__Scale-5,self.__Margin+self.__W_Canvas*0.5+20,self.__Margin+118*self.__Scale+5, fill = "#000000")
    
            
    def ShowC (self):
        if (self.__C_active):
            self.__C_active = False
        else:
            self.__C_active = True
            
        self.Courbe()
        
    def ShowM (self):
        if (self.__M_active):
            self.__M_active = False
        else:
            self.__M_active = True
        self.Trace()
        
    def ShowH (self):
        if (self.__H_active):
            self.__H_active = False
        else:
            self.__H_active = True

        self.HeatMap()
            
    def HeatMap(self):
        
        #self.DrawTerrain()
        
        self.__Div    = self.__H_Divisions_Scale.get()
        self.__X_step = int((self.__W_Canvas)/self.__Div)+1
        self.__Y_step = int((self.__H_Canvas)/self.__Div)+1
        
        self.__Start_Time = self.__H_Init_Time_Scale.get()
        self.__End_Time   = self.__H_Final_Time_Scale.get()
        self.__Duration   = self.__H_Duration_Time_Scale.get()
        
        if (self.__H_Duration_aux != self.__Duration):
            self.__End_Time=self.__Start_Time+self.__Duration
            self.__H_Final_Time_Scale.set(self.__End_Time) 
            
        if (self.__H_End_Time_aux !=  self.__End_Time):
            self.__Duration=self.__End_Time-self.__Start_Time
            self.__H_Duration_Time_Scale.set(self.__Duration) 
            
        if(self.__H_Start_Time_aux !=  self.__Start_Time):
            self.__Duration=self.__End_Time-self.__Start_Time
            self.__H_Duration_Time_Scale.set(self.__Duration)
        
        self.__H_Start_Time_aux  = self.__Start_Time
        self.__H_End_Time_aux    = self.__End_Time
        self.__H_Duration_aux    = self.__Duration
        
        self.__Start_Time = self.__Start_Time/100*self.__Time[-1]
        self.__End_Time   = self.__End_Time/100*self.__Time[-1]
        self.__Duration   = self.__Duration/100*self.__Time[-1]
        
        self.__Local_Time=[]        
        self.__Local_X=[]
        self.__Local_Y=[]
        
        for i in range(len(self.__Time)):
            if (self.__Time[i]>self.__Start_Time and self.__Time[i]<self.__End_Time):
                self.__Local_Time.append(self.__Time[i])
                self.__Local_X.append(self.__X[i])
                self.__Local_Y.append(self.__Y[i])
                
   # Stat matrix initiation
        self.__Stat=[]
        for i in range(self.__Div):
           self.__Stat.append([0])
           for j in range(self.__Div): 
               self.__Stat[i].append(0)
    
    # Stat matrix calculation
        self.__MaxStat=1
        for i in range(len(self.__Local_X)):
            self.__Stat[int(self.__Local_X[i]/self.__X_step)][int(self.__Local_Y[i]/self.__Y_step)]+=1
            if (self.__Stat[int(self.__Local_X[i]/self.__X_step)][int(self.__Local_Y[i]/self.__Y_step)]>self.__MaxStat):
                self.__MaxStat=self.__Stat[int(self.__Local_X[i]/self.__X_step)][int(self.__Local_Y[i]/self.__Y_step)]

    # HeatMap drawing
    
        for i in range(self.__Div):
            for j in range(self.__Div): 
                color = '#%02x%02x%02x' % (int((1-(self.__Stat[i][j]/self.__MaxStat))*255),int((1-(self.__Stat[i][j]/self.__MaxStat))*255),int((1-(self.__Stat[i][j]/self.__MaxStat))*255))
                self.__Canvas.create_rectangle(self.__Margin+self.__X_step*i,self.__Margin+self.__Y_step*j,self.__Margin+self.__X_step*(i+1),self.__Margin+self.__Y_step*(j+1), outline="white", fill = color)
                
    def Trace(self):
        
        self.__Speed           = self.__M_Percent_Speed_Scal.get()
        self.__Trace_Duration  = self.__M_Duration_Trace_Scale.get()
        
        self.DrawTerrain()
        
        self.__trace=[]
        self.__Waiting_Time = 0.00000001*self.__Speed
        self.__Trace_Duration = int(len(self.__X)*self.__Trace_Duration/100)
        
        for i in range(len(self.__Time)):
            self.__trace.append(self.__Canvas.create_line(self.__X[i],self.__Y[i],self.__X[i+1],self.__Y[i+1]))
            #time.sleep(self.__Waiting_Time) 
            
            if (len(self.__trace) > self.__Trace_Duration):
                self.__Canvas.delete(self.__trace[0])
                self.__trace.pop(0)
            self.__Canvas.update()

    def Courbe(self):

        self.__Angle=[]
        aux=-1
        self.__Delta = pow(10,aux)     
        self.__delta = []
        
        while (self.__Delta < 1000):
            
            step = int(self.__Delta/self.__Time[1])
            
            Local_Sum = 0
            Count=0
            
            for i in range(len(self.__Time)-step*2):      
                if ((self.__X[i+step]-self.__X[i]) !=0 and (self.__X[i+step*2]-self.__X[i+step]) !=0 ):
                    
                    M12 = (self.__Y[i+step]-self.__Y[i])/(self.__X[i+step]-self.__X[i])
                    M23 = (self.__Y[i+step*2]-self.__Y[i+step])/(self.__X[i+step*2]-self.__X[i+step])
                    
                    Local_Sum += math.atan((M23-M12)/(1+M12*M23)) 
                    Count +=1
            
            self.__Angle.append(Local_Sum/Count)
            self.__Delta = math.pow(10,aux)
            self.__delta.append(self.__Delta)
            
            aux += 0.1
            
        x=self.__delta
        y=self.__Angle
        
        plt.plot(x,y)
        
        
window = MainWindow() 
window.mainloop() 



















         
         