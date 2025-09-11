terms=['3m','6m','9m','12m','18m','24m']
curren =['UAH', 'USD', 'EUR']	
					
for word in result:
	rate=re.findall('<td>.+/(.+)<sup>', word)
	rates=rates+rate 
rates_u=[]
rates_d=[]	
rates_e=[]	
for d in [0,1,2,3,4,5]:
	if d<4:
		rates_u.append(float(rates[d*3].replace('%','').replace(',','.'))) 
		rates_d.append(float(rates[d*3+2].replace('%','').replace(',','.')))
		rates_e.append(float(rates[d*3+3].replace('%','').replace(',','.')))
	else:
		rates_u.append(rates_u[d-1])
		rates_d.append(rates_d[d-1])
		rates_e.append(rates_e[d-1])
