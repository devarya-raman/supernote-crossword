#!/usr/bin/env python3
"""
Dump all Chrome cookies for nytimes.com in `document.cookie` style.
Requires:  pip install browser-cookie3
"""

import browser_cookie3

# 1. Load cookies straight from your local Chrome profile
cj = browser_cookie3.chrome(domain_name="nytimes.com")  # includes sub‑domains & HttpOnly ﻿:contentReference[oaicite:0]{index=0}

# 2. Convert CookieJar → {name: value}, keeping the *last* cookie seen for each name
cookie_map = {}
for c in cj:
    cookie_map[c.name] = c.value          # later duplicates overwrite earlier ones

# 3. Join into the exact format Chrome’s `document.cookie` returns
cookie_string = "; ".join(f"{k}={v}" for k, v in cookie_map.items())

print(cookie_string)
