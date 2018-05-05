
import numpy as np
import math as mth
import matplotlib.pyplot as plt
import os

class Joueur():

    def __init__(self):   

        # Variables brutes de chaques joueur
        self.__Time=[] 
        self.__X_Pos=[]
        self.__Y_Pos=[]
        self.__X_Vel=[]
        self.__Y_Vel=[]
        self.__X_Acc=[]
        self.__Y_Acc=[]        
    
        self.__Stat=[]  #matrix pour le heat map
        
        self.__Tau=[]
        self.__Theta=[]
        self.__Theta_Mean=[]
        
    def Set_Work_Directory (self, value):
        self.__Work_Directory = value
        os.chdir(self.__Work_Directory)
        
    def Get_Time(self, i):
        return self.__Time[i]
        
    def Get_X_Pos(self, i):
        return self.__X_Pos[i]
        
    def Get_Y_Pos(self, i):
        return self.__Y_Pos[i]

    def Get_X_Vel(self, i):
        return self.__X_Vel[i]
    
    def Get_Y_Vel(self, i):
        return self.__Y_Vel[i]
    

    def Get_X_Acc(self, i):
        return self.__X_Acc[i]
    

        
    def Get_Y_Acc(self, i):
        return self.__Y_Acc[i]

        
    def Get_len(self):
        return len(self.__Time)
    
    def Data_Load(self, Match_Name, Player_Name, Work_Directory):
        os.chdir(Work_Directory)
        try:
            os.chdir(Work_Directory+"/Images")
        except FileNotFoundError:
            os.mkdir(Work_Directory+"/Images")
        os.chdir(Work_Directory)
        
        self.__PI = 3.14159
        self.__R_Earth = 6378000.0   
        self.__Resize=self.__PI*self.__R_Earth/180*1.8
        
        # Match Data
        self.__MatchFile = open(Match_Name+".txt","r")
        self.__MatchData = self.__MatchFile.readlines()
    
        self.__BR_GPS_Pin = [float(self.__MatchData[5].split()[4]),float(self.__MatchData[5].split()[5])]
        self.__TR_GPS_Pin = [float(self.__MatchData[5].split()[4]),float(self.__MatchData[5].split()[5])]
        self.__BL_GPS_Pin = [float(self.__MatchData[5].split()[4]),float(self.__MatchData[5].split()[5])]
        self.__TL_GPS_Pin = [float(self.__MatchData[5].split()[4]),float(self.__MatchData[5].split()[5])]
        
        self.__MatchFile.close()

        # Player Data
        self.__PlayerFile = open(Player_Name,"r")
        self.__PlayerData = self.__PlayerFile.readlines()
           
        for l in self.__PlayerData:
            dataline = l.split()
            try:
                self.__Time.append(float(dataline[0]))
                self.__X_Vel.append(float(dataline[1])/3.6)
                self.__X_Acc.append(float(dataline[2]))
                #self.__Odometer.append(float(dataline[3]))
                self.__Y_Pos.append(float(dataline[4]))
                self.__X_Pos.append(float(dataline[5]))
            except:
                print('')
            
        self.__PlayerFile.close()
        
        for i in range(len(self.__X_Pos)):
            self.__X_Pos[i] = abs(self.__BL_GPS_Pin[1]-self.__X_Pos[i])*self.__Resize+5
            self.__Y_Pos[i] = abs(self.__BL_GPS_Pin[0]-self.__Y_Pos[i])*self.__Resize+7

#-------------------------------------------------------------------------------------------------------------------------------------------
    def Theta_Calc(self,Delta):
        
        step = int(Delta/self.__Time[1])
        self.__Theta=[]
        
        for i in range(len(self.__Time)-step*2):
            
            condx = self.__X_Pos[i] != self.__X_Pos[i+step] and self.__X_Pos[i+step*2] != self.__X_Pos[i+step] and self.__X_Pos[i] != self.__X_Pos[i+step*2] 
            condy = self.__Y_Pos[i] != self.__Y_Pos[i+step] and self.__Y_Pos[i+step*2] != self.__Y_Pos[i+step] and self.__Y_Pos[i] != self.__Y_Pos[i+step*2] 
            
            if (condx and condy):
                M12 = (self.__Y_Pos[i+step]-self.__Y_Pos[i])/(self.__X_Pos[i+step]-self.__X_Pos[i])
                M23 = (self.__Y_Pos[i+step*2]-self.__Y_Pos[i+step])/(self.__X_Pos[i+step*2]-self.__X_Pos[i+step])
                    
                self.__Theta.append(mth.atan((M23-M12)/(1+M12*M23)))

#-------------------------------------------------------------------------------------------------------------------------------------------
    
    def HeatMap(self, Start_Time, End_Time, Nb_Div, X_step, Y_step, Scale):
        
        self.__Max_Stat=1
        
        # Stat matrix initiation
        self.__Stat=[]
        for i in range(Nb_Div):
            self.__Stat.append([])
            for j in range(Nb_Div): 
                self.__Stat[i].append(0)

        for i in range(len(self.__Time)):
            if (self.__Time[i]>Start_Time and self.__Time[i]<End_Time):
                x=int(self.__X_Pos[i]*Scale/X_step)
                y=int(self.__Y_Pos[i]*Scale/Y_step)
                self.__Stat[x][y]+=1
                if (self.__Stat[x][y]>self.__Max_Stat):
                    self.__Max_Stat=self.__Stat[x][y]
                    
    def Get_Stat(self, i , j ):
        return self.__Stat[i][j]
    
    def Get_MaxStat(self):
        return self.__Max_Stat
    
#-------------------------------------------------------------------------------------------------------------------------------------------
    def Tau_Plot(self, Start_Time, End_Time, Label):
        self.__Tau = np.logspace(0,2,num=50)
        count = 0
        self.__Theta_Mean = []
        
        for Delta in self.__Tau:
            self.Theta_Calc(Delta)
            self.__Theta_Mean.append(self.Tau_Plot_aux(Delta, Start_Time, End_Time))
            count +=1
            Label.configure(text = str(count*2)+" %")
            Label.update()
 
        plt.figure('Tau_Plot')
        plt.plot(self.__Tau, self.__Theta_Mean)
        plt.axhline(y=3.1415*2/3)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Tau (s)')
        plt.ylabel('Theta mean (deg)')
        plt.title('Tau/Theta')
        plt.savefig('Tau_Plot.png',transparent=True)    
            
    def Tau_Plot_aux(self, Delta, Start_Time,End_Time):
        theta_mean=0
        count=0
        step = int(Delta/self.__Time[1])
        
        for i in range(len(self.__Theta)-step):
            if ((self.__Time[i]>Start_Time) and (self.__Time[i+step]<End_Time)) : 
                theta_mean += abs(self.__Theta[i+step]-self.__Theta[i])
                count +=1
        
        return theta_mean/count
    
    def Get_Tau(self, i):
        return self.__Tau[i]
        
    def Get_Theta_Mean(self, i):
        return self.__Theta_Mean[i]
    
#-------------------------------------------------------------------------------------------------------------------------------------------
    
    def Speed_Plot(self, Start_Time, End_Time):
        
        Vel_Aux = []
        Time_Aux = []
        
        for i in range(len(self.__Time)):
            if (self.__Time[i]>Start_Time and self.__Time[i]<End_Time):
                Vel_Aux.append(self.__X_Vel[i])
                Time_Aux.append(self.__Time[i])
        plt.figure('Speed_Plot')     
        plt.plot(Time_Aux, Vel_Aux, '.')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (px/s)')
        plt.title('Evolution of Velocity')
        plt.savefig('Speed_Plot.png',transparent=True)
        
    def Speed_Hist_Plot(self, Start_Time, End_Time):
        
        Vel_Aux = []
        Time_Aux = []
        
        for i in range(len(self.__Time)):
            if (self.__Time[i]>Start_Time and self.__Time[i]<End_Time):
                Vel_Aux.append(self.__X_Vel[i])
                Time_Aux.append(self.__Time[i])
        plt.figure('Speed_Hist_Plot')
        plt.hist(Vel_Aux)
        plt.xlabel('Velocity (px/s)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Velocity')
        plt.savefig('Speed_Hist_Plot.png',transparent=True)
    
#-------------------------------------------------------------------------------------------------------------------------------------------
  
    def Theta_Plot(self, Start_Time, End_Time):
        
        Theta_Aux = []
        Time_Aux = []
        
        self.Theta_Calc(self.__Time[1])
        
        for i in range(len(self.__Theta)):
            if (self.__Time[i]>Start_Time and self.__Time[i]<End_Time):
                Theta_Aux.append(self.__Theta[i])
                Time_Aux.append(self.__Time[i])
        plt.figure('Theta_Plot')
        plt.plot(Time_Aux,Theta_Aux,'.')
        plt.xlabel('Time (s)')
        plt.ylabel('Theta (deg)')
        plt.title('Variation of Theta')
        plt.savefig('Theta_Plot.png',transparent=True)
    
    
    
    
    
    
    
    
    