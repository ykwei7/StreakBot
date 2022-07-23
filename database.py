#!/usr/bin/python
import psycopg2
from utils.config import config
from habit.habit import Habit
from datetime import date
from utils.logger import Logger

SCHEMA = "streakBotDB"
USERS = "users"
HABITS = "habitsDB"

logger = Logger.config("PostgreSQL")


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()
        logger.info("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        logger.info("PostgreSQL database version: " + db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed.")


def view_all_users():
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        query = f'SELECT * FROM "{SCHEMA}".{USERS}'
        cur.execute(query)
        result = cur.fetchall()
        logger.info("Retrieving all users")
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed.")


def add_user(userId: str) -> str:
    """Adds user to database

    Args:
        userId (str): telegram userID of intended user
    """
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO "streakBotDB".users ("userID") VALUES (%(userId)s)',
            {"userId": str(userId)},
        )
        conn.commit()
        logger.info("Adding user to database | " + str(userId))
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def add_habit_to_db(habit: Habit, userId: str):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
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
        cur.execute(
            'SELECT "streakBotDB"."habitsDB"."habitID" FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s ORDER BY "streakBotDB"."habitsDB"."habitID" DESC LIMIT 1',
            {
                "userId": str(userId),
            },
        )
        logger.info("Adding habit to database | " + str(userId))
        return cur.fetchall()[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def get_habits(userId: str):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s ORDER BY "streakBotDB"."habitsDB"."reminderTime"',
            {
                "userId": str(userId),
            },
        )
        result = cur.fetchall()
        logger.info("Reading habits from database for user:" + str(userId))
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def get_all_habits():
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM "streakBotDB"."habitsDB"')
        result = cur.fetchall()
        logger.info("Reading all habits from database")
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def delete_habit_in_db(userId, habit):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'DELETE FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s AND "habitID" = %(habitID)s',
            {
                "habitID": habit[0],
                "userId": str(userId),
            },
        )
        conn.commit()
        logger.info(f"Deleting habit from database | habitId: {habit[0]}")
        return
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    return


def update_habit(userId: str, habit: Habit, field: str, newVal):
    if field == "habitName":
        pass
    elif field == "desc":
        pass
    elif field == "reminderTime":
        pass
    elif field == "numStreaks":
        update_streak(userId, habit, newVal)
        return
    pass


def update_streak(userId, habit, newVal):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'UPDATE "streakBotDB"."habitsDB" SET "numStreaks" = %(newVal)s, "lastUpdated" = %(now)s  WHERE "userID" = %(userId)s AND "habitID" = %(habitID)s',
            {
                "habitID": habit[0],
                "userId": str(userId),
                "newVal": newVal,
                "now": date.today(),
            },
        )
        conn.commit()
        logger.info(f"Updating streak of habitID: {habit[0]}")
        return
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    return


def clear_user_habits(userId):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'DELETE FROM "streakBotDB"."habitsDB" WHERE "userID" = %(userId)s',
            {
                "userId": str(userId),
            },
        )
        conn.commit()
        logger.info(f"Deleting all habits from userId: {str(userId)}")
        return
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    return

def get_habit_by_id(habitID: str):
    try:
        params = config()
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM "streakBotDB"."habitsDB" WHERE "streakBotDB"."habitsDB"."habitID" = %(habitID)s',
            {
                "habitID": str(habitID),
            },
        )
        result = cur.fetchall()
        logger.info(f"Retrieving habit: {str(habitID)}")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        return None
    return result[0]


if __name__ == "__main__":
    connect()
    pass
