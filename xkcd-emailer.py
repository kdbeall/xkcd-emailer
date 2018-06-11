#!/usr/bin/python3

""" A simple program to email xkcd comics to yourself. """

import schedule
import time
import urllib3
import smtplib
import configparser
from email.message import EmailMessage
from bs4 import BeautifulSoup


def fetch_comic_img():
    """ Fetch the src of the image on the xkcd home page. """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    req = http.request('GET', 'https://xkcd.com')
    page = req.data
    soup = BeautifulSoup(page, 'html5lib')
    img_src = soup.find('div', attrs={'id': 'comic'}).img['src']
    return img_src


def send_email(img_src):
    """ Read the config file and send the email. """
    config = configparser.ConfigParser()
    config.read('xkcd-emailer.ini')
    smtp_server = config.get('Default', 'smtp_server')
    smtp_port = config.get('Default', 'smtp_port')
    sender_email = config.get('Default', 'sender_email')
    sender_password = config.get('Default', 'sender_password')
    receiver_email = config.get('Default', 'receiver_email')
    msg = EmailMessage()
    msg.set_content('https://www.xkcd.com' + img_src)
    msg['Subject'] = 'Your new xkcd email!'
    msg['From'] = 'XkcdMailer'
    msg['To'] = receiver_email
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.starttls()
    s.login(sender_email, sender_password)
    s.send_message(msg)
    s.quit()


def job():
    img_src = fetch_comic_img()
    send_email(img_src)


schedule.every().monday.at("23:59").do(job)
schedule.every().wednesday.at("23:59").do(job)
schedule.every().friday.at("23:59").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
