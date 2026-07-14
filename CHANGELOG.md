# Changelog

All notable changes to Ghost Key are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-14

### Added
- Masked password input by default (via `getpass`) so secrets no longer echo to
  the screen. Set `GHOSTKEY_VISIBLE=1` to restore visible typing where a
  terminal cannot disable echo.
- Honest passphrase entropy: `generator.passphrase_entropy()` reports the true
  bit-strength of a generated passphrase based on the wordlist size, and the
  interactive UI now shows it instead of the character-model score.
- Test coverage for the CLI (`tests/test_cli.py`) and the interactive menu
  (`tests/test_interactive.py`).
- `LICENSE` (MIT), `CHANGELOG.md`, and `.gitignore`.
- Linting stage (Ruff) in CI alongside the test stage.

### Changed
- Expanded the passphrase wordlist from 50 to 266 words (~8 bits per word) for
  meaningfully stronger passphrases.
- README refreshed with badges, clearer security notes, and project metadata.

## [1.1.0] - 2026-07-14

### Added
- Easy launchers (`ghostkey.bat`, `ghostkey.sh`) so no Python commands are
  required to run the tool.
- ASCII banner and W1ZARD branding.

## [1.0.0] - 2026-07-14

### Added
- Initial release: password strength checker, HaveIBeenPwned breach detection
  via k-anonymity, secure password/passphrase generator, interactive terminal
  UI, and colorized CLI.
