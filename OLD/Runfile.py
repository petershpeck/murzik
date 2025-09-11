import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup 
import re
import time 
import xlsxwriter
from datetime import datetime
import xlrd
import xlwt


	
i=0
pdfs=[]	
broken=[] 
problems=[]
scrapped=[] 
names=[] 
links=[]
date_full=datetime.today()
date=date_full.strftime("%d.%m.%Y")
text_link='d:/UsersNBU/011019/Desktop/Python/file.txt'
path_to_bank_profiles="d:/UsersNBU/011019/Desktop/Python/bank_profiles.xlsx" 
path_to_bps ="d:/UsersNBU/011019/Desktop/Python/bank_page_structures" 
char_format=['cell=str(cell)','cell=int(cell)','cell=str(cell)','cell=str(cell)','cell=str(cell)','cell=str(cell)','cell=str(cell)']
titles=["short_name","nkb","full_name","group_1","Reuters","Date","day","year","month","week","currency","term","rates"] 
row_format=['cell=str(cell)','cell=int(cell)','cell=str(cell)','cell=str(cell)','cell=str(cell)', 'cell=date_full.strftime("%d.%m.%Y")','cell=int(date_full.strftime("%d"))', "cell=int(date_full.strftime('%Y'))","cell=int(date_full.strftime('%m'))", "cell=int(date_full.strftime('%V'))",'cell=str(cell)','cell=str(cell)', 'cell=float(cell)'] 
bank_chars=["short_name","nkb","full_name","group_1","Reuters","currency","term"]

print('Collecting Process`s Started...') 

# Activating Excel document
file_name = 'Deposits_' + str(date_full.strftime('%d.%m.%Y'))+'.xlsx'	
workbook=xlsxwriter.Workbook(file_name)	
worksheet=workbook.add_worksheet()
for t,title in enumerate(titles):
	worksheet.write(i, t, title)
i=1

# get names and links from bank profile
table_of_profiles=xlrd.open_workbook(path_to_bank_profiles)
profile_sheet=table_of_profiles.sheet_by_index(0)
pdf_sheet=table_of_profiles.sheet_by_name('PDF')		
link_col = profile_sheet.col_values(6,start_rowx=1)
for link in link_col:
	if len(str(link))>1: 
		links.append(link) 
name_row=profile_sheet.col_values(0,start_rowx=1)
for name in name_row:
	if len(str(name))>1: 
		names.append(name)
		

for s in links: 
	rates=[]
	rates_u=[]
	rates_d=[]	
	rates_e=[]
	error_message=dict()
	url=s
	
				#Sending Request and And Saving Responce to text file	
	try:
		html=urllib.request.urlopen(url)
		soup=BeautifulSoup(html.read(), "html.parser") 
		with open(text_link, 'w', encoding='utf-8') as f:
			f.write(str(soup))
		soup=BeautifulSoup(open(text_link, encoding="utf-8"), "html.parser")
		result=str(soup).split()
	except: 
		if links.count(s)<=3:
			links.append(s)
		continue
		
		
# Adding profile information
	bank_row= link_col.index(url)+1	 
	for char in range(len(bank_chars)):
		cell=profile_sheet.cell_value(bank_row, char)
		exec(char_format[char])
		vars()[bank_chars[char]]= cell 
	
	
# Specifying page structure
	
	ps= str(short_name)+'.py'
	ps_adress= path_to_bps+'/'+ str(short_name)+'.py'
			
	with open(ps_adress) as f:
		try:
			code=compile(f.read(),'ps','exec') 
			exec(code)
		except:
			error_type="Page Structure Error"
			error_message[short_name]=error_type
			broken.append(error_message)
			continue

		
# Write Excel		
	try:
		all_cur = [rates_u,rates_d,rates_e]
		for c,curr in enumerate(curren): 
			rates = all_cur[c] 
			if len(rates)<1: 
				continue
			for t,term in enumerate(terms):
				line=[short_name,int(nkb),full_name, group_1, Reuters, date,int(date_full.strftime('%d')), int(date_full.strftime('%Y')), int(date_full.strftime('%m')), int(date_full.strftime('%V')), curr, term, float(rates[t].replace('%','').replace(',','.'))]
				for l,col in enumerate(line):
					worksheet.write(i, l, col) 
				i=i+1		
		scrapped.append(short_name)
		print('Collected   ', short_name.upper())
	except:
		error_type="Data writing Error"
		error_message[short_name]=error_type	
		broken.append(error_message)
		continue

		
# Collecting Data from PDFs		

	


for n in names:  
	if n not in scrapped: 
		pdfs.append(n) 
		print('Collected   ', str(n).upper()) 
		time.sleep(1)

try: 
	pdf_names = pdf_sheet.col_values(1,start_rowx=0)
	pdf_links = pdf_sheet.col_values(1,start_rowx=1)
	for n,l in zip(pdfs,pdf_links):	
		pdfs[n]=l
		
	for pdf in pdfs:

		file=open(pdf, 'rb') 
		pdfreader=PyPDF2.PdfFileReader(file) 
		pageobj=pdfreader.getPage(0)
		text=pageobj.extractText()
		rates=text.split(rate=re.findall('(.+,%.+)', word))
		for rate in rates: 
			line=[short_name,int(nkb),full_name, group_1, Reuters, date,int(date_full.strftime('%d')), int(date_full.strftime('%Y')),int(date_full.strftime('%m')), int(date_full.strftime('%V')), curr, term, float(rates[t].replace('%','').replace(',','.'))]
			pdf_sheet.add_row(line)
			
except:
	pass

for rownum in range(pdf_sheet.nrows):
	row = pdf_sheet.row_values(rownum)
	if str(row[0]) in pdfs: 
		for q,ro in enumerate(row):
			cell=ro
			exec(row_format[q])
			worksheet.write(i, q, cell)
		i=i+1
			

workbook.close() 

print("\n" * 3)	
print("Web-Spider collected rates for ",len(names)," banks")
print("")
if len(broken)>0: 
	print("Problems: ")
	for b in broken:
		print("")
		for key,value in b.items(): 
			print(key, ' : ', value)
	
		

		
		
		
		

