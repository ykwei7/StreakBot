from asyncio.log import logger
from database import (
    update_habit,
    get_habit_by_id
)

import re

from datetime import date

from habit.habit import Habit

from helpers.helpers import view_concise_habits

from utils.messages import UPDATE, STREAK, HABIT_NAME, STREAK, REMINDER_TIME, DESC, UPDATE_STREAK

from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

editSelections = {
    f'EDIT {HABIT_NAME}': 'Name',
    f'EDIT {DESC}': 'Description',
    f'EDIT {REMINDER_TIME}': 'Reminder Time',
}

class HabitUpdate:
    def __init__(self, bot, scheduler, logger):
        self.bot = bot
        self.logger = logger
        self.scheduler = scheduler
    
    def update_streak(self, user_id, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def update_streak_helper():
            view_concise_habits(self.bot, user_id, chat_id, type=UPDATE)
            return
        update_streak_helper()

    def handle_update(self, user_id, chat_id, data):
        currentHabit = get_habit_by_id(data.split()[1])
        habitToBeUpdated = Habit.createHabitFromDB(currentHabit)
        message = f"What would you like to edit?\n\n{habitToBeUpdated.toString()}"

        buttons = []
        for key in editSelections:
            row = []
            option = InlineKeyboardButton(
                editSelections[key], callback_data=f'{key} {habitToBeUpdated.id}'
            )
            row.append(option)
            buttons.append(row)

        self.bot.send_message(
            chat_id, message, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
        )
        return


    def remind(self, habit: Habit, chat_id=None, user_id=None):
        buttons = [[InlineKeyboardButton(
                f'Completed: {habit.name}', callback_data=f'{UPDATE_STREAK} {habit.id}' 
            )]]
        try:
            if chat_id:
                self.bot.send_message(
                    chat_id,
                    f"Remember to do your habit today!\n\n{habit.toString()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode="Markdown",
                )

            elif user_id:
                self.bot.send_message(
                    user_id,
                    f"Remember to do your habit today!\n\n{habit.toString()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode="Markdown",
                )
            else:
                self.logger.error('No ID found for reminder')
        except Exception as e:
            self.logger.error(e)

    def edit_habit(self, user_id, chat_id, data):
        try:
            dataFields = data.split()
            operation = dataFields[1]
            habitId = dataFields[2]
            if operation == HABIT_NAME:
                get_new_habit_name(self, user_id, habitId)
            elif operation == DESC:
                get_new_desc(self, user_id, habitId)
            elif operation == REMINDER_TIME:
                get_new_reminder_time(self, user_id, habitId)
        except Exception as e:
            logger.error(e)

    def update_single_habit(self, user_id, chat_id, data):
        try:
            currentHabit = get_habit_by_id(str(data.split()[1]))
            habitToBeUpdated = Habit.createHabitFromDB(currentHabit)
            update_habit(str(user_id), currentHabit, STREAK, habitToBeUpdated.streaks + 1)
            habitToBeUpdated.streaks += 1
            self.bot.send_message(
                chat_id,
                f"Have updated the following habit:\n\n{habitToBeUpdated.toString()}",
                parse_mode="Markdown",
            )
        except Exception as e:
            self.logger.error(e)
        
    def update_handler(self, msg, user_id, habitId, field):

        habit = get_habit_by_id(habitId)
        newHabit = Habit.createHabitFromDB(update_habit(user_id, habit, field, msg.text))
        
        if field == REMINDER_TIME:
            regex = re.compile("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$")
            if regex.match(msg.text) is None:
                self.bot.send_message(
                    msg.chat.id, "Format of time is not correct!\n\n Try creating a habit again!"
                )
                return
            
            unique_id = str(newHabit.id) + "-user-" + str(user_id)
            currDate = date.today().strftime("%Y-%m-%d")
            self.scheduler.add_job(self.remind, trigger='interval', days = 1, start_date=f"{currDate} {msg.text}:00", jobstore="default", args=[newHabit, None, user_id], replace_existing=True, id=unique_id, misfire_grace_time=30) 
            self.bot.send_message(user_id, f'New reminder timing set to {msg.text}', parse_mode="Markdown")
        
        try:
            self.bot.send_message(user_id, f'Have updated the following habit:\n\n{newHabit.toString()}', parse_mode="Markdown")
        except Exception as e:
            logger.error(e)
        return

def get_new_habit_name(self, user_id, habitId):
    sent_msg = self.bot.send_message(user_id, 'What would you like to rename this habit to?', parse_mode="Markdown")
    self.bot.register_next_step_handler(sent_msg, self.update_handler, user_id, habitId, HABIT_NAME)
    pass

def get_new_desc(self, user_id, habitId):
    sent_msg = self.bot.send_message(user_id, 'What would you like to have as the new description?', parse_mode="Markdown")
    self.bot.register_next_step_handler(sent_msg, self.update_handler, user_id, habitId, DESC)
    pass

def get_new_reminder_time(self, user_id, habitId):
    sent_msg = self.bot.send_message(user_id, 
    'What would you like to be the new reminder time? Please key it in a 24-Hour HH:MM format, for e.g 08:00',
     parse_mode="Markdown")
    self.bot.register_next_step_handler(sent_msg, self.update_handler, user_id, habitId, REMINDER_TIME)
    pass
