import math
import matplotlib.pyplot as plt
import os
import tkinter
from tkinter import ttk
import Joueur_v3 as J
import time
from PIL import Image, ImageTk
   
class MainWindow(tkinter.Tk):
    def __init__(self):
        
        """ VARIABLES """
        # MAIN ________________________________________________________________
        """MARC"""
        self.__Work_Directory_Marc = "C:/Users/marcl/Dropbox/PAr 143 - Acquisition de donnée sportives/Programmation/Data"
        """ALFONSO"""
        self.__Work_Directory_Alfonso = "C:/Users/fonss/Dropbox (Personal)/PAr 143 - Acquisition de donnée sportives/Programmation Python/Data"
        
        # Main Window _________________________________________________________
        self.__Title = "PAr 143 - Traitement Donnée Sportives"
        # Data ________________________________________________________________
        self.__Charge_Done = False     # Allows to know if any data has been charge before using the program
        # Figures _____________________________________________________________
        self.__H_Canvas = 600
        self.__W_Canvas = 400
        # Heat Map ____________________________________________________________
        self.__Div = 100
        # Time Line ___________________________________________________________    
        self.__Start_Time = 0
        self.__End_Time = 0
       
        self.__Trace_Condition=False

        """RUGBY"""
        self.__Rugby_W=70     #meters
        self.__Rugby_H=140    #meters

    # Initialize
        tkinter.Tk.__init__(self)         
        self.title(self.__Title)  
        
        try:
            os.chdir(self.__Work_Directory_Marc)
            self.__Matchs_List = os.listdir(self.__Work_Directory_Marc)
            self.__Work_Directory=self.__Work_Directory_Marc
            self.__Players_List = []
            
        except FileNotFoundError:
            os.chdir(self.__Work_Directory_Alfonso)
            self.__Matchs_List = os.listdir(self.__Work_Directory_Alfonso)
            self.__Work_Directory=self.__Work_Directory_Alfonso
            self.__Players_List = []
    
    # Notebook
        self.__Notebook = tkinter.ttk.Notebook(self)
        
        self.__Data_Frame = ttk.Frame(self.__Notebook)
        self.__Visualitation_Frame = tkinter.ttk.Frame(self.__Notebook)
        self.__Analyse_Frame = tkinter.ttk.Frame(self.__Notebook)
        
        self.__Notebook.add(self.__Data_Frame, text='DATA')
        self.__Notebook.add(self.__Visualitation_Frame, text='VISUALITATION')
        self.__Notebook.add(self.__Analyse_Frame, text='ANALYSE')
        
        self.__Notebook.pack(fill = "both",expand = "true")
        
        self.Data_Panel_init()
        self.Visualitation_Panel_init()
        self.Analyse_Panel_init()
        
        self.bind("<Configure>", self.Main_Window_Resize)
        
    def Main_Window_Resize(self,event):
        self.__H_Canvas = self.__Pitch_Panel.winfo_height()
        self.__W_Canvas = self.__Pitch_Panel.winfo_width()
        self.__H_Time_Canvas = self.__Time_Panel.winfo_height()
        self.__W_Time_Canvas = self.__Time_Panel.winfo_width() 
        self.__W_Heat_Map_Canvas = self.__Heat_Map_Canvas.winfo_width()   
        self.__H_Heat_Map_Canvas = self.__Heat_Map_Canvas.winfo_height()  
 
        if(self.__Charge_Done):
            self.DrawTerrain()
            self.DrawRangeSlider()
#-----------------------------------------------------------------------------------------------------------------------------------
    # Data Panels  
    def Data_Panel_init(self):
        self.__Match = tkinter.StringVar()
        self.__Players = tkinter.StringVar()
        
        self.__Match_Label    = tkinter.Label(self.__Data_Frame, text =" Choose any match")     
        self.__Matchs_Combobox = tkinter.ttk.Combobox(self.__Data_Frame, textvariable = self.__Match)
        self.__Players_Label    = tkinter.Label(self.__Data_Frame, text =" ")     
        self.__Players_Combobox = tkinter.ttk.Combobox(self.__Data_Frame, textvariable = self.__Players)
        self.__LoadMatchButton    = tkinter.Button(self.__Data_Frame, text = "Load Match", relief = "raised", command = self.Load_Match)
        self.__Info_Label    = tkinter.Label(self.__Data_Frame, text =" Choose any match to see more info")
        self.__LoadPlayerButton    = tkinter.Button(self.__Data_Frame, text = "Load Player", relief = "raised", command = self.Load_Player)
        
        self.__Match_Label.pack(expand = "true",side="top")
        self.__Matchs_Combobox.pack(expand = "true",side="top")
        self.__LoadMatchButton.pack(expand = "true",side="top")
        self.__Players_Label.pack(expand = "true",side="top")
        self.__Players_Combobox.pack(expand = "true",side="top")
        self.__LoadPlayerButton.pack(expand = "true",side="top")
        self.__Info_Label.pack(expand = "true",side="top")
        
        self.__Matchs_Combobox['values'] = self.__Matchs_List
        self.__Players_Combobox['values'] = self.__Players_List
#-----------------------------------------------------------------------------------------------------------------------------------
    # ANALYSE Panels        
    def Analyse_Panel_init(self):
        self.__Figure_Check = []
        for i in range(4):
            self.__Figure_Check.append(tkinter.IntVar())
            
        self.__S_Panel = tkinter.LabelFrame(self.__Analyse_Frame, text="Selection of Figures ")
        self.__F_Panel = tkinter.LabelFrame(self.__Analyse_Frame, text="Figures Visualitation ")
        self.__Analyse_Frame.grid_columnconfigure(0,weight=1)
        self.__Analyse_Frame.grid_columnconfigure(1,weight=8) 
        self.__Analyse_Frame.grid_rowconfigure(0,weight=1) 
        self.__Speed_CheckButton    = tkinter.Checkbutton(self.__S_Panel, text='Vitesse / Temps', variable=self.__Figure_Check[0], command = self.ShowFigure)
        self.__Angle_CheckButton    = tkinter.Checkbutton(self.__S_Panel, text='Theta / Temps', variable=self.__Figure_Check[1], command = self.ShowFigure)
        self.__AngleVar_CheckButton = tkinter.Checkbutton(self.__S_Panel, text='Theta / Tau', variable=self.__Figure_Check[2], command = self.ShowFigure)
        self.__AngleVar_Label       = tkinter.Label(self.__S_Panel, text='')
        self.__Aux_CheckButton      = tkinter.Checkbutton(self.__S_Panel, text='Vitesse Histogram', variable=self.__Figure_Check[3], command = self.ShowFigure)
        self.__Speed_CheckButton.pack(expand = "true",fill = "both",side = "top")
        self.__Angle_CheckButton.pack(expand = "true",fill = "both",side = "top")
        self.__AngleVar_CheckButton.pack(expand = "true",fill = "both",side = "top")
        self.__AngleVar_Label.pack(expand = "true",fill = "both",side = "top")
        self.__Aux_CheckButton.pack(expand = "true",fill = "both",side = "top")
        self.__S_Panel.grid(row = 0, column=0,sticky='NSEW')
        self.__Speed_Plot      = tkinter.Label(self.__F_Panel)
        self.__Speed_Hist_Plot = tkinter.Label(self.__F_Panel)
        self.__Tau_Plot        = tkinter.Label(self.__F_Panel)
        self.__Theta_Plot      = tkinter.Label(self.__F_Panel)        
        self.__Speed_Plot.pack(expand = "true",fill = "both")
        self.__Speed_Hist_Plot.pack(expand = "true",fill = "both")
        self.__Tau_Plot.pack(expand = "true",fill = "both")
        self.__Theta_Plot.pack(expand = "true",fill = "both")
        self.__F_Panel.grid(row = 0,column=1,sticky='NSEW')
#-----------------------------------------------------------------------------------------------------------------------------------
    # VISUALITATION Panel
    def Visualitation_Panel_init(self):
        self.__P_Panel        = tkinter.LabelFrame(self.__Visualitation_Frame, text="Visualitation Parameters ")
        self.__Pitch_Panel    = tkinter.LabelFrame(self.__Visualitation_Frame, text="Pitch")
        self.__Time_Panel     = tkinter.LabelFrame(self.__Visualitation_Frame, text="Time and Pitch Area")  
        self.__Heat_Map_Panel = tkinter.LabelFrame(self.__Visualitation_Frame, text="Heat Map")           
        self.__Video_Panel    = tkinter.LabelFrame(self.__Visualitation_Frame, text="Video")
        self.__Visualitation_Frame.grid_columnconfigure(0,weight=1)
        self.__Visualitation_Frame.grid_columnconfigure(1,weight=6)     
        self.__Visualitation_Frame.grid_rowconfigure(0,weight=3)
        self.__Visualitation_Frame.grid_rowconfigure(1,weight=3)      
        self.__Visualitation_Frame.grid_rowconfigure(2,weight=1)
    # Parameters_Panel elements
        self.__P_PlayButoton = tkinter.Button(self.__P_Panel, text = "Play",relief = "raised",command = self.Play_Button)
        self.__P_StopButton  = tkinter.Button(self.__P_Panel, text = "Stop",relief = "raised",command = self.Stop_Button)
        self.__P_PauseButton = tkinter.Button(self.__P_Panel, text ="Pause",relief = "raised",command = self.Pause_Button) 
        self.__P_PointsButton = tkinter.Button(self.__P_Panel, text ="Points",relief = "raised",command = self.ShowPoints)
        self.__P_PlayButoton.pack(fill = "both", expand = "true",side="left")
        self.__P_StopButton.pack(fill = "both", expand = "true", side="left")
        self.__P_PauseButton.pack(fill = "both", expand = "true", side="left")
        self.__P_PointsButton.pack(fill = "both", expand = "true", side="left")
        self.__P_Panel.grid(row=0, column=0,sticky='NSEW')  
    # Heat_Map Panel
        self.__Heat_Map_Canvas = tkinter.Canvas(self.__Heat_Map_Panel, bd = 0, highlightthickness=0)
        self.__Heat_Map_Canvas.pack(fill = "both", expand = "true")
        self.__Heat_Map_Panel.grid(row=1,column=0,sticky='NSEW')    
    # Video Panel
        self.__Video_Panel.grid(row=2,column=0,sticky='NSEW')
    # Pitch Panel
        self.__Pitch_Canvas = tkinter.Canvas(self.__Pitch_Panel, bd = 0, highlightthickness=0)
        self.__Pitch_Canvas.pack(expand="true")
        self.__Pitch_Panel.grid(row=0,column=1,rowspan=2,sticky='NSEW') 
     # Time Slider elements
        self.__Time_Canvas = tkinter.Canvas(self.__Time_Panel, bd = 0, highlightthickness=0)
        self.__Time_Canvas.pack(expand="true")
        self.__Time_Panel.grid(row=2,column=1,sticky='NSEW')
#-----------------------------------------------------------------------------------------------------------------------------------
    def Load_Match(self):
        self.__Match_Name = str(self.__Matchs_Combobox.get())
        self.__Work_Directory += "/" + self.__Match_Name 
        self.__Players_List = os.listdir(self.__Work_Directory)
        self.__Players_Combobox['values'] = self.__Players_List
        self.__Players_Label.config(text = "Choose any player NOW")
#-----------------------------------------------------------------------------------------------------------------------------------
    def Load_Player(self):
        self.__Charge_Done = True
        File_Name = str(self.__Players_Combobox.get())
        self.__Player = J.Joueur()
        self.__Player.Data_Load(self.__Match_Name,File_Name,self.__Work_Directory)         
        self.__Info_Label.configure(text = "Data Load Done")
#-----------------------------------------------------------------------------------------------------------------------------------
    def DrawTerrain(self):
        self.__Pitch_Canvas.delete("all")
        
        self.__Ratio = self.__Rugby_H/self.__Rugby_W
        self.__W_Canvas = 0.99*self.__W_Canvas
        self.__H_Canvas = self.__W_Canvas/self.__Ratio
        self.__Scale    = self.__H_Canvas/self.__Rugby_H
        self.__X_Margin = self.__W_Canvas*0.01
        self.__Y_Margin = self.__X_Margin*self.__Ratio

        self.__Pitch_Canvas.configure(height = self.__H_Canvas, width = self.__W_Canvas)
        self.__Pitch_Canvas.pack(expand="true")
        
        # PITCH
        self.__Pitch_Canvas.create_rectangle(self.__X_Margin,                   self.__Y_Margin,     self.__W_Canvas-self.__X_Margin,                   self.__H_Canvas-self.__Y_Margin,   fill = "#38CB3F")
        self.__Pitch_Canvas.create_rectangle(self.__X_Margin+20*self.__Scale,   self.__Y_Margin,     self.__W_Canvas-20*self.__Scale-self.__X_Margin,   self.__H_Canvas-self.__Y_Margin,   fill = "#27CF2E")
        self.__Pitch_Canvas.create_line(     self.__W_Canvas*0.5,               self.__Y_Margin,     self.__W_Canvas*0.5,                               self.__H_Canvas-self.__Y_Margin)
#-----------------------------------------------------------------------------------------------------------------------------------    
    def DrawRangeSlider(self):
        self.__Time_Canvas.delete("all")
        
        self.__H_Time_Canvas = self.__H_Time_Canvas
        self.__W_Time_Canvas = 0.99*self.__W_Time_Canvas
        self.__Margin = 0.05*self.__W_Time_Canvas
        
        self.__Time_Canvas.configure(width = self.__W_Time_Canvas)
        self.__Time_Canvas.pack(expand="true")
        
        self.__H_Back_Bar= 0.1*self.__H_Time_Canvas
        self.__H_Front_Bar= 0.5*self.__H_Back_Bar
        self.__W_Cursor = 0.02*self.__W_Time_Canvas
        self.__H_Cursor = 0.2*self.__H_Time_Canvas
        
        self.__XA = self.__Margin+self.__W_Cursor+1
        self.__XB = self.__W_Time_Canvas-self.__Margin-self.__W_Cursor-1
        
        self.__Time_Canvas.create_rectangle(             self.__W_Cursor*0.5+self.__Margin,  self.__H_Time_Canvas*0.75-self.__H_Back_Bar*0.5,     self.__W_Time_Canvas-self.__Margin-self.__W_Cursor*0.5,   self.__H_Time_Canvas*0.75+self.__H_Back_Bar/2,    fill = "#38CB3F")  
        self.__Bar = self.__Time_Canvas.create_rectangle(self.__XA,                      self.__H_Time_Canvas*0.75-self.__H_Front_Bar*0.5,    self.__XB,                                            self.__H_Time_Canvas*0.75+self.__H_Front_Bar/2,   fill = "#000000")
        
        self.__A_Cursor = self.__Time_Canvas.create_rectangle(self.__XA-self.__W_Cursor*0.5,   self.__H_Time_Canvas*0.75-self.__H_Cursor*0.5,  self.__XA+self.__W_Cursor*0.5,        self.__H_Time_Canvas*0.75+self.__H_Cursor*0.5,fill = "#000000")
        self.__B_Cursor = self.__Time_Canvas.create_rectangle(self.__XB-self.__W_Cursor*0.5,   self.__H_Time_Canvas*0.75-self.__H_Cursor*0.5,  self.__XB+self.__W_Cursor*0.5,        self.__H_Time_Canvas*0.75+self.__H_Cursor*0.5,fill = "#000000")
        
        self.__Time_Canvas.bind('<B1-Motion>', self.Cursor_Moved)
        self.__Time_Canvas.bind('<Button-1>', self.Cursor_Clicked)
        
        self.Aux_Time_Function()
        
        self.__A_Time = self.__Time_Canvas.create_text(self.__XA,  self.__H_Time_Canvas*0.75, text = self.TimeConversion(self.__Start_Time),fill="white")                                                 
        self.__B_Time = self.__Time_Canvas.create_text(self.__XB,  self.__H_Time_Canvas*0.75, text = self.TimeConversion(self.__End_Time),  fill="white")                                         
        
    def Cursor_Moved(self, event):

        if (abs(event.x-self.__XA) < self.__W_Cursor) and (event.x>self.__Margin) and (event.x<(self.__W_Time_Canvas-self.__Margin)) :
            self.__Time_Canvas.move(self.__A_Cursor,event.x-self.__XA,0)
            self.__XA=event.x
            
            self.__Time_Canvas.delete(self.__Bar)
            self.__Bar = self.__Time_Canvas.create_rectangle(self.__XA,    self.__H_Time_Canvas*0.75-self.__H_Front_Bar*0.5,    self.__XB,       self.__H_Time_Canvas*0.75+self.__H_Front_Bar/2,   fill = "#000000")
                                              
        elif (abs(event.x-self.__XB) < self.__W_Cursor) and (event.x>self.__Margin) and (event.x<(self.__W_Time_Canvas-self.__Margin)) :
            self.__Time_Canvas.move(self.__B_Cursor,event.x-self.__XB,0)
            self.__XB=event.x   
            
            self.__Time_Canvas.delete(self.__Bar)
            self.__Bar = self.__Time_Canvas.create_rectangle(self.__XA,    self.__H_Time_Canvas*0.75-self.__H_Front_Bar*0.5,    self.__XB,       self.__H_Time_Canvas*0.75+self.__H_Front_Bar/2,   fill = "#000000")
                   
        elif (event.x>self.__XA) and (event.x < self.__XB) and (abs(event.y-self.__H_Time_Canvas)<self.__H_Front_Bar):
            if (self.__XA>(self.__Margin+1)) and (self.__XB<(self.__W_Time_Canvas-self.__Margin-1)):
                dif = event.x-self.__aux_x
                self.__Time_Canvas.move(self.__B_Cursor,dif,0)
                self.__Time_Canvas.move(self.__A_Cursor,dif,0)
                self.__Time_Canvas.move(self.__Bar,dif,0)
                self.__XA+=dif
                self.__XB+=dif
                self.__aux_x = event.x
                
        self.__Time_Canvas.delete(self.__A_Time)
        self.__Time_Canvas.delete(self.__B_Time) 

        self.__A_Time = self.__Time_Canvas.create_text(self.__XA,  self.__H_Time_Canvas*0.75, text = self.TimeConversion(self.__Start_Time),fill="white")                                                 
        self.__B_Time = self.__Time_Canvas.create_text(self.__XB,  self.__H_Time_Canvas*0.75, text = self.TimeConversion(self.__End_Time),  fill="white")                                         
       
        self.Aux_Time_Function()
   
    def Cursor_Clicked(self, event):
        self.__aux_x = event.x

#-----------------------------------------------------------------------------------------------------------------------------------
    def DrawHeatMap(self): 
        self.__Heat_Map_Canvas.delete("all")
        self.__Div = 100
        self.__X_step = (self.__W_Heat_Map_Canvas/self.__Div)
        self.__Y_step = (self.__H_Heat_Map_Canvas/self.__Div)

        self.__Ratio = self.__Rugby_H/self.__Rugby_W
        self.__H_Heat_Map_Canvas = self.__W_Heat_Map_Canvas/self.__Ratio
        self.__HM_Scale    = self.__H_Heat_Map_Canvas/self.__Rugby_H
        self.__X_HM_Margin = self.__W_Heat_Map_Canvas*0.01
        self.__Y_HM_Margin = self.__X_HM_Margin*self.__Ratio

        self.__Heat_Map_Canvas.configure(height = self.__H_Heat_Map_Canvas, width = self.__W_Heat_Map_Canvas)
        self.__Heat_Map_Canvas.pack(expand = 'false')
        
        self.__Player.HeatMap(self.__Start_Time, self.__End_Time, self.__Div, self.__X_step, self.__Y_step, self.__HM_Scale)
 
        Max_Aux = self.__Player.Get_MaxStat()
        
        for i in range(self.__Div):
            for j in range(self.__Div):
                aux = int((1-(self.__Player.Get_Stat(i,j)/Max_Aux))*255)
                color = '#%02x%02x%02x' % (aux, aux, aux)
                self.__Heat_Map_Canvas.create_rectangle(self.__X_step*i,self.__Y_step*j,self.__X_step*(i+1),self.__Y_step*(j+1), outline=color , fill = color)
        """
        # PITCH
        self.__Heat_Map_Canvas.create_rectangle(self.__X_HM_Margin,                      self.__Y_HM_Margin,     self.__W_Heat_Map_Canvas-self.__X_HM_Margin,                      self.__H_Heat_Map_Canvas-self.__Y_HM_Margin,   fill = "#38CB3F")
        self.__Heat_Map_Canvas.create_rectangle(self.__X_HM_Margin+20*self.__HM_Scale,   self.__Y_HM_Margin,     self.__W_Heat_Map_Canvas-20*self.__HM_Scale-self.__X_HM_Margin,   self.__H_Heat_Map_Canvas-self.__Y_HM_Margin,   fill = "#27CF2E")
        self.__Heat_Map_Canvas.create_line(     self.__W_Heat_Map_Canvas*0.5,            self.__Y_HM_Margin,     self.__W_Heat_Map_Canvas*0.5,                                     self.__H_Heat_Map_Canvas-self.__Y_HM_Margin)
        """
#------------------------------------------------------------------------------------------------------------------------------------------
    def Trace(self):
        self.Aux_Time_Function()
        Time_Length = self.__Player.Get_len()
        
        self.__trace=[]
        i = 0
        self.__Timer = self.__Pitch_Canvas.create_text(self.__Margin*4, self.__Margin*2, text="")
        while (self.__Trace_Condition):
            s = self.__Player.Get_Time(i)            
            if (s > self.__Start_Time and s < self.__End_Time):
                self.__trace.append(self.__Pitch_Canvas.create_line(self.__Player.Get_X_Pos(i)*self.__Scale,self.__Player.Get_Y_Pos(i)*self.__Scale,self.__Player.Get_X_Pos(i+1)*self.__Scale,self.__Player.Get_Y_Pos(i+1)*self.__Scale))
                self.__Pitch_Canvas.itemconfigure(self.__Timer,text = self.TimeConversion(s))
                if (len(self.__trace) > 100):
                    self.__Pitch_Canvas.delete(self.__trace[0])
                    self.__trace.pop(0)
            i += 1
            if (s > Time_Length):
                self.__Trace_Condition = False
                   
            self.__Pitch_Canvas.update()
#--------------------------------------------------------------------------------------------------------------------------------------------
    def ShowFigure(self):
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
            self.__Player.Tau_Plot(self.__Start_Time, self.__End_Time,self.__AngleVar_Label)
            self.__MyImage_2 = Image.open("Tau_Plot.png")
            self.__Tau_Plot_Image = ImageTk.PhotoImage(self.__MyImage_2)
            self.__Tau_Plot.config(image = self.__Tau_Plot_Image)
            self.__Tau_Plot.update()
        else:
            self.__Tau_Plot.config(image = '')
            self.__AngleVar_Label.config(text = '')
            
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
        self.__Start_Time = (self.__XA-self.__Margin)/(self.__W_Time_Canvas-self.__Margin)
        self.__End_Time   = (self.__XB-self.__Margin)/(self.__W_Time_Canvas-self.__Margin)
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
    def ShowPoints(self):
        self.__Charge_Done = False
        self.DrawTerrain()
        self.Aux_Time_Function()
        
        Time_aux = self.__Player.Get_len()-1
   
        for i in range(Time_aux):          
            s = self.__Player.Get_Time(i)
            if (s > self.__Start_Time and s < self.__End_Time):
                x=self.__Player.Get_X_Pos(i)*self.__Scale
                y=self.__Player.Get_Y_Pos(i)*self.__Scale
                if (x>0 and x+1<self.__W_Canvas and y>0 and y+1<self.__H_Canvas):
                    self.__Pitch_Canvas.create_line(x,y,x+1,y+1)                   
        self.__Pitch_Canvas.update()
        self.__Charge_Done = True        
#-----------------------------------------------------------------------------------
    def Play_Button(self):
        self.__Trace_Condition=True
        self.Trace()
        
    def Pause_Button(self):
        self.__Trace_Condition=False
        
    def Stop_Button(self):
        self.DrawHeatMap()
        
        
window = MainWindow() 
window.mainloop() 



















         
         