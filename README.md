# Ghost Key

> `>_ check · breach · generate` — a terminal-grade password security suite by **W1ZARD**

[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/runtime%20deps-none-brightgreen.svg)](requirements.txt)
[![Linter: Ruff](https://img.shields.io/badge/lint-ruff-261230.svg?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)
[![Tests](https://img.shields.io/badge/tests-45%20passing-brightgreen.svg)](tests/)

Ghost Key is a Python terminal toolkit for checking password strength, detecting breached passwords, and generating industry-standard secure passwords. Includes an interactive menu-driven UI and a colorized CLI. **Zero runtime dependencies** — it uses only the Python standard library.

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

## How it works

- **Strength** — estimates entropy as `length × log2(charset)`, maps it to a 0–100 score, and applies penalties for common passwords, sequences (`abc`, `321`), repeats (`aaa`), and keyboard walks (`qwerty`). Follows the spirit of NIST SP 800-63B: length and unpredictability over arbitrary composition rules.
- **Breach** — hashes the password with SHA-1 locally, sends only the first 5 hex characters of the hash to the [HaveIBeenPwned](https://haveibeenpwned.com/Passwords) range API (k-anonymity), and matches the suffix on your machine. `Add-Padding` is requested to blur response size.
- **Generation** — draws from Python's `secrets` CSPRNG, guarantees at least one character from every enabled class, and shuffles with a cryptographically secure Fisher–Yates. Passphrases report their *true* entropy (`words × log2(wordlist size)`), which the character model would otherwise underrate.

## Security notes

- **Password input is masked by default** (via `getpass`) so secrets are not echoed to the screen. Set `GHOSTKEY_VISIBLE=1` to type visibly in environments where echo cannot be disabled.
- Your full password — and its full hash — **never leave your machine**. The breach check only ever sends a 5-character hash prefix.
- Generation uses `secrets`, not `random`, for cryptographic security.
- The bundled wordlist (266 words, ~8 bits/word) is convenient, not maximal. For the strongest passphrases, swap in the full [EFF Diceware list](https://www.eff.org/dice) (7776 words, ~12.9 bits/word); `passphrase_entropy()` will report the new strength automatically.

## Development

```bash
python -m pip install -e ".[dev]"   # installs pytest + ruff
pytest                              # run the test suite (45 tests)
ruff check .                        # lint
```

CI (`.gitlab-ci.yml`) runs Ruff plus the test suite on Python 3.9 and 3.12.
See [CHANGELOG.md](CHANGELOG.md) for release history and [LICENSE](LICENSE) for terms (MIT).

## Credits

Crafted with care by **W1ZARD**

Portfolio: [jugaljoshi.vercel.app](https://jugaljoshi.vercel.app)
