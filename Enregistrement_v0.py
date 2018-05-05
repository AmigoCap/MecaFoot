# -*- coding: utf-8 -*-


import openpyxl
import os

Work_Directory_Marc = "C:/Users/marcl/Dropbox/PAr 143 - Acquisition de donnée sportives/Programmation/Data/Match 12 25nov2016"
Work_Directory_Alfonso = "C:/Users/fonss/Dropbox (Personal)/PAr 143 - Acquisition de donnée sportives/Programmation/Data/Match 12 25nov2016"

try:
    os.chdir(Work_Directory_Marc)
    DataFiles_List = os.listdir(Work_Directory_Marc)
except FileNotFoundError:
    os.chdir(Work_Directory_Alfonso)
    DataFiles_List = os.listdir(Work_Directory_Alfonso)
    print(DataFiles_List)
    for data in DataFiles_List :
        try :
            doc = openpyxl.load_workbook(data) 
            s = doc.sheetnames[0]
            Sheet = doc.get_sheet_by_name(s)
            txt = data.replace(".xlsx",".txt")
            result=open(txt,"w")
            for i in Sheet.rows:
                for j in i:
                    l = j.value
                    dataline = l.split(',')
                    for w in range(len(dataline)):
                        if (w>0):
                            result.write(str(dataline[w])+" ")    
                    result.write("\n")
        
            result.close()
        except :
            print ("File can not be open ! ")
            try:
                print (txt)
            except :
                print("No file.xlsx")
