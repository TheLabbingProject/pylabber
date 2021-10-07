"""
Utilities for the :mod:`accouts.filters` module.
"""
from typing import Tuple

#: Task result status choices.
STATUS_CHOICES: Tuple[Tuple[str, str]] = (
    ("SUCCESS", "SUCCESS"),
    ("FAILURE", "FAILURE"),
    ("STARTED", "STARTED"),
    ("PENDING", "PENDING"),
    ("RECEIVED", "RECEIVED"),
    ("REVOKED", "REVOKED"),
    ("RETRY", "RETRY"),
)
