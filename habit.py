from datetime import datetime


class Habit:
    def __init__(self):
        self.id = None
        self.name = None
        self.desc = None
        self.reminderTime = None
        self.streaks = 0
        # self.lastUpdatedTime = datetime.now()

    @classmethod
    def createHabit(cls, name, desc, reminderTime):
        habit = Habit()
        habit.name = name
        habit.desc = desc
        habit.reminderTime = datetime.strptime(reminderTime, "%H:%M")
        habit.streaks = 0
        # habit.lastUpdatedTime = datetime.now()
        return habit

    @classmethod
    def createHabitFromDB(cls, dbResult):
        habit = Habit()
        habit.id = dbResult[0]
        habit.name = dbResult[1]
        habit.desc = dbResult[2]
        habit.reminderTime = dbResult[3]  # datetime.strptime(dbResult[3], "%H:%M")
        habit.streaks = dbResult[4]
        # habit.lastUpdatedTime = dbResult[5]
        return habit

    def parseToDB(self):
        return f"{self.name}, {self.desc}, {self.reminderTime.strftime('%H:%M')}"

    @classmethod
    def formatStringFromDB(cls, dbResult):
        habit = Habit.createHabitFromDB(dbResult)
        return habit.toString()

    def toString(self):
        result = ""
        result += f"Name of habit: {self.name}\n"
        result += f"Description: {self.desc}\n"
        result += f"Reminder Time: {self.reminderTime.strftime('%H:%M')}\n"
        result += f"Streaks: {str(self.streaks)}\n"
        return result

    @classmethod
    def formatHabitTuple(cls, habitTuple):
        habit = Habit.createHabitFromDB(habitTuple)
        return habit.toString()
