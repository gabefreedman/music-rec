#!/usr/bin/env python

"""This module defines functions for creating, authenticating,
and sending an email via SMTP containing tabular data. The
credentials for the sending email address should be stored in
a file 'login.txt'.

"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_user_and_pass():
    """Retrieve email login credentials from .txt file

    This function reads a specifically formatted .txt file
    to parse out user and pass of certain email address.
    This file must be created ahead of time before running
    this function.

    Parameters
    ----------

    Returns
    -------
    contents : list of str
        Contains email login credentials as [user, pass]

    """
    with open('login.txt', 'r') as file:
        contents = file.readlines()
        contents = [line.rstrip() for line in contents]
        return contents


def send_email(data):
    """Send email via SMTP containing input DataFrame.

    Sending address is authenticated using get_user_and_pass
    function. Receiving address must be defined in function.
    Body of email is brief message and tabular data parsed
    from input DataFrame.

    Parameters
    ----------
    data : DataFrame
        Tabular data to be written to html then sent
        via email.

    Returns
    -------

    """
    auth = get_user_and_pass()
    sender = auth[0]
    password = auth[1]
    receiver = 'gfreedman2108@comcast.net'
    msg = MIMEMultipart()
    msg['Subject'] = 'New music from last week'
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
