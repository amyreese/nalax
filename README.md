# nalax

nginx analytics

[![version](https://img.shields.io/pypi/v/nalax.svg)](https://pypi.org/project/nalax)
[![license](https://img.shields.io/pypi/l/nalax.svg)](https://github.com/amyreese/nalax/blob/main/LICENSE)

Install
-------

```shell-session
$ pip install nalax
```

Nginx Logging
-------------

Enabling logging in nalax format:

```
http {
    log_format nalax escape=json '{'
        '"time": "$time_iso8601", '
        '"host": "$http_host", '
        '"method": "$request_method", '
        '"uri": "$request_uri", '
        '"status": "$status", '
        '"referrer": "$http_referrer", '
        '"remote": "$remote_addr", '
        '"agent": "$http_user_agent"'
        '}';

    access_log /opt/homebrew/var/log/nginx/access.nalax.json nalax;
}
```

License
-------

nalax is copyright Amethyst Reese, and licensed under the MIT license.