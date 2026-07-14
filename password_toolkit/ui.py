"""Terminal UI helpers: ANSI colors, banner, and strength bars.

Colors are disabled automatically when stdout is not a TTY or when the
NO_COLOR environment variable is set (https://no-color.org).
"""

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

BANNER = """
╔════════════════════════════╗
║       PASSWORD TOOLKIT       ║
║  check · breach · generate   ║
╚════════════════════════════╝"""


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
