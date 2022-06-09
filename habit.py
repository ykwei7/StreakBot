class Habit:
    def __init__(self):
        self.name = None
        self.desc = None
        self.freq = None
        self.time = None
        self.streaks = 0

    def parseToDB(self):
        return f"'{self.name}', '{self.desc}', '{self.freq}', TO_DATE('{self.time}', 'YYYYMMDD'), '{str(self.streaks)}'"
