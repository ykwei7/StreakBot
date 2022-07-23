from database import (
    delete_habit_in_db,
    get_habit_by_id,
)

from helpers.helpers import view_concise_habits

import re
from habit.habit import Habit
from utils.messages import DELETE


class HabitDeletion:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler

    def delete_habit(self, user_id, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def delete_habit_helper():
            view_concise_habits(self.bot, user_id, chat_id, type=DELETE)
        delete_habit_helper()

    def handle_delete(self, user_id, chat_id, data):
        deletedHabit = get_habit_by_id(data.split()[1])
        delete_habit_in_db(str(user_id), deletedHabit)
        self.scheduler.remove_job(str(deletedHabit[0]) + "-user-" + str(user_id))
        self.bot.send_message(
            chat_id,
            f"Have deleted the following habit:\n\n{Habit.formatHabitTuple(deletedHabit)}",
            parse_mode="Markdown",
        )
