# Copyright Amethyst Reese
# Licensed under the MIT license

from unittest import TestCase

from ..agent import user_agent
from ..types import Agent


class AgentTest(TestCase):
    def test_user_agent(self):
        # https://www.whatismybrowser.com/guides/the-latest-user-agent/
        for name, value, expected in (
            ("empty", "", Agent("unknown", "unknown", "unknown")),
            # chrome
            (
                "chrome android",
                "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.76 Mobile Safari/537.36",
                Agent("mobile", "android", "chrome"),
            ),
            (
                "chrome ipad",
                "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/113.0.5672.69 Mobile/15E148 Safari/604.1",
                Agent("ipad", "ios", "chrome"),
            ),
            (
                "chrome iphone",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/113.0.5672.69 Mobile/15E148 Safari/604.1",
                Agent("iphone", "ios", "chrome"),
            ),
            (
                "chrome desktop linux",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                Agent("desktop", "linux", "chrome"),
            ),
            (
                "chrome desktop macos",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                Agent("desktop", "macos", "chrome"),
            ),
            (
                "chrome desktop windows",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                Agent("desktop", "windows", "chrome"),
            ),
            # edge
            (
                "android edge",
                "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.76 Mobile Safari/537.36 EdgA/112.0.1722.59",
                Agent("mobile", "android", "edge"),
            ),
            (
                "iphone edge",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 EdgiOS/112.1722.64 Mobile/15E148 Safari/605.1.15",
                Agent("iphone", "ios", "edge"),
            ),
            (
                "edge desktop macos",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/112.0.1722.71",
                Agent("desktop", "macos", "edge"),
            ),
            (
                "edge desktop windows",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/112.0.1722.71",
                Agent("desktop", "windows", "edge"),
            ),
            # firefox
            (
                "firefox android",
                "Mozilla/5.0 (Android 13; Mobile; rv:109) Gecko/112.0 Firefox/112.0",
                Agent("mobile", "android", "firefox"),
            ),
            (
                "firefox ipad",
                "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/112.0 Mobile/15E148 Safari/605.1.15",
                Agent("ipad", "ios", "firefox"),
            ),
            (
                "firefox iphone",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/112.0 Mobile/15E148 Safari/605.1.15",
                Agent("iphone", "ios", "firefox"),
            ),
            (
                "firefox desktop linux",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109) Gecko/20100101 Firefox/112.0",
                Agent("desktop", "linux", "firefox"),
            ),
            (
                "firefox desktop macos",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:109) Gecko/20100101 Firefox/112.0",
                Agent("desktop", "macos", "firefox"),
            ),
            (
                "firefox desktop windows",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109) Gecko/20100101 Firefox/112.0",
                Agent("desktop", "windows", "firefox"),
            ),
            # safari
            (
                "safari ipad",
                "Mozilla/5.0 (iPad; CPU OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
                Agent("ipad", "ios", "safari"),
            ),
            (
                "safari iphone",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
                Agent("iphone", "ios", "safari"),
            ),
            (
                "safari desktop macos",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
                Agent("desktop", "macos", "safari"),
            ),
            (
                "safari weird",
                "MobileSafari/8615.1.26.10.24 CFNetwork/1406.0.4 Darwin/22.4.0",
                Agent("other", "other", "safari"),
            ),
            # brave
            (
                "brave android",
                "Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Brave/107.0.0.0 Mobile Safari/537.36v",
                Agent("mobile", "android", "brave"),
            ),
            (
                "brave desktop linux",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Brave/537.36",
                Agent("desktop", "linux", "brave"),
            ),
            (
                "brave desktop macos",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Brave/107.0.0.0 Safari/537.36",
                Agent("desktop", "macos", "brave"),
            ),
            (
                "brave desktop windows",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.4472.124 Safari/537.3 brave/5035",
                Agent("desktop", "windows", "brave"),
            ),
            # lol
            (
                "ie9",
                "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                Agent("desktop", "windows", "ie"),
            ),
            (
                "ie10",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
                Agent("desktop", "windows", "ie"),
            ),
            (
                "ie11",
                "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
                Agent("desktop", "windows", "ie"),
            ),
        ):
            with self.subTest(name):
                result = user_agent(value)
                self.assertEqual(expected, result)
