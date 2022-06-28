import requests
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime

now = datetime.strftime(datetime.now(), '%m_%d_%H:%M')

URL = 'https://polygonscan.com/address/asdasdasdasd'

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
    gmail_user = 'Myemail'
    gmail_password = 'MyPassword.'

    sent_from = gmail_user
    to = ['myemail']
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
