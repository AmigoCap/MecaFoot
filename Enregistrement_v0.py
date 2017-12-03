# -*- coding: utf-8 -*-


import openpyxl

doc = openpyxl.load_workbook("Donnée Match Rugby.xlsx") #suponiendo que el archivo esta en el mismo directorio del script

Sheet = doc.get_sheet_by_name("Donnée Match Rugby")

result=open("Rugby_Data.txt","w")


for i in Sheet.rows:
    for j in i:
        l = j.value
        dataline = l.split(',')
        for w in range(len(dataline)):
            if (w>0):
                result.write(str(dataline[w])+" ")
        result.write("\n")
        
result.close()