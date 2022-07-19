from database import (
    add_user,
    delete_habit_in_db,
    get_habits,
    add_habit_to_db,
    update_habit,
    clear_user_habits,
    get_all_habits,
)

from habit.habit import Habit

class HabitRetrieval:
    def __init__(self, bot):
        self.bot = bot
    
    def view_habits(self, user_id, chat_id):
        @self.bot.message_handler(content_types=["text"])
        def view_habits_helper():
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
        view_habits_helper()