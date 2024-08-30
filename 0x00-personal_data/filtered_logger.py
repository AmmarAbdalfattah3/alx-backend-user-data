#!/usr/bin/env python3
"""
This module provides utilities for logging and handling personal data.
"""


import re
import logging
from typing import List, Tuple


PII_FIELDS: Tuple[str, ...] = (
    'password', 'email', 'ssn', 'address', 'phone_number'
)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redacts specified fields in the log message.

    Args:
        fields (List[str]): List of field names to redact.
        redaction (str): String to replace sensitive field values with.
        message (str): The log message containing fields to be redacted.
        separator (str): Character that separates fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for f in fields:
        message = re.sub(f'{f}=[^{separator}]*', f'{f}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    A logging formatter that redacts sensitive information.

    Attributes:
        REDACTION (str): String used to replace sensitive field values.
        FORMAT (str): Format of the log message.
        SEPARATOR (str): Character separating fields in the log message.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the formatter with fields to redact.

        Args:
            fields (List[str]): List of field names to be redacted.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger
