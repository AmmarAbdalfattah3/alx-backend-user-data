#!/usr/bin/env python3
"""
This module provides utilities for logging and handling personal data.
"""


import logging
import os
import re
from typing import List

import mysql.connector


# Define PII_FIELDS with fields considered sensitive
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Redacts sensitive information from the message."""
    for field in fields:
        message = re.sub(
            f'{field}=[^{separator}]*',
            f'{field}={redaction}',
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts sensitive information in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to redact."""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with redaction."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and returns a logger configured for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to the MySQL database and returns the connection object."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection


def main():
    """Main function to retrieve and log user data."""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    for row in cursor.fetchall():
        message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
