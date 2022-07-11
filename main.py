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
from database import (
    add_user,
    delete_habit_in_db,
    get_habits,
    add_habit_to_db,
    update_habit,
    clear_user_habits,
    get_all_habits,
)
import schedule
from threading import Thread
from time import sleep
import os
import re
from utils.logger import Logger

load_dotenv("secret.env")
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

logger = Logger.config("Main")

bot.set_my_commands(
    [
        BotCommand("start", "Starts the bot"),
        BotCommand("help", "Get list of commands"),
        # BotCommand("add", "Add a habit"),
        # BotCommand("delete", "Delete a habit"),
        # BotCommand("view", "View all habits"),
        # BotCommand("update", "Update a habit"),
        BotCommand("clear", "Clears all habits"),
    ]
)

functionsMapping = {
    "view": "View all habits",
    "add": "Add habit",
    "delete": "Delete habit",
    "update": "Update streak",
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
    logger.info("Application initialized by " + str(user_id))
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
    elif data == functionsMapping["update"]:
        update_streak(user_id, chat_id)
    else:
        logger.error("Function not found during /help callback")
        bot.send_message(chat_id, err_msg)


@bot.message_handler(content_types=["text"])
def add_habit(chat_id):
    message = "What is the name of the habit that you hope to cultivate?"
    msg = bot.send_message(chat_id, message)
    bot.register_next_step_handler(msg, name_handler)
    return


def name_handler(pm):
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
        f"Got it! *{name}: {desc}*.\n\nSet a daily reminder! Please key it in an HH:MM format, for e.g 08:00",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(sent_msg, reminder_time_handler, name, desc)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(58)


def reminder_time_handler(pm, name, desc):
    time = pm.text
    chat_id = pm.chat.id
    regex = re.compile("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$")
    if regex.match(time) is None:
        bot.send_message(
            pm.chat.id, "Format of time is not correct!\n\n Try creating a habit again!"
        )
        return
    habit = Habit.createHabit(name, desc, time)
    add_habit_to_db(habit, pm.from_user.id)
    bot.send_message(
        pm.chat.id,
        f"Have created the following habit!\n\n{habit.toString()}",
        parse_mode="Markdown",
    )

    reminderTime = habit.getReminderTime()
    schedule.every().day.at(reminderTime).do(lambda: remind(habit, chat_id))
    Thread(target=schedule_checker).start()
    return


@bot.message_handler(content_types=["text"])
def view_habits(user_id, chat_id):
    data = get_habits(str(user_id))
    if data is None or len(data) == 0:
        bot.send_message(chat_id, "No habits found! Create a habit to start")
        return None
    habits = [
        f"*#{str(i+1)}* " + Habit.formatStringFromDB(data[i]) for i in range(len(data))
    ]
    msg = "\n".join(habits)
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    return data


@bot.message_handler(content_types=["text"])
def delete_habit(user_id, chat_id):
    data = view_habits(user_id, chat_id)
    if data is None:
        return
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
    delete_habit_in_db(user_id, deletedHabit)
    bot.send_message(
        chat_id,
        f"Have deleted the following habit:\n\n{Habit.formatHabitTuple(deletedHabit)}",
        parse_mode="Markdown",
    )


@bot.message_handler(content_types=["text"])
def update_streak(user_id, chat_id):
    data = view_habits(user_id, chat_id)
    if data is None:
        return
    message = "Which habit did you complete today? Key in the corresponding number"
    msg = bot.send_message(chat_id, message)
    bot.register_next_step_handler(msg, streak_handler, data)
    return


def streak_handler(pm, data):
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
    currentHabit = data[int(idx) - 1]
    habitToBeUpdated = Habit.createHabitFromDB(currentHabit)
    update_habit(str(user_id), currentHabit, "numStreaks", habitToBeUpdated.streaks + 1)
    habitToBeUpdated.streaks += 1
    bot.send_message(
        chat_id,
        f"Have updated the following habit:\n\n{habitToBeUpdated.toString()}",
        parse_mode="Markdown",
    )


def remind(habit: Habit, chat_id):
    bot.send_message(
        chat_id,
        f"Remember to do your habit today!\n\n{habit.toString()}",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["clear"])
def clear_all_habits(message):
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        f"Would you like to clear all existing habits? Type 'YES' to clear all habits or 'NO' to cancel this action.",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, clear_all_handler)


def clear_all_handler(msg):
    if msg.text == "YES":
        clear_user_habits(msg.from_user.id)
        bot.send_message(msg.chat.id, "All habits have been cleared!")
    else:
        bot.send_message(
            msg.chat.id, "Habits were not cleared successfully. Try again!"
        )


print("Telegram bot running")
bot.polling()
