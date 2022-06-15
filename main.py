import os
import re
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
from database import add_user, delete_habit_in_db, get_habits, add_habit_to_db

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
    bot.register_next_step_handler(msg, name_handler)
    return


def name_handler(pm):
    print(type(pm))
    name = pm.text
    sent_msg = bot.send_message(
        pm.chat.id,
        f"{name} sounds like a great habit to cultivate. Would you mind describing it briefly?",
    )
    bot.register_next_step_handler(sent_msg, desc_handler, name)


def desc_handler(pm, name):
    desc = pm.text
    sent_msg = bot.send_message(
        pm.chat.id,
        f"Got it! {name} : {desc}.\n\nWhat time would you like to receive the reminders? Please key it in an HH:MM format, for e.g 08:00",
    )
    bot.register_next_step_handler(sent_msg, reminder_time_handler, name, desc)


def reminder_time_handler(pm, name, desc):
    time = pm.text
    regex = re.compile("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$")
    if regex.match(time) is None:
        bot.send_message(pm.chat.id, "Format of time is not correct!\n\n Try again!")
        return
    habit = Habit.createHabit(name, desc, time)
    add_habit_to_db(habit, pm.from_user.id)
    bot.send_message(
        pm.chat.id, f"Have created the following habit!\n\n{habit.toString()}"
    )
    return


def view_habits(user_id, chat_id):
    data = get_habits(str(user_id))
    if data is None:
        bot.send_message(chat_id, "No habits found! Create a habit to start")
        return
    habits = [Habit.formatStringFromDB(result) for result in data]
    msg = "\n".join(habits)
    bot.send_message(chat_id, msg)
    return data


@bot.message_handler(content_types=["text"])
def delete_habit(user_id, chat_id):
    data = view_habits(user_id, chat_id)
    msg = bot.send_message(
        chat_id,
        "Which habit would you like to delete? Key in the corresponding number.",
    )
    bot.register_next_step_handler(msg, delete_handler, data)
    return


def delete_handler(pm, data):
    idx = pm.text
    regex = re.compile("^\d+$")
    chat_id = pm.chat.id
    user_id = pm.from_user.id

    if regex.match(idx) is None:
        bot.send_message(
            pm.chat.id, "This does not seem to be a valid number!\n\n Try again!"
        )
        return
    elif int(idx) > len(data) or int(idx) <= 0:
        bot.send_message(
            pm.chat.id,
            "The index provided does not fall within the list!\n\n Try again!",
        )
        return

    deletedHabit = data[int(idx) - 1]
    print(type(deletedHabit))
    print(deletedHabit)
    delete_habit_in_db(user_id, deletedHabit)
    bot.send_message(
        chat_id,
        f"Have deleted the following habit:\n\n {Habit.formatHabitTuple(deletedHabit)}",
    )


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
# HabitID Autogenerated
# userID FK
# Habit Name varchar(20)
# Habit desc TEXT
# Habit reminderTime Time
# Habit streaks int => Do not get from user
