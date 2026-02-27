"""Password analysis service.

Provides a single pure function `analyze_password` which computes entropy,
estimated time to crack (based on guesses/sec), strength category, and
suggestions. This module does not perform any I/O, logging, or storage.
"""
from typing import Dict, Any
import math


def _human_time(seconds: float) -> str:
    """Convert seconds into a human-friendly approximate string."""
    if seconds <= 1:
        return "<1 second"
    minute = 60
    hour = 3600
    day = 86400
    year = 31536000
    if seconds < minute:
        return f"{int(seconds)} seconds"
    if seconds < hour:
        return f"{int(seconds//minute)} minutes"
    if seconds < day:
        return f"{int(seconds//hour)} hours"
    if seconds < year:
        return f"{int(seconds//day)} days"
    years = seconds / year
    if years < 100:
        return f"{years:.1f} years"
    centuries = years / 100
    if centuries < 1000:
        return f"{centuries:.1f} centuries"
    return "millennia+"


def analyze_password(password: str, guesses_per_second: float = 1e9) -> Dict[str, Any]:
    """Analyze a password and return metrics and suggestions.

    Args:
        password: The plaintext password to analyze. This function does not
            store or log the password; it only uses it to compute metrics.
        guesses_per_second: Attack rate to estimate time-to-crack (default 1e9).

    Returns:
        A dict with keys: `entropy_bits`, `guesses`, `time_seconds`,
        `time_display`, `strength`, `suggestions`.
    """
    pwd = password or ""
    length = len(pwd)
    # Determine character pool size
    lower = any(c.islower() for c in pwd)
    upper = any(c.isupper() for c in pwd)
    digits = any(c.isdigit() for c in pwd)
    # symbols: characters that are not alnum
    symbols = any(not c.isalnum() for c in pwd)

    pool = 0
    if lower:
        pool += 26
    if upper:
        pool += 26
    if digits:
        pool += 10
    if symbols:
        # approximate common printable symbols
        pool += 33

    if pool <= 0 or length == 0:
        return {
            "entropy_bits": 0.0,
            "guesses": 0,
            "time_seconds": 0.0,
            "time_display": "n/a",
            "strength": "Weak",
            "suggestions": ["Enter a password to analyze."],
        }

    # Entropy estimate (bits) using log2(pool^length)
    entropy = length * math.log2(pool)

    # Rough guesses needed (searching half the space on average)
    guesses = pow(pool, length) / 2.0

    # Estimate time to crack
    time_seconds = guesses / float(max(1.0, guesses_per_second))
    time_display = _human_time(time_seconds)

    # Strength classification thresholds (bits)
    if entropy < 28:
        strength = "Weak"
    elif entropy < 60:
        strength = "Medium"
    else:
        strength = "Strong"

    suggestions = []
    if length < 12:
        suggestions.append("Increase length to at least 12 characters.")
    if not upper:
        suggestions.append("Add uppercase letters (A-Z).")
    if not lower:
        suggestions.append("Add lowercase letters (a-z).")
    if not digits:
        suggestions.append("Include digits (0-9).")
    if not symbols:
        suggestions.append("Include symbols (e.g. !@#$%).")
    if "password" in pwd.lower() or pwd.lower().strip() in ["123456", "qwerty", "admin"]:
        suggestions.append("Avoid common words or simple sequences.")

    if not suggestions:
        suggestions.append("No immediate improvements suggested; consider increasing length for extra safety.")

    return {
        "entropy_bits": round(float(entropy), 2),
        "guesses": int(guesses) if guesses < 1e18 else float("inf"),
        "time_seconds": time_seconds,
        "time_display": time_display,
        "strength": strength,
        "suggestions": suggestions,
    }
