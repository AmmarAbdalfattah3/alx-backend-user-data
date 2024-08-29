#!/usr/bin/env python3
"""This module filters the message
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.
    """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
