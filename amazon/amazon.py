import requests
from bs4 import BeautifulSoup
import smtplib

#URL = "https://www.amazon.com/Sony-Full-Frame-Mirrorless-Interchangeable-Lens-ILCE7M3/dp/B07B43WPVK/ref=sr_1_4?keywords=sony+a7&qid=1580031730&sr=8-4"
URL = "https://www.amazon.es/Nintendo-Switch-Lite-Coral/dp/B085SPRQSQ/ref=sr_1_2?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1UEFHJ439POZL&dchild=1&keywords=nintendo%2Bswitch%2Blite&qid=1585417037&sprefix=nintendo%2B%2Caps%2C166&sr=8-2&th=1"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0"}

def check_price():
	#returns all the data from the page
	page = requests.get(URL, headers=headers)

	#parse all the page to pull out different pieces of data
	soup1 = BeautifulSoup(page.content, "html.parser")

	soup2 = BeautifulSoup(soup1.prettify(), "html.parser")



	title = soup2.find(id="productTitle")

	price = soup2.find(id="priceblock_ourprice").get_text()
	print(price)
	if float(price) < 210.00:
		send_mail()

def send_mail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()	

	server.login('davidmt1997@gmail.com', 'cs2010116F!')

	subject = 'Amaaon price fell down'
	body = 'Check the amazon link: '

	msg = f"Subject: {subject}\n\n{body}"

	server.send_mail(
		'davidmt1997@gmail.com',
		'davidmt1997@gmail.com'
		msg
	)

	print('Email has been sent')

	server.quit()

check_price()