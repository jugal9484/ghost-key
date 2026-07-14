from password_toolkit import strength


def test_common_password_scores_very_weak():
    result = strength.check_strength("password")
    assert result["rating"] == "Very Weak"
    assert result["score"] <= 5


def test_strong_password_scores_high():
    result = strength.check_strength("G7#kPz!q92@WmXe4")
    assert result["score"] >= 80
    assert result["rating"] == "Very Strong"


def test_sequence_detection():
    assert strength.has_sequence("abc")
    assert strength.has_sequence("cba")
    assert strength.has_sequence("xx123xx")
    assert not strength.has_sequence("a1b2c3")


def test_repeat_detection():
    assert strength.has_repeat("aaa")
    assert strength.has_repeat("x111y")
    assert not strength.has_repeat("aabb")


def test_keyboard_walk_detection():
    assert strength.has_keyboard_walk("qwerty")
    assert strength.has_keyboard_walk("asdf")
    assert not strength.has_keyboard_walk("G7#kPz")


def test_entropy_zero_for_empty():
    assert strength.estimate_entropy("") == 0.0


def test_feedback_present():
    result = strength.check_strength("short")
    assert any("12 characters" in item for item in result["feedback"])
