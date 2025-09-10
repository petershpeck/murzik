rates=[] 
terms=['3m','6m','12m','18m']
curren=['UAH','USD']
for word in result: 	
	rate=re.findall('<td>(.+)%</td>', word) 
	rates=rates+rate


rates_u=[]
rates_d=[]	
rates_e=[]	
for d in [0,2,5,8]:	
	rates_u.append(str(rates[d]))

all_cur = [rates_u,rates_d,rates_e]	