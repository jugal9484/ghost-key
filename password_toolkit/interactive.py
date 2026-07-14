"""Interactive menu-driven terminal UI for Ghost Key."""

from password_toolkit import breach, generator, strength, ui

MENU = """
  [1] Check password strength
  [2] Check password against known breaches
  [3] Full audit (strength + breach)
  [4] Generate a secure password
  [5] Generate a passphrase
  [q] Quit
"""


def _prompt(label: str) -> str:
    return input(ui.colorize(f"  {label}: ", ui.CYAN)).strip()


def _read_password() -> str:
    while True:
        password = input(ui.colorize("  Password: ", ui.CYAN))
        if password:
            return password
        print(ui.colorize("  Please enter a password.", ui.YELLOW))


def _ask_int(label: str, default: int) -> int:
    raw = _prompt(f"{label} [{default}]")
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(ui.colorize("  Not a number, using default.", ui.YELLOW))
        return default


def _ask_yes_no(label: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    raw = _prompt(f"{label} [{hint}]").lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def _report_breach(password: str) -> None:
    try:
        count = breach.breach_count(password)
    except breach.BreachCheckError as exc:
        print(ui.colorize(f"\n  Error: {exc}\n", ui.RED))
        return
    if count:
        print(ui.colorize(
            f"\n  \u26a0 COMPROMISED: found in {count:,} known breaches. Do not use it!\n",
            ui.RED, ui.BOLD,
        ))
    else:
        print(ui.colorize("\n  \u2714 Not found in known breaches.\n", ui.GREEN))


def _do_check() -> None:
    ui.print_strength_result(strength.check_strength(_read_password()))


def _do_breach() -> None:
    _report_breach(_read_password())


def _do_audit() -> None:
    password = _read_password()
    ui.print_strength_result(strength.check_strength(password))
    _report_breach(password)


def _show_generated(password: str) -> None:
    print(f"\n  {ui.colorize(password, ui.GREEN, ui.BOLD)}\n")
    result = strength.check_strength(password)
    print(f"  Strength: {ui.strength_bar(result['score'])} {result['score']}/100\n")


def _do_generate() -> None:
    length = _ask_int("Length", generator.DEFAULT_LENGTH)
    symbols = _ask_yes_no("Include symbols?")
    digits = _ask_yes_no("Include digits?")
    upper = _ask_yes_no("Include uppercase?")
    try:
        password = generator.generate_password(
            length=length, use_upper=upper, use_digits=digits, use_symbols=symbols,
        )
    except ValueError as exc:
        print(ui.colorize(f"  Error: {exc}", ui.RED))
        return
    _show_generated(password)


def _do_passphrase() -> None:
    words = _ask_int("Number of words", 4)
    separator = _prompt("Separator [-]") or "-"
    try:
        _show_generated(generator.generate_passphrase(words=words, separator=separator))
    except ValueError as exc:
        print(ui.colorize(f"  Error: {exc}", ui.RED))


ACTIONS = {
    "1": _do_check,
    "2": _do_breach,
    "3": _do_audit,
    "4": _do_generate,
    "5": _do_passphrase,
}


def run() -> int:
    """Run the interactive menu loop. Returns a process exit code."""
    ui.print_banner()
    while True:
        print(MENU)
        try:
            choice = _prompt("Select an option").lower()
        except (EOFError, KeyboardInterrupt):
            print(ui.colorize("\n  Goodbye!", ui.CYAN))
            return 0
        if choice in ("q", "quit", "exit"):
            print(ui.colorize("  Goodbye!", ui.CYAN))
            return 0
        action = ACTIONS.get(choice)
        if action is None:
            print(ui.colorize("  Unknown option, try again.", ui.YELLOW))
            continue
        try:
            action()
        except (EOFError, KeyboardInterrupt):
            print()  # cancelled mid-action, back to menu
