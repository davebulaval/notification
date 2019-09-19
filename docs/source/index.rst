.. Notification documentation master file, created by
    sphinx-quickstart on Sat Feb 17 12:19:43 2019.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

:github_url: https://github.com/davebulaval/notification

.. meta::
   :description: Notif is a package to send notification from a python script.
   :keywords: notification, python
   :author: David Beauchemin

Notif - The notification package
=====================================

Notif is a easy to use package to send notification from a python script.

Use this package to send during or at the end of a python script a
    - Slack notification
    - email notification
    - Channel notification
    - Facebook messenger notification.

.. warning:: Please be careful with your login credential. Use a .env or any other file not publish by your git (configured in .gitignore). Read the `following <https://stackoverflow.com/questions/2397822/what-is-the-best-practice-for-dealing-with-passwords-in-git-repositories/>`_ for best pratices

Installation
============

.. code-block:: sh

   pip install notif

API Reference
=============

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   notificator
   decorator