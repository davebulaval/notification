<div align="center">
    
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7cc518c9c5f54c4cab83930cba5f958d)](https://app.codacy.com/gh/davebulaval/notification?utm_source=github.com&utm_medium=referral&utm_content=davebulaval/notification&utm_campaign=Badge_Grade_Settings)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notif)](https://pypi.org/project/notif/)
[![PyPI Status](https://badge.fury.io/py/notif.svg)](https://badge.fury.io/py/notif)
[![PyPI Status](https://pepy.tech/badge/notif)](https://pepy.tech/project/notif)
[![Continuous Integration](https://github.com/davebulaval/notification/workflows/Continuous%20Integration/badge.svg)](https://github.com/davebulaval/notification/actions?query=workflow%3A%22Continuous+Integration%22+branch%3Amaster)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![codecov](https://codecov.io/gh/davebulaval/notification/branch/master/graph/badge.svg?token=43ARF9LF94)](https://codecov.io/gh/davebulaval/notification)
    
</div>

# Notif - The notification package for every python project

Notif is an easy-to-use package to send notification from a python script.

Use this package to send during, at the end or when failing of a python script a

    - Slack notification,
    - Email notification,
    - Channel notification,
    - Microsoft Teams notification,
    - Discord.
    
> Please be careful with your login credential. Use a .env or any other file not publish by your git (configured in .gitignore). Read the [following](https://stackoverflow.com/questions/2397822/what-is-the-best-practice-for-dealing-with-passwords-in-git-repositories) for best pratices.

    
Read the documentation at [notificationdoc.ca](https://notificationdoc.ca).

Notif is compatible with the latest version of __Python >= 3.6__.

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
Use the following for the package citation;
```
@misc{notif,
    title={{Notif - The Notification Package}},
    author={David Beauchemin},
    year={2019},
    note   = {\url{https://notificationdoc.ca/}}
}
```

### License
Notif is LGPLv3 licensed, as found in the [LICENSE file](https://github.com/davebulaval/notification/blob/master/LICENSE).

