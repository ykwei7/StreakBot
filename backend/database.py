#!/usr/bin/python
import psycopg2
from config import config


SCHEMA = "streakBotDB"
USERS = "users"
HABITS = "habits"


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print("PostgreSQL database version:")
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def view_all_users():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = f'SELECT * FROM "{SCHEMA}".{USERS};'
        cur.execute(query)
        result = cur.fetchall()
        print("Query was executed successfully.")
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def add_user(userId: str) -> str:
    """Adds user to database

    Args:
        userId (str): telegram userID of intended user
    """
    # TODO: Add exception when user is already added
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        add_user_query = (
            f'INSERT INTO "{SCHEMA}".{USERS} ("userID") VALUES (\'{userId}\');'
        )
        print(add_user_query)
        cur.execute(add_user_query)
        conn.commit()
        print("Query was executed successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == "__main__":
    add_user("12345")
    print(view_all_users())
