from bs4 import BeautifulSoup
import requests
import json
import smtplib
import time

end_date = "2019-01-15"

def send_mail(msg=""):
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()

	#Next, log in to the server
	server.login("mail", "password")
		
	msg += "\n hawlik lien : https://app.bookitit.com/es/hosteds/widgetdefault/2c51618dd2b463d4d7da1304ee47755ca#datetime"
	
	server.sendmail("your_mail",
                                ["destination_mails"],
                                msg)

	server.close()

send_mail()
while True:
	start_date = time.strftime("%Y-%m-%d")

	res = requests.get('https://app.bookitit.com/onlinebookings/datetime/?callback=jQuery211011478143345995351_1544212826766&type=default&publickey=2c51618dd2b463d4d7da1304ee47755ca&lang=es&services%5B%5D=bkt278212&agendas%5B%5D=bkt129679&version=201811721&src=https%3A%2F%2Fapp.bookitit.com%2Fes%2Fhosteds%2Fwidgetdefault%2F2c51618dd2b463d4d7da1304ee47755ca&srvsrc=https%3A%2F%2Fapp.bookitit.com&start={}&end={}&selectedPeople=1&_=1544212826778'.format(start_date, end_date))
	soup = BeautifulSoup(res.content, "lxml")

	content = json.loads(soup.text[51:-2])
	print ('time: {}'.format(time.ctime()))
	

	dates = []
	msg = ""
	
	for jour in content['Slots']:
		if len(jour['availabletime']) > 0:
			
			dates.append("\t{}\t{}".format(jour['availabletime'], jour['date']))

			print("\t{}\t{}".format(len(jour['availabletime']), jour['date']))

	try:
		if dates:
			for d in dates:
				#Send the mail
				msg += "\nkayn rendez vous fi had la date {}".format(d) # The /n separates the message from the headers

			send_mail(msg)

	except: 
		print("error in sending the mail!!!")

	time.sleep(60*5)
