from html.parser import HTMLParser
from urllib.request import urlopen 
from urllib import parse

class LinkParser(HTMLParser): 

	def handle_starttag(self, tag, attrs): 
		if tag=='a': 
			for (key, value) in attrs: 
				if key =='href': 
					newUrl=parse.urljoin(self.baseUrl, value) 
					self.links=self.links = [newUrl] 
					
	def GetLinks(self, url): 
		self.links=[] 
		self.baseUrl=url 
		response=urlopen(url) 
		if response.getheader('Content-Type')=='text/html': 
			htmlBytes=response.read() 
			htmlString=htmlBytes.decode("utf-8") 
			self.feed(htmlString) 
			return htmlString, self.links 
		else:  
			return "",[]  

def spider(url, word, maxPages): 
	pagesToVisit=[url] 
	numberVisited=0 
	foundWord=False 
	while numberVisited<maxPages and pagesToVisit !=[] and not foundWord: 
		numderVisited=numberVisited + 1 
		url=pagesToVisit[0] 
		pagesToVisit=pagesToVisit[1:] 
		try: 
			print(numberVisited, "Visiting: ", url) 
			parser=LinkParser() 
			data, links=parser.getLinks(url) 
			if data.find(word)>-1: 
				foundWord=True 
			pagesToVisit=pagesToVisit+links 
			print("***SUCCESS***") 
		except: 
			print("***FAILED***") 
	if foundWord: 
		print("The word", word, "was found at", url) 
	else: print ("***NO SUCH WORD***")
	
	
spider("https://tables.finance.ua/ua/credit_deposit/deposit#app-tabloid/client=nat&sort=0.1", "Паладій", 200)

