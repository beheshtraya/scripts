# -*- coding: utf-8 -*-
import smtplib

SMTP_SERVER = 'smtp.chmail.ir'
SMTP_PORT = 465 #25
EMAIL_SENDER = 'test.project@chmail.ir'
EMAIL_PASSWORD = '123qweASD'


def send_email(email_addr):
    server = SMTP_SERVER
    port = SMTP_PORT
    sender = EMAIL_SENDER

    recipient = email_addr
    subject = 'Subject'
    body = 'Body'
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)


    ### for some mail server these options may required.

    ##session = smtplib.SMTP(server, port)
    ##session.ehlo()
    ##session.starttls()
    ##session.ehlo

    mail_server = smtplib.SMTP_SSL()
    mail_server.connect(server, port)
    mail_server.login(sender, EMAIL_PASSWORD)

    mail_server.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    print "sent"
    mail_server.quit()


send_email('beheshtraya@gmail.com')
