
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