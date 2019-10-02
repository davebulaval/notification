.. role:: hidden
    :class: hidden-section

Decorator
=========

Since script can often fail, it's convenient to have a notification. The fail decorator attend to catch any exception and send a notification threw the notificator.

.. currentmodule:: notif.fail_decorator

Fail Decorator
--------------

.. autofunction:: notification_on_fail

Notificator & Sacred
--------------------

Unfortunately the `fail decorator` is not working with the package (yet) with the `Sacred <https://pypi.org/project/sacred/>`_ package.

