# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:39:21 2017

@author: Alfonso
"""
import numpy as np
import math as mth
import matplotlib.pyplot as plt
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
        
    def Set0_Time(self, value):
        self.__Time.append(value)
        
    def Set0_X_Pos(self, value):
        self.__X_Pos.append(value)
        
    def Set0_Y_Pos(self, value):
        self.__Y_Pos.append(value)
  
    def Set0_X_Vel(self, value):
        self.__X_Vel.append(value)
        
    def Set0_Y_Vel(self, value):
        self.__Y_Vel.append(value)
        
    def Set0_X_Acc(self, value):
        self.__X_Acc.append(value)

    def Set0_Y_Acc(self, value):
        self.__Y_Acc.append(value)
        
    def Get_Time(self, i):
        return self.__Time[i]
    
    def Set_Time(self, i,value):
        self.__Time[i]=value
        
    def Get_X_Pos(self, i):
        return self.__X_Pos[i]
    
    def Set_X_Pos(self, i, value):
        self.__X_Pos[i]=value
        
    def Get_Y_Pos(self, i):
        return self.__Y_Pos[i]
    
    def Set_Y_Pos(self, i, value):
        self.__Y_Pos[i]=value
        
    def Get_X_Vel(self, i):
        return self.__X_Vel[i]
    
    def Set_X_Vel(self, i, value):
        self.__X_Vel[i]=value
        
    def Get_Y_Vel(self, i):
        return self.__Y_Vel[i]
    
    def Set_Y_Vel(self, i, value):
        self.__Y_Vel[i]=value
        
    def Get_X_Acc(self, i):
        return self.__X_Acc[i]
    
    def Set_X_Acc(self, i, value):
        self.__X_Acc[i]=value
        
    def Get_Y_Acc(self, i):
        return self.__Y_Acc[i]
    
    def Set_Y_Acc(self, i, value):
        self.__X_Acc[i]=value
        
    def Get_len(self):
        return len(self.__Time)
    
#-------------------------------------------------------------------------------------------------------------------------------------------
    def Theta_Calc(self,Delta):
        
        step = int(Delta/self.__Time[1])
        
        for i in range(len(self.__Time)-step*2):
            
            condx = self.__X_Pos[i] != self.__X_Pos[i+step] and self.__X_Pos[i+step*2] != self.__X_Pos[i+step] and self.__X_Pos[i] != self.__X_Pos[i+step*2] 
            condy = self.__Y_Pos[i] != self.__Y_Pos[i+step] and self.__Y_Pos[i+step*2] != self.__Y_Pos[i+step] and self.__Y_Pos[i] != self.__Y_Pos[i+step*2] 
            
            if (condx and condy):
                M12 = (self.__Y_Pos[i+step]-self.__Y_Pos[i])/(self.__X_Pos[i+step]-self.__X_Pos[i])
                M23 = (self.__Y_Pos[i+step*2]-self.__Y_Pos[i+step])/(self.__X_Pos[i+step*2]-self.__X_Pos[i+step])
                    
                self.__Theta.append(mth.atan((M23-M12)/(1+M12*M23)))

#-------------------------------------------------------------------------------------------------------------------------------------------
    
    def HeatMap(self, Start_Time, End_Time, Nb_Div, X_step, Y_step):
        
        self.__Max_Stat=1
        
        # Stat matrix initiation
        self.__Stat=[]
        for i in range(Nb_Div):
            self.__Stat.append([0])
            for j in range(Nb_Div): 
                self.__Stat[i].append(0)


        for i in range(len(self.__Time)):
            if (self.__Time[i]>Start_Time and self.__Time[i]<End_Time):
                x=int(self.__X_Pos[i]/X_step)
                y=int(self.__Y_Pos[i]/Y_step)
                self.__Stat[x][y]+=1
                if (self.__Stat[x][y]>self.__Max_Stat):
                    self.__Max_Stat=self.__Stat[x][y]
                    
    def Get_Stat(self, i , j ):
        return self.__Stat[i][j]
    
    def Get_MaxStat(self):
        return self.__Max_Stat
    
#-------------------------------------------------------------------------------------------------------------------------------------------
    def Tau_Plot(self, Start_Time, End_Time):
        self.__Tau = np.linspace(0.1,100)

        for Delta in self.__Tau:
            self.Theta_Calc(Delta)
            self.__Theta_Mean.append(self.Tau_Plot_aux(Delta))
            
        plt.figure('Tau_Plot')
        plt.plot(self.__Tau, self.__Theta_Mean)
        plt.xlabel('Tau (s)')
        plt.ylabel('Theta mean (deg)')
        plt.title('Tau/Theta')
        plt.savefig('Tau_Plot.png')    
            
    def Tau_Plot_aux(self, Delta):
        
        theta_mean=0
        count=0
        
        step = int(Delta/self.__Time[1])
        
        for i in range(len(self.__Theta)-step*2):
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
        plt.savefig('Speed_Plot.png')
        
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
        plt.savefig('Speed_Hist_Plot.png')
    
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
        plt.savefig('Theta_Plot.png')
    
    
    
    
    
    
    
    
    
    