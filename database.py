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
        query = f'SELECT * FROM "{SCHEMA}".{USERS}'
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
    # TODO: Add exception handling when user is already added
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO "streakBotDB"."users" VALUES (%(userId)s)',
            {"userId": str(userId)},
        )
        conn.commit()
        print("Query was executed successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def add_habit_to_db(habit: Habit, userId: str):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        paramList = [
            '"habitName"',
            '"desc"',
            '"reminderTime"',
            '"userID"',
        ]
        # paramsListStr = ", ".join(param for param in paramList)
        cur.execute(
            'INSERT INTO "streakBotDB"."habitsDB" ("habitName", "desc", "reminderTime", "userID") VALUES (%(habitName)s, %(desc)s, %(reminderTime)s, %(userId)s)',
            {
                "habitName": habit.name,
                "desc": habit.desc,
                "reminderTime": habit.reminderTime,
                "userId": str(userId),
            },
        )
        conn.commit()
        print("Query was executed successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_habits(userId: str):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s',
            {
                "userId": str(userId),
            },
        )
        print("Fetching results..")
        result = cur.fetchall()
        print("Fetched result")
        print(result)
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_habit_in_db(userId, habit):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            'DELETE FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s AND "habitID" = %(habitID)s',
            {
                "habitID": habit[0],
                "userId": str(userId),
            },
        )
        conn.commit()
        print("Query was executed successfully")
        return
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return


if __name__ == "__main__":
    # x = get_habits("612160086")
    # print(x)
    # print(type(Habit.createHabit("test", "testdesc", "08:00")))
    # add_habit_to_db(Habit.createHabit("test", "testdesc", "08:00"), "123")
    # x = get_habits("123")[0]
    # print(get_habits("123"))
    # delete_habit_in_db("123", x)
    # print(get_habits("123"))
    pass
