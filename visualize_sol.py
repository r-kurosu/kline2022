import pandas as pd
import sys
import openpyxl as excel

def main():
    a = 4 # number of row of block
    b = 8 # number of column of block
    
    wb = excel.Workbook()
    wb.save("results_sample.xlsx")
    
    ws = wb.active
    
    red = excel.styles.PatternFill(patternType='solid', fgColor='FF0000')
    blue = excel.styles.PatternFill(patternType='solid', fgColor='0000FF')
    green = excel.styles.PatternFill(patternType='solid', fgColor='00FF00')
    
    for i in range(a):
        for j in range(b):
            ws.cell(row=2*i+1, column=2*j+1).value = i*a+j
            ws.cell(row=2*i+1, column=2*j+1).fill = red
            
    wb.save("results_sample.xlsx")
    
    return

main()
    
    
    
    