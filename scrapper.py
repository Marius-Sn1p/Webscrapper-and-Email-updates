import requests
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime

now = datetime.strftime(datetime.now(), '%m_%d_%H:%M')

URL = 'https://polygonscan.com/address/0xbfd23d88e04ace72ae863151c0ccedd986ae34eb'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

converted_balance=0

def check_balance():

    global previous_balance, converted_balance
    
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    previous_balance = converted_balance

    matic_balance= soup.find(class_="col-md-8").get_text()

    converted_balance = float(matic_balance[0:3])
    
    
    with open("balance.txt", 'a') as updater:
        updater.write(now +' '+ matic_balance + '\n')
        updater.close()
        print('updated')
    
    if converted_balance > previous_balance:
        send_email()
    

def send_email():
    gmail_user = 'mypythonchecker@gmail.com'
    gmail_password = 'Skersys7.'

    sent_from = gmail_user
    to = ['marius.skersys1@gmail.com']
    subject= 'Woohoo'
    body = 'Your Matic Balance increased'

    email_text = f"Subject: {subject}\n\n{body}"

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


while True:
    check_balance()
    time.sleep(21600)
