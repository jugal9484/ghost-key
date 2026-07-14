"""Cryptographically secure password and passphrase generation.

Uses the `secrets` module per NIST SP 800-63B / OWASP recommendations.
"""

import secrets
import string

MIN_LENGTH = 8
DEFAULT_LENGTH = 16
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

# Small embedded wordlist for passphrases. For maximum entropy, swap in a
# full EFF Diceware wordlist (7776 words).
WORDLIST = (
    "apple", "anchor", "autumn", "basket", "beacon", "bridge", "cactus",
    "candle", "canyon", "copper", "cosmic", "crater", "dolphin", "drift",
    "ember", "falcon", "forest", "garnet", "glacier", "granite", "harbor",
    "hazel", "island", "jungle", "kettle", "lantern", "lunar", "maple",
    "meadow", "nectar", "nimbus", "ocean", "orbit", "pebble", "pinnacle",
    "prairie", "quartz", "quiver", "raven", "ripple", "saddle", "summit",
    "thistle", "timber", "tundra", "umber", "velvet", "walnut", "willow",
    "zephyr",
)


def generate_password(
    length: int = DEFAULT_LENGTH,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Generate a secure random password.

    Guarantees at least one character from each enabled class.
    """
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be at least {MIN_LENGTH}.")

    pools = [string.ascii_lowercase]
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(SYMBOLS)

    if length < len(pools):
        raise ValueError("Length too short for the selected character classes.")

    # One guaranteed character per class, remainder from the combined pool.
    all_chars = "".join(pools)
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]

    # Cryptographically secure Fisher-Yates shuffle.
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    return "".join(chars)


def generate_passphrase(words: int = 4, separator: str = "-", capitalize: bool = True) -> str:
    """Generate a random passphrase, e.g. 'Falcon-Quartz-Meadow-Zephyr'."""
    if words < 3:
        raise ValueError("Use at least 3 words for a passphrase.")
    chosen = [secrets.choice(WORDLIST) for _ in range(words)]
    if capitalize:
        chosen = [word.capitalize() for word in chosen]
    return separator.join(chosen)
