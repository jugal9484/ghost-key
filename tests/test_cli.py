import pytest

from password_toolkit import cli, generator


def _fixed_password(pw):
    return lambda label="Password": pw


def test_no_args_launches_interactive(monkeypatch):
    calls = []
    monkeypatch.setattr(cli.interactive, "run", lambda: (calls.append(True), 0)[1])
    assert cli.main([]) == 0
    assert calls == [True]


def test_generate_default_length(capsys):
    assert cli.main(["generate"]) == 0
    out = capsys.readouterr().out.strip()
    assert len(out) == generator.DEFAULT_LENGTH


def test_generate_no_symbols(capsys):
    assert cli.main(["generate", "--length", "20", "--no-symbols"]) == 0
    out = capsys.readouterr().out.strip()
    assert len(out) == 20
    assert not any(c in generator.SYMBOLS for c in out)


def test_generate_passphrase(capsys):
    assert cli.main(["generate", "--passphrase", "--words", "4"]) == 0
    out = capsys.readouterr().out.strip()
    assert len(out.split("-")) == 4


def test_generate_invalid_length_returns_2(capsys):
    assert cli.main(["generate", "--length", "4"]) == 2
    assert "Error" in capsys.readouterr().err


def test_check_command(monkeypatch, capsys):
    monkeypatch.setattr(cli.ui, "read_password", _fixed_password("G7#kPz!q92@WmXe4"))
    assert cli.main(["check"]) == 0
    assert "/100" in capsys.readouterr().out


def test_empty_password_exits_2(monkeypatch):
    monkeypatch.setattr(cli.ui, "read_password", _fixed_password(""))
    with pytest.raises(SystemExit) as exc:
        cli.main(["check"])
    assert exc.value.code == 2


def test_breach_compromised_returns_1(monkeypatch, capsys):
    monkeypatch.setattr(cli.ui, "read_password", _fixed_password("password"))
    monkeypatch.setattr(cli.breach, "breach_count", lambda pw: 42)
    assert cli.main(["breach"]) == 1
    assert "COMPROMISED" in capsys.readouterr().out


def test_breach_clean_returns_0(monkeypatch, capsys):
    monkeypatch.setattr(cli.ui, "read_password", _fixed_password("uniq-pass-123"))
    monkeypatch.setattr(cli.breach, "breach_count", lambda pw: 0)
    assert cli.main(["breach"]) == 0
    assert "not found" in capsys.readouterr().out.lower()


def test_breach_network_error_returns_1(monkeypatch, capsys):
    monkeypatch.setattr(cli.ui, "read_password", _fixed_password("anything"))

    def boom(pw):
        raise cli.breach.BreachCheckError("offline")

    monkeypatch.setattr(cli.breach, "breach_count", boom)
    assert cli.main(["breach"]) == 1
    assert "Error" in capsys.readouterr().err


def test_no_command_is_a_parse_error():
    with pytest.raises(SystemExit):
        cli.main(["bogus"])
