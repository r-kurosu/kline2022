import openpyxl as excel
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
import test

# color setting
red_fill = excel.styles.PatternFill(patternType='solid', fgColor='FF0000')
blue_fill = excel.styles.PatternFill(patternType='solid', fgColor='0000FF')
green_fill = excel.styles.PatternFill(patternType='solid', fgColor='00FF00')
yellow_fill = excel.styles.PatternFill(patternType='solid', fgColor='FFFF00')

block_border = Border(top=Side(style='thin', color='000000'), 
                bottom=Side(style='thin', color='000000'), 
                left=Side(style='thin', color='000000'),
                right=Side(style='thin', color='000000'))

center_alignment = Alignment(horizontal="centerContinuous", vertical="center" , wrap_text=True)

def paint_cell(a, b, sol, ws):
    for i in range(a):
        for j in range(b):
            # print(f"{i*a+j}: {sol[i*a+j]}")
            ws.cell(row=2*i+1, column=2*j+1).value = i*a+j
            ws.cell(row=2*i+1, column=2*j+1).border = block_border
            ws.cell(row=2*i+1, column=2*j+1).alignment = center_alignment
            
            if sol[i*a+j] == 0:
                pass
            elif sol[i*a+j] == 1:
                ws.cell(row=2*i+1, column=2*j+1).fill = red_fill
            elif sol[i*a+j] == 2:
                ws.cell(row=2*i+1, column=2*j+1).fill = blue_fill
            elif sol[i*a+j] == 3:
                ws.cell(row=2*i+1, column=2*j+1).fill = green_fill
            elif sol[i*a+j] == 4:
                ws.cell(row=2*i+1, column=2*j+1).fill = yellow_fill
            
    return ws


def print_edge_in(a, b, sola, ws):
    for edge in sola:
        if edge[0] + 1 == edge[1]:
            # print(f"edge: {edge}")
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)+2).value = "→\n"
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)+2).alignment = center_alignment
        elif edge[0] - 1 == edge[1]:
            # print(f"edge: {edge}")
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)).value = "←\n"
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)).alignment = center_alignment
        elif edge[0] + a == edge[1]:
            # print(f"edge: {edge}")
            ws.cell(row=2*(edge[0]//a)+2, column=2*(edge[0]%a)+1).value = "↓"
            ws.cell(row=2*(edge[0]//a)+2, column=2*(edge[0]%a)+1).alignment = center_alignment
        elif edge[0] - a == edge[1]:
            # print(f"edge: {edge}")
            ws.cell(row=2*(edge[0]//a), column=2*(edge[0]%a)+1).value = "↑"
            ws.cell(row=2*(edge[0]//a), column=2*(edge[0]%a)+1).alignment = center_alignment
    return


def print_edge_out(a, b, solb, ws):
    for edge in solb:
        if edge[0] + 1 == edge[1]:
            # print(f"edge: {edge}")
            cell_contents = ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)+2).value
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)+2).value = (cell_contents or "") + "→"
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)+2).alignment = center_alignment
        elif edge[0] - 1 == edge[1]:
            # print(f"edge: {edge}")
            cell_contents = ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)).value
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)).value = (cell_contents or "") + "←"
            ws.cell(row=2*(edge[0]//a)+1, column=2*(edge[0]%a)).alignment = center_alignment
        elif edge[0] + a == edge[1]:
            # print(f"edge: {edge}")
            cell_contents = ws.cell(row=2*(edge[0]//a)+2, column=2*(edge[0]%a)+1).value
            ws.cell(row=2*(edge[0]//a)+2, column=2*(edge[0]%a)+1).value = (cell_contents or "") + "↓"
            ws.cell(row=2*(edge[0]//a)+2, column=2*(edge[0]%a)+1).alignment = center_alignment
        elif edge[0] - a == edge[1]:
            # print(f"edge: {edge}")
            cell_contents = ws.cell(row=2*(edge[0]//a), column=2*(edge[0]%a)+1).value
            ws.cell(row=2*(edge[0]//a), column=2*(edge[0]%a)+1).value = (cell_contents or "") + "↑"
            ws.cell(row=2*(edge[0]//a), column=2*(edge[0]%a)+1).alignment = center_alignment
    
    return


def main():
    a = 5 # number of row of block
    b = 5 # number of column of block
    sol, sola, solb = test.main()
    sol[0] = 0 # 0 is not used
    
    wb = excel.Workbook()
    wb.save("results_sample.xlsx")
    
    ws = wb.active
    
    ws = paint_cell(a, b, sol, ws)
    print_edge_in(a, b, sola, ws)
    print_edge_out(a, b, solb, ws)
    
    wb.save("results_sample.xlsx")
    
    return

main()
