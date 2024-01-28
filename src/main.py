from botconfig import bot
from telebot.types import Message
from keyboards import main_keyboard
from tools import calculator
from classes import User


user_dict = {}

@bot.message_handler(commands=["start"],chat_types=["private"])
def main_menu(message:Message):
    bot.send_message(chat_id=message.chat.id,text="سلام به ربات محاسبه شاخص توده بدنی(BMI) خوش آمدید",reply_markup=main_keyboard)


def start_calculate(message:Message):
    
    msg = bot.send_message(chat_id=message.chat.id,text="نام خود را وارد کنید")
    bot.register_next_step_handler(message=msg,callback=process_name_step)


def process_name_step(message:Message):
    name = message.text
    chat_id = message.chat.id
    user = User(name)
    user_dict[chat_id] = user
    msg = bot.send_message(chat_id=message.chat.id,text="قد خود را وارد کنید :")
    bot.register_next_step_handler(message=msg, callback=process_height_step)


def process_height_step(message:Message):
    try:
        chat_id = message.chat.id
        height = float(message.text)
        user:User = user_dict[chat_id]
        user.height = height
        msg = bot.send_message(chat_id=message.chat.id,text="وزن خود را وارد کنید :")
    except:
        msg = bot.send_message(chat_id=message.chat.id,text="خطا❗❗ قد را با فرمت صحیح ارسال کنید")
        bot.register_next_step_handler(message=msg, callback=process_height_step)
        return
    bot.register_next_step_handler(message=msg, callback=process_weight_step)
    
    
    
def process_weight_step(message:Message):
    chat_id = message.chat.id
    try:
        weight = float(message.text)
        user:User = user_dict[chat_id]
        user.weight = weight
    except:
        msg = bot.send_message(chat_id=message.chat.id,text="خطا❗❗ وزن را با فرمت صحیح ارسال کنید")
        bot.register_next_step_handler(message=msg, callback=process_weight_step)
        return
    height = user.height
    weight = user.weight
    result = calculator(height,weight)
    
    bot.send_message(chat_id=chat_id,text=f"وزن : {weight}\nقد : {height}\nBMI : {result}")
    user_dict.__delitem__(chat_id)