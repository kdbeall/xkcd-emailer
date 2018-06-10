import schedule
import time
import urllib3
import html5lib
import smtplib
import configparser
from email.message import EmailMessage
from bs4 import BeautifulSoup

def job():
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	config = configparser.ConfigParser()
	config.read('xkcd_emailer.ini')
	smtp_server = config.get('Default', 'smtp_server')
	smtp_port = config.get('Default', 'smtp_port')
	sender_email = config.get('Default', 'sender_email')
	sender_password = config.get('Default', 'sender_password')
	receiver_email = config.get('Default', 'receiver_email')
	http = urllib3.PoolManager()
	req = http.request('GET', 'https://xkcd.com')
	page = req.data
	soup = BeautifulSoup(page, 'html5lib')
	img_src = soup.find('div', attrs={'id': 'comic'}).img['src']
	msg = EmailMessage()
	msg.set_content('https://www.xkcd.com' + img_src)
	msg['Subject'] = 'Your new xkcd email!'
	msg['From'] = 'Mailer'
	msg['To'] = receiver_email
	s = smtplib.SMTP(smtp_server, smtp_port)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(sender_email, sender_password)
	s.send_message(msg)
	s.quit()

schedule.every().monday.at("23:59").do(job)
schedule.every().wednesday.at("23:59").do(job)
schedule.every().friday.at("23:59").do(job)

while True:
	schedule.run_pending()
        #Sleep a minute
	time.sleep(60)
