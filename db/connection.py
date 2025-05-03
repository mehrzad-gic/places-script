import mysql.connector
import sqlite3
import psycopg2
from mariadb import connect as mariadb_connect
import sys

def connect_db(db_type, host, user, password, database, port):
    try:
        if db_type == 'mysql':
            return mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)
        elif db_type == 'mariadb':
            return mariadb_connect(host=host, user=user, password=password, database=database, port=port)
        elif db_type == 'postgresql':
            return psycopg2.connect(host=host, user=user, password=password, dbname=database, port=port)
        elif db_type == 'sqlite':
            return sqlite3.connect(database)
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)