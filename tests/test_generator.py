import string

import pytest

from password_toolkit import generator


def test_default_length():
    assert len(generator.generate_password()) == generator.DEFAULT_LENGTH


def test_custom_length():
    assert len(generator.generate_password(length=32)) == 32


def test_minimum_length_enforced():
    with pytest.raises(ValueError):
        generator.generate_password(length=4)


def test_contains_all_enabled_classes():
    password = generator.generate_password(length=12)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in generator.SYMBOLS for c in password)


def test_no_symbols_option():
    password = generator.generate_password(length=20, use_symbols=False)
    assert not any(c in generator.SYMBOLS for c in password)


def test_passwords_are_unique():
    assert generator.generate_password() != generator.generate_password()


def test_passphrase_word_count_and_separator():
    phrase = generator.generate_passphrase(words=5, separator="-")
    assert len(phrase.split("-")) == 5


def test_passphrase_minimum_words():
    with pytest.raises(ValueError):
        generator.generate_passphrase(words=2)
