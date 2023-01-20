import pandas as pd
import sys
import openpyxl as excel

# color setting
red_fill = excel.styles.PatternFill(patternType='solid', fgColor='FF0000')
blue_fill = excel.styles.PatternFill(patternType='solid', fgColor='0000FF')
green_fill = excel.styles.PatternFill(patternType='solid', fgColor='00FF00')


def main():
    a = 4 # number of row of block
    b = 8 # number of column of block
    
    wb = excel.Workbook()
    wb.save("results_sample.xlsx")
    
    ws = wb.active
    
    for i in range(a):
        for j in range(b):
            if (i*a+j) % 3 == 0:
                ws.cell(row=2*i+1, column=2*j+1).value = i*a+j
                ws.cell(row=2*i+1, column=2*j+1).fill = red_fill
            elif (i*a+j) % 3 == 1:
                ws.cell(row=2*i+1, column=2*j+1).value = i*a+j
                ws.cell(row=2*i+1, column=2*j+1).fill = blue_fill
            else:
                ws.cell(row=2*i+1, column=2*j+1).value = i*a+j
                ws.cell(row=2*i+1, column=2*j+1).fill = green_fill
                
            
    wb.save("results_sample.xlsx")
    
    return

main()
