from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import get_habits

from utils.messages import ERR_NO_HABITS_FOUND_MESSAGE, DELETE, UPDATE, ERR_INVALID_OPERATION_MESSAGE

from habit.habit import Habit

from utils.logger import Logger

logger = Logger.config('helper')

def view_concise_habits(bot, user_id: str, chat_id: str, type: str):
    """ View menu list of habits for desired operation

    Args:
        user_id (str): user_id specified
        chat_id (str): current chat
        type (str): "DELETE" or "UPDATE" operation
    """
    if type != DELETE and type != UPDATE:
        bot.send_message(chat_id, ERR_INVALID_OPERATION_MESSAGE)
        return

    data = get_habits(str(user_id))
    if data is None or len(data) == 0:
        bot.send_message(chat_id, ERR_NO_HABITS_FOUND_MESSAGE)
        return None
    
    habitList = [Habit.createHabitFromDB(habit) for habit in data]

    buttons = []
    index = 1
    for habit in habitList:
        row = []
        if type == UPDATE:
            habit_info = f"{index}. {habit.name}\n Streaks: {habit.streaks}"
        elif type == DELETE:
            habit_info = f"{index}. {habit.name}"
        option = InlineKeyboardButton(
            habit_info, callback_data=f"{type} {habit.id}"
        )
        row.append(option)
        buttons.append(row)
        index += 1

    if type == DELETE:
        message = "Which habit would you like to delete?"
    elif type == UPDATE:
        message = "Which habit would you like to update?"
    bot.send_message(
        chat_id, message, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML"
    )
