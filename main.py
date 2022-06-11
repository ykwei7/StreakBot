import os
import json
from venv import create
from dotenv import load_dotenv
import telebot
from telebot.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedSticker,
)
from habit import Habit
from database import add_user, get_habits

load_dotenv("secret.env")
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

# user_id = "612160086"

bot.set_my_commands([BotCommand("start", "Starts the bot")])

functionsMapping = {
    "view": "View all habits",
    "add": "Add habit",
    "delete": "Delete habit",
}

freqMapping = {"daily": "Daily", "weekly": "Weekly"}


@bot.message_handler(commands=["start"])
def start(message):
    """
    Command that welcomes the user and adds userid to db
    """
    user_id = message.from_user.id
    add_user(str(user_id))
    chat_id = message.chat.id
    message = "Welcome to Streak-o!"

    bot.send_message(chat_id, message)
    return None


@bot.message_handler(commands=["help"])
def help(message):
    chat_id = message.chat.id
    message = "View, add or delete a habit"
    buttons = []
    for key in functionsMapping:
        row = []
        option = InlineKeyboardButton(
            functionsMapping[key], callback_data=functionsMapping[key]
        )
        row.append(option)
        buttons.append(row)

    bot.send_message(
        chat_id, message, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML"
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    err_msg = "Function not found"

    if data == functionsMapping["view"]:
        view_habits(user_id, chat_id)
        return
    elif data == functionsMapping["add"]:
        add_habit(chat_id)
        return
    elif data == functionsMapping["delete"]:
        delete_habit(user_id, chat_id)
        return
    else:
        bot.send_message(chat_id, err_msg)


@bot.message_handler(content_types=["text"])
def add_habit(chat_id):
    message = "What is the name of the habit that you hope to cultivate?"
    msg = bot.send_message(chat_id, message)
    bot.register_next_step_handler(msg, process_name_step)
    return


@bot.message_handler(content_types=["text"])
def process_name_step(message):
    name = message.text
    chat_id = message.chat.id
    habit = Habit()
    habit.name = name
    successMsg = f"Habit: {habit.name} is added"
    # call function to add into DB
    bot.send_message(chat_id, successMsg)
    print(successMsg)


def view_habits(user_id, chat_id):
    data = get_habits(user_id)
    habits = [Habit.formatStringFromDB(result) for result in data]
    msg = "\n".join(habits)
    bot.send_message(chat_id, msg)
    return


def delete_habit(user_id, chat_id):
    # TODO Create function once DB is setup
    return


# upon setup, append to json file with userid
# stores array of Habit objects
# Habit: int id, string text unique, string description, string frequency
# int streaks, Time time
# MVP: way to add Habit object, delete Habit object
# good to have: edit habit object
#
print("Telegram bot running")
bot.polling()


# Users table
# userID

# Habit table
# HabitID
# userID FK
# Habit Name varchar(20)
# Habit desc TEXT
# Habit freq varchar(20)
# Habit time DATE
# Habit streaks int
