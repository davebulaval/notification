.. Notification documentation master file, created by
    sphinx-quickstart on Sat Feb 17 12:19:43 2019.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

:github_url: https://github.com/davebulaval/notification

.. meta::
   :description: Notif is a easy to use package to send notification from a python script.
   :keywords: notification, python
   :author: David Beauchemin

Notif - The notification package for every python project
=========================================================

Notif is a easy to use package to send notification from a python script.

Use this package to send during, at the end or when failing of a python script a

    - Slack notification,
    - Email notification,
    - Channel notification,
    - Microsoft Teams notification,
    - Discord.

Notif is compatible with the latest version of **Python >= 3.6**.

.. warning:: Please be careful with your login credential. Use a .env or any other file not publish by your git (configured in .gitignore). Read the `following <https://stackoverflow.com/questions/2397822/what-is-the-best-practice-for-dealing-with-passwords-in-git-repositories/>`_ for best practices.

Installation
============

Install the stable version of notif:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   pip install notif


Install the latest version of notif:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    pip install -U git+https://github.com/davebulaval/notification.git

Cite
^^^^

Use the following for the package citation;

.. code-block:: bib

    @misc{notif,
        title={{Notif - The Notification Package}},
        author={David Beauchemin},
        year={2019},
        note   = {\url{https://notificationdoc.ca/}}
    }

License
^^^^^^^
Notif is LGPLv3 licensed, as found in the `LICENSE file <https://github.com/davebulaval/notification/blob/master/LICENSE>`_.


API Reference
-------------

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   notificator
   decorator
