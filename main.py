# load email and password from .env.local file
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from posixpath import basename
from dotenv import load_dotenv

from get_elsys_team import Teams
load_dotenv('.env.local')

import os
EMAIL = os.getenv('EMAIL')
PASS = os.getenv('PASS')
TEAMS_NUM = 63

SUBJECT = "Сертификати за участие в HackTUES 9"

BODY = """
Здравейте,

Радваме се, че участвахте в тазгодишното издание на HackTUES - HackTUES Security. Ето и вашите грамоти за участие :)

Поздрави,
Екипът на HackTUES 9
"""

# functions for email - send email & attach files

import smtplib
from email.mime.text import MIMEText
from get_elsys_team import *

class EmailSender:
    def __init__(self):
        self.server = None
        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.login(EMAIL, PASS)
        except Exception as e:
            print(e)
            exit(-1)


    def send_email_with_attachments(self, subject, body, to, files=[]):
        print(f"[SENDING] Email to \"{to}\" with {len(files)} attachments")

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        for file in files:
            with open(file, "rb") as f:
                part = MIMEApplication(f.read(), Name=basename(file))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
            msg.attach(part)

        self.server.sendmail(EMAIL, to, msg.as_string())
            

    def get_recipients_string(self, emails):
        recipients = ""
        for email in emails:
            recipients += email[0] + ", "
        recipients = recipients[:-2]
        return recipients

    def send_emails (self):
        TESTMAILS = [("kaloyan.s.doychinov.2019@elsys-bg.org", "Калоян Дойчинов"), ("kokolia1070@gmail.com", "Калоян Дойчинов Две")]
        self.send_email_with_attachments(SUBJECT, BODY, self.get_recipients_string(TESTMAILS), ["certificates/Християн Тодоров.png", "certificates/Филостратос Титопулос.png"])
        # for i in range(TEAMS_NUM):
        #     print(f"[SENDING] Email to team {i+1}")
        #     send_email(f"Сертификати за участие", BODY, emails[i][0][0])

    def print_emails(self):
        db = Teams()

        for i in range(TEAMS_NUM):
            print(f"[SENDING] Email to team {i+1}")
            print(db.get_team_emails(i+1))

    def close(self):
        self.server.quit()


# main.py

def __main__():
    email_sender = EmailSender()
    try:
        email_sender.print_emails()

    except Exception as e:
        print(e)
        email_sender.close()

    try:
        email_sender.send_emails()
    except Exception as e:
        print(e)
        email_sender.close()

    email_sender.close()

if __name__ == "__main__":
    __main__()
        