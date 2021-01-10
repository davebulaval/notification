import json
import smtplib
import warnings
from abc import ABC, abstractmethod
from smtplib import SMTPRecipientsRefused
from time import sleep
from typing import Union

try:
    import requests
except ImportError:
    requests = None

try:
    from notify_run import Notify as ChannelNotify
except ImportError:
    ChannelNotify = None

try:
    import pymsteams
except ImportError:
    pymsteams = None


class Notificator(ABC):
    # pylint: disable=line-too-long
    """
    Abstract class to define a notificator. Force implementation of method `send_notification` and specify how to send
    a notification error.

    Args:

        on_error_sleep_time (int): When an error occurs for the sending of the notification, it will wait this time to
            retry one more time. Time is in seconds.
    """
    def __init__(self, on_error_sleep_time: int):
        self.on_error_sleep_time = on_error_sleep_time

    @abstractmethod
    def send_notification(self, message: str, subject: Union[str, None] = None) -> None:
        """
        Abstract method to send a notification.

        Args:

            message (str): The message to send as a notification message through the notificator.
            subject (str): The subject of the notification. If None, the default message is use. By default None.
        """

    def send_notification_error(self, error: Exception) -> None:
        """
        Send a notification error message through the notificator, used with the wrapper.

        Args:

            error (Exception): The exception raise during the script execution.
        """
        notification_error_message = self._parse_error(error)
        self.send_notification(message=notification_error_message)

    @abstractmethod
    def _format_subject(self, subject_message: str) -> str:
        """
        Abstract class to format a subject to create a 'title'.

        Args:

            subject_message (str): The message to format.

        Return:
            A formatted subject message.
        """

    @staticmethod
    def _parse_error(error: Exception) -> str:
        """
        Format the error into a readable text.

        Args:

            error (Exception): The exception raise during the script execution.

        Return:
            A formatted string base on the error message and error type.
        """
        error_type = type(error)
        error_message = error.args[0]

        formatted_error_message = "An error of type {} occurred. An the error message is {}".format(
            error_type, error_message)

        return formatted_error_message


class SlackNotificator(Notificator):
    # pylint: disable=line-too-long
    """
    Notificator to send a notification into a Slack channel.

    Args:

        webhook_url (str): a webhook URL given by Slack to post content into a channel. See
            `here <https://api.slack.com/incoming-webhooks>`_ for more detail.
        on_error_sleep_time (int): When an error occurs for the sending of a notification, it will wait this time
            (in seconds) to retry one more time. Default is 120 sec.

    Example:

    .. code-block:: python

        notif = SlackNotificator(webhook_url="webhook_url")
        notif.send_notification("The script is finish")

    """
    def __init__(self, webhook_url: str, on_error_sleep_time: int = 120):
        super().__init__(on_error_sleep_time)
        if requests is None:
            raise ImportError("package requests need to be installed to use this class.")
        self.webhook_url = webhook_url
        self.headers = {'content-type': 'application/json'}

        self.default_subject_message = "Python script Slack notification"

    def _format_subject(self, subject_message: str) -> str:
        """
        We use Markdown formatting as specified in Slack
        `documentation <https://api.slack.com/reference/surfaces/formatting>`_.
        """
        return f"*{subject_message}*\n"

    def send_notification(self, message: str, subject: Union[str, None] = None) -> None:
        """
        Send a notification message to the webhook URL.

        Args:

            message (str): The message to send as a notification message to the webhook URL.

            subject (str): The subject of the notification. If None, the default message
                'Python script Slack notification' is used. Note that the subject is formatted, the text is bolded and
                a new line is appended after the subject creates a 'title' effect. Default is None.


        """
        subject = subject if subject is not None else self.default_subject_message
        subject = self._format_subject(subject)
        message = subject + message

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
                warnings.warn("Second error when trying to send notification, will abort sending message.", Warning)


class EmailNotificator(Notificator):
    # pylint: disable=line-too-long
    """
    Notificator to send a notification email.

    Args:

        sender_email (str): The email of the sender.
        sender_login_credential (str): The login credential of the sender email.
        destination_email (str): The recipient of the email can be the same as the sender_email.
        smtp_server (smtplib.SMTP): The SMTP server to relay the email.
        on_error_sleep_time (int): When an error occurs for the sending of a notification, it will wait this time
            (in seconds) to retry one more time. Default is 120 sec.

    Examples:

        Using gmail server::

                sender_email = "my_email"
                sender_login_credential = "my_password"
                destination_email = sender_email
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)

                notif = EmailNotificator(sender_email, sender_login_credential,
                                               destination_email, smtp_server)
                notif.send_notification(message="text")


        Using hotmail server::

                sender_email = "my_email"
                sender_login_credential = "my_password"
                destination_email = "other_email"
                smtp_server = smtplib.SMTP('smtp.live.com', 587)

                notif = EmailNotificator(sender_email, sender_login_credential,
                                               destination_email, smtp_server)
                notif.send_notification(message="text")

    """
    def __init__(self,
                 sender_email: str,
                 sender_login_credential: str,
                 destination_email: str,
                 smtp_server: smtplib.SMTP,
                 on_error_sleep_time: int = 120) -> None:
        # pylint: disable=too-many-arguments
        super().__init__(on_error_sleep_time)
        self.sender_email = sender_email
        self.destination_email = destination_email
        self.smtp_server = smtp_server

        # login and TTLS connection
        self.smtp_server.starttls()
        self.smtp_server.login(self.sender_email, sender_login_credential)

        self.default_subject_message = "Python script notification email"

    def _format_subject(self, subject_message: str) -> str:
        """
        None since subject is the subject of the email.
        """
        pass

    def send_notification(self, message: str, subject: Union[str, None] = None) -> None:
        """
        Send a notification message to the destination email.

        Args:

            message (str): The message of the email.
            subject (str): The subject of the email. If None, the default message 'Python script notification email'
                is used. Default is None.

        """
        subject = subject if subject is not None else self.default_subject_message
        content = 'Subject: %s\n\n%s' % (subject, message)

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
                warnings.warn("Second error when trying to send notification, will abort sending message.", Warning)

    def __del__(self):
        self.smtp_server.quit()


class ChannelNotificator(Notificator):
    # pylint: disable=line-too-long
    """
    Wrapper around notify_run to send a notification to a phone or a desktop. Can have multiple devices in
    the channel.

    Args:

        channel_url (str): A channel_rul created on `notify.run <https://notify.run/>`.
        on_error_sleep_time (int): When an error occurs for the sending of a notification, it will wait this time
            (in seconds) to retry one more time. Default is 120 sec.

    Example:

        .. code-block:: python

            notif = ChannelNotificator(channel_url="https://notify.run/some_channel_id")
            notif.send_notification('Hi there!')

    """
    def __init__(self, channel_url: str, on_error_sleep_time: int = 120) -> None:
        super().__init__(on_error_sleep_time)
        if ChannelNotify is None:
            raise ImportError("package notify_run need to be installed to use this class.")
        self.notifier = ChannelNotify(endpoint=channel_url)

        self.default_subject_message = "Python script notification"

    def _format_subject(self, subject_message: str) -> str:
        """
        We use a similar logic as Markdown formatting as specified to highlight the subject.
        """
        return f"**{subject_message}**\n"

    def send_notification(self, message: str, subject: Union[str, None] = None) -> None:
        """
        Send a notification message to the channel.

        Args:

            message (str): The message to send as a notification message to the channel.
            subject (str): The subject of the notification. If None, the default message
                'Python script notification' is used. Note that subject are formatted, the text is surrounded with '*'
                and a new line is appended after the subject creates a 'title' effect. Default is None.

        """
        subject = subject if subject is not None else self.default_subject_message
        subject = self._format_subject(subject)
        message = subject + message
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
                warnings.warn("Second error when trying to send notification, will abort sending message.", Warning)


class TeamsNotificator(Notificator):
    # pylint: disable=line-too-long
    """
    Notificator to send a notification into a Microsoft Teams channel.

    Args:

        webhook_url (str): A webhook URL given by Microsoft Teams to post content into a channel. See
            `this <https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using>`_
            for more detail.
        on_error_sleep_time (int): When an error occurs for the sending of a notification, it will wait this time
            (in seconds) to retry one more time. Default is 120 sec.

    Example:

    .. code-block:: python

        notif = TeamsNotificator(webhook_url="webhook_url")
        notif.send_notification("The script is finish")

    """
    def __init__(self, webhook_url: str, on_error_sleep_time: int = 120):
        super().__init__(on_error_sleep_time)
        if pymsteams is None:
            raise ImportError("package pymsteams need to be installed to use this class.")
        self.teams_hook = pymsteams.connectorcard(webhook_url)

        self.default_subject_message = "Python script Teams notification"

    def _format_subject(self, subject_message: str) -> str:
        """
        We use a similar logic as Markdown formatting as specified in Microsoft Teams
        `documentation <https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cconnector-html>`_.
        """
        return f"**{subject_message}**\n"

    def send_notification(self, message: str, subject: Union[str, None] = None) -> None:
        # pylint: disable=line-too-long
        """
        Send a notification message to the webhook URL.

        Args:

            message (str): The message to send as a notification message to the webhook URL.
            subject (str): The subject of the notification. If None, the default message
                'Python script Teams notification' is used. Note that the subject is formatted, the text is bolded,
                and a new line is appended after the subject creates a 'title' effect. Default is None.

        """
        subject = subject if subject is not None else self.default_subject_message
        subject = self._format_subject(subject)
        message = subject + message

        self.teams_hook.text(message)
        try:
            self.teams_hook.send()
        except pymsteams.TeamsWebhookException:
            warnings.warn(
                "Error when trying to send notification. Will retry in {} seconds.".format(self.on_error_sleep_time),
                Warning)
            sleep(self.on_error_sleep_time)
            try:
                self.teams_hook.send()
            except pymsteams.TeamsWebhookException:
                warnings.warn("Second error when trying to send notification, will abort sending message.", Warning)
