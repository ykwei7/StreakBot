class Habit:
    def __init__(self):
        self.name = None
        self.desc = None
        self.freq = None
        self.time = None
        self.streaks = 0

    @classmethod
    def createHabitFromDB(cls, dbResult):
        habit = Habit()
        habit.name = dbResult[1]
        habit.desc = dbResult[2]
        habit.freq = dbResult[3]
        habit.time = dbResult[4]
        habit.streaks = dbResult[5]
        return habit

    def parseToDB(self):
        return f"'{self.name}', '{self.desc}', '{self.freq}', TO_DATE('{self.time}', 'YYYYMMDD'), '{str(self.streaks)}'"

    @classmethod
    def formatStringFromDB(cls, dbResult):
        habit = Habit.createHabitFromDB(dbResult)
        return habit.toString()

    def toString(self):
        result = ""
        result += f"Name of habit: {self.name}\n"
        result += f"Description: {self.desc}\n"
        result += f"Frequency: {self.freq}\n"
        result += f"Streaks: {str(self.streaks)}\n"
        return result
