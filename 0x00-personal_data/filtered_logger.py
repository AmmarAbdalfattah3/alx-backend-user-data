#!/usr/bin/env python3
"""This module filters the message
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.

    Args:
    fields: a list of strings representing all fields to obfuscate.
    redaction: a string representing by what the field will be obfuscated.
    message: a string representing the log line.
    separator: a string representing by which character is separated.

    Returns:
    The obfuscated log message.
    """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
