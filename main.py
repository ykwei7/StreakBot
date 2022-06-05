import os
from dotenv import load_dotenv
import telebot
from telebot.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedSticker,
)

load_dotenv("secret.env")
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([BotCommand("start", "Starts the bot")])

functionsMapping = {
    "view": "View all habits",
    "add": "Add habit",
    "delete": "Delete habit",
}

freqMapping = {"daily": "Daily", "weekly": "Weekly", "monthly": "Monthly"}


@bot.message_handler(commands=["start"])
def start(message):
    """
    Command that welcomes the user and adds userid to db
    """
    user_id = message.from_user.id
    # add user_id to database
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
    """
      Handles the execution of the respective functions upon receipt of the
    callback query
    """

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    err_msg = "Function not found"

    if data == functionsMapping["view"]:
        view_habits(user_id, chat_id)
        return
    elif data == functionsMapping["add"]:
        add_habit(user_id, chat_id)
        return
    elif data == functionsMapping["delete"]:
        delete_habit(user_id, chat_id)
        return
    elif data == freqMapping["daily"]:
        return
    elif data == freqMapping["weekly"]:
        bot.send_message(chat_id, "weekly")
        return
    elif data == freqMapping["monthly"]:
        bot.send_message(chat_id, "monthly")
        return
    else:
        bot.send_message(chat_id, err_msg)


"""
Functions to add habit
"""


@bot.message_handler(content_types=["text"])
def add_habit(user_id, chat_id):
    message = "What is the name of the habit that you hope to cultivate?"
    msg = bot.send_message(chat_id, message)
    bot.register_next_step_handler(msg, desc_handler)


def desc_handler(pm):
    habit = Habit.createHabit()
    habit.setText(pm.text)
    msg = f"{pm.text} sounds like a great name! How should we describe this habit?"
    sent_msg = bot.send_message(pm.chat.id, msg)
    bot.register_next_step_handler(sent_msg, freq_handler, habit)


def freq_handler(pm, habit):
    desc = pm.text
    habit.setDesc(desc)
    msg = "How often should we have it?"
    buttons = []
    for key in freqMapping:
        row = []
        option = InlineKeyboardButton(freqMapping[key], callback_data=freqMapping[key])
        row.append(option)
        buttons.append(row)
    bot.send_message(
        pm.chat.id, msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML"
    )


"""
End of functions to add habit
"""


def view_habits(user_id, chat_id):
    return


def delete_habit(user_id, chat_id):
    return


# upon setup, append to json file with userid
# stores array of Habit objects
# Habit: int id, string text unique, string description, string frequency
# int streaks, Time time
# MVP: way to add Habit object, delete Habit object
# good to have: edit habit object
#
bot.polling()
