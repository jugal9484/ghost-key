import pytest

from password_toolkit import breach


def test_breach_count_parses_matching_suffix(monkeypatch):
    # SHA-1 of 'password' is 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
    suffix = "1E4C9B93F3F0682250B6CF8331B7EE68FD8"
    monkeypatch.setattr(breach, "_fetch_range", lambda prefix: f"ABCDEF:1\r\n{suffix}:12345")
    assert breach.breach_count("password") == 12345


def test_breach_count_zero_when_not_found(monkeypatch):
    monkeypatch.setattr(breach, "_fetch_range", lambda prefix: "ABCDEF:1\r\n123456:2")
    assert breach.breach_count("some-password") == 0


def test_network_error_raises_breach_check_error(monkeypatch):
    def boom(prefix):
        raise breach.BreachCheckError("offline")

    monkeypatch.setattr(breach, "_fetch_range", boom)
    with pytest.raises(breach.BreachCheckError):
        breach.breach_count("anything")
