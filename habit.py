from datetime import datetime


class Habit:
    def __init__(self):
        self.name = None
        self.desc = None
        self.reminderTime = None
        self.streaks = 0

    @classmethod
    def createHabit(cls, name, desc, reminderTime):
        habit = Habit()
        habit.name = name
        habit.desc = desc
        habit.reminderTime = reminderTime
        habit.streaks = 0
        return habit

    @classmethod
    def createHabitFromDB(cls, dbResult):
        habit = Habit()
        habit.name = dbResult[1]
        habit.desc = dbResult[2]
        habit.reminderTime = dbResult[3]
        habit.streaks = dbResult[4]
        return habit

    def parseToDB(self):
        return f"{self.name}, {self.desc}, {self.reminderTime}"

    @classmethod
    def formatStringFromDB(cls, dbResult):
        habit = Habit.createHabitFromDB(dbResult)
        return habit.toString()

    def toString(self):
        result = ""
        result += f"Name of habit: {self.name}\n"
        result += f"Description: {self.desc}\n"
        result += f"Reminder Time: {self.reminderTime}\n"
        result += f"Streaks: {str(self.streaks)}\n"
        return result

    @classmethod
    def formatHabitTuple(cls, habitTuple):
        result = ""
        result += f"Name of habit: {habitTuple[1]}\n"
        result += f"Description: {habitTuple[2]}\n"
        result += f"Reminder Time: {str(habitTuple[3])}\n"
        result += f"Streaks: {str(habitTuple[4])}\n"
        return result
