# Copyright Amethyst Reese
# Licensed under the MIT license

import re

from .types import Agent

AGENT_RE = re.compile(r"mozilla/\d.\d \(([^)]*)\)(.*)")


def user_agent(agent: str) -> Agent:
    agent = agent.lower()
    if match := AGENT_RE.match(agent):
        system, client = match.groups()

        if "android" in system:
            device = "mobile"
            os = "android"
        elif "ipad" in system:
            device = "ipad"
            os = "ios"
        elif "iphone" in system:
            device = "iphone"
            os = "ios"
        elif "mac os" in system:
            device = "desktop"
            os = "macos"
        elif "windows" in system:
            device = "desktop"
            os = "windows"
        elif "linux" in system:
            device = "desktop"
            os = "linux"
        else:
            device = "other"
            os = "other"

        if any(c in client for c in ("firefox/", "fxios/")):
            browser = "firefox"
        elif any(c in client for c in ("edg/", "edge/", "edga/", "edgios/")):
            browser = "edge"
        elif "brave/" in client:
            browser = "brave"
        elif any(c in client for c in ("chrome/", "crios/")):
            browser = "chrome"
        elif "safari/" in client:
            browser = "safari"
        elif "trident" in system or "msie" in system:
            browser = "ie"
        else:
            browser = "other"

        return Agent(device, os, browser)

    else:
        return Agent("unknown", "unknown", "unknown")
