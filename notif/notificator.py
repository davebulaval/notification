import json
from email.policy import SMTP

import requests

try:
    from fbchat import Client, Message, ThreadType
except ImportError:
    Client = None
    Message = None
    ThreadType = None

try:
    from notify_run import Notify as ChannelNotify
except ImportError:
    ChannelNotify = None


class SlackNotificator:
    # pylint: disable=line-too-long
    """
    Notificator to send a notification into a Slack channel.

    Args:

        webhook_url (str): a webhook url given by Slack to post content into a channel. See `here <https://api.slack.com/incoming-webhooks>`_ for more detail.

    Attributes:

        webhook_url (str): The webhook url to push notification to.
        headers (dict): The headers of the notification.

    Example:

    .. code-block:: python

        notif = SlackNotificator(url="webhook_url")
        notif.send_notification("The script is finish")

    """

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.headers = {'content-type': 'application/json'}

    def send_notification(self, message: str) -> None:
        """
        Send a notificiation message to the webhook url.

        Args:
            message (str): The message to send as a notification message to the webhook url.

        """
        payload_message = {"text": message}

        requests.post(self.webhook_url, data=json.dumps(payload_message), headers=self.headers)


class EmailNotificator:
    # pylint: disable=line-too-long
    """
    Notificator to send a notification email.

    Args:

        sender_email (str): The email of the sender.
        sender_login_credential (str): The login credential of the sender email.
        destination_email (str): The recipient of  the email, can be the same as the sender_email.
        smtp_server (SMTP): The smtp server to relay the email.

    Attributes:

        sender_email (str): The email of the sender.
        sender_login_credential (str): The login credential of the sender.
        destination_email (str): The email of the recipient of the notification.
        smtp_server (SMTP): The smtp server.

    Example:

        Using gmail server::

                sender_email = "my_email"
                sender_login_credential = "my_password"
                destination_email = sender_email
                smtp_server = smtplib.SMTP('smtp.gmail.com',587)

                notif = EmailNotificator(sender_email, sender_login_credential,
                                               destination_email, smtp_server)
                notif.send_notification(subject="subject", text="text")

        Using hotmail server::

                sender_email = "my_email"
                sender_login_credential = "my_password"
                destination_email = "other_email"
                smtp_server = smtplib.SMTP('smtp.live.com',587)

                notif = EmailNotificator(sender_email, sender_login_credential,
                                               destination_email, smtp_server)
                notif.send_notification(subject="subject", text="text")

    """

    def __init__(self, sender_email: str, sender_login_credential: str, destination_email: str, smtp_server: SMTP):
        self.sender_email = sender_email
        self.sender_login_credential = sender_login_credential
        self.destination_email = destination_email
        self.smtp_server = smtp_server

    def send_notification(self, subject, text):
        """
        Send a notificiation message to the destination email.

        Args:

            subject (str): The subject to been show in the email.
            text (str): The text of the email.

        """
        self.smtp_server.ehlo()
        self.smtp_server.starttls()

        self.smtp_server.login(self.sender_email, self.sender_login_credential)

        content = 'Subject: %s\n\n%s' % (subject, text)
        self.smtp_server.sendmail(self.sender_email, self.destination_email, content)

        self.smtp_server.close()


class ChannelNotificator:
    # pylint: disable=line-too-long
    """
    Wrapper notif around notify_run to send a notification to a phone or a desktop. Can have multiple devices in
    the channel.

    Args:

        channel_url (str): A channel_rul created on `notify.run <https://notify.run/>`

    Attributes:

        notifier (Notify): A notify object to send notification.

    Example:

        .. code-block:: python

            notif = Notify(endpoint="https://notify.run/some_channel_id")
            notif.send_notification('Hi there!')

    """

    def __init__(self, channel_url: str):
        if ChannelNotify is None:
            raise ImportError("notify_run need to be installed to use this class.")
        self.notifier = ChannelNotify(endpoint=channel_url)

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to the channel.

        Args:
            message (str): The message to send as a notification message to the channel.

        """
        self.notifier.send(message)


class FacebookMessengerNotificator:
    # pylint: disable=line-too-long
    """
    Wrapper notif around fbchat to send a notification threw Facebook messenger to yourself.

    Args:

        email_logging (str): Your email to login into Facebook.
        logging_credential (str): Your login credential to login into Facebook.

    Attributes:

        fb_client (Client): A fbchat client

    Example:

        .. code-block:: python

            notif = Client('email', 'password')
            notif.send_notification(text="test")

    """

    def __init__(self, email_logging: str, logging_credential: str):
        if Client is None:
            raise ImportError("fbchat need to be installed to use this class.")
        self.fb_client = Client(email_logging, logging_credential)

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to your Facebook messenger.

        Args:
            message (str): The message to send as a notification message to your Facebook messenger.

        """
        self.fb_client.send(Message(text=message), thread_id=self.fb_client.uid, thread_type=ThreadType.USER)

    def __del__(self):
        self.fb_client.logout()
