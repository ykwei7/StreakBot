from database import (
    update_habit,
    get_habit_by_id
)
import re
from habit.habit import Habit

from helpers.helpers import view_concise_habits

from utils.messages import ERR_INVALID_INDEX_MESSAGE , ERR_INDEX_OUT_OF_BOUNDS_MESSAGE, UPDATE

class HabitUpdate:
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
    
    def update_streak(self, user_id, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def update_streak_helper():
            view_concise_habits(self.bot, user_id, chat_id, type=UPDATE)
            return
        update_streak_helper()


    def handle_update(self, user_id, chat_id, data):
        currentHabit = get_habit_by_id(data.split()[1])
        habitToBeUpdated = Habit.createHabitFromDB(currentHabit)
        update_habit(str(user_id), currentHabit, "numStreaks", habitToBeUpdated.streaks + 1)
        habitToBeUpdated.streaks += 1
        self.bot.send_message(
            chat_id,
            f"Have updated the following habit:\n\n{habitToBeUpdated.toString()}",
            parse_mode="Markdown",
        )

    def update_single_habit(self, user_id, chat_id, data):
        try:
            currentHabit = get_habit_by_id(str(data.split()[1]))
            habitToBeUpdated = Habit.createHabitFromDB(currentHabit)
            update_habit(str(user_id), currentHabit, "numStreaks", habitToBeUpdated.streaks + 1)
            habitToBeUpdated.streaks += 1
            self.bot.send_message(
                chat_id,
                f"Have updated the following habit:\n\n{habitToBeUpdated.toString()}",
                parse_mode="Markdown",
            )
        except Exception as e:
            self.logger.error(e)


