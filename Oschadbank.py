rates=[]
terms=['3m','6m','12m','18m']
curren =['UAH', 'USD', 'EUR']
for word in result: 	
	rate=re.findall('^text-bold">(.+)%', word) 
	rates=rates+rate
		
rates_u=[]
rates_d=[]	
rates_e=[]	
for d in [0,1,2,3]:	
	rates_u.append(str(rates[d]))
	rates_d.append(str(rates[d+4]))
	rates_e.append(str(rates[d+8]))
all_cur = [rates_u,rates_d,rates_e]