import math
import matplotlib.pyplot as plt
import tkinter
from tkinter import ttk
import Joueur_v1 as J
from PIL import Image, ImageTk

   
class MainWindow(tkinter.Tk):
    
    
    def __init__(self):
         
    # Initialize
        tkinter.Tk.__init__(self)         
        self.title('Traitement Donnée Sportives')  

        
        #os.chdir("/Users/marc/Desktop/Studium/ECL/Cloud/UE Pro/PA/Projet Souris")
        
        self.__C_active = False
        self.__M_active = False
        self.__H_active = False
        
        self.__H_Start_Time_aux  = 0
        self.__H_End_Time_aux    = 0
        self.__H_Duration_aux    = 0
        
        self.__Player_List = []
        
        self.__Match_List = tkinter.StringVar()  
        self.__DataFiles_List = []
        
        self.__DataFiles_List.append("Hola")
        self.__DataFiles_List.append("Adios")
        
    # Main Panels
    
        self.__D_Panel      = tkinter.LabelFrame(self, text="Choix des données")
        self.__C_Panel      = tkinter.LabelFrame(self, text="Paramètres des courbes :")
        self.__H_Panel      = tkinter.LabelFrame(self, text="Paramètres du HeatMap :")
        self.__T_Panel      = tkinter.LabelFrame(self, text="Paramètres temporeles ")
        self.__I_Panel      = tkinter.LabelFrame(self, text="Information du Match :")  
        self.__F_Panel      = tkinter.LabelFrame(self, text="Affichage du terrain :")
        self.__Fig_Panel    = tkinter.LabelFrame(self, text="Affichage des Courbes :")
        self.__RS_Panel     = tkinter.LabelFrame(self, text="Range Slider :")
        
    # Data_Panel elements 

        self.__D_Data_Combobox     = tkinter.ttk.Combobox(self.__D_Panel, textvariable = self.__Match_List)
        self.__D_Player_Combobox   = tkinter.ttk.Combobox(self.__D_Panel, textvariable = "Choisir Joueur")
        self.__D_LoadButton        = tkinter.Button(self.__D_Panel, text = "Charger", relief = "raised", command = self.Load_Data)
        
        self.__D_Data_Combobox['values'] = ('hola', 'que', 'tal?')
        
        self.__D_Data_Combobox.pack(expand="true")
        self.__D_Player_Combobox.pack(expand="true")
        self.__D_LoadButton.pack(expand="true")
        
        self.__D_Panel.grid(row=0, column=0,sticky='NSEW')
        
    # Figure_Parameter_Panel elements
    
        self.__Figure_Check = []
        for i in range(4):
            self.__Figure_Check.append(tkinter.IntVar())
        
        self.__C_Speed_CheckButton      = tkinter.Checkbutton(self.__C_Panel, text='Vitesse / Temps', variable=self.__Figure_Check[0])
        self.__C_Angle_CheckButton      = tkinter.Checkbutton(self.__C_Panel, text='Theta / Temps', variable=self.__Figure_Check[1])
        self.__C_AngleVar_CheckButton   = tkinter.Checkbutton(self.__C_Panel, text='Theta / Tau', variable=self.__Figure_Check[2])
        self.__C_Aux_CheckButton        = tkinter.Checkbutton(self.__C_Panel, text='Vitesse Histogram', variable=self.__Figure_Check[3])
        self.__C_ShowButton             = tkinter.Button(self.__C_Panel, text = "Afficher", relief = "raised", command = self.ShowFigure)
        
        self.__C_Speed_CheckButton.pack(expand="true")
        self.__C_Angle_CheckButton.pack(expand="true")     
        self.__C_AngleVar_CheckButton.pack(expand="true")
        self.__C_Aux_CheckButton.pack(expand="true")   
        self.__C_ShowButton.pack(expand="true")
        
        self.__C_Panel.grid(row=1, column=0,sticky='NSEW')
        
    # HeatMap_Panel elements
    
        self.__H_Divisions_Scale     = tkinter.Scale(self.__H_Panel,from_=1, to=200, orient="horizontal", label = "Nb de division")
        self.__H_ShowButton          = tkinter.Button(self.__H_Panel, text = "Afficher", relief = "raised", command = self.ShowHeatMap)
        
        self.__H_Divisions_Scale.pack(expand="true")
        self.__H_ShowButton.pack(expand="true")
        
        self.__H_Panel.grid(row=2, column=0,sticky='NSEW')
    
    # Temporal_Panel elements
    
        self.__T_Init_Time_Scale      = tkinter.Scale(self.__T_Panel,from_=0, to=100, orient="horizontal", label = "Temps Initial (%)")
        self.__T_Final_Time_Scale     = tkinter.Scale(self.__T_Panel,from_=0, to=100, orient="horizontal", label = "Temps Final (%)")
        self.__T_ShowButton           = tkinter.Button(self.__T_Panel, text = "Afficher", relief = "raised", command = self.ShowTrace)
        
        self.__T_Init_Time_Scale.pack(expand="true")
        self.__T_Final_Time_Scale.pack(expand="true")
        self.__T_ShowButton.pack(expand="true")
        
        self.__T_Panel.grid(row=3, column=0,sticky='NSEW')
        
    # Information_Panel elements
        self.__I_Data_Duration_Var = tkinter.StringVar()
        self.__I_Data_HalfTime_Var = tkinter.StringVar()
        
        self.__I_Data_Duration_Var.set("Duration Time: ")
        self.__I_Data_HalfTime_Var.set("Half Time: ")
        
    
        self.__I_Data_Duration  = tkinter.Label(self.__I_Panel, textvariable = self.__I_Data_Duration_Var)
        self.__I_Data_HalfTime  = tkinter.Label(self.__I_Panel, textvariable = self.__I_Data_HalfTime_Var)
        
        self.__I_Data_Duration.pack(expand="true")
        self.__I_Data_HalfTime.pack(expand="true")
        
        self.__I_Panel.grid(row=4, column=0,sticky='NSEW')
        
    # Terrain Panel
        
        self.__Rugby_W=70     #meters
        self.__Rugby_H=140    #meters
        
        self.__Margin = 10    #pixel
        
        self.__Scale = 5
        
        self.__W_Canvas = self.__Rugby_W*self.__Scale
        self.__H_Canvas = self.__Rugby_H*self.__Scale
    
        self.__Canvas = tkinter.Canvas(self.__F_Panel,width = self.__W_Canvas+self.__Margin, height = self.__H_Canvas+self.__Margin, bg="white")
        self.__Canvas.pack(expand="true")
        self.__F_Panel.grid(row=0,column=1,columnspan=1,rowspan=5,sticky='NSEW') 
        
        self.DrawTerrain()
        
    # Figure Panel 
    
        self.__Speed_Plot      = tkinter.Label(self.__Fig_Panel)
        self.__Speed_Hist_Plot = tkinter.Label(self.__Fig_Panel)
        self.__Tau_Plot        = tkinter.Label(self.__Fig_Panel)
        self.__Theta_Plot      = tkinter.Label(self.__Fig_Panel)
        
        self.__Speed_Plot.pack()
        self.__Speed_Hist_Plot.pack()
        self.__Tau_Plot.pack()
        self.__Theta_Plot.pack()
        
        self.__Fig_Panel.grid(row=0, column=2, columnspan=1, rowspan=5,sticky='NSEW')
        

#-----------------------------------------------------------------------------------------------------------------------------------
     
    def Load_Data(self):
        
        #File_Name    = self.__D_Data_Combobox.get()
        #Player_Name  = self.__D_Player_Combobox.get()
        
        File_Name = "Rugby_Data.txt"
        self.__Player = J.Joueur()
        
        self.__DataFile = open(File_Name,"r")
        self.__Data = self.__DataFile.readlines()
        
        self.__Time=[]
        self.__Velocity=[]
        self.__Acceleration=[]
        self.__Odometer=[]
        self.__Y=[]
        self.__X=[]
    
        for l in self.__Data:
            dataline = l.split()
            self.__Player.Set0_Time(float(dataline[0]))
            self.__Player.Set0_X_Vel(float(dataline[1])/3.6*self.__Scale)
            self.__Player.Set0_X_Acc(float(dataline[2]))
            #self.__Odometer.append(float(dataline[3]))
            self.__Player.Set0_Y_Pos(float(dataline[5]))
            self.__Player.Set0_X_Pos(float(dataline[4]))
        
        self.__DataFile.close()
        
        X_mid = 43.482162
        Y_mid = -1.536879
        self.__PI = 3.14159
        self.__R_Earth = 6378000.0
        
        X_max = 0
        Y_max = 0
        for i in range(self.__Player.Get_len()):
            self.__Player.Set_X_Pos(i,abs(X_mid-self.__Player.Get_X_Pos(i))*self.__PI/180*self.__R_Earth)
            if self.__Player.Get_X_Pos(i)> X_max:
                    X_max = self.__Player.Get_X_Pos(i)
            
                    
        for i in range(self.__Player.Get_len()):
            self.__Player.Set_Y_Pos(i,abs(Y_mid-self.__Player.Get_Y_Pos(i))*self.__PI/180*self.__R_Earth)
            if self.__Player.Get_Y_Pos(i)> Y_max:
                    Y_max = self.__Player.Get_Y_Pos(i)
            
        for i in range(self.__Player.Get_len()):
            self.__Player.Set_X_Pos(i,self.__Player.Get_X_Pos(i)/X_max*self.__W_Canvas)
            
        
        for i in range(self.__Player.Get_len()):
            self.__Player.Set_Y_Pos(i,self.__Player.Get_Y_Pos(i)/Y_max*self.__H_Canvas)
            
        self.Info_Actualitation()
            
        print ("Data Load Done")
#-----------------------------------------------------------------------------------------------------------------------------------
          
    def DrawTerrain(self):
                
        self.__Canvas.delete('all')
        
        self.__Canvas.create_rectangle(self.__Margin,self.__Margin,self.__W_Canvas,self.__H_Canvas, fill = "#38CB3F")
        self.__Canvas.create_rectangle(self.__Margin,self.__Margin+20*self.__Scale,self.__W_Canvas,self.__H_Canvas-20*self.__Scale, fill = "#27CF2E")
        self.__Canvas.create_line(self.__Margin,self.__Margin+self.__H_Canvas*0.5,self.__W_Canvas,self.__Margin+self.__H_Canvas*0.5)
        self.__Canvas.create_rectangle(self.__Margin+self.__W_Canvas*0.5-20,self.__Margin+20*self.__Scale-5,self.__Margin+self.__W_Canvas*0.5+20,self.__Margin+20*self.__Scale+5, fill = "#000000")
        self.__Canvas.create_rectangle(self.__Margin+self.__W_Canvas*0.5-20,self.__Margin+118*self.__Scale-5,self.__Margin+self.__W_Canvas*0.5+20,self.__Margin+118*self.__Scale+5, fill = "#000000")
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
        
    # HeatMap drawing
    
        Max_Aux = self.__Player.Get_MaxStat()

        for i in range(self.__Div):
            for j in range(self.__Div):
                aux = int((1-(self.__Player.Get_Stat(i,j)/Max_Aux))*255)
                color = '#%02x%02x%02x' % (aux, aux, aux)
                self.__Canvas.create_rectangle(self.__Margin+self.__X_step*i,self.__Margin+self.__Y_step*j,self.__Margin+self.__X_step*(i+1),self.__Margin+self.__Y_step*(j+1), outline="white", fill = color)
                
#------------------------------------------------------------------------------------------------------------------------------------------
    def Trace(self):
        
        self.DrawTerrain()
        
        self.Aux_Time_Function()
        Time_aux = self.__Player.Get_len()
        
        self.__trace=[]
        

        self.__Timer = self.__Canvas.create_text(self.__Margin*4, self.__Margin*2, text=" 0 s")
        
        for i in range(Time_aux):
            s = self.__Player.Get_Time(i)
            if (s > self.__Start_Time and s < self.__End_Time):
                self.__trace.append(self.__Canvas.create_line(self.__Player.Get_X_Pos(i),self.__Player.Get_Y_Pos(i),self.__Player.Get_X_Pos(i+1),self.__Player.Get_Y_Pos(i+1)))
                self.__Canvas.itemconfigure(self.__Timer,text = str(s) + " s")
                if (len(self.__trace) > self.__Duration):
                    self.__Canvas.delete(self.__trace[0])
                    self.__trace.pop(0)
                   
            self.__Canvas.update()

#--------------------------------------------------------------------------------------------------------------------------------------------
    def Courbe(self):
        self.Aux_Time_Function()
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
            self.__Player.Tau_Plot(self.__Start_Time, self.__End_Time)
            self.__MyImage_2 = Image.open("Tau_Plot.png")
            self.__Tau_Plot_Image = ImageTk.PhotoImage(self.__MyImage_2)
            self.__Tau_Plot.config(image = self.__Tau_Plot_Image)
            self.__Tau_Plot.update()
        else:
            self.__Tau_Plot.config(image = '')
            
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
        self.__X_step = int((self.__W_Canvas)/self.__Div)+1
        self.__Y_step = int((self.__H_Canvas)/self.__Div)+1
        
        self.__Start_Time = self.__T_Init_Time_Scale.get()
        self.__End_Time   = self.__T_Final_Time_Scale.get()

        self.__End_Time_aux = 0
        self.__Start_Time_aux = 0
        self.__Duration = 0
               
        if (self.__End_Time_aux !=  self.__End_Time):
            self.__Duration=self.__End_Time-self.__Start_Time

            
        if(self.__Start_Time_aux !=  self.__Start_Time):
            self.__Duration=self.__End_Time-self.__Start_Time
       
        self.__Start_Time_aux  = self.__Start_Time
        self.__End_Time_aux    = self.__End_Time
     
        self.__Start_Time = self.__Start_Time/100*self.__Player.Get_Time(-1)
        self.__End_Time   = self.__End_Time/100*self.__Player.Get_Time(-1)
        self.__Duration   = self.__Duration/100*self.__Player.Get_Time(-1)
        
#-----------------------------------------------------------------------------------
        
    def Info_Actualitation(self):
        a = self.__Player.Get_Time(-1)
        b = a/2
        self.__I_Data_Duration_Var.set("Duration Time: "+ str(a) + "s")
        self.__I_Data_HalfTime_Var.set("Half Time: "+ str(b) + "s")
        
        self.__I_Data_Duration.update()
        self.__I_Data_HalfTime.update()
        
window = MainWindow() 
window.mainloop() 



















         
         