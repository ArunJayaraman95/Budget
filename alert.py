
from tkinter import *
import re
import smtplib, ssl
import random, string


def alertSend_Email(to, subject, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "robiakther007@gmail.com"  # Enter your address
    receiver_email = to # Enter receiver address
    password = "ra101112"
    message = "Subject: """+subject+"\n"+message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        
        message = "expense is over and it needs to reduce expense."
        alertSend_Email(
        to='test@test.com',        # Receiver's email
        subject='Alerts',         # Subject of mail
        message=message )               # The message as you want to send
    