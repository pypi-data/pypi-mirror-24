# 3bot-hook

[![Build Status](https://travis-ci.org/3bot/3bot-hook.svg?branch=master)](https://travis-ci.org/3bot/3bot-hook)
[![Coverage Status](https://coveralls.io/repos/3bot/3bot-hook/badge.svg?branch=master&service=github)](https://coveralls.io/github/3bot/3bot-hook?branch=master)
[![PyPI](https://img.shields.io/pypi/v/threebot-hook.svg)](https://pypi.python.org/pypi/threebot-hook)


Webhook handler for 3bot workflow execution. Basically for Github and Bitbucket but works with other POST requests as well.


## Installation

### Stable version from PyPI

	pip install threebot-hook

### Development version

```sh
$ pip install -e git+https://github.com/3bot/3bot-hook.git#egg=theebot_hook
```

```python

'threebot_hook',
'rest_framework.authtoken',
```

```python
url(r'^hooks/', include('threebot_hook.urls')),
```

## Credits

This is an adopted and adapted version of S. Andrew Sheppard's [django-github-hook](https://github.com/sheppard/django-github-hook).
