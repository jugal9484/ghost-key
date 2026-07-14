"""Breach detection via the HaveIBeenPwned Pwned Passwords range API.

Uses k-anonymity: only the first 5 characters of the password's SHA-1
hash are sent to the API. The full password or full hash never leaves
the machine; suffix matching happens locally.
"""

import hashlib
import urllib.error
import urllib.request

API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
TIMEOUT_SECONDS = 10


class BreachCheckError(Exception):
    """Raised when the breach check cannot be completed (e.g. network error)."""


def _fetch_range(prefix: str) -> str:
    """Fetch the list of hash suffixes for a 5-character SHA-1 prefix."""
    request = urllib.request.Request(
        API_URL.format(prefix=prefix),
        headers={"User-Agent": "password-toolkit", "Add-Padding": "true"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise BreachCheckError(f"Could not reach the HaveIBeenPwned API: {exc}") from exc


def breach_count(password: str) -> int:
    """Return how many times the password appears in known breaches (0 = not found)."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    body = _fetch_range(prefix)
    for line in body.splitlines():
        candidate, _, count = line.partition(":")
        if candidate.strip() == suffix:
            try:
                return int(count.strip())
            except ValueError:
                return 0
    return 0
