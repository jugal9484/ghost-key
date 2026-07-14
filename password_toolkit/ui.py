"""Terminal UI helpers: ANSI colors, banner, and strength bars.

Colors are disabled automatically when stdout is not a TTY or when the
NO_COLOR environment variable is set (https://no-color.org).
"""

import getpass
import os
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

RATING_COLORS = {
    "Very Weak": RED,
    "Weak": RED,
    "Moderate": YELLOW,
    "Strong": GREEN,
    "Very Strong": GREEN,
}

BANNER = r"""
  ____ _               _
 / ___| |__   ___  ___| |_
| |  _| '_ \ / _ \/ __| __|
| |_| | | | | (_) \__ \ |_
 \____|_| |_|\___/|___/\__|

██╗  ██╗███████╗██╗   ██╗
██║ ██╔╝██╔════╝╚██╗ ██╔╝
█████╔╝ █████╗   ╚████╔╝
██╔═██╗ ██╔══╝    ╚██╔╝
██║  ██╗███████╗   ██║
╚═╝  ╚═╝╚══════╝   ╚═╝

     [ Check ] • [ Breach ] • [ Generate ]

     crafted with care by W1ZARD • jugaljoshi.vercel.app"""


def supports_color(stream=None) -> bool:
    stream = stream if stream is not None else sys.stdout
    if os.environ.get("NO_COLOR"):
        return False
    return hasattr(stream, "isatty") and stream.isatty()


def colorize(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes when color output is supported."""
    if not codes or not supports_color():
        return text
    return "".join(codes) + text + RESET


def read_password(label: str = "Password") -> str:
    """Read a password from the user, masked by default.

    Uses ``getpass`` so the secret is not echoed to the screen. Set the
    environment variable ``GHOSTKEY_VISIBLE=1`` to type visibly instead, which
    is useful in environments (some IDE consoles) where echo cannot be
    disabled and ``getpass`` would otherwise fall back with a warning.
    """
    prompt = colorize(f"  {label}: ", CYAN)
    if os.environ.get("GHOSTKEY_VISIBLE"):
        return input(prompt)
    try:
        return getpass.getpass(prompt)
    except (getpass.GetPassWarning, EOFError, KeyboardInterrupt):
        raise
    except Exception:
        # Terminal can't disable echo; fall back to visible input.
        return input(prompt)


def strength_bar(score: int, width: int = 30) -> str:
    """Render a colored progress bar for a 0-100 strength score."""
    filled = round(width * max(0, min(100, score)) / 100)
    color = GREEN if score >= 60 else YELLOW if score >= 40 else RED
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    return colorize(bar, color)


def print_banner() -> None:
    print(colorize(BANNER, CYAN, BOLD))


def print_strength_result(result: dict) -> None:
    """Pretty-print a result dict from strength.check_strength()."""
    color = RATING_COLORS.get(result["rating"], YELLOW)
    print()
    print(f"  {strength_bar(result['score'])} {result['score']}/100")
    print(f"  Rating:  {colorize(result['rating'], color, BOLD)}")
    print(f"  Entropy: {result['entropy_bits']} bits")
    print("  Feedback:")
    for item in result["feedback"]:
        print(colorize(f"    \u2022 {item}", DIM))
    print()
