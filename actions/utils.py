import random
import re
from typing import Text


def to_snake_case(name):
    string = re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', name).strip().replace(' ', '_')
    return ''.join(string.lower())


import logging
import os
import smtplib
import traceback
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def send_email(subject:Text, recipient_email:Text, otp: Text, content: Text):
    try:
        message_data = EmailMessage()
        message_data["Subject"] = subject
        username = os.environ["EMAIL"]
        password = os.environ["PASS"]
        message_data["From"] = username
        message_data["To"] = recipient_email
        message_data.add_alternative(content.format(otp=otp), subtype="html")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(message_data)
        return True
    except Exception as error:
        logger.error(f"Error: {error}")
        logger.info(traceback.print_exc())
        return False


def get_html_data(filepath:str):
    with open(filepath, "r") as html_data:
        return html_data.read()


def generate_otp():
    return random.randint(0000, 9999)