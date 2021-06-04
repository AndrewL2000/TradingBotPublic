import os
import smtplib
from tickerClass import _tickerClass

#EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
#EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

EMAIL_ADDRESS = 'luzerker@gmail.com'
EMAIL_PASSWORD = 'ctzwayofspjrruhb'
EMAIL_RECEIVE = 'martinle.au@gmail.com'

def sendEmail(time_msg, ticker, tradePrice):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()     # Identifies us with the mail server (i.e. gmail)
        smtp.starttls() # Encrypt msg traffic
        smtp.ehlo()     # Reidentify us as an encrypted connection

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject  = '[' + ticker.tickerName + '] Trade Notification'
        body =  f"[{ticker.tickerName} ({ticker.resolution})]\n {str(time_msg)} at price {tradePrice}"

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS, 'buyhighselllow123@gmail.com', msg)  
        #smtp.sendmail(EMAIL_ADDRESS, 'martinlespam00@gmail.com', msg)  
        print(f"Sent Email for {ticker.tickerName} at price ${tradePrice}")

        # martinlespam00@gmail.com
        # benedictlu@hotmail.com
        # martinle.au@gmail.com
        # richiekim501@gmail.com