# 
import xlrd

xlsx_link='d:/UsersNBU/011019/Desktop/Python/agg.xlsx'

wb=xlrd.open_workbook(xlsx_link)		
sheet = wb.sheet_by_index(0)  
sheet.cell_value(0, 0) 

dic={}

for i in range(sheet.nrows):
	dic[int(sheet.cell_value(i,1))]=sheet.cell_value(i,3)
print(dic) 

