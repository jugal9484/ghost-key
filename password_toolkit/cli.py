"""Command-line interface for the password toolkit.

Running with no arguments launches the interactive terminal UI.
"""

import argparse
import getpass
import sys

from password_toolkit import breach, generator, interactive, strength, ui


def _read_password() -> str:
    password = getpass.getpass("Password (input hidden): ")
    if not password:
        print("No password entered.", file=sys.stderr)
        raise SystemExit(2)
    return password


def _cmd_check(_args) -> int:
    ui.print_strength_result(strength.check_strength(_read_password()))
    return 0


def _cmd_breach(_args) -> int:
    password = _read_password()
    try:
        count = breach.breach_count(password)
    except breach.BreachCheckError as exc:
        print(ui.colorize(f"Error: {exc}", ui.RED), file=sys.stderr)
        return 1
    if count:
        print(ui.colorize(
            f"COMPROMISED: this password appeared in {count:,} known breaches.",
            ui.RED, ui.BOLD,
        ))
        print("Do not use it. Generate a new one with: python -m password_toolkit generate")
        return 1
    print(ui.colorize("Good news: this password was not found in known breaches.", ui.GREEN))
    return 0


def _cmd_generate(args) -> int:
    try:
        if args.passphrase:
            secret = generator.generate_passphrase(words=args.words, separator=args.separator)
        else:
            secret = generator.generate_password(
                length=args.length,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
            )
    except ValueError as exc:
        print(ui.colorize(f"Error: {exc}", ui.RED), file=sys.stderr)
        return 2
    print(ui.colorize(secret, ui.GREEN, ui.BOLD))
    return 0


def _cmd_interactive(_args) -> int:
    return interactive.run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password_toolkit",
        description="Check password strength, detect breached passwords, and generate secure passwords.",
        epilog="Run with no arguments to launch the interactive terminal UI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Check password strength")
    check.set_defaults(func=_cmd_check)

    breach_cmd = subparsers.add_parser("breach", help="Check password against known breaches (HaveIBeenPwned)")
    breach_cmd.set_defaults(func=_cmd_breach)

    gen = subparsers.add_parser("generate", help="Generate a secure password or passphrase")
    gen.add_argument("--length", type=int, default=generator.DEFAULT_LENGTH, help="Password length (default: 16)")
    gen.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    gen.add_argument("--no-digits", action="store_true", help="Exclude digits")
    gen.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    gen.add_argument("--passphrase", action="store_true", help="Generate a word-based passphrase instead")
    gen.add_argument("--words", type=int, default=4, help="Number of words in the passphrase (default: 4)")
    gen.add_argument("--separator", default="-", help="Passphrase word separator (default: '-')")
    gen.set_defaults(func=_cmd_generate)

    inter = subparsers.add_parser("interactive", help="Launch the interactive terminal UI")
    inter.set_defaults(func=_cmd_interactive)

    return parser


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        return interactive.run()
    args = build_parser().parse_args(argv)
    return args.func(args)
