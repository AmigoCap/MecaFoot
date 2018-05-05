import math
import matplotlib.pyplot as plt
import os
import tkinter
from tkinter import ttk
import Joueur_v2 as J
from PIL import Image, ImageTk
   
class MainWindow(tkinter.Tk):
    def __init__(self):
        
        """ VARIABLES """
        # MAIN ________________________________________________________________
        """MARC"""
        self.__Work_Directory_Marc = "C:/Users/marcl/Dropbox/PAr 143 - Acquisition de donnée sportives/Programmation/Data"
        """ALFONSO"""
        self.__Work_Directory_Alfonso = "C:/Users/fonss/Dropbox (Personal)/PAr 143 - Acquisition de donnée sportives/Programmation/Data"
        
        # Main Window _________________________________________________________
        self.__Title = "PAr 143 - Traitement Donnée Sportives"
    
        self.__BG_Color   = ""
        self.__Text_Style = ""
        self.__Text_Size  = ""
        
        # Data ________________________________________________________________
        self.__Charge_Done = False     # Allows to know if any data has been charge before using the program
        # Figures _____________________________________________________________
        
        # Heat Map ____________________________________________________________
        
        # Time Line ___________________________________________________________    
        self.__Start_Time = 0
        self.__End_Time = 0
        
        # Terrain _____________________________________________________________
        self.__H_Canvas=500
        self.__W_Canvas=300
                
        self.__Margin = 0
        self.__Scale = 0
        
        self.__Ratio = 1 
        
        self.__Terrain = "Rugby"
        """RUGBY"""
        self.__Rugby_W=70     #meters
        self.__Rugby_H=140    #meters

        """FOOT"""
        self.__Foot_W=75
        self.__Foot_H=110
         
        """IN-SIDE HOCKEY"""
        self.__IS_Hockey_W=25
        self.__IS_Hockey_H=50
        
        """OUT-SIDE HOCKEY"""
        self.__OS_Hockey_W=50
        self.__OS_Hockey_H=90
        
        # Range Slider ________________________________________________________
        self.__H_RS_Canvas=100
        self.__W_RS_Canvas=500
        
    # Initialize
        tkinter.Tk.__init__(self)         
        self.title(self.__Title)  
        
        try:
            os.chdir(self.__Work_Directory_Marc)
            self.__DataFiles_List = os.listdir(self.__Work_Directory_Marc)
            self.__Work_Directory=self.__Work_Directory_Marc
        
        except FileNotFoundError:
            os.chdir(self.__Work_Directory_Alfonso)
            self.__DataFiles_List = os.listdir(self.__Work_Directory_Alfonso)
            self.__Work_Directory=self.__Work_Directory_Alfonso
            
    # Main Panels
    
        self.__D_Panel      = tkinter.LabelFrame(self, text="Data selection")
        self.__C_Panel      = tkinter.LabelFrame(self, text="Figure parameters")
        self.__H_Panel      = tkinter.LabelFrame(self, text="HeatMap parameters")
        self.__T_Panel      = tkinter.LabelFrame(self, text="Mouvement parameters ")
        self.__F_Panel      = tkinter.LabelFrame(self, text="Terrain Drawing")
        self.__Fig_Panel    = tkinter.LabelFrame(self, text="Figure Drawing")
        self.__RS_Panel     = tkinter.LabelFrame(self, text="Time Line")
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=6)
        self.grid_columnconfigure(2,weight=2)      
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)      
        self.grid_rowconfigure(3,weight=0)
        self.grid_rowconfigure(4,weight=1)
        
    # Data_Panel elements
        self.__Match = tkinter.StringVar()
    
        self.__D_Data_Combobox = tkinter.ttk.Combobox(self.__D_Panel, textvariable = self.__Match)
        self.__D_LoadButton    = tkinter.Button(self.__D_Panel, text = "Charger", relief = "raised", command = self.Load_Data)
        self.__D_Info_Label    = tkinter.Label(self.__D_Panel, text =" Choose any match to see more info")
        
        self.__D_Data_Combobox['values'] = self.__DataFiles_List
        
        self.__D_Data_Combobox.grid(row = 0, column = 0)
        self.__D_LoadButton.grid(row = 0, column = 1)
        self.__D_Info_Label.grid(row = 1, column = 0, columnspan=1, sticky='N' )

        self.__D_Panel.grid_columnconfigure(0,weight=1)
        self.__D_Panel.grid_columnconfigure(1,weight=1)
        self.__D_Panel.grid_rowconfigure(0,weight=1)
        self.__D_Panel.grid_rowconfigure(1,weight=1)
        self.__D_Panel.grid(row=0, column=0,sticky='NSEW')
      
    # Figure_Parameter_Panel elements
    
        self.__Figure_Check = []
        self.__Figure_Save_Check = []
        for i in range(4):
            self.__Figure_Check.append(tkinter.IntVar())
            self.__Figure_Save_Check .append(tkinter.IntVar())
        
        self.__C_Speed_CheckButton    = tkinter.Checkbutton(self.__C_Panel, text='Vitesse / Temps', variable=self.__Figure_Check[0], command = self.ShowFigure)
        self.__C_Angle_CheckButton    = tkinter.Checkbutton(self.__C_Panel, text='Theta / Temps', variable=self.__Figure_Check[1], command = self.ShowFigure)
        self.__C_AngleVar_CheckButton = tkinter.Checkbutton(self.__C_Panel, text='Theta / Tau', variable=self.__Figure_Check[2], command = self.ShowFigure)
        self.__C_Aux_CheckButton      = tkinter.Checkbutton(self.__C_Panel, text='Vitesse Histogram', variable=self.__Figure_Check[3], command = self.ShowFigure)
        self.__C_Speed_SaveButton     = tkinter.Button(self.__C_Panel, text='Save Plot as ',command = self.SaveFigure)
        self.__C_Angle_SaveButton     = tkinter.Button(self.__C_Panel, text='Save Plot as ',command = self.SaveFigure)
        self.__C_AngleVar_SaveButton  = tkinter.Button(self.__C_Panel, text='Save Plot as ',command = self.SaveFigure)
        self.__C_Aux_SaveButton       = tkinter.Button(self.__C_Panel, text='Save Plot as ',command = self.SaveFigure)
        self.__C_AngleVar_Label       = tkinter.Label(self.__C_Panel, text= '')

        self.__C_Speed_CheckButton.grid(row = 0, column = 0, sticky = "W")  
        self.__C_Speed_SaveButton.grid(row = 0, column = 1, sticky = "E")
        self.__C_Angle_CheckButton.grid(row = 1, column = 0, sticky = "W")   
        self.__C_Angle_SaveButton.grid(row = 1, column = 1, sticky = "E")
        self.__C_AngleVar_CheckButton.grid(row = 2, column = 0, sticky = "W")
        self.__C_AngleVar_SaveButton.grid(row = 2, column = 1, sticky = "E")
        self.__C_AngleVar_Label.grid(row = 2, column = 2, sticky = "E")
        self.__C_Aux_CheckButton.grid(row = 3, column = 0, sticky = "W")
        self.__C_Aux_SaveButton.grid(row = 3, column = 1, sticky = "E")
        
        self.__C_Panel.grid(row=1, column=0,sticky='NSEW')
        
    # HeatMap_Panel elements
    
        self.__H_Divisions_Scale = tkinter.Scale(self.__H_Panel,from_=1, to=200, orient="horizontal", label = "Nb de division")
        self.__H_ShowButton      = tkinter.Button(self.__H_Panel, text = "Afficher", relief = "raised", command = self.ShowHeatMap)
        
        self.__H_Divisions_Scale.pack(expand="true")
        self.__H_ShowButton.pack(expand="true")
        
        self.__H_Panel.grid(row=2, column=0,sticky='NSEW')
        
    # Trace_Panel elements
    
        self.__T_PlayButoton = tkinter.Button(self.__T_Panel, text = "Play",relief = "raised",command = self.ShowTrace)
        self.__T_StopButton  = tkinter.Button(self.__T_Panel, text = "Stop", relief = "raised",command = self.ShowTrace)
        self.__T_PauseButton = tkinter.Button(self.__T_Panel, text = "Pause", relief = "raised",command = self.ShowPoints)
        
        self.__T_PlayButoton.pack(fill = "both", expand = "true",side="left")
        self.__T_StopButton.pack(fill = "both", expand = "true", side="left")
        self.__T_PauseButton.pack(fill = "both", expand = "true", side="left")
        
        self.__T_Panel.grid(row=3, column=0,sticky='NSEW')
        
    # Terrain Panel
   
        self.__Canvas = tkinter.Canvas(self.__F_Panel,height = self.__H_Canvas,width = self.__W_Canvas,highlightthickness=0)
        self.__Canvas.pack(expand="true")
        
        self.__F_Panel.grid(row=0,column=1,rowspan=4,sticky='NSEW') 
        
    # Figure Panel 
    
        self.__Speed_Plot      = tkinter.Label(self.__Fig_Panel)
        self.__Speed_Hist_Plot = tkinter.Label(self.__Fig_Panel)
        self.__Tau_Plot        = tkinter.Label(self.__Fig_Panel)
        self.__Theta_Plot      = tkinter.Label(self.__Fig_Panel)
                
        self.__Speed_Plot.pack()
        self.__Speed_Hist_Plot.pack()
        self.__Tau_Plot.pack()
        self.__Theta_Plot.pack()
        
        self.__Fig_Panel.grid(row=0,column=2,rowspan=4,sticky='NSEW')

     # Range Slider elements 

        self.__RS_Canvas = tkinter.Canvas(self.__RS_Panel,height = self.__H_RS_Canvas,width = self.__W_RS_Canvas,highlightthickness=0)
        self.__RS_Canvas.pack(expand="true")
        
        self.__RS_Panel.grid(row=4,column=0,columnspan=3,sticky='NSEW') 

#-----------------------------------------------------------------------------------------------------------------------------------
     
    def Load_Data(self):
        X_mid = 43.482162
        Y_mid = -1.536879
        self.__PI = 3.14159
        self.__R_Earth = 6378000.0

        File_Name = str(self.__D_Data_Combobox.get())
        
        self.__Player = J.Joueur()
        self.__Player.Set_Work_Directory(self.__Work_Directory)
        
        self.__DataFile = open(File_Name,"r")
        self.__Data = self.__DataFile.readlines()
           
        for l in self.__Data:
            dataline = l.split()
            self.__Player.Set0_Time(float(dataline[0]))
            self.__Player.Set0_X_Vel(float(dataline[1])/3.6*self.__Scale)
            self.__Player.Set0_X_Acc(float(dataline[2]))
            #self.__Odometer.append(float(dataline[3]))
            self.__Player.Set0_Y_Pos(float(dataline[5]))
            self.__Player.Set0_X_Pos(float(dataline[4]))
        
        self.__DataFile.close()
        
        self.DrawTerrain()
        self.DrawRangeSlider()

        """Data Transformation from GPS to M relative to the up left corner"""

        self.__X_Translation = self.__Margin*self.__Scale*0.2
        self.__Y_Translation = self.__Margin*self.__Scale*0.2
        
        for i in range(self.__Player.Get_len()):
            self.__Player.Set_X_Pos(i,(abs(X_mid-self.__Player.Get_X_Pos(i))*self.__PI/180*self.__R_Earth*self.__Scale*0.5)+self.__X_Translation)
            self.__Player.Set_Y_Pos(i,(abs(Y_mid-self.__Player.Get_Y_Pos(i))*self.__PI/180*self.__R_Earth*self.__Scale*0.5)+self.__Y_Translation)

        self.__Charge_Done = True
        print ("Data Load Done")
        
#-----------------------------------------------------------------------------------------------------------------------------------
    def TerrainSize(self):
        if (self.__Terrain == "Rugby"):
            print ("Rugby Terrain Choose")
            self.__Ratio = self.__Rugby_W/self.__Rugby_H
            
        elif (self.__Terrain == "Football"):
            print ("Football Terrain Choose")
            self.__Ratio = self.__Foot_W/self.__Foot_H
            
        elif (self.__Terrain == "Out-Side Hockey"):
            print ("Out-Side Hockey Terrain Choose") 
            self.__Ratio = self.__OS_Hockey_W/self.__OS_Hockey_H
            
        elif (self.__Terrain == "In-Side Hockey"):
            print ("In-Side Hockey Terrain Choose")
            self.__Ratio = self.__IS_Hockey_W/self.__IS_Hockey_H
        else: 
            print ("ERROR : No terrain form catch ! ")
#-----------------------------------------------------------------------------------------------------------------------------------
          
    def DrawTerrain(self):
        
        self.__Canvas.delete("all")
        self.TerrainSize()
        
        self.__H_Canvas = 0.98*self.__F_Panel.winfo_height()
        self.__W_Canvas = self.__H_Canvas*self.__Ratio
        self.__Margin=0.05*self.__F_Panel.winfo_width()

        self.__Canvas.configure(height = self.__H_Canvas, width = self.__H_Canvas*self.__Ratio)
        self.__Canvas.pack(expand="true")

        if (self.__Terrain == "Rugby"):  
            
            self.__Scale=self.__H_Canvas/self.__Rugby_H
            self.__Canvas.create_rectangle(self.__Margin*self.__Ratio,             self.__Margin,                                    self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas-self.__Margin,                 fill = "#38CB3F")
            self.__Canvas.create_rectangle(self.__Margin*self.__Ratio,             self.__Margin+20*self.__Scale,                    self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas-20*self.__Scale-self.__Margin, fill = "#27CF2E")
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5,                              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5)
            # GOALS
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-2.5*self.__Scale,   self.__Margin+20*self.__Scale-5,                  self.__W_Canvas*0.5+2.5*self.__Scale,              self.__Margin+20*self.__Scale+5,                fill = "#000000")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-2.5*self.__Scale,   self.__H_Canvas-self.__Margin-20*self.__Scale-5,  self.__W_Canvas*0.5+2.5*self.__Scale,              self.__H_Canvas-self.__Margin-20*self.__Scale+5,fill = "#000000")
           
        elif (self.__Terrain == "Football"):
            self.__Scale=self.__H_Canvas/self.__Foot_H
            self.__Canvas.create_rectangle(self.__Margin*self.__Ratio,             self.__Margin,                                    self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas-self.__Margin,                 fill = "#38CB3F")
            # CENTER
            self.__Canvas.create_oval(     self.__W_Canvas*0.5-9*self.__Scale,     self.__H_Canvas*0.5-9*self.__Scale,               self.__W_Canvas*0.5+9*self.__Scale,                self.__H_Canvas*0.5+9*self.__Scale,            fill = "#27CF2E")
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5,                              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5)
            # BIG AREAS 
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-20*self.__Scale,    self.__Margin,                                    self.__W_Canvas*0.5+20*self.__Scale,               self.__Margin+16*self.__Scale,                 fill = "#27CF2E")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-20*self.__Scale,    self.__H_Canvas-self.__Margin,                    self.__W_Canvas*0.5+20*self.__Scale,               self.__H_Canvas-self.__Margin-16*self.__Scale, fill = "#27CF2E")
            # S AREAS 
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-9*self.__Scale,     self.__Margin,                                    self.__W_Canvas*0.5+9*self.__Scale,                self.__Margin+5.5*self.__Scale,                 fill = "#38CB3F")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-9*self.__Scale,     self.__H_Canvas-self.__Margin,                    self.__W_Canvas*0.5+9*self.__Scale,                self.__H_Canvas-self.__Margin-5.5*self.__Scale, fill = "#38CB3F")
            # GOALS
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-3.5*self.__Scale,   self.__Margin-5,                                  self.__W_Canvas*0.5+3.5*self.__Scale,              self.__Margin+5,                                fill = "#000000")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-3.5*self.__Scale,   self.__H_Canvas-self.__Margin-5,                  self.__W_Canvas*0.5+3.5*self.__Scale,              self.__H_Canvas-self.__Margin+5,                fill = "#000000")
           
        elif (self.__Terrain == "Out-Side Hockey"):
            self.__Scale=self.__H_Canvas/self.__OS_Hockey_H
            self.__Canvas.create_rectangle(self.__Margin*self.__Ratio,             self.__Margin,                                    self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas-self.__Margin,                 fill = "#38CB3F")
            # AREAS 
            self.__Canvas.create_arc(self.__W_Canvas*0.5-15*self.__Scale,          self.__Margin-15*self.__Scale,                    self.__W_Canvas*0.5+15*self.__Scale,               self.__Margin+15*self.__Scale,                 fill = "#27CF2E", start = 180, extent = 180)
            self.__Canvas.create_arc(self.__W_Canvas*0.5-15*self.__Scale,          self.__H_Canvas-self.__Margin-15*self.__Scale,    self.__W_Canvas*0.5+15*self.__Scale,               self.__H_Canvas-self.__Margin+15*self.__Scale, fill = "#27CF2E", start = 0,   extent = 180)
            # CENTER
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5,                              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5)
            # QUARTER LINES
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5-20*self.__Scale,              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5-20*self.__Scale)
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5+20*self.__Scale,              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5+20*self.__Scale)
            # GOALS
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-1.5*self.__Scale,   self.__Margin-5,                                  self.__W_Canvas*0.5+1.5*self.__Scale,              self.__Margin+5,                                fill = "#000000")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-1.5*self.__Scale,   self.__H_Canvas-self.__Margin-5,                  self.__W_Canvas*0.5+1.5*self.__Scale,              self.__H_Canvas-self.__Margin+5,                fill = "#000000")
           
        elif (self.__Terrain == "In-Side Hockey"):
            self.__Scale=self.__H_Canvas/self.__IS_Hockey_H
            self.__Canvas.create_rectangle(self.__Margin*self.__Ratio,             self.__Margin,                                    self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas-self.__Margin,                 fill = "#38CB3F")
            # CENTER
            self.__Canvas.create_line(     self.__Margin*self.__Ratio,             self.__H_Canvas*0.5,                              self.__W_Canvas-self.__Margin*self.__Ratio,        self.__H_Canvas*0.5)
            # AREAS 
            self.__Canvas.create_arc(self.__W_Canvas*0.5-10*self.__Scale,        self.__Margin-10*self.__Scale,                  self.__W_Canvas*0.5+10*self.__Scale,               self.__Margin+10*self.__Scale,                 fill = "#27CF2E", start = 180, extent = 180)
            self.__Canvas.create_arc(self.__W_Canvas*0.5-10*self.__Scale,        self.__H_Canvas-self.__Margin-10*self.__Scale,  self.__W_Canvas*0.5+10*self.__Scale,               self.__H_Canvas-self.__Margin+10*self.__Scale, fill = "#27CF2E", start = 0,   extent = 180)
            # GOALS
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-1.5*self.__Scale,   self.__Margin-5,                                  self.__W_Canvas*0.5+1.5*self.__Scale,              self.__Margin+5,                                fill = "#000000")
            self.__Canvas.create_rectangle(self.__W_Canvas*0.5-1.5*self.__Scale,   self.__H_Canvas-self.__Margin-5,                  self.__W_Canvas*0.5+1.5*self.__Scale,              self.__H_Canvas-self.__Margin+5,                fill = "#000000")
           
        else: 
            print ("ERROR : No terrain form catch ! ")
                
#-----------------------------------------------------------------------------------------------------------------------------------    
    def DrawRangeSlider(self):
        
        self.__RS_Canvas.delete("all")
        
        self.__H_RS_Canvas = 0.90*self.__RS_Panel.winfo_height()
        self.__W_RS_Canvas = 0.90*self.__RS_Panel.winfo_width()

        self.__RS_Canvas.configure(height = self.__H_RS_Canvas, width = self.__W_RS_Canvas)
        self.__RS_Canvas.pack(expand="true")
        
        self.__H_Back_Bar= 0.2*self.__H_RS_Canvas
        self.__H_Front_Bar= 0.5*self.__H_Back_Bar
        self.__W_Cursor = 0.02*self.__W_RS_Canvas
        self.__H_Cursor = 0.4*self.__H_RS_Canvas
        
        self.__XA = self.__Margin
        self.__XB = self.__W_RS_Canvas-self.__Margin
        
        self.__RS_Canvas.create_rectangle(self.__Margin,self.__H_RS_Canvas/2-self.__H_Back_Bar/2,self.__W_RS_Canvas-self.__Margin,self.__H_RS_Canvas/2+self.__H_Back_Bar/2, fill = "#38CB3F")  
        self.__A_Cursor = self.__RS_Canvas.create_rectangle(self.__XA-self.__W_Cursor/2,self.__H_RS_Canvas/2-self.__H_Cursor/2,self.__XA+self.__W_Cursor/2,self.__H_RS_Canvas/2+self.__H_Cursor/2,fill = "#000000")
        self.__B_Cursor = self.__RS_Canvas.create_rectangle(self.__XB-self.__W_Cursor/2,self.__H_RS_Canvas/2-self.__H_Cursor/2,self.__XB+self.__W_Cursor/2,self.__H_RS_Canvas/2+self.__H_Cursor/2,fill = "#000000")
        self.__Bar = self.__RS_Canvas.create_rectangle(self.__XA,self.__H_RS_Canvas/2-self.__H_Front_Bar/2,self.__XB,self.__H_RS_Canvas/2+self.__H_Front_Bar/2,fill = "#000000")

        self.__RS_Canvas.bind('<B1-Motion>', self.Cursor_Moved)
        self.__RS_Canvas.bind('<Button-1>', self.Cursor_Clicked)
        
        self.Aux_Time_Function()
        
        self.__A_Time = self.__RS_Canvas.create_text(self.__XA, self.__Margin*0.4, text = self.TimeConversion(self.__Start_Time))                                                 
        self.__B_Time = self.__RS_Canvas.create_text(self.__XB, self.__Margin*0.4, text = self.TimeConversion(self.__End_Time))                                                 
        
    def Cursor_Moved(self, event):

        if (abs(event.x-self.__XA) < self.__W_Cursor*2) and (event.x>self.__Margin) and (event.x<self.__W_RS_Canvas-self.__Margin) :
            self.__RS_Canvas.move(self.__A_Cursor,event.x-self.__XA,0)
            self.__XA=event.x
            self.__RS_Canvas.delete(self.__Bar)
            self.__Bar = self.__RS_Canvas.create_rectangle(self.__XA,self.__H_RS_Canvas/2-self.__H_Front_Bar/2,self.__XB,self.__H_RS_Canvas/2+self.__H_Front_Bar/2,fill = "#000000") 
                                                  
        elif (abs(event.x-self.__XB) < self.__W_Cursor*2) and (event.x>self.__Margin) and (event.x<self.__W_RS_Canvas-self.__Margin) :
            self.__RS_Canvas.move(self.__B_Cursor,event.x-self.__XB,0)
            self.__XB=event.x        
            self.__RS_Canvas.delete(self.__Bar)
            self.__Bar = self.__RS_Canvas.create_rectangle(self.__XA,self.__H_RS_Canvas/2-self.__H_Front_Bar/2,self.__XB,self.__H_RS_Canvas/2+self.__H_Front_Bar/2,fill = "#000000")
                       
        elif (event.x>self.__XA) and (event.x < self.__XB) and (abs(event.y-self.__H_RS_Canvas/2)<self.__H_Front_Bar):
            if (self.__XA>self.__Margin) and (self.__XB<self.__W_RS_Canvas-self.__Margin):
                dif = event.x-self.__aux_x
                self.__RS_Canvas.move(self.__B_Cursor,dif,0)
                self.__RS_Canvas.move(self.__A_Cursor,dif,0)
                self.__RS_Canvas.move(self.__Bar,dif,0)
                self.__XA+=dif
                self.__XB+=dif
                self.__aux_x = event.x
                
        self.__RS_Canvas.delete(self.__A_Time)
        self.__RS_Canvas.delete(self.__B_Time) 

        self.__A_Time = self.__RS_Canvas.create_text(self.__XA, self.__Margin*0.4, text = self.TimeConversion(self.__Start_Time))                                                 
        self.__B_Time = self.__RS_Canvas.create_text(self.__XB, self.__Margin*0.4, text = self.TimeConversion(self.__End_Time))                                                 
    
        self.Aux_Time_Function()
   
    def Cursor_Clicked(self, event):
        self.__aux_x = event.x

#-----------------------------------------------------------------------------------------------------------------------------------
       
    def ShowFigure (self):
        self.Courbe()
        
    def ShowTrace (self):
        self.Trace()
        
    def ShowHeatMap (self):
        self.HeatMap()
    
#-----------------------------------------------------------------------------------------------------------------------------------
    def HeatMap(self):
        self.DrawTerrain()
        self.Aux_Time_Function()
        
        self.__Player.HeatMap(self.__Start_Time, self.__End_Time, self.__Div, self.__X_step, self.__Y_step)
 
        Max_Aux = self.__Player.Get_MaxStat()

        for i in range(self.__Div):
            for j in range(self.__Div):
                aux = int((1-(self.__Player.Get_Stat(i,j)/Max_Aux))*255)
                color = '#%02x%02x%02x' % (aux, aux, aux)
                self.__Canvas.create_rectangle(self.__X_step*i,self.__Y_step*j,self.__X_step*(i+1),self.__Y_step*(j+1), outline="white", fill = color)
                
#------------------------------------------------------------------------------------------------------------------------------------------
    def Trace(self):
        self.DrawTerrain()
        self.Aux_Time_Function()
        Time_Length = self.__Player.Get_len()
        
        self.__trace=[]

        self.__Timer = self.__Canvas.create_text(self.__Margin*4, self.__Margin*2, text="")
        
        for i in range(Time_Length):
            s = self.__Player.Get_Time(i)
            if (s > self.__Start_Time and s < self.__End_Time):
                self.__trace.append(self.__Canvas.create_line(self.__Player.Get_X_Pos(i),self.__Player.Get_Y_Pos(i),self.__Player.Get_X_Pos(i+1),self.__Player.Get_Y_Pos(i+1)))
                self.__Canvas.itemconfigure(self.__Timer,text = self.TimeConversion(s))
                if (len(self.__trace) > 100):
                    self.__Canvas.delete(self.__trace[0])
                    self.__trace.pop(0)
                   
            self.__Canvas.update()

#--------------------------------------------------------------------------------------------------------------------------------------------
    def Courbe(self):
        if str(self.__Figure_Check[0].get()) == "1":
            self.__Player.Speed_Plot(self.__Start_Time, self.__End_Time)
            self.__MyImage_0 = Image.open("Speed_Plot.png")
            self.__Speed_Plot_Image = ImageTk.PhotoImage(self.__MyImage_0)
            self.__Speed_Plot.config(image = self.__Speed_Plot_Image)
            self.__Speed_Plot.update()
        else:
            self.__Speed_Plot.config(image = '')
            
        if str(self.__Figure_Check[1].get()) == "1":
            self.__Player.Theta_Plot(self.__Start_Time, self.__End_Time)
            self.__MyImage_1 = Image.open("Theta_Plot.png")
            self.__Theta_Plot_Image = ImageTk.PhotoImage(self.__MyImage_1)
            self.__Theta_Plot.config(image = self.__Theta_Plot_Image)
            self.__Theta_Plot.update()
        else:
            self.__Theta_Plot.config(image = '')
            
        if str(self.__Figure_Check[2].get()) == "1":
            self.__Player.Tau_Plot(self.__Start_Time, self.__End_Time,self.__C_AngleVar_Label)
            self.__MyImage_2 = Image.open("Tau_Plot.png")
            self.__Tau_Plot_Image = ImageTk.PhotoImage(self.__MyImage_2)
            self.__Tau_Plot.config(image = self.__Tau_Plot_Image)
            self.__Tau_Plot.update()
        else:
            self.__Tau_Plot.config(image = '')
            self.__C_AngleVar_Label.config(text = '')
            
        if str(self.__Figure_Check[3].get()) == "1":
            self.__Player.Speed_Hist_Plot(self.__Start_Time, self.__End_Time)
            self.__MyImage_3 = Image.open("Speed_Hist_Plot.png")
            self.__Speed_Hist_Plot_Image = ImageTk.PhotoImage(self.__MyImage_3)
            self.__Speed_Hist_Plot.config(image = self.__Speed_Hist_Plot_Image)
            self.__Speed_Hist_Plot.update()
        else:
            self.__Speed_Hist_Plot.config(image = '')
            
#-------------------------------------------------------------------------------------------------------
        
    def Aux_Time_Function(self):
        
        self.__Div    = self.__H_Divisions_Scale.get()
        self.__X_step = int((self.__W_Canvas-self.__Margin*self.__Ratio)/self.__Div)+1
        self.__Y_step = int((self.__H_Canvas-self.__Margin)/self.__Div)+1

        self.__Start_Time = (self.__XA-self.__Margin)/(self.__W_RS_Canvas-self.__Margin)
        self.__End_Time   = (self.__XB-self.__Margin)/(self.__W_RS_Canvas-self.__Margin)
        self.__Duration   = self.__End_Time-self.__Start_Time
                            
        self.__Start_Time = self.__Start_Time*self.__Player.Get_Time(-1)
        self.__End_Time   = self.__End_Time*self.__Player.Get_Time(-1)
        self.__Duration   = self.__Duration*self.__Player.Get_Time(-1)
        
#-----------------------------------------------------------------------------------
        
    def TimeConversion(self, Time):
        if Time<60 : 
            Text_Time = str(int(Time)) + " s "
        elif Time>3600: 
            Text_Time = str(int(Time/3600))+" h "+str(int((Time-3600)/60))+" min "+str(int(Time-int(Time/60)*60))+" s "
        else : 
            Text_Time = str(int(Time/60))+" min "+str(int(Time-int(Time/60)*60))+" s "
        return Text_Time
    
#-----------------------------------------------------------------------------------
    
    def SaveFigure(self):
        print("Figure saved succesfuly")
        
#-----------------------------------------------------------------------------------
    def ShowPoints(self):

        self.Aux_Time_Function()
        
        Time_aux = self.__Player.Get_len()
   
        for i in range(Time_aux):          
            s = self.__Player.Get_Time(i)
            if (s > self.__Start_Time and s < self.__End_Time):
                x=self.__Player.Get_X_Pos(i)
                y=self.__Player.Get_Y_Pos(i)
                self.__Canvas.create_line(x,y,x+1,y+1)                   
        self.__Canvas.update()
        
#-----------------------------------------------------------------------------------
          
        
window = MainWindow() 
window.mainloop() 



















         
         