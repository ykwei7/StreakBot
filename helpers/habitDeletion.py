from database import (
    add_user,
    delete_habit_in_db,
    get_habits,
    add_habit_to_db,
    update_habit,
    clear_user_habits,
    get_all_habits,
)

import re
from habit.habit import Habit


class HabitDeletion:
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler
    
    def view_habits(self, user_id, chat_id):
        data = get_habits(str(user_id))
        if data is None or len(data) == 0:
            self.bot.send_message(chat_id, "No habits found! Create a habit to start")
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
                pm.chat.id, "This does not seem to be a valid number!\n\n Try again!"
            )
            return
        elif int(idx) > len(data) or int(idx) <= 0:
            self.bot.send_message(
                pm.chat.id,
                "The index provided does not fall within the list!\n\n Try again!",
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
