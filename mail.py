#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_user_and_pass():
    with open('login.txt', 'r') as file:
        contents = file.readlines()
        contents = [line.rstrip() for line in contents]
        return contents


def send_email(data):
    auth = get_user_and_pass()
    sender = auth[0]
    password = auth[1]
    receiver = 'gfreedman2108@comcast.net'
    msg = MIMEMultipart()
    msg['Subject'] = 'Test message'
    msg['To'] = receiver
    msg['From'] = sender

    html = """\
    <html>
      <head></head>
      <body>
        Happy Monday! Here's a list of recently released music from the past week.
        
        {0}
      </body>
    </html>
    """.format(data.to_html())

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP_SSL('smtp.comcast.net')
    server.login(sender, password)

    server.sendmail(sender, [receiver], msg.as_string())
    server.quit()
