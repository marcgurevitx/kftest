import random

import psycopg2
from flask import current_app, g


def get_connection():
    """
    Return connection to Postgresql
    """
    if "conn" not in g:
        dsn = current_app.config["POSTGRES_DSN"]
        g.conn = psycopg2.connect(dsn)
    return g.conn


def close_connection(error=None):
    """
    Close connection to Postgresql
    """
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()
