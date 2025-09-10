import PyPDF2 
import io
from bs4 import BeautifulSoup 
import time 
import re
import csv
import xlsxwriter

newfile=open('file.txt', 'w')
file=open('alfa.pdf', 'rb')
pdfreader=PyPDF2.PdfFileReader(file) 

pageobj=pdfreader.getPage(0)

text=pageobj.extractText()

newfile.write(pageobj.extractText())

newfile.close



link='d:/UsersNBU/011019/Desktop/Python/pdf/file.txt'


text= open(link, encoding="utf-8")
  

print(text)


pip install numpy

#text=text.split 
#rates=[]


#for p in text: 
	#rate=re.findall('(.+%)', p)
	#rates=rates+rate

#print(text)