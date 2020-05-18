from collections import namedtuple

import psycopg2
from flask import current_app, g
from psycopg2 import sql


ESTATE_FIELDS = "id,object_id,title,address,floor,area,estatetype"


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


def preload_metro_choices(app):
    """
    Load (and cache) all existing metro stations from database
    """
    
    # get_connection() and close_connection() will not work here, because we're out of app context
    conn = psycopg2.connect(app.config["POSTGRES_DSN"])
    try:
        with conn, conn.cursor() as cursor:
            query = """
            
                SELECT
                    id,
                    title
                FROM
                    t_metrostation
                ;
            
            """
            app.logger.debug("Executing %s", query)
            cursor.execute(query, locals())
            rv = cursor.fetchall()  # XXX: exposing database ID's to the user, i hope it's no big deal
            app.logger.debug("Got %s", rv)
            return rv
    finally:
        conn.close()


def get_estate_objects(criteria):
    """
    Select estate objects using criteria
    """
    with get_connection() as conn, conn.cursor() as cursor:
        
        where1 = sql.SQL(" AND ").join(
            filter(None, [
                sql.SQL("1 = 1"),
                sql.SQL("e.area >= {0}").format(sql.Literal(criteria["area_min"]))
                if criteria["area_min"] is not None else None,
                sql.SQL("e.area <= {0}").format(sql.Literal(criteria["area_max"]))
                if criteria["area_max"] is not None else None,
                sql.SQL("e.floor >= {0}").format(sql.Literal(criteria["floor_min"]))
                if criteria["floor_min"] is not None else None,
                sql.SQL("e.floor <= {0}").format(sql.Literal(criteria["floor_max"]))
                if criteria["floor_max"] is not None else None,
            ])
        )
        where2 = sql.SQL(" AND ").join(
            filter(None, [
                sql.SQL("1 = 1"),
                sql.SQL("metro_ids && {0}").format(sql.Literal(criteria["metro_stations"]))
                if len(criteria["metro_stations"]) > 0 else None,
            ])
        )
        contructed_query = sql.SQL("""
        
            SELECT
                *
            FROM
                ( SELECT
                    e.id,
                    e.object_id,
                    e.title,
                    e.address,
                    e.floor,
                    e.area,
                    e.estatetype,
                    ARRAY_AGG(m.id) as metro_ids,
                    ARRAY_AGG(m.title) as metro_titles
                FROM
                    t_estate e
                        LEFT JOIN
                    t_proximity p ON e.id = p.estate_id
                        LEFT JOIN
                    t_metrostation m ON p.metrostation_id = m.id
                WHERE
                    {0}
                GROUP BY
                    e.id ) AS foo
            WHERE
                {1}
            ;
        
        """).format(where1, where2)
        query = contructed_query.as_string(conn)
        current_app.logger.debug("Executing %s", query)
        cursor.execute(query, locals())
        Estate = namedtuple("Estate", ESTATE_FIELDS + ",metro_ids,metro_titles")
        rv = [Estate(*e) for e in cursor]
        current_app.logger.debug("Got %s", rv)
        return rv


def get_estate_object(object_id):
    """
    Select estate object by id
    """
    with get_connection() as conn, conn.cursor() as cursor:
        query = """
        
            SELECT
                e.id,
                e.object_id,
                e.title,
                e.address,
                e.floor,
                e.area,
                e.estatetype,
                ARRAY_AGG(m.title) as metro_stations
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
        
        """
        current_app.logger.debug("Executing %s", query)
        cursor.execute(query, locals())
        Estate = namedtuple("Estate", ESTATE_FIELDS + ",metro_stations")
        rv = Estate(*cursor.fetchone())
        current_app.logger.debug("Got %s", rv)
        return rv
