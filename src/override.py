import numpy as np
from openpyxl import load_workbook

def writeTo(value, valueCell : str, sheetName : str):
    wb = load_workbook('data\Microcontroler-Datasheet.xlsx')
    
    sheet = wb[sheetName]
    sheet[valueCell] = value
    
    wb.save('data\Microcontroler-Datasheet.xlsx')
    
    