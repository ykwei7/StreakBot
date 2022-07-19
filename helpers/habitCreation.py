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
from datetime import date
from habit.habit import Habit

class HabitCreation:
    def __init__(self, bot, scheduler, logger):
        self.bot = bot
        self.scheduler = scheduler
        self.logger = logger
    
    def add_habit(self, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def add_habit_helper():
            message = "What is the name of the habit that you hope to cultivate?"
            msg = self.bot.send_message(chat_id, message)
            self.bot.register_next_step_handler(msg, self.name_handler)
            return
        add_habit_helper()

    def name_handler(self, pm):
        name = pm.text
        sent_msg = self.bot.send_message(
            pm.chat.id,
            f"{name} sounds like a great habit to cultivate. Would you mind describing it briefly?",
        )
        self.bot.register_next_step_handler(sent_msg, self.desc_handler, name)

    def desc_handler(self, pm, name):
        desc = pm.text
        sent_msg = self.bot.send_message(
            pm.chat.id,
            f"Got it! *{name}: {desc}*.\n\nSet a daily reminder! Please key it in an HH:MM format, for e.g 08:00",
            parse_mode="Markdown",
        )
        self.bot.register_next_step_handler(sent_msg, self.reminder_time_handler, name, desc)

    def reminder_time_handler(self, pm, name, desc):
        time = pm.text
        user_id = pm.from_user.id
        chat_id = pm.chat.id
        regex = re.compile("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$")
        if regex.match(time) is None:
            self.bot.send_message(
                pm.chat.id, "Format of time is not correct!\n\n Try creating a habit again!"
            )
            return
        habit = Habit.createHabit(name, desc, time)
        add_habit_to_db(habit, pm.from_user.id)
        self.bot.send_message(
            pm.chat.id,
            f"Have created the following habit!\n\n{habit.toString()}",
            parse_mode="Markdown",
        )

        reminderTime = habit.getReminderTime()
        unique_id = str(habit.id) + "-user-" + str(user_id)
        currDate = date.today().strftime("%Y-%m-%d")
        self.scheduler.add_job(self.remind, trigger='interval', days = 1, start_date=f"{currDate} {reminderTime}:00", jobstore="default", args=[habit, chat_id], replace_existing=True, id=unique_id, misfire_grace_time=30)
        return
    
    def remind(self, habit: Habit, chat_id=None, user_id=None):
        if chat_id:
            self.bot.send_message(
                chat_id,
                f"Remember to do your habit today!\n\n{habit.toString()}",
                parse_mode="Markdown",
            )
        elif user_id:
            self.bot.send_message(
                user_id,
                f"Remember to do your habit today!\n\n{habit.toString()}",
                parse_mode="Markdown",
            )
        else:
            self.logger.error('No ID found for reminder')