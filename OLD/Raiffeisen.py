	
		
rates=[]
terms=['1m','2m','3m','6m','12m']
curren =['UAH', 'USD', 'EUR']
for word in result: 	
	rate=re.findall('">(.+,.+?)%<br/', word)
	if len(rate)>10:
		lrate=rate[range(5)] 
		rrate=rate[range(-5)] 
		rates.append(rrate,lrate) 
		continue
	rates=rates+rate	

for d in [0,1,2,3,4]:	
	if d==3: 
		rates_u.append(str(15))
		rates_d.append(str(0.25))
		continue
	if d==4: 
		rates_u.append(str(14))
		rates_d.append(str(0.35))

		continue
	rates_u.append(str(rates[d]))
	rates_d.append(str(rates[d+8]))
rates_e=rates_d
all_cur = [rates_u,rates_d,rates_e]	
