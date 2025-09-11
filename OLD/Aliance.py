terms=["3m", "6m","9m","12m","18m","24m"]
curren =['UAH']	

for word in result:
			
	rate=re.findall('<td>(.+?)%</td>', word)
					
	rates=rates+rate



for d in [0,1,2,3,1,1]: 
	rates_u.append(str(rates[d+6]))
	rates_d.append(str(rates[d+16]))
 
all_cur = [rates_u,rates_d,rates_e]	
