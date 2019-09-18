import json
from email.policy import SMTP

import requests


class SlackNotificator:
    """

    """

    def __init__(self, url: str):
        self.url = url
        self.headers = {'content-type': 'application/json'}

    def send_notification(self, message):
        payload_message = {"text": message}

        requests.post(self.url, data=json.dumps(payload_message), headers=self.headers)


class EmailNotificator:
    """

    """

    def __init__(self, sender_email: str, sender_login_credential: str, destination_email: str,
                 smtp_server: SMTP):
        self.sender_email = sender_email
        self.sender_login_credential = sender_login_credential
        self.destination_email = destination_email
        self.smtp_server = smtp_server

    def send_notification(self, subject, text):
        self.smtp_server.ehlo()
        self.smtp_server.starttls()

        self.smtp_server.login(self.sender_email, self.sender_login_credential)

        content = 'Subject: %s\n\n%s' % (subject, text)
        self.smtp_server.sendmail(self.sender_email, self.destination_email, content)

        self.smtp_server.close()
