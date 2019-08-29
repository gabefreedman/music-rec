#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText


def get_user_and_pass():
    with open('login.txt', 'r') as file:
        contents = file.readlines()
        contents = [line.rstrip() for line in contents]
        return contents


def send_email():
    auth = get_user_and_pass()
    sender = auth[0]
    password = auth[1]
    receiver = 'gfreedman2108@comcast.net'
    msg = MIMEText('This is a test message. Please work...')
    msg['Subject'] = 'Test message'
    msg['To'] = receiver
    msg['From'] = sender

    server = smtplib.SMTP_SSL('smtp.comcast.net')
    server.login(sender, password)

    server.sendmail(sender, [receiver], msg.as_string())
    server.quit()
