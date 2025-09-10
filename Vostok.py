rates=[]
broke=[]
terms=['3m','6m','12m']
curren=['UAH','USD','EUR']
for word in result:				
	rate=re.findall('tabs-text">(.+%)</div>', word)					
	rates=rates+rate 	

for d in [0,1,2]:	
	rates_u.append(str(rates[d*3]))
	rates_d.append(str(rates[d*3+1]))
	rates_e.append(str(rates[d*3+2])) 
