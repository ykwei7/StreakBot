class Habit:
    def __init__(self):
        self.name = None
        self.desc = None
        self.freq = None
        self.time = None
        self.streaks = 0


def create_habit(msg):
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    name = message.text
    user_id = message.user_id
    habit = Habit()
    habit.name = name
    print(f"habit {habit.name} is added to {user_id}")
