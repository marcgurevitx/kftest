from collections import namedtuple

import psycopg2
from flask import current_app, g


ESTATE_FIELDS = "id,object_id,title,address,floor,area,estatetype"
#METRO_FIELDS = "id,title"
#PROXIMITY_FIELDS = "id,estate_id,metrostation_id"


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


def get_estate_objects():
    """
    Select estate objects
    """
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("""
        
            SELECT
                *
            FROM
                t_estate
            ;
        
        """, locals())
        Result = namedtuple("Result", ESTATE_FIELDS)
        rv = [Result(*e) for e in cursor]
        return rv


def get_estate_object(object_id):
    """
    Select estate object by id
    """
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("""
        
            SELECT
                e.id,
                e.object_id,
                e.title,
                e.address,
                e.floor,
                e.area,
                e.estatetype,
                ARRAY_AGG(m.title)
            FROM
                t_estate e
                    LEFT JOIN
                t_proximity p ON e.id = p.estate_id
                    LEFT JOIN
                t_metrostation m ON p.metrostation_id = m.id
            WHERE
                e.object_id = %(object_id)s
            GROUP BY
                e.id
            ;
        
        """, locals())
        Result = namedtuple("Result", ESTATE_FIELDS + ",metro_stations")
        rv = Result(*cursor.fetchone())
        return rv
