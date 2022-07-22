from database import (
    delete_habit_in_db,
    get_habits,
)

import re
from habit.habit import Habit
from utils.messages import ERR_NO_HABITS_FOUND_MESSAGE, ERR_INVALID_INDEX_MESSAGE, ERR_INDEX_OUT_OF_BOUNDS_MESSAGE


class HabitDeletion:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler
    
    def view_habits(self, user_id, chat_id):
        data = get_habits(str(user_id))
        if data is None or len(data) == 0:
            self.bot.send_message(chat_id, ERR_NO_HABITS_FOUND_MESSAGE)
            return None
        habits = [
            f"*#{str(i+1)}* " + Habit.formatStringFromDB(data[i]) for i in range(len(data))
        ]
        msg = "\n".join(habits)
        self.bot.send_message(chat_id, msg, parse_mode="Markdown")
        return data

    def delete_habit(self, user_id, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def delete_habit_helper():
            data = self.view_habits(user_id, chat_id)
            if data is None:
                return
            msg = self.bot.send_message(
                chat_id,
                "Which habit would you like to delete? Key in the corresponding number.",
            )
            self.bot.register_next_step_handler(msg, self.delete_handler, data)
            return
        delete_habit_helper()

    def delete_handler(self, pm, data):
        idx = pm.text
        regex = re.compile("^\d+$")
        chat_id = pm.chat.id
        user_id = pm.from_user.id

        if regex.match(idx) is None:
            self.bot.send_message(
                pm.chat.id, ERR_INVALID_INDEX_MESSAGE
            )
            return
        elif int(idx) > len(data) or int(idx) <= 0:
            self.bot.send_message(
                pm.chat.id,
                ERR_INDEX_OUT_OF_BOUNDS_MESSAGE,
            )
            return

        deletedHabit = data[int(idx) - 1]
        delete_habit_in_db(str(user_id), deletedHabit)
        self.scheduler.remove_job(str(deletedHabit[0]) + "-user-" + str(user_id))
        self.bot.send_message(
            chat_id,
            f"Have deleted the following habit:\n\n{Habit.formatHabitTuple(deletedHabit)}",
            parse_mode="Markdown",
        )
