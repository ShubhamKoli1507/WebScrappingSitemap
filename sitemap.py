import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

try: 
    conn = MongoClient('mongodb://localhost:27017' ) 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 

db = conn.rtpa4

def trade_spider(max_pages):
    page = 1
    count = 1
    while page <= max_pages:
        url = 'https://websites.co.in/sitemap?page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,'html.parser')
        table_body=soup.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
        	cols=row.find_all('td')
        	cols=[x.text.strip() for x in cols]
        	#print (cols)
        	link = str(row.a["href"])
        	name = cols[0]
        	category = cols[1]
        	city = cols[2]
        	
        	print("website "+str(count))
        	print("Link:"+link)
        	print("Name:"+name)
        	print("Category:"+category)
        	print("City:"+city)
        	
        	count = count + 1
        	source_code = requests.get("https:"+link)
        	plain_text = source_code.text
        	soup = BeautifulSoup(plain_text,'html.parser')
        	title = soup.find('title').text
        	print("title:"+title)
        	try:
        		p = soup.find('div',{"class":"update-content","class": "update-text","class":"update-details"})
        		#paragraph = p.find('p').text
        		#print("Description:"+paragraph)
        		header = soup.find("h1").text
        		print("header:"+header)
        		
        	except AttributeError:
        		x = " "
        		print(x)
        	#header = soup.find("h1").text
        	#print("header:"+header)
        	print("################################################")
        	db.myindex.insert_one(
				{
				'Link' : link,
				'Name': name,
        		'Category' : category,
        		'City': city,
        		'title' : title,
        		#'Description' : paragraph,
        		'Header' : header
    			})

        page+=1                            
trade_spider(2)
print("Done")
