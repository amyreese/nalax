# Nalax

No-nonsense access log analytics experiment

[![version](https://img.shields.io/pypi/v/nalax.svg)](https://pypi.org/project/nalax)
[![license](https://img.shields.io/pypi/l/nalax.svg)](https://github.com/amyreese/nalax/blob/main/LICENSE)

Nalax provides minimal, privacy-preserving analytics based on webserver access
logs, without retaining or cataloguing private user data.

Nalax aggregates the following data, and nothing more:

- timestamp
- URL (hostname and path, without parameters or query strings)
- HTTP method (get/post/etc)
- HTTP status (200, 404, etc)
- user country
- broad device categories:
  - form factor (mobile or desktop)
  - OS brand (Android, iOS, Linux, macOS, or Windows)
  - browser brand (Chrome, Edge, Firefox, Safari)
  - connection type (IPv4 or IPv6)

Any personally identifiable information (including IP address, OS or browser
version, and user agent string) is immediately categorized, discarded, and
never logged.

Note: Nalax cannot understand if URL paths contain PII, and assumes that PII
will only be part of (discarded) query strings. It is up to the user to ensure
that PII in URL paths are appropriately anonymized before ingesting into
Nalax's database.


Install
-------

```shell-session
$ pip install nalax
```

### Nginx Logging

```
# nginx.conf

http {
    log_format nalax escape=json '{'
        '"time": "$time_iso8601", '
        '"host": "$http_host", '
        '"method": "$request_method", '
        '"uri": "$request_uri", '
        '"status": "$status", '
        '"remote": "$remote_addr", '
        '"agent": "$http_user_agent"'
        '}';

    access_log /opt/homebrew/var/log/nginx/access.nalax.json nalax;
}
```

License
-------

nalax is copyright Amethyst Reese, and licensed under the MIT license.