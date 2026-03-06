from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from mysql.connector import pooling
from mysql.connector.connection import MySQLConnection


_POOL: pooling.MySQLConnectionPool | None = None


def mysql_config(include_database: bool = True) -> dict[str, object]:
    config: dict[str, object] = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "volunteer_user"),
        "password": os.getenv("MYSQL_ PASSWORD", "volunteer_pass"),
        "connection_timeout": int(os.getenv("MYSQL_CONNECT_TIMEOUT", "10")),
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "use_unicode": True,
        "autocommit": False,
    }
    if include_database:
        config["database"] = os.getenv("MYSQL_DATABASE", "volunteer_managing")
    return config


def get_pool() -> pooling.MySQLConnectionPool:
    global _POOL
    if _POOL is None:
        _POOL = pooling.MySQLConnectionPool(
            pool_name="volunteer_managing_pool",
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", "5")),
            pool_reset_session=True,
            **mysql_config(include_database=True),
        )
    return _POOL


@contextmanager
def get_connection() -> Iterator[MySQLConnection]:
    conn = get_pool().get_connection()
    try:
        yield conn
    finally:
        conn.close()


def reset_pool() -> None:
    global _POOL
    _POOL = None
