"""
Password Entropy and Crack Time Calculator Utility.

Calculates Shannon entropy score in bits, estimates brute-force crack time,
and determines visual color status gradients.
"""

import math
from typing import Tuple


class PasswordEntropy:
    """
    Calculates password complexity, entropy score, and crack time estimates.
    """

    @staticmethod
    def calculate_entropy(password: str) -> float:
        """
        Calculates Shannon entropy score in bits.

        Formula: Entropy = Length * log2(Charset Size)
        """
        if not password:
            return 0.0

        charset_size = 0
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)

        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += 32

        if charset_size == 0:
            charset_size = 256

        return len(password) * math.log2(charset_size)

    @staticmethod
    def get_crack_time_estimate(entropy_bits: float) -> str:
        """
        Estimates brute-force time based on 100 Billion guesses/sec (GPU array).
        """
        if entropy_bits == 0:
            return "Instant"

        combinations = 2**entropy_bits
        guesses_per_sec = 100_000_000_000  # 100 Billion
        seconds = combinations / (2 * guesses_per_sec)  # Average half space search

        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds // 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds // 86400)} days"
        elif seconds < 31536000 * 1000:
            return f"{int(seconds // 31536000)} years"
        else:
            return "100M+ years"

    @staticmethod
    def get_strength_rating(password: str) -> Tuple[float, str, str, str]:
        """
        Returns tuple: (progress_ratio [0.0-1.0], rating_label, color_hex, crack_time)
        """
        bits = PasswordEntropy.calculate_entropy(password)
        crack_time = PasswordEntropy.get_crack_time_estimate(bits)

        if bits == 0:
            return 0.0, "Empty", "#555555", "Instant"
        elif bits < 28:
            return 0.25, "Very Weak", "#D13438", crack_time
        elif bits < 40:
            return 0.50, "Weak", "#FF8C00", crack_time
        elif bits < 60:
            return 0.75, "Good", "#FCE100", crack_time
        else:
            return 1.00, "Very Strong", "#107C41", crack_time

    @staticmethod
    def get_suggestions(password: str) -> list[str]:
        """
        Returns a list of actionable security improvement suggestions.
        """
        if not password:
            return ["Enter a strong secret password."]

        suggestions = []
        if len(password) < 12:
            suggestions.append("Make password at least 12 characters long.")
        if not any(c.isupper() for c in password):
            suggestions.append("Add uppercase letters (A-Z).")
        if not any(c.islower() for c in password):
            suggestions.append("Add lowercase letters (a-z).")
        if not any(c.isdigit() for c in password):
            suggestions.append("Add numbers (0-9).")
        if not any(not c.isalnum() for c in password):
            suggestions.append("Add special symbols (!@#$%^&*).")

        if not suggestions:
            suggestions.append("Great password! Extremely high cryptographic entropy.")

        return suggestions
