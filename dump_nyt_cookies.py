#!/usr/bin/env python3
"""
Dump nytimes.com cookies in `document.cookie` format.

• Installs `browser-cookie3` automatically if missing.
• Searches Chrome, Brave, Edge, Firefox, and Opera profiles.
• “Logged-in” means the profile contains cookie name 'NYT-S' (case-insensitive).
• Chooses the logged-in profile whose newest cookie has the highest expiry.
• Outputs that profile’s cookies as:  name=value; name=value; ...
• If no logged-in profile exists, prints:  No NYTIMES Account found
"""

import sys
import subprocess
from typing import Callable, List, Tuple

# --------------------------------------------------------------------------- #
# Ensure browser_cookie3 is installed
# --------------------------------------------------------------------------- #
try:
    import browser_cookie3 as bc3
except ImportError:  # install quietly, then import again
#    print("# Installing browser-cookie3 …", file=sys.stderr)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "browser-cookie3"]
    )
    import browser_cookie3 as bc3
 
# bc3 = importlib.import_module("browser_cookie3")

# --------------------------------------------------------------------------- #
# Supported browsers and their loaders
# --------------------------------------------------------------------------- #
BROWSERS: List[Tuple[str, Callable[..., "bc3.CookieJar"]]] = [
    ("chrome", bc3.chrome),
    ("brave", bc3.brave),
    ("edge", bc3.edge),
    ("firefox", bc3.firefox),
    ("opera", bc3.opera),
]

DOMAIN = "nytimes.com"
LOGIN_COOKIE = "nyt-s"  # NYT login token (case‑insensitive)


def load_logged_in_jar() -> "bc3.CookieJar | None":
    """Return CookieJar from the logged‑in profile with the newest cookie."""
    newest_ts = -1
    newest_cj = None

    for name, loader in BROWSERS:
        try:
            cj = loader(domain_name=DOMAIN)
        except Exception:
            continue  # browser profile not present

        if not cj:
            continue

        # Check for NYT‑S (logged‑in) cookie
        if not any(c.name.lower() == LOGIN_COOKIE for c in cj):
            continue

        latest = max(
            (
                c.expires
                or c._rest.get("expiry")
                or 0  # expiry may be missing; treat as 0
                for c in cj
            ),
            default=0,
        )

        if latest > newest_ts:
            newest_ts = latest
            newest_cj = cj

    return newest_cj


def cookiejar_to_docstring(cj) -> str:
    """Convert CookieJar to `name=value; …` (last value per name wins)."""
    pairs = {}
    for c in cj:
        pairs[c.name] = c.value
    return "; ".join(f"{k}={v}" for k, v in pairs.items())


if __name__ == "__main__":
    cj = load_logged_in_jar()
    if cj is None:
        print("No NYTIMES Account found")
    else:
        print(cookiejar_to_docstring(cj))


