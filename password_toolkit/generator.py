"""Cryptographically secure password and passphrase generation.

Uses the `secrets` module per NIST SP 800-63B / OWASP recommendations.
"""

import math
import secrets
import string

MIN_LENGTH = 8
DEFAULT_LENGTH = 16
MIN_PASSPHRASE_WORDS = 3
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

# Embedded wordlist for passphrases: 266 short, easy-to-type words, giving
# ~8 bits of entropy per word. For maximum entropy, swap in a full EFF
# Diceware wordlist (7776 words, ~12.9 bits per word); passphrase_entropy()
# reports the true strength based on whatever list is used.
WORDLIST = (
    "able", "acid", "acorn", "actor", "adobe", "agile", "album", "alien",
    "alloy", "amber", "amble", "angle", "anchor", "apex", "apple", "april",
    "apron", "arbor", "arctic", "arena", "armor", "arrow", "ashen", "aspen",
    "atlas", "atom", "attic", "autumn", "azure", "bacon", "badge", "bagel",
    "baker", "banjo", "barge", "basil", "basket", "beacon", "beak", "beam",
    "bean", "bear", "beaver", "bench", "berry", "birch", "bison", "blade",
    "blaze", "bloom", "board", "boat", "bolt", "bonus", "boots", "brave",
    "bread", "brick", "bridge", "brisk", "bronze", "brook", "broom", "brush",
    "bugle", "bulb", "cabin", "cable", "cacao", "cactus", "cameo", "camel",
    "candle", "canoe", "canyon", "cape", "cargo", "carol", "cedar", "chalk",
    "charm", "cheese", "cherry", "chess", "chief", "chime", "cider", "cinder",
    "cliff", "cloak", "clock", "cloud", "clover", "coast", "cobra", "cocoa",
    "comet", "coral", "cosmic", "cotton", "cove", "cozy", "crane", "crater",
    "creek", "crest", "crisp", "crown", "crumb", "cube", "curve", "dahlia",
    "daisy", "dandy", "dawn", "delta", "denim", "depot", "diner", "ditch",
    "dock", "dolphin", "dome", "donut", "dove", "draft", "dream", "drift",
    "drum", "dune", "eagle", "earth", "easel", "ebony", "elbow", "elder",
    "ember", "emu", "envoy", "epic", "ether", "fable", "fairy", "falcon",
    "fancy", "fauna", "fawn", "feast", "fern", "ferry", "fiber", "field",
    "finch", "flame", "flask", "fleet", "flint", "float", "flora", "flute",
    "foam", "forest", "fox", "frost", "fudge", "fungi", "gadget", "gala",
    "garnet", "gecko", "gem", "ginger", "glacier", "glade", "gleam", "globe",
    "glove", "gnome", "grain", "granite", "grape", "grove", "guava", "gully",
    "harbor", "hawk", "hazel", "heron", "hickory", "hollow", "honey", "husk",
    "igloo", "ingot", "inlet", "iris", "island", "ivory", "jade", "jaguar",
    "jasmine", "jelly", "jetty", "jewel", "jolly", "jungle", "juniper", "kayak",
    "kelp", "kettle", "koala", "lagoon", "lantern", "larch", "lemon", "lily",
    "linen", "llama", "lotus", "lunar", "lupine", "maize", "mango", "maple",
    "marble", "meadow", "medal", "melon", "mesa", "mint", "misty", "moss",
    "mural", "nectar", "nimbus", "noble", "north", "oasis", "ocean", "olive",
    "onyx", "opal", "orbit", "otter", "pansy", "pearl", "pebble", "pecan",
    "pixel", "plum", "pond", "prairie", "quartz", "quiver", "raven", "ripple",
    "saddle", "summit", "thistle", "timber", "tundra", "umber", "velvet",
    "walnut", "willow", "zephyr",
)


def _shuffle_secure(items: list) -> None:
    """Cryptographically secure in-place Fisher-Yates shuffle."""
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]


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

    _shuffle_secure(chars)
    return "".join(chars)


def generate_passphrase(words: int = 4, separator: str = "-", capitalize: bool = True) -> str:
    """Generate a random passphrase, e.g. 'Falcon-Quartz-Meadow-Zephyr'."""
    if words < MIN_PASSPHRASE_WORDS:
        raise ValueError(f"Use at least {MIN_PASSPHRASE_WORDS} words for a passphrase.")
    chosen = [secrets.choice(WORDLIST) for _ in range(words)]
    if capitalize:
        chosen = [word.capitalize() for word in chosen]
    return separator.join(chosen)


def passphrase_entropy(words: int, wordlist_size: int = len(WORDLIST)) -> float:
    """Return the true entropy in bits of a passphrase of ``words`` words.

    Each word is chosen uniformly and independently from the wordlist, so the
    entropy is ``words * log2(wordlist_size)`` regardless of capitalization or
    separators. This reflects real strength far better than the character-based
    model, which underrates dictionary-word passphrases.
    """
    if words <= 0 or wordlist_size <= 1:
        return 0.0
    return words * math.log2(wordlist_size)
