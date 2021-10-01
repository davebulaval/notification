# pylint: disable=W0702, inconsistent-return-statements
import sys
import traceback


def notification_on_fail(notificator, verbose_level=3):
    # pylint: disable=line-too-long
    """
    Decorator to wrap a function to track if the script fail and push notification to a previously set notif.
    Mostly inspire from the `Fabric 1.1 <https://github.com/fabric/fabric/tree/1.10>`_ wrapper.

    Args:

        notificator (Notificator): The notif to push notification threw.
        verbose_level (int) or (str): The verbose level of the notification message, 1 been the lesser and 3 the maximum
        of verbosity.

    Returns:
        A wrapped function which will catch if an error occur and send a notification through the notificator.

    Example:

        .. code-block:: python

            notif = SlackNotificator(url="webhook_url")

            @notification_on_fail(notif=notif, verbose_level='2')
            def fail_test():
                print(t)

    """
    def wrapper(func):
        def decorated(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                exception_type, value, _ = sys.exc_info()
                verbose = str(verbose_level)
                if verbose == '1':
                    message = "An error occurred of type {} when running the script.".format(exception_type)
                elif verbose == '2':
                    message = "An error occurred when running the script. The error message is: {}".format(value)
                else:
                    message = traceback.format_exc()
                notificator.send_notification(message=message)

        return decorated

    return wrapper
