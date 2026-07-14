# Ghost Key

> `>_ check · breach · generate` — a terminal-grade password security suite by **W1ZARD**

Ghost Key is a Python terminal toolkit for checking password strength, detecting breached passwords, and generating industry-standard secure passwords. Includes an interactive menu-driven UI and a colorized CLI.

## Features

- **Interactive terminal UI**: menu-driven interface with colors and strength bars, just run it with no arguments
- **Strength checker**: scores passwords (0-100) using entropy estimation, character variety, and penalties for common patterns (sequences, repeats, keyboard walks, common passwords)
- **Breach check**: checks passwords against the [HaveIBeenPwned](https://haveibeenpwned.com/Passwords) database using the k-anonymity range API. Your full password (or its full hash) never leaves your machine.
- **Generator**: cryptographically secure passwords and passphrases using Python's `secrets` module, following NIST SP 800-63B / OWASP guidance

## Quick start (no Python commands needed)

Requires Python 3.9+ installed. Get the code:

```bash
git clone https://gitlab.com/w1zard1/password-toolkit.git
cd password-toolkit
```

**Windows** — double-click `ghostkey.bat`, or from a terminal:

```bat
ghostkey.bat
```

**Linux / macOS**:

```bash
chmod +x ghostkey.sh   # first time only
./ghostkey.sh
```

Both launchers open the interactive Ghost Key UI. Arguments pass straight through for CLI mode, e.g. `./ghostkey.sh generate --length 24` or `ghostkey.bat check`.

**Optional: install as a global command**

```bash
pip install .
ghostkey             # interactive UI, from anywhere
ghostkey check
ghostkey generate --length 24
```

## Interactive mode

```
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

     crafted with care by W1ZARD • jugaljoshi.vercel.app

  [1] Check password strength
  [2] Check password against known breaches
  [3] Full audit (strength + breach)
  [4] Generate a secure password
  [5] Generate a passphrase
  [q] Quit
```

## CLI mode

The launchers accept the same subcommands. With Python directly:

```bash
# Check password strength (prompts for the password)
python -m password_toolkit check

# Check if a password appears in known data breaches
python -m password_toolkit breach

# Generate a secure 16-character password
python -m password_toolkit generate

# Generate a 24-character password without symbols
python -m password_toolkit generate --length 24 --no-symbols

# Generate a 5-word passphrase
python -m password_toolkit generate --passphrase --words 5

# Launch the interactive UI explicitly
python -m password_toolkit interactive
```

### Example output

```
$ python -m password_toolkit check
Password: MyPassw0rd

  ███████████░░░░░░░░░░░░░░░░░░░ 38/100
  Rating:  Weak
  Entropy: 41.4 bits
  Feedback:
    • Use at least 12 characters.
    • Add symbols to increase complexity.
```

Colors are disabled automatically when output is piped or when the `NO_COLOR` environment variable is set.

## Running tests

```bash
pip install pytest
pytest
```

## Security notes

- Password input is visible while typing, so be mindful of who can see your screen
- The breach check sends only the first 5 characters of the SHA-1 hash to the HIBP API (k-anonymity); matching happens locally
- Generation uses `secrets`, not `random`, for cryptographic security

## Credits

Crafted with care by **W1ZARD**

Portfolio: [jugaljoshi.vercel.app](https://jugaljoshi.vercel.app)
