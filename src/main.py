from botconfig import bot
from pyrogram import filters
from pyrogram.types import Message
from keyboards import main_keyboard
from database_config import bmi



@bot.on_message(filters=filters.private & filters.command("start"))
async def main_menu(client, message:Message):
    user_id = message.from_user.id
    users = bmi["USERS"]
    user = users.find_one({"_id":user_id})
    if user:
        user_step = user["step"]
        user_bmi = user["bmi"]
        user_height = user["height"]
        user_weight = user["weight"]
    else:
        users.insert_one({"_id":user_id,"step":"home","bmi":None,"height":None,"weight":None})
        user_step = "home"
    
    if user_step == "home":
        bot.send_message(chat_id=user_id,
                        text="سلام به ربات محاسبه شاخص توده بدنی خوش آمدید",
                        reply_markup=main_keyboard)


@bot.on_message(filters=filters.private & filters.regex("محاسبه BMI من"))
async def calculate_bmi(client, message:Message):
