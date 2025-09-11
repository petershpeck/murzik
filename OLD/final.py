import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup 
import time 
import re
import csv
import xlsxwriter
import datetime

total_rates=[]

date=str(datetime.date.today()) 
file_name='Deposits.xlsx'

links_in_progress=[
	#'https://www.aval.ua/ru/personal/accounts/main_table_dep/',
	#'https://bank.com.ua/ru/deposit/profit-plus',
	#'https://www.bisbank.com.ua/deposit_private/pributkovij-depozit/', 
	#'https://globusbank.com.ua/ru/depoziti.html',
	#'http://btabank.ua/ukr/record.php',
	#'http://www.clhs.kiev.ua/site/page_priv.php?lang=UA&id_part=67',
	#'https://www.eximb.com/ukr/personal/deposits/interest-rates-on-deposits-fo/#classic-term'
	#
	#	
	#'https://europrombank.kiev.ua/%D1%80%D0%BE%D0%B7%D1%80%D0%B0%D1%85%D1%83%D0%B9%D1%82%D0%B5-%D0%B4%D0%BE%D1%85%D1%96%D0%B4-%D0%B2%D1%96%D0%B4-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%B7%D0%B0%D0%BE%D1%89%D0%B0%D0%B4%D0%B6%D0%B5%D0%BD/', 
]





link='d:/UsersNBU/011019/Desktop/Python/file.txt'
sites=[
	#'https://www.oschadbank.ua/ua/private/deposit/my-deposit/', # done
	
	#'http://www.ukrgasbank.com/private/deposits/termconti',
	
	#'https://www.eximb.com/ua/business/pryvatnym-klientam/pryvatnym-klientam-depozyty/dodatkovo/procentni-stavky-za-vkladamy-fizychnyh-osib-yaki-diyut-v-at-ukreksimbank',
	
	#'https://my.ukrsibbank.com/ua/personal/deposits/at_the_end/',
	#'https://www.sberbank.ua/deposits/view/1/',
	#'https://credit-agricole.ua/privatnym-kliyentam/depoziti/depozit-strokovij', 
	#"https://ru.otpbank.com.ua/privateclients/deposits/termdeposit/",
	#'https://www.pib.ua/ru/private/depozity/deposit_stable/',
	
	'https://tascombank.ua/index.php?option=com_content&task=view&id=654&Itemid=45',
	'https://bankvostok.com.ua/private/deposits/deposit-maximalniy',
	'http://www.coopinvest.com.ua/uk/individuals',
	
	'https://www.ideabank.ua/ru/private-clients/deposits/deposit-safe/',
	"http://www.piraeusbank.ua/ru/individuals/deposits/european.html",
	
	'https://arkada.ua/ua/fiz/1737/2299/',
	'http://www.forward-bank.com/deposits/maximal/', 
	'http://www.poltavabank.com/home/index.php?option=com_content&task=view&id=2&Itemid=71', 
	'http://www.crediteurope.com.ua/ru/srochnyij_vklad.html',
	'https://concord.ua/ru/deposit/depozit-klassicheskij-', 
	'http://rwsbank.com.ua/info/chastnym-litsam/depozitnye-programmy-dlya-fizicheskikh-lits',
	'https://www.asviobank.ua/depozity-kredity.html',
	'http://www.radabank.com.ua/ogo-ogo-na-srok.html',
	'http://www.iboxbank.online/ua/depozit_ctandartniy.html',
	'https://crystalbank.com.ua/privatnim-klientam/depoziti/depozitnij-vklad-klasichnij',
	'https://unexbank.ua/site/page.php?lang=UA&id_part=3623',
	'https://ubib.com.ua/private/deposits',
	'https://www.ap-bank.com/individual-deposits.html',
	'http://www.sky.bank/ru/deposit-cli',
	'https://www.zemcap.com/ru/depozity.html', 
	'https://vernumbank.com/ru/depozit-strokovoy-1.html',
	
	'https://www.banklviv.com/deposit-private-client/#2'
	]

workbook=xlsxwriter.Workbook(file_name)

print('Starting the process...')
 
for s in sites: 

	url=s 
	html=urllib.request.urlopen(url)
	soup=BeautifulSoup(html.read(), "html.parser") 
	with open(link, 'w', encoding='utf-8') as f:
		f.write(str(soup)) 
	text= open(link, encoding="utf-8")
	soup=BeautifulSoup(text, "html.parser")
	result=str(soup)
	result=result.split()  

	
	if len(re.findall('.+oschadbank.+',s))>0: 
		curen=['UAH','USD','EUR']
		rates=[] 
		terms=[]
		for word in result: 
					
			term=re.findall('^scope="row">(.+)', word) 
			terms=terms+term 
			rate=re.findall('^text-bold">(.+)%', word) 
			rates=rates+rate  
		
		rh=rates[0:4] 
		rd=rates[4:8]
		reu=rates[8:13]
		terms=terms[0:4]
		worksheet=workbook.add_worksheet("Owad")
		for t in [1,2,3]:
			worksheet.write(0,t,curen[t-1])	
		for t2 in [1,2,3,4]:
			worksheet.write(t2,0,terms[t2-1])
			worksheet.write(t2,1,rh[t2-1])
			worksheet.write(t2,2,rd[t2-1])
			worksheet.write(t2,3,reu[t2-1])
			
		print('Get ',len(rates),'Oschadbank')
		total_rates=total_rates+rates
		
	if len(re.findall('.+eximb.+',s))>0: 
		terms=[]
		rates=[] 
		for word in result:
			
			term=re.findall('^width=".+%">(.+-.+)', word)
			terms=terms+term		
			rate=re.findall('^<td>(.+%)</td>', word) 
			rates=rates+rate 

		


		rates=rates[0:18]	
		terms=terms[0:6]
		fr=rates[0:6] 
		sr=rates[6:12]
		tr=rates[12:19]

		worksheet2=workbook.add_worksheet("Exim")
		row=0
		col=1
		worksheet2.write(1,0,"від 30 000 до 499 999,99 грн")	
		worksheet2.write(2,0,"від 500 000 до 999 999,99 грн") 
		

		
		for t in [0,1,2,3,4,5]:
			worksheet2.write(row,col+t,terms[t])	
			worksheet2.write(1,col+t,fr[t]) 
			worksheet2.write(2,col+t,sr[t])
			worksheet2.write(0,0,"Сума\Строк")
			
		print('Get ',len(rates),'UkrEksimbank')
		
		
	if len(re.findall('.+ukrgasbank.+',s))>0 : 
		curen=['UAH','USD','EUR'] 
		terms=['1m','3m', '6m', '9m','12m','18m']
		rates=[] 
		
		for word in result:
			rate=re.findall('<strong>(.+%)</strong>', word) 
			rate1=re.findall('<strong>(.+%)\u200b', word) 
			rates=rates+rate+rate1
		rates=rates[1:]
			
		worksheet3=workbook.add_worksheet("UkrGaz")
		
		
		
		worksheet3.write(0,0,"Строк(міс)\Валюта")
		for t in [0,1,2,3,4,5]: 
			worksheet3.write(t+1,0,terms[t])
			worksheet3.write(t+1,1,rates[t*3])
			worksheet3.write(t+1,2,rates[(t*3)+1])
			worksheet3.write(t+1,3,rates[(t*3)+2])
		for t2 in [0,1,2]: 
			worksheet3.write(0,t2+1,curen[t2])

			
		print('Get ',len(rates),'For UkrGazbank')
		
		
	
	if s=='https://my.ukrsibbank.com/ua/personal/deposits/at_the_end/': 
		rates=[]
		for word in result:
			
			terms=['9 міс.', '12 міс.', '18 міс.', '24 міс.']
			rate=re.findall('<td>(.+%)</td>', word)
			rates=rates+rate 
		
		worksheet5=workbook.add_worksheet("UkrSib")		
		for i in [0,1,2,3]:
			worksheet5.write(0,i+1,terms[i])
			worksheet5.write(1,i+1,rates[i])	 
		worksheet5.write(0,0,'Строк') 
		worksheet5.write(1,0,'Ставка (Гривня)')
		
		print('Get ',len(rates),'For Ukrsib')
		
		
		
	if s=='https://credit-agricole.ua/privatnym-kliyentam/depoziti/depozit-strokovij': 
		rates=[]
		for word in result:
			terms=['3 міс','6 міс','12 міс','18 міс']
			rate=re.findall('<td.(.+%)</td>', word)
			rates=rates+rate 
			
		worksheet7=workbook.add_worksheet("Credi-Agricole")	
		for f,u in zip([0,1,2,3],[0,1,4,7]):
				worksheet7.write(f+1,1,rates[u])
				worksheet7.write(f+1,0,terms[f]) 
		for t in [2,3]:
			worksheet7.write(t,2,rates[t]) 
		worksheet7.write(0,1,'Гривня') 
		worksheet7.write(0,2,'Долар')
		
		print('Get ',len(rates),'Credi Agricole')
		total_rates=total_rates+rates

		
	if s=="https://ru.otpbank.com.ua/privateclients/deposits/termdeposit/": 
		rates=[]
		ratesUAH=[]
		curren=['UAH', 'USD', 'EUR', 'CHF']
		for word in result:
			
			terms=['3 міс.', '6 міс.', '9 міс.', '12 міс.']
			rate=re.findall('<td>.+/(.+)<sup>', word)
			rate=rate[0:3]
			rates=rates+rate  
			
		worksheet8=workbook.add_worksheet("OTP")	
		for i in [0,1,2,3]: 
			worksheet8.write(0,i+1,curren[i])
			worksheet8.write(i+1,0,terms[i])
			worksheet8.write(i+1,1,rates[i]) 
			worksheet8.write(i+1,2,rates[4])
			worksheet8.write(i+1,3,rates[5])
			worksheet8.write(i+1,4,rates[6]) 
		worksheet8.write(0,0,"** - Ставка з виплатою у кінці строку")
		print('Get ',len(rates),'OTP')
		total_rates=total_rates+rates
		
	if len(re.findall('.+www.pib.ua.+',s))>0:	
		
		rates=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
			
			terms=['1 міс','2 міс','3 міс','4 міс','6 міс','7 міс','9 міс','12 міс']
			rate=re.findall('align="center"><strong>(.+)</strong></p>', word) 
			rate1=re.findall('align="center"><b>(.+)</b></p>', word)
			rates=rates+rate+rate1  
			
		worksheet9=workbook.add_worksheet("Prominvest")
		for m in [0,1,2,3,4,5,6,7]: 
			worksheet9.write(m+1,0,terms[m])
			worksheet9.write(m+1,1,rates[m*3])
			worksheet9.write(m+1,2,rates[m*3+1])
			worksheet9.write(m+1,3,rates[m*3+2])
		for t in [0,1,2]: 
			worksheet9.write(0,t+1,curren[t])
			
		print('Get ',len(rates),'Prominvest')
		total_rates=total_rates+rates	
		
	if len(re.findall('.+s://bank.com.ua/ru/individuals/deposits/doxod.+',s))>0:
		rates=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
			
			terms=['1 міс','3 міс','6 міс','9 міс','13 міс']
			rate=re.findall('<td>(.+,.+)</td>', word)
			
			rates=rates+rate  
		rates=rates[15:] 
		
		worksheet10=workbook.add_worksheet("Pivdenniy")
		
		for u in [0,1,2,3,4]: 
			worksheet10.write(u+1,0,terms[u])
			worksheet10.write(u+1,1,rates[u])
			worksheet10.write(u+1,2,rates[u+5])
			worksheet10.write(u+1,3,rates[u+10]) 
			
		for x in [0,1,2]: 
			worksheet10.write(0,x+1,curren[x]) 
			
		print('Get ',len(rates),'Pivdenniy')
		total_rates=total_rates+rates	


		
	if len(re.findall('.+kredobank.+',s))>0:		
		rates_u=[]
		rates_d=[]
		rates_e=[]

		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["3m", "6m","12m"]
			rate=re.findall('align="center">(.+)</p>', word)
							
			rates=rates+rate

		for p in [0,4,10]:	
			rates_u.append(rates[p])

			rates_d.append(rates[p+2])	
			
			rates_e.append(rates[p+3])	
	 
			
		worksheet12=workbook.add_worksheet("Credobank") 
		
		for u in [0,1,2]: 
			worksheet12.write(u+1,0,terms[u])
			worksheet12.write(u+1,1,rates_u[u]) 
			worksheet12.write(u+1,2,rates_d[u])
			worksheet12.write(u+1,3,rates_e[u]) 
		for x in [0,1,2]: 
			worksheet12.write(0,x+1,curren[x])  
			
		print('Get ',len(rates),'Credobank')
		
		
	
			 
	if len(re.findall('.+tascombank.+',s))>0:		 
		rates=[]
		curren=['UAH', 'USD', 'EUR']
		terms=["1 міс","3 міс","6 міс", "9 міс","12 міс"]
		for word in result:
			
			rate=re.findall('.>(.+%)</td>', word)
			rate1=re.findall('(15.75%)</td>', word)
			rates=rates+rate+rate1 
			
			rates=rates+rate+rate1   
			
		worksheet13=workbook.add_worksheet("Taskombank")
		
		for x in [0,1,2]: 
			worksheet13.write(0,x+1,curren[x]) 

		for y in [0,1,2,3,4]:
			worksheet13.write(y+1,0,terms[y])
			worksheet13.write(y+1,1,rates[y]) 
			worksheet13.write(y+1,2,rates[y+5])
			worksheet13.write(y+1,3,rates[y+10])
		
		print('Get ',len(rates),'Taskombank')
		
		
	if len(re.findall('.+bisbank.+',s))>0:	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["1 міс","2 міс", "3 міс", "6 міс", "12 міс"]
			rate=re.findall('<td>(.+%)</td>', word)
			rates=rates+rate				

		
		worksheet14=workbook.add_worksheet("BIS")
		for u in [0,1,2,3,4]: 
				worksheet14.write(u+1,0,terms[u])
				worksheet14.write(u+1,1,rates[u]) 
				worksheet14.write(u+1,2,rates[u+5])
				worksheet14.write(u+1,3,rates[u+10]) 
		for x in [0,1,2]: 
			worksheet14.write(0,x+1,curren[x])   
				
		print('Get ',len(rates),'BIS')	

		
	if len(re.findall('.+ideabank.+',s))>0:
	
		rates=[]
		curren=['UAH in Office', 'USD', 'EUR', 'UAH online']
		for word in result:
			
			terms=['3 міс','6 міс','9 міс','12 міс']
			rate=re.findall('align="center">(.+%)</p></td>', word) 
			
			rates=rates+rate
			rates=rates[0:18] 
			
		worksheet16=workbook.add_worksheet("Idea")
		
		for u in [0,1,2,3]:
				worksheet16.write(u+1,0,terms[u])
				worksheet16.write(0,u+1,curren[u])		
				worksheet16.write(1,u+1,rates[u])
				worksheet16.write(2,u+1,rates[u+4]) 
				worksheet16.write(3,u+1,rates[u+8]) 
				worksheet16.write(4,u+1,rates[u+12])

			
		print('Get ',len(rates),'Idea')
		

	
	if len(re.findall('.+piraeusbank.+',s))>0:  
	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["1 міс","2 міс", "3 міс","6 міс","9 міс", "12 міс"]
			rate=re.findall('<div>(.+%)</div>', word)
			rate1=re.findall('valign="top">(.+%)</td>', word)
			rates=rates+rate+rate1				

			
		worksheet17=workbook.add_worksheet("Pireus")
		
		for i in [0,1,2,3,4,5]:
			worksheet17.write(i+1,0,terms[i])
			if i==0: 
				worksheet17.write(i+1,1,rates[1])
			elif i>3: 
				worksheet17.write(i+1,1,rates[(i*6)-1])	
			else:
				worksheet17.write(i+1,1,rates[i*6])	
			
			worksheet17.write(0,1,'UAH') 
			
			
		print('Get ',len(rates),'Pireus')
		
		
		
	if len(re.findall('.+globusbank.+',s))>0:	
		
		rates=[] 
		rates_u=[] 
		rates_d=[]
		terms=["1 міс", "3 міс", "6 міс", "9 міс", "12 міс"]
		curren=['UAH', 'USD', 'EUR']
		for word in result:

			rate=re.findall('align=.+>(.+?%)</td>', word) 									
			rates=rates+rate

		rates_u=rates[:5] 

	
			
		worksheet18=workbook.add_worksheet("Globus")	
		
		for u in [0,1,2,3,4]:	
			worksheet18.write(u+1,0,terms[u])
			worksheet18.write(u+1,1,rates_u[u])
		for x in [0,1,2]: 
			worksheet18.write(0,x+1,curren[x]) 
		
		
		print('Get ',len(rates),'Globus')
			 

	if len(re.findall('.+btabank.+',s))>0:	
		
		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["3 міс", "6 міс","12 міс","18 міс"]
			rate=re.findall('align="center">(.+)</td>', word)
			rate1=re.findall('color="#FF0000">(.+)</font></td>', word)
			rates=rates+rate+rate1	
		
		rates=rates[0:11]	
			
		worksheet19=workbook.add_worksheet("BTA")
		
		for u in [0,1,2,3]:	
			worksheet19.write(u+1,0,terms[u])
			worksheet19.write(u+1,1,rates[u*3]) 
			worksheet19.write(u+1,2,rates[(u*3+1)])
		for x in [0,1,2]: 
			worksheet19.write(0,x+1,curren[x])
			worksheet19.write(x+1,3,rates[(x*3+2)]) 
			
			
		print('Get ',len(rates),'BTA')
		
	if len(re.findall('.+mistobank.+',s))>0:

		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["1 міс","2 міс", "3 міс","6 міс","9 міс", "12 міс", "18 міс"]
			rate=re.findall('width="65">(.+%)</td>', word)
			rate1=re.findall('bold">(.+%)</td>',word)
			rates=rates+rate+rate1				

		worksheet20=workbook.add_worksheet("Misto")	
		for u in [0,1,2,3,4,5,6]:	
			worksheet20.write(u+1,0,terms[u]) 
			worksheet20.write(u+1,1,rates[u])
			worksheet20.write(u+1,2,rates[u+7])
			worksheet20.write(u+1,3,rates[u+7])
		for u in [0,1,2]:	
			worksheet20.write(0,u+1,curren[u])
		print('Get ',len(rates),'Misto')

			
	if len(re.findall('.+clhs.kiev.+',s))>0:
	
		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
				
		for word in result:
					
			terms=["1 міс","3 міс", "6 міс", "12 міс"]
			rate=re.findall('style="text-align:center">(.+)</p>', word) 
			rate1=re.findall('style="text-align:center">(.+)</td>', word) 
							
			rates=rates+rate+rate1
				
		rates=rates[12:]
		
		worksheet21=workbook.add_worksheet("ClDim")	
		for u in [0,1,2,3]:	
			worksheet21.write(u+1,0,terms[u]) 
			worksheet21.write(u+1,1,rates[u*3]) 
			worksheet21.write(u+1,2,rates[(u*3+1)]) 
			worksheet21.write(u+1,3,rates[(u*3+2)])
			
		for u in [0,1,2]:
			worksheet21.write(0,u+1,curren[u])
			
		print('Get ',len(rates),'ClDim')	

		
		
	if len(re.findall('.+arkada.+',s))>0:	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=[ "3 міс",  "6 міс", "9 міс", "12 міс",]
			rates=[ '6.00%', '13,5%', '13,5%', '14.00%', ]
					
			
			
		worksheet22=workbook.add_worksheet("Arkada")	
		
		for u in [0,1,2,3]:	
			worksheet22.write(0,u+1,terms[u]) 
			worksheet22.write(1,u+1,rates[u])
			
		worksheet22.write(0,0,'Строк') 
		worksheet22.write(1,0,"Ставка") 
		
		
		print('Get ',len(rates),'Arkada')
		
		
		
	if len(re.findall('.+forward-bank.+',s))>0:	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=["90 днів", "180 днів","367 днів","734 днів"]
			rate=re.findall('.+,.+%', word)
					
			rates=rates+rate

		worksheet23=workbook.add_worksheet("Forward")	
				
		for u in [0,1,2,3]:	
			worksheet23.write(u+1,0,terms[u]) 
			worksheet23.write(u+1,1,rates[u])
		worksheet23.write(0,1,'UAH')
 
		print('Get ',len(rates),'Forward')


	
	if len(re.findall('.+poltavabank.+',s))>0:	
		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=["3 міс", "6 міс", "9 міс", "12 міс",  "13 міс", "18 міс", "24 міс"]
			rate=re.findall('class="contentpane">(.+)</p></td><td', word)
	
			rates=rates+rate
		
		rates=rates[3:]			
		worksheet24=workbook.add_worksheet("Poltava")	
				
		for u in [0,1,2,3,4,5,6]:	
			worksheet24.write(u+1,0,terms[u]) 
			worksheet24.write(u+1,1,rates[u])
		worksheet24.write(0,1,'UAH')
 
		print('Get ',len(rates),'Poltava')
		
		
		
		
	if len(re.findall('.+crediteurope.+',s))>0:		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=["7 дн",  "14 дн", "21 дн", "1 міс", "2 міс", "3 міс", "6 міс", "12 міс",  "24 міс"]
			rate=re.findall('class="tdLight">(.+)</td>', word)              
			rates=rates+rate
			

		worksheet25=workbook.add_worksheet("KredEuro")	
				
		for u in [0,1,2,3,4,5,6,7,8]:	
			worksheet25.write(u+1,0,terms[u]) 
			worksheet25.write(u+1,1,rates[u*6])
			worksheet25.write(u+1,2,rates[(u*6+1)])
			worksheet25.write(u+1,3,rates[(u*6+2)])
		
		for x in [0,1,2]: 
			worksheet25.write(0,x+1,curren[x])
		
		print('Get ',len(rates),'KredEURO')
	
	if len(re.findall('.+coopinvest.+',s))>0: 
	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["12 міс","18 міс", "24 міс"]
			rate=re.findall('<td>(.+%)</td>', word)
			rates=rates+rate				
		rates=rates[24:]
		
		worksheet26=workbook.add_worksheet("Kominvest")	
				
		for u in [0,1,2]:	
			worksheet26.write(u+1,0,terms[u]) 
			worksheet26.write(u+1,1,rates[(u*3)])
			worksheet26.write(u+1,2,rates[(u*3+1)])
			worksheet26.write(u+1,3,rates[(u*3+2)]) 
			worksheet26.write(0,u+1,curren[u]) 
			
		worksheet26.write(0,0,'Term(Month)')
	
		print('Get ',len(rates),'Kominvest')
		
			
			
	if len(re.findall('.+motor-bank.+',s))>0: 		
			
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=[ "3 міс", "6 міс", "12 міс"]
			rate=re.findall('size="2">(.+)</font></td></tr>', word) 
			rate1=re.findall('size="2">(.+)</font></td><td', word)												
			rates=rates+rate+rate1

		rates=rates[:9]	

		worksheet27=workbook.add_worksheet("Motor")	
				
		for u in [0,1,2]:	
			worksheet27.write(u+1,0,terms[u]) 
			worksheet27.write(u+1,1,rates[(u*3)])
			worksheet27.write(u+1,2,rates[(u*3+1)])
			worksheet27.write(u+1,3,rates[(u*3+2)])  
			worksheet27.write(0,u+1,curren[u])
			
			
		worksheet27.write(0,0,'За умови вкладу від 100 000 грн')	
			
		print('Get ',len(rates),'Motor')
		
		
		
	if len(re.findall('.+bmbank.+',s))>0:	
		
		
	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			
			terms=[ "3 міс", "6 міс"]
			rate=re.findall('align="center">(.+%)</p></td>', word) 									
			rates=rates+rate

		worksheet28=workbook.add_worksheet("BMBank")
		for u in [0,1,2]:	
			worksheet28.write(0,u+1,curren[u])

		for u in [0,1]:	
			worksheet28.write(u+1,1,rates[(u*6+3)])
			worksheet28.write(u+1,2,rates[(u*6+4)]) 
			worksheet28.write(u+1,3,rates[(u*6+5)])
			worksheet28.write(u+1,0,terms[(u)])
		
		
		print('Get ',len(rates),'BMBank')
		
		
		rates=['13%','3%']
		worksheet29=workbook.add_worksheet("Grant")
		
		for u in [0,1]:	
			worksheet29.write(1,u+1,rates[u]) 
			worksheet29.write(0,u+1, curren[u])	
			worksheet29.write(1,0, "12 міс + 1 день") 
		print('Get ',len(rates),'Grant')
		
		
		
		
	if len(re.findall('.+asviobank.+',s))>0:	
			
		
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
	
			
		terms=["1 міс", "3 міс", "6 міс", "12 міс"]
		rates=['10%','11%','12%','16%','-','-','4%','6%']	


		worksheet30=workbook.add_worksheet("ASVIO")
			
		for u in [0,1,2,3]:	
			worksheet30.write(u+1,0,terms[u])
			worksheet30.write(u+1,1,rates[u])
			worksheet30.write(u+1,2,rates[u+4])
			
		for u in [0,1]:
			worksheet30.write(0,u+1, curren[u]) 
			
		print('Get ',len(rates),'ASVIO')
	
	if len(re.findall('.+radabank.+',s))>0:	
	
		rates2=[]
		curren=['UAH', 'USD', 'EUR']
		terms=["1 міс", "2 міс","3 міс", "6 міс", "12 міс"]
		
		for word in result:
			rate=re.findall('geneva;">(.+%)</span></td>', word) 
			rates=rates+rate

		for word2 in result:
			rate2=re.findall('geneva;">(.+%)</span></p>', word2) 
			rates2=rates2+rate2 
			
		rates_d=rates2[0:5] 
		rates_e=rates2[5:11] 

		
		curren=['UAH', 'USD', 'EUR']
		
		worksheet31=workbook.add_worksheet("RADA")
		
		for s in [0, 1, 2, 3,4]:	
			worksheet31.write(s+1,0,terms[s])
			worksheet31.write(s+1,1,rates[s])
			worksheet31.write(s+1,2,rates_d[s]) 
			worksheet31.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet31.write(0,u+1, curren[u])
			
		print('Get ',len(rates),'RADA')
	



	
	if s=='https://crystalbank.com.ua/privatnim-klientam/depoziti/depozitnij-vklad-klasichnij':	
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["12 міс","18 міс", "24 міс"]
			rate=re.findall('14pt;">(.+%)<br', word)
			rates=rates+rate		

	
		
		worksheet32=workbook.add_worksheet("Crystal")
		
		l=len(rates)
		for s in range(l):	
			worksheet32.write(s+1,0,rates[s])

		print('Get ',len(rates),'Crystal')	
		
		
		
		curren=['UAH', 'USD', 'EUR']
		terms=["1m", "2m", "3m", "4m", "6m", "12m"]
		rates_u=['10,5%', '10,5%', '13,5%', '13,5%', '14,5%', '15%'] 
		rates_d=['-','-', '2%', '2%', '3%', '3,25%'] 
		rates_e=['-','-','2','2','3%', '3,25%']
	
		worksheet33=workbook.add_worksheet("Unex")
			
		for s in [0, 1, 2, 3, 4, 5]:	
			worksheet33.write(s+1,0,terms[s])
			worksheet33.write(s+1,1,rates_u[s])
			worksheet33.write(s+1,2,rates_d[s]) 
			worksheet33.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet33.write(0,u+1, curren[u]) 
		
		
		print('Get ',len(rates),'Unex')
		
		
		rates=[]
		terms=["3 міс", "6 міс", "12 міс", "12+ міс" ]
		rates_u=['12%', '13%', '13,6%', '13,7%'] 
		rates_d=['1%','1.5%', '4%', '4%'] 
		rates_e=['1%','1.5%','2%','2%']
		rates=rates_u+rates_d+rates_e

		
		worksheet34=workbook.add_worksheet("Meta")
			
		for s in [0, 1, 2, 3]:	
			worksheet34.write(s+1,0,terms[s])
			worksheet34.write(s+1,1,rates_u[s])
			worksheet34.write(s+1,2,rates_d[s]) 
			worksheet34.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet34.write(0,u+1, curren[u]) 
		
		
		print('Get ',len(rates),'Meta')
	
	if s=="http://www.iboxbank.online/ua/depozit_ctandartniy.html":
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["","1 міс","3 міс", "6 міс", "12 міс"]
			rate=re.findall('center;">(.+)</td>', word)
			rates=rates+rate				

		
		worksheet35=workbook.add_worksheet("I-Box")
		
		for s in [0, 1, 2, 3, 4]:	
			worksheet35.write(s,0,terms[s])
			worksheet35.write(s,1,rates[s])
			worksheet35.write(s,2,rates[s+5]) 
			worksheet35.write(s,3,rates[s+10])
		
		print('Get ',len(rates),'I-Box')
		
		
	if s =='https://ubib.com.ua/private/deposits':	
		
		
		rates=[]
		terms=["1 міс", "3 міс", "6 міс", "12 міс" ]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			rate=re.findall('class="cell"><span><span>(.+%)</span></span></div>', word) 									
			rates=rates+rate

		rates=rates[9:19]
		
		worksheet36=workbook.add_worksheet("Ukrbudinvest")
		
		worksheet36.write(1,1,rates[0])
		
		for s in [0, 1, 2, 3]:	
			worksheet36.write(s+1,0,terms[s])

		
		
		for u in [0,1,2]:
			worksheet36.write(0,u+1, curren[u])
			worksheet36.write(2,u+1, rates[u+1])
			worksheet36.write(3,u+1, rates[u+4])
			worksheet36.write(4,u+1, rates[u+7])
			
			
		print('Get ',len(rates),'Ukrbudinvest')	
		
		
		
		terms=["1 міс", "3 міс", "6 міс","9 міс", "12 міс", "18 міс"]
		rates_u=['12%', '14.1%', '14.4%', '14.7%', '15%', '15,7%'] 
		rates_d=['1.5%', '2%', '3%', '3.5%', '4%', '4.1%']  
		rates_e=['1%', '2%', '2.5%', '3%', '3.5%', '3,7%'] 
		rates=rates_u+rates_d+rates_e

		
		worksheet37=workbook.add_worksheet("PoliCom")
		
		for s in [0, 1, 2, 3,4,5]:	
			worksheet37.write(s+1,0,terms[s])
			worksheet37.write(s+1,1,rates_u[s])
			worksheet37.write(s+1,2,rates_d[s]) 
			worksheet37.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet37.write(0,u+1, curren[u]) 
		
		
		print('Get ',len(rates),'PoliCom')	
		
		
		worksheet38=workbook.add_worksheet("Akkord")
		
		terms=["1 міс", "3 міс", "6 міс", "12 міс"]
		rates_u=['10%', '14%', '15.5%', '16%'] 
		rates_d=['1%', '3%', '4%', '4.5%']  
		rates_e=['1%', '3%', '4%', '4.5%'] 
		rates=rates_u+rates_d+rates_e
		
		
		for s in [0, 1, 2, 3]:	
			worksheet38.write(s+1,0,terms[s])
			worksheet38.write(s+1,1,rates_u[s])
			worksheet38.write(s+1,2,rates_d[s]) 
			worksheet38.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet38.write(0,u+1, curren[u]) 

		
		
		print('Get ',len(rates),'Akkord')
		
		
	if s =='https://www.ap-bank.com/individual-deposits.html': 	
		
		rates=[]
		terms=["1 міс", "3 міс", "6 міс","9 міс", "12 міс", "18 міс"]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		

		for word in result:
			rate=re.findall('<p>(.+%)</p>', word) 
			rates=rates+rate
			
	
		

		worksheet39=workbook.add_worksheet("AP")
	
		for s in [0,1,2,3,4]:	
			worksheet39.write(s+1,0,terms[s])
			worksheet39.write(s+1,1,rates[s])
			
			worksheet39.write(s+1,3,"0,1%")
			
		for v in [0, 1, 2, 3]:
			worksheet39.write(v+1,2,rates[(v+5)]) 
		
		for u in [0,1,2]:
			worksheet39.write(0,u+1, curren[u]) 
		
		print('Get ',len(rates),'Agroprosperies')
		
		
		
		
	if s=='https://concord.ua/ru/deposit/depozit-klassicheskij-':	
		
		rates=[]
		terms=["1 міс", "3 міс", "6 міс", "12 міс"]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			rate=re.findall('>(.+%)</td>', word) 									
			rates=rates+rate

		worksheet40=workbook.add_worksheet("Konkord")
	
		for s in [0, 1, 2]:	
			worksheet40.write(s+1,0,terms[s])
			worksheet40.write(s+1,1,rates[(s)])
			worksheet40.write(s+1,2,rates[(s+3)]) 
		
		for u in [0,1]:
			worksheet40.write(0,u+1, curren[u]) 
		
		print('Get ',len(rates),'Konkord')
		

	if s=='https://www.zemcap.com/ru/depozity.html': 

		rates=[]
		terms=["1 міс", "3 міс", "6 міс","9 міс", "12 міс", "18 міс"]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:

			rate=re.findall('>(\d+\,\d+)', word) 									
			rates=rates+rate

		rates=rates[32:]	
		rates_u=[rates[0],rates[3],rates[6],rates[9],rates[12],rates[15]]
		rates_d=[rates[1],rates[4],rates[7],rates[10],rates[13],rates[16]]
		rates_e=[rates[2],rates[5],rates[8],rates[11],rates[14],rates[17]]

				
		
		worksheet40=workbook.add_worksheet("ZemCap")
	
		for s in [0, 1, 2, 3, 4, 5]:	
			worksheet40.write(s+1,0,terms[s])
			worksheet40.write(s+1,1,rates_u[s])
			worksheet40.write(s+1,2,rates_d[s])  
			worksheet40.write(s+1,3,rates_e[s])
		
		for u in [0, 1, 2]:
			worksheet40.write(0,u+1, curren[u]) 
		
		print('Get ',len(rates),'ZemCap')
		
		
		
		
		
	if s== 'https://vernumbank.com/ru/depozit-strokovoy-1.html':	
		
		rates=[]
		terms=[ "1 міс","3 міс", "6 міс","9 міс", "12 міс"]
		curren=['UAH', 'USD', 'EUR']
		sum=['<50k UAH', '<350k UAH', ">350K UAH"]
		for word in result:
			rate=re.findall('>(.+%)', word) 
			rates=rates+rate


		worksheet41=workbook.add_worksheet("Vernum")
	
		for s in [0, 1, 2, 3, 4]:	
			worksheet41.write(s+1,0,terms[s])
			worksheet41.write(s+1,1,rates[(s+2)])
			worksheet41.write(s+1,2,rates[(s+10)])  
			worksheet41.write(s+1,3,rates[(s+17)])
		
		for u in [0, 1, 2]:
			worksheet41.write(0,u+1, curren[u]) 
		
		
		print('Get ',len(rates),'Vernum')
	

	
	if s=='http://rwsbank.com.ua/info/chastnym-litsam/depozitnye-programmy-dlya-fizicheskikh-lits':
		rates=[]
		curren=['UAH', 'USD', 'EUR']
		terms=["1 міс", "3 міс", "6 міс", "12 міс","18 міс","24 міс" ]
		for word in result:
			
			terms=["1 міс","3 міс", "6 міс", "12 міс", "18 міс", "24 міс"]
			rate=re.findall('center;"><strong>(.+%)</strong></p>', word)
	
			rates=rates+rate				
		rates_u=rates[:6]
		rates_d=rates[16:22]
		rates_e=rates[28:35]
		worksheet43=workbook.add_worksheet("RwS")

		for s in [0, 1, 2, 3, 4, 5]:	
			worksheet43.write(s+1,0,terms[s])
			worksheet43.write(s+1,1,rates_u[s])
			worksheet43.write(s+1,2,rates_d[s]) 
			worksheet43.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet43.write(0,u+1, curren[u]) 

		print('Get ',len(rates),'RwS')
		
		
	if s== 'https://www.bankcenter.com.ua/ua/private/Depozitni-programi-3':		
		
		rates=[]
		rates_u=[] 
		rates_d=[] 
		rates_e=[]
		terms=["1 міс", "3 міс", "6 міс", "9 міс", "12 міс"]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
			rate=re.findall('align="center">(.+%)</p>', word) 
			rates=rates+rate

		for i in [0,1,2,3]:
			rates_u.append(rates[i*2]) 
			rates_d.append(rates[i*2+13])
			rates_e.append(rates[i*2+26])


		worksheet44=workbook.add_worksheet("Center")

		for s in [0, 1, 2]:	
			worksheet44.write(s+1,0,terms[s])
			worksheet44.write(s+1,1,rates_u[s])
			worksheet44.write(s+1,2,rates_d[s]) 
			worksheet44.write(s+1,3,rates_e[s]) 
		
		for u in [0,1,2]:
			worksheet44.write(0,u+1, curren[u]) 
			
		worksheet44.write(5,0,terms[4]) 
		worksheet44.write(4,0,terms[3])
		worksheet44.write(5,1,rates_u[3])
		worksheet44.write(5,2,rates_d[3]) 
		worksheet44.write(5,3,rates_e[3]) 


		print('Get ',len(rates),'Center')
		
		
		
	if s=="https://www.credit-optima.com.ua/ukr/private/deposits/classic/":	
		
		
		
		rates=[]
		terms=["1 міс", "3 міс", "6 міс","9 міс", "12 міс", "18 міс"]
		curren=['UAH', 'USD', 'EUR']

		for word in result:
			rate=re.findall('3px"><strong>(.+%)</strong></p></td>', word) 
			rates=rates+rate
			
		rates_u=rates[0:5]
		rates_d=rates[5:10]
		rates_e=rates[10:15] 
		rates_e.insert(0, '')
			

		worksheet44=workbook.add_worksheet("Cred-Optima")
		
		for s in [0, 1, 2, 3, 4]:	
			worksheet44.write(s+1,0,terms[s])
			worksheet44.write(s+1,1,rates_u[s])
			worksheet44.write(s+1,2,rates_d[s]) 
			worksheet44.write(s+1,3,rates_e[s])
		
		for u in [0,1,2]:
			worksheet44.write(0,u+1, curren[u]) 
		
		
		print('Get ',len(rates),'Cred-Optima')	
		
		
		
		
		
	if s=='https://www.sberbank.ua/deposits/view/1/':		
		
		
		
		rates=[]
		terms=["3 міс", "6 міс", "12 міс"]
		curren=['UAH', 'USD', 'EUR']

				

		for word in result:
			rate=re.findall('class="tac"><strong>(.+)</strong></td>', word) 
			rates=rates+rate
			

		worksheet46=workbook.add_worksheet("SBER")
		
		
		for s in [0,1,2]:
			worksheet46.write(0,s+1, curren[s]) 
			worksheet46.write(s+1,0,terms[s])
			worksheet46.write(s+1,1,rates[s])
		
		print('Get ',len(rates),'SBER')	 
		
		
	if s=='https://bankvostok.com.ua/private/deposits/deposit-maximalniy':		
		
		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["3m", "6m","12m"]
			rate=re.findall('tabs-text">(.+%)</div>', word)
							
			rates=rates+rate

	
		worksheet46=workbook.add_worksheet("Vostok")

		for s in [0,1,2]:
			worksheet46.write(0,s+1, curren[s]) 
			worksheet46.write(s+1,0,terms[s])
			worksheet46.write(s+1,1,rates[s*3])
			worksheet46.write(s+1,2,rates[s*3+1]) 
			worksheet46.write(s+1,3,rates[s*3+2])
			
		print('Get ',len(rates),'Vostok')	 
		
		
		
		
		
	if s=='https://europrombank.kiev.ua/%D1%80%D0%BE%D0%B7%D1%80%D0%B0%D1%85%D1%83%D0%B9%D1%82%D0%B5-%D0%B4%D0%BE%D1%85%D1%96%D0%B4-%D0%B2%D1%96%D0%B4-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%B7%D0%B0%D0%BE%D1%89%D0%B0%D0%B4%D0%B6%D0%B5%D0%BD/':	
		
		rates=[]
		rates_u=[] 
		rates_d=[] 
		rates_e=[]
		rates=[]
		curren=['UAH', 'USD', 'EUR','CHF']
		
		for word in result:		
			terms=["3 мес","6 мес", "9 мес","12 мес"]
			rate=re.findall('річних:">(.+)', word)
			rates=rates+rate		
		rates=rates[3:]

		rates_u=rates[4:8]
		rates_d=rates[23:27]
		rates_e=rates[41:45]
		
		worksheet46=workbook.add_worksheet("Evroprom")
		
		
		for s in [0, 1, 2, 3]:	
			worksheet46.write(s+1,0,terms[s])
			worksheet46.write(s+1,1,rates_u[s])
			worksheet46.write(s+1,2,rates_d[s]) 
			worksheet46.write(s+1,3,rates_e[s]) 
			worksheet46.write(0,s+1,curren[s])
			
		print('Get ',len(rates),'Evroprom')	
		
		
		
	if s=='https://www.banklviv.com/deposit-private-client/#2':	
		
		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
							
			terms=["3 міс","6 міс","12 міс"]
			rate=re.findall('>(.+%)</div>', word)


			rates=rates+rate

		worksheet47=workbook.add_worksheet("Lviv")
		
		
		for s in [0, 1, 2]:	
			worksheet47.write(s+1,0,terms[s])
			worksheet47.write(s+1,1,rates[s*3]) 
			worksheet47.write(0,s+1, curren[s]) 
			
		print('Get ',len(rates),'Lviv')	
		
	if s=='http://www.sky.bank/ru/deposit-cli':
		rates=[]
		terms=["1 міс","2 міс", "3 міс","6 міс", "9 міс","12 міс", "18 міс","24 міс"]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
				
			rate=re.findall('<p>(.+%)</p>', word)
			rates=rates+rate		

		rates=rates[18:]



		worksheet47=workbook.add_worksheet("Region")
		
		for s in [0, 1, 2, 3,4,5,6,7]:
			worksheet47.write(s+1,0,terms[s])
			worksheet47.write(s+1,1,rates[s])
		
		
		
		print('Get ',len(rates),'Region')	
		
		
	if s=='https://www.aval.ua/ru/personal/accounts/main_table_dep/':	

		rates=[]
		terms=[]
		curren=['UAH', 'USD', 'EUR']
		for word in result:
					
			terms=["1 міс","2 міс", "3 міс","6 міс","12 міс"]
			rate=re.findall('(.+%)</td><td', word)
			rate1=re.findall('(.+%)</td></tr', word)
			rates=rates+rate+rate1			

		worksheet48=workbook.add_worksheet("Raiffeisen")
		
		for s in [0, 1, 2, 3, 4]:
			worksheet48.write(s+1,0,terms[s])
			worksheet48.write(s+1,1,rates[s*3+1])
			worksheet48.write(s+1,2,rates[s*4+2])
	
		for u in [0,1,2]:
			worksheet48.write(0,u+1, curren[u]) 
		print('Get ',len(rates),'Raiffeisen')	
		
print("Well Done")		
		
		
		
		
