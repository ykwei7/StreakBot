#!/usr/bin/python
import psycopg2
from requests import post
from backend.config import config
from habit import Habit

SCHEMA = "streakBotDB"
USERS = "users"
HABITS = "habitsDB"


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


def add_habit(habit: Habit, userId):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        paramList = [
            '"habitName"',
            '"desc"',
            '"freq"',
            '"startDate"',
            '"numStreaks"',
            '"userID"',
        ]
        paramsListStr = ", ".join(param for param in paramList)
        add_habit_query = f'INSERT INTO "{SCHEMA}"."{HABITS}" ({paramsListStr}) VALUES ({habit.parseToDB()}, \'{str(userId)}\');'
        print(add_habit_query)
        cur.execute(add_habit_query)
        conn.commit()
        print("Query was executed successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_habits(user_Id):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        view_habit_query = (
            f'SELECT * FROM "{SCHEMA}"."{HABITS}" WHERE "userID"=\'{str(user_Id)}\''
        )
        cur.execute(view_habit_query)
        result = cur.fetchall()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == "__main__":
    # x = view_habits("1")[1]
    # print(Habit.formatStringFromDB(x))
    pass
    # habit = Habit()
    # habit.name = "name"
    # habit.freq = "daily"
    # habit.desc = "test"
    # habit.streaks = 0
    # habit.time = "20201209"
    # add_habit(habit, "123")
