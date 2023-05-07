# Copyright Amethyst Reese
# Licensed under the MIT license

from unittest import TestCase
from ipaddress import ip_address
from random import randint

from .. import iplookup


class IPLookupTest(TestCase):
    @classmethod
    def setUpClass(cls):
        iplookup.load()

    def test_lookup(self):
        for value, expected in (
            ("127.0.0.1", ("None", "ipv4")),
            ("192.168.0.1", ("None", "ipv4")),
            ("192.168.0.1", ("None", "ipv4")),
            ("::", ("None", "ipv6")),
            ("fe80::1ff:fe23:4567:890a", ("None", "ipv6")),
        ):
            with self.subTest(value):
                self.assertEqual(expected, iplookup.lookup(value))

    def test_random_ipv4_lookups(self):
        # may need to be updated if ip2country dataset is updated
        for idx, expected in (
            (24, "TH"),
            (950, "KR"),
            (1794, "RU"),
            (5035, "DE"),
            (8350, "US"),
            (467868, "JP"),
        ):
            rng = iplookup.IP2COUNTRY_V4[idx]
            for ip32 in (rng.start, randint(rng.start, rng.end), rng.end):
                ips = str(ip_address(ip32))
                with self.subTest((idx, expected, ips)):
                    self.assertEqual((expected, "ipv4"), iplookup.lookup(ips))