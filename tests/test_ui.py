from password_toolkit import ui


def test_strength_bar_has_requested_width(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert len(ui.strength_bar(50, width=10)) == 10


def test_colorize_disabled_with_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert ui.colorize("hello", ui.RED) == "hello"


def test_score_clamped(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert len(ui.strength_bar(150, width=10)) == 10
    assert len(ui.strength_bar(-5, width=10)) == 10
