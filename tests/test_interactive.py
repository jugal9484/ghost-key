import builtins

from password_toolkit import interactive, ui


def _feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *a, **k: next(it))


def test_ask_int_default(monkeypatch):
    _feed(monkeypatch, [""])
    assert interactive._ask_int("Length", 16) == 16


def test_ask_int_value(monkeypatch):
    _feed(monkeypatch, ["24"])
    assert interactive._ask_int("Length", 16) == 24


def test_ask_int_invalid_uses_default(monkeypatch, capsys):
    _feed(monkeypatch, ["not-a-number"])
    assert interactive._ask_int("Length", 16) == 16


def test_ask_yes_no(monkeypatch):
    _feed(monkeypatch, ["y"])
    assert interactive._ask_yes_no("ok?") is True
    _feed(monkeypatch, ["n"])
    assert interactive._ask_yes_no("ok?") is False
    _feed(monkeypatch, [""])
    assert interactive._ask_yes_no("ok?", default=True) is True


def test_run_quits_immediately(monkeypatch, capsys):
    _feed(monkeypatch, ["q"])
    assert interactive.run() == 0
    assert "Goodbye" in capsys.readouterr().out


def test_run_unknown_option(monkeypatch, capsys):
    _feed(monkeypatch, ["9", "q"])
    assert interactive.run() == 0
    assert "Unknown option" in capsys.readouterr().out


def test_run_eof_exits_cleanly(monkeypatch):
    def raise_eof(*a, **k):
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)
    assert interactive.run() == 0


def test_run_check_flow(monkeypatch, capsys):
    monkeypatch.setattr(ui, "read_password", lambda label="Password": "G7#kPz!q92@WmXe4")
    _feed(monkeypatch, ["1", "q"])
    assert interactive.run() == 0
    assert "/100" in capsys.readouterr().out


def test_run_generate_password_flow(monkeypatch, capsys):
    _feed(monkeypatch, ["4", "16", "y", "y", "y", "q"])
    assert interactive.run() == 0
    out = capsys.readouterr().out
    assert "Strength" in out and "bits" in out


def test_run_passphrase_flow(monkeypatch, capsys):
    _feed(monkeypatch, ["5", "4", "-", "q"])
    assert interactive.run() == 0
    out = capsys.readouterr().out
    assert "bits" in out and "words" in out
