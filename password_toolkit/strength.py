"""Password strength evaluation.

Scores a password from 0 to 100 based on estimated entropy, character
variety, and penalties for predictable patterns.
"""

import math
import re

# Small embedded sample of the most common passwords.
COMMON_PASSWORDS = {
    "password", "password1", "123456", "12345678", "123456789",
    "1234567890", "qwerty", "qwerty123", "abc123", "111111", "letmein",
    "monkey", "dragon", "iloveyou", "trustno1", "sunshine", "master",
    "welcome", "shadow", "football", "baseball", "admin", "654321",
    "1q2w3e4r", "qazwsx", "passw0rd", "p@ssw0rd", "letmein123",
}

KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890")

RATINGS = (
    (80, "Very Strong"),
    (60, "Strong"),
    (40, "Moderate"),
    (20, "Weak"),
    (0, "Very Weak"),
)


def _charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"[0-9]", password):
        size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        size += 33
    return size


def estimate_entropy(password: str) -> float:
    """Estimate password entropy in bits (length * log2 of charset size)."""
    size = _charset_size(password)
    if not password or size == 0:
        return 0.0
    return len(password) * math.log2(size)


def has_sequence(password: str, min_len: int = 3) -> bool:
    """Detect ascending or descending character sequences (abc, 321)."""
    lower = password.lower()
    for i in range(len(lower) - min_len + 1):
        chunk = lower[i : i + min_len]
        diffs = {ord(b) - ord(a) for a, b in zip(chunk, chunk[1:])}
        if diffs == {1} or diffs == {-1}:
            return True
    return False


def has_repeat(password: str, min_len: int = 3) -> bool:
    """Detect runs of the same character (aaa, 111)."""
    return re.search(r"(.)\1{%d,}" % (min_len - 1), password) is not None


def has_keyboard_walk(password: str, min_len: int = 4) -> bool:
    """Detect keyboard walks like 'qwer' or 'asdf' (forwards or backwards)."""
    lower = password.lower()
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - min_len + 1):
            walk = row[i : i + min_len]
            if walk in lower or walk[::-1] in lower:
                return True
    return False


def is_common(password: str) -> bool:
    return password.lower() in COMMON_PASSWORDS


def check_strength(password: str) -> dict:
    """Evaluate a password and return score, rating, entropy, and feedback."""
    feedback = []
    entropy = estimate_entropy(password)

    # Base score from entropy: ~75 bits maps to 100.
    score = min(100.0, (entropy / 75.0) * 100.0)

    if len(password) < 12:
        feedback.append("Use at least 12 characters.")
    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letters.")
    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letters.")
    if not re.search(r"[0-9]", password):
        feedback.append("Add digits.")
    if not re.search(r"[^a-zA-Z0-9]", password):
        feedback.append("Add symbols to increase complexity.")

    if is_common(password):
        score = min(score, 5.0)
        feedback.append("This is one of the most commonly used passwords.")
    if has_sequence(password):
        score -= 15
        feedback.append("Avoid sequential characters (e.g. 'abc', '123').")
    if has_repeat(password):
        score -= 15
        feedback.append("Avoid repeated characters (e.g. 'aaa').")
    if has_keyboard_walk(password):
        score -= 15
        feedback.append("Avoid keyboard patterns (e.g. 'qwerty', 'asdf').")

    score = max(0, min(100, round(score)))
    rating = next(label for threshold, label in RATINGS if score >= threshold)

    if not feedback:
        feedback.append("Great password!")

    return {
        "score": score,
        "rating": rating,
        "entropy_bits": round(entropy, 1),
        "feedback": feedback,
    }
