import json
import warnings
from abc import ABC, abstractmethod
from email.policy import SMTP
from smtplib import SMTPRecipientsRefused
from time import sleep

try:
    import requests
except ImportError:
    requests = None

try:
    from fbchat import Client, Message, ThreadType, FBchatException
except ImportError:
    Client = None
    Message = None
    ThreadType = None

try:
    from notify_run import Notify as ChannelNotify
except ImportError:
    ChannelNotify = None

try:
    import pymsteams
except ImportError:
    pymsteams = None


class Notification(ABC):
    # pylint: disable=line-too-long
    """
    Abstract class to define a notification. Force implementation of method `send_notification` and specify how to send
    a notification error.

    Args:

        on_error_sleep_time (int): When an error occurs for the sending of the notification, it will wait this time to
            retry one more time. Time is in seconds.
    """

    def __init__(self, on_error_sleep_time: int):
        self.on_error_sleep_time = on_error_sleep_time

    @abstractmethod
    def send_notification(self, message: str) -> None:
        """
        Abstract method to send a notification.

        Args:
            message (str): The message to send as a notification message through the notificator.
        """
        pass

    def send_notification_error(self, error: Exception) -> None:
        """
        Send a notification error message through the notificator, used with the wrapper.


        Args:
            error (Exception): The exception raised during the script execution.
        """
        notification_error_message = self._parse_error(error)
        self.send_notification(message=notification_error_message)

    @staticmethod
    def _parse_error(error: Exception) -> str:
        """
        Format the error into a readable text.

        Args:
            error (Exception): The exception raised during the script execution.

        Returns:
            A formatted string base on the error message and error type.
        """
        error_type = type(error)
        error_message = error.args[0]

        formatted_error_message = "An error of type {} occurred. An the error message is {}".format(
            error_type, error_message)

        return formatted_error_message


class SlackNotificator(Notification):
    # pylint: disable=line-too-long
    """
    Notificator to send a notification into a Slack channel.

    Args:

        webhook_url (str): a webhook url given by Slack to post content into a channel. See
            `here <https://api.slack.com/incoming-webhooks>`_ for more detail.
        on_error_sleep_time (int): When an error occurs for the sending of the notification, it will wait this time to
            retry one more time. Time is in seconds.
            (Default value = 300)

    Attributes:

        webhook_url (str): The webhook url to push notification to.
        headers (dict): The headers of the notification.

    Example:

    .. code-block:: python

        notif = SlackNotificator(webhook_url="webhook_url")
        notif.send_notification("The script is finish")

    """

    def __init__(self, webhook_url: str, on_error_sleep_time: int = 300):
        super().__init__(on_error_sleep_time)
        if requests is None:
            raise ImportError("package requests need to be installed to use this class.")
        self.webhook_url = webhook_url
        self.headers = {'content-type': 'application/json'}

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to the webhook url.

        Args:
            message (str): The message to send as a notification message to the webhook url.

        """
        payload_message = {"text": message}
        try:
            requests.post(self.webhook_url, data=json.dumps(payload_message), headers=self.headers)
        except requests.exceptions.HTTPError:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                requests.post(self.webhook_url, data=json.dumps(payload_message), headers=self.headers)
            except requests.exceptions.HTTPError:
                warnings.warn("Second error when trying to send notification, will abort.", Warning)
                pass


class EmailNotificator(Notification):
    # pylint: disable=line-too-long
    """
    Notificator to send a notification email.

    Args:

        sender_email (str): The email of the sender.
        sender_login_credential (str): The login credential of the sender email.
        destination_email (str): The recipient of the email can be the same as the sender_email.
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
                notif.send_notification(message="text")

        Using hotmail server::

                sender_email = "my_email"
                sender_login_credential = "my_password"
                destination_email = "other_email"
                smtp_server = smtplib.SMTP('smtp.live.com',587)

                notif = EmailNotificator(sender_email, sender_login_credential,
                                               destination_email, smtp_server)
                notif.send_notification(message="text")

    """

    def __init__(self, sender_email: str, sender_login_credential: str, destination_email: str, smtp_server: SMTP,
                 on_error_sleep_time: int):
        # pylint: disable=too-many-arguments
        super().__init__(on_error_sleep_time)
        self.sender_email = sender_email
        self.sender_login_credential = sender_login_credential
        self.destination_email = destination_email
        self.smtp_server = smtp_server

        self._validate_login_credential()

    def send_notification(self, message: str):
        """
        Send a notification message to the destination email.

        Args:

            message (str): The message of the email.

        """

        self.smtp_server.helo()
        self.smtp_server.starttls()

        self.smtp_server.login(self.sender_email, self.sender_login_credential)

        subject = "Python script notification email"
        content = 'Subject: %s\n\n%s' % (subject, message)

        self.smtp_server.sendmail(self.sender_email, self.destination_email, content)

        try:
            self.smtp_server.sendmail(self.sender_email, self.destination_email, content)
        except SMTPRecipientsRefused:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                self.smtp_server.sendmail(self.sender_email, self.destination_email, content)
            except SMTPRecipientsRefused:
                warnings.warn("Second error when trying to send notification, will abort.", Warning)
                pass
        finally:
            self.smtp_server.close()

    def _validate_login_credential(self):
        self.smtp_server.helo()
        self.smtp_server.starttls()

        self.smtp_server.login(self.sender_email, self.sender_login_credential)


class ChannelNotificator(Notification):
    # pylint: disable=line-too-long
    """
    Wrapper around notify_run to send a notification to a phone or a desktop. Can have multiple devices in
    the channel.

    Args:

        channel_url (str): A channel_rul created on `notify.run <https://notify.run/>`

    Attributes:

        notifier (Notify): A notify object to send notification.

    Example:

        .. code-block:: python

            notif = ChannelNotificator(endpoint="https://notify.run/some_channel_id")
            notif.send_notification('Hi there!')

    """

    def __init__(self, channel_url: str, on_error_sleep_time: int):
        super().__init__(on_error_sleep_time)
        if ChannelNotify is None:
            raise ImportError("package notify_run need to be installed to use this class.")
        self.notifier = ChannelNotify(endpoint=channel_url)

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to the channel.

        Args:
            message (str): The message to send as a notification message to the channel.

        """
        try:
            self.notifier.send(message)
        except requests.exceptions.HTTPError:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                self.notifier.send(message)
            except requests.exceptions.HTTPError:
                warnings.warn("Second error when trying to send notification, will abort.", Warning)
                pass


class FacebookMessengerNotificator(Notification):
    # pylint: disable=line-too-long
    """
    Wrapper around fbchat to send a notification through Facebook messenger to yourself.

    Args:

        email_logging (str): Your email to login into Facebook.
        logging_credential (str): Your login credential to login into Facebook.

    Attributes:

        fb_client (Client): A fbchat client

    Example:

        .. code-block:: python

            notif = FacebookMessengerNotificator('email', 'password')
            notif.send_notification(message="test")

    """

    def __init__(self, email_logging: str, logging_credential: str, on_error_sleep_time: int):
        super().__init__(on_error_sleep_time)
        if Client is None:
            raise ImportError("package fbchat need to be installed to use this class.")
        self.fb_client = Client(email_logging, logging_credential)

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to your Facebook messenger.

        Args:
            message (str): The message to send as a notification message to your Facebook messenger.

        """
        try:
            self.fb_client.send(Message(text=message), thread_id=self.fb_client.uid, thread_type=ThreadType.USER)
        except FBchatException:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                self.fb_client.send(Message(text=message), thread_id=self.fb_client.uid, thread_type=ThreadType.USER)
            except FBchatException:
                warnings.warn("Second error when trying to send notification, will abort.", Warning)
                pass

    def __del__(self):
        self.fb_client.logout()


class TeamsNotificator(Notification):
    # pylint: disable=line-too-long
    # pylint: disable=line-too-long
    """
    Notificator to send a notification into a Microsoft Teams channel.

    Args:

        webhook_url (str): A webhook url given by Microsoft Teams to post content into a channel. See
            `here <https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using>`_
            for more detail.

    Attributes:

        teams_hook (str): The webhook url to push notification to.

    Example:

    .. code-block:: python

        notif = TeamsNotificator(webhook_url="webhook_url")
        notif.send_notification("The script is finish")

    """

    def __init__(self, webhook_url: str, on_error_sleep_time: int):
        super().__init__(on_error_sleep_time)
        if pymsteams is None:
            raise ImportError("package pymsteams need to be installed to use this class.")
        self.teams_hook = pymsteams.connectorcard(webhook_url)

    def send_notification(self, message: str) -> None:
        """
        Send a notification message to the webhook url.

        Args:
            message (str): The message to send as a notification message to the webhook url.

        """
        self.teams_hook.text(message)
        try:
            self.teams_hook.send()
        except pymsteams.TeamsWebhookException:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                self.teams_hook.text(message)
            except FBchatException:
                warnings.warn("Second error when trying to send notification, will abort.", Warning)
                pass
