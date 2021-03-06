[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notif)](https://pypi.org/project/notif/)
[![PyPI Status](https://badge.fury.io/py/notif.svg)](https://badge.fury.io/py/notif)
[![PyPI Status](https://pepy.tech/badge/notif)](https://pepy.tech/project/notif)
[![Continuous Integration](https://github.com/davebulaval/notification/workflows/Continuous%20Integration/badge.svg)](https://github.com/davebulaval/notification/actions?query=workflow%3A%22Continuous+Integration%22+branch%3Amaster)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

# Notif - The notification package for every python project

Notif is a easy to use package to send notification from a python script.

Use this package to send during, at the end or when failing of a python script a

    - Slack notification
    - Email notification
    - Channel notification
    - Microsoft Teams notification.
    
> Please be careful with your login credential. Use a .env or any other file not publish by your git (configured in .gitignore). Read the [following](https://stackoverflow.com/questions/2397822/what-is-the-best-practice-for-dealing-with-passwords-in-git-repositories) for best pratices.

    
Read the documentation at [notificationdoc.ca](https://notificationdoc.ca).

Notif is compatible with the __latest version of PyTorch__ and  __Python >= 3.6__.

---------

## Installation

- **Install the stable version of notif:**

```shell script
pip install notif
```

- **Install the latest version of notif:**

```shell script
pip install -U git+https://github.com/davebulaval/notification.git
```

### Cite
Use the following for the article;
```
@misc{notif,
    title={{Notif - The notification package}},
    author={David Beauchemin},
    year={2019},
    note   = {\url{https://notificationdoc.ca/}}
}
```
