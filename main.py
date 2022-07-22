import os
import re
import telebot

from dotenv import load_dotenv
from datetime import date
from habit.habit import Habit
from telebot.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database import (
    add_user,
    delete_habit_in_db,
    get_habits,
    add_habit_to_db,
    update_habit,
    clear_user_habits,
    get_all_habits,
)
from utils.messages import (
    WELCOME_MESSAGE,
    ERR_FUNC_NOT_FOUND_MESSAGE
)
from utils.logger import Logger
from helpers.habitRetrieval import HabitRetrieval
from helpers.habitCreation import HabitCreation
from helpers.habitDeletion import HabitDeletion
from helpers.habitUpdate import HabitUpdate
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv("secret.env")
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

scheduler = BackgroundScheduler(timezone="Asia/Taipei")

logger = Logger.config("Main")
habitRetrieval = HabitRetrieval(bot, logger)
habitCreation = HabitCreation(bot, scheduler, logger)
habitUpdate = HabitUpdate(bot, logger)
habitDeletion = HabitDeletion(bot, scheduler)

bot.set_my_commands(
    [
        BotCommand("start", "Starts the bot"),
        BotCommand("help", "Get list of commands"),
        BotCommand("clear", "Clears all habits"),
        BotCommand("add", "Create a habit"),
        BotCommand("delete", "Delete a habit"),
        BotCommand("view", "View all habits"),
        BotCommand("update", "Update a habit"),
    ]
)

functionsMapping = {
    "view": "View all habits",
    "add": "Add habit",
    "delete": "Delete habit",
    "update": "Update streak",
    "reminder_update": 'update_habit'
}


@bot.message_handler(commands=["start"])
def start(message):
    """
    Command that welcomes the user and adds userid to db
    """
    user_id = message.from_user.id
    add_user(str(user_id))
    chat_id = message.chat.id
    bot.send_message(chat_id, WELCOME_MESSAGE)
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
    data_identifer = data.split()[0]
    try:
        if data == functionsMapping["view"]:
            habitRetrieval.view_habits(user_id, chat_id)
            return
        elif data == functionsMapping["add"]:
            habitCreation.add_habit(chat_id)
            return
        elif data == functionsMapping["delete"]:
            habitDeletion.delete_habit(user_id, chat_id)
            return
        elif data == functionsMapping["update"]:
            habitUpdate.update_streak(user_id, chat_id)
        elif data_identifer == functionsMapping['reminder_update']:
            habitUpdate.update_single_habit(user_id, chat_id, data)
        else:
            logger.warning("Function not found during /help callback")
            bot.send_message(chat_id, ERR_FUNC_NOT_FOUND_MESSAGE)
    except Exception as e:
        logger.error(e)



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

def remind(habit: Habit, chat_id=None, user_id=None):
    buttons = [[InlineKeyboardButton(
            'Completed', callback_data=f'update_habit {habit.id}' 
        )]]
    if chat_id:
        bot.send_message(
            chat_id,
            f"Remember to do your habit today!\n\n{habit.toString()}",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown",
        )

    elif user_id:
        bot.send_message(
            user_id,
            f"Remember to do your habit today!\n\n{habit.toString()}",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown",
        )
    else:
        logger.error('No ID found for reminder')

def set_all_jobs():
    habits = get_all_habits()
    if habits is None:
        logger.info('No habits to reboot')
        return
    logger.info('Adding habits to scheduler')
    for habit in habits:
        user_id = str(habit[5])
        habit = Habit.createHabitFromDB(habit)
        unique_id = str(habit.id) + "-user-" + user_id
        currDate = date.today().strftime("%Y-%m-%d")
        scheduler.add_job(remind, trigger='interval', days = 1, start_date=f"{currDate} {habit.reminderTime}", jobstore="default", args=[habit, None, user_id], replace_existing=True, id=unique_id, misfire_grace_time=30)
    

@bot.message_handler(commands=["view"])
def view(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    habitRetrieval.view_habits(user_id, chat_id)

@bot.message_handler(commands=["add"])
def add_habit(message):
    chat_id = message.chat.id
    habitCreation.add_habit(chat_id)

@bot.message_handler(commands=["delete"])
def delete_habit(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    habitDeletion.delete_habit(user_id, chat_id)


@bot.message_handler(commands=["delete"])
def update_habit(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    habitUpdate.update_streak(user_id, chat_id)

logger.info("Telegram bot starting up")
scheduler.start()
scheduler.remove_all_jobs()
set_all_jobs()
logger.info("Telegram bot running")
bot.polling()
