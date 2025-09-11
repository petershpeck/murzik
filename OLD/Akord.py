terms=["12m", "6m","3m"]
curren =['UAH', 'USD','EUR']	





rates=[]	

for word in result:
			
	rate=re.findall('10.5pt">(.+)%</font></i></p></td>', word)
	rate1=re.findall('10.5pt">(.+)%</font></p></td>', word)				
	rates=rates+rate + rate1



for d in [0,1,2]:	
		rates_u.append(str(rates[d*3]))
		rates_d.append(str(rates[d*3+1])) 
		rates_e.append(str(rates[d*3+2]))
all_cur = [rates_u,rates_d,rates_e]	
