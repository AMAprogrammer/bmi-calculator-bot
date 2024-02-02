from botconfig import bot
from pyrogram import filters
from pyrogram.types import Message
from keyboards import main_keyboard
from database_config import bmi
from tools import calculator



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
    
    user_id = message.from_user.id
    text = message.text
    users = bmi["USERS"]
    user = users.find_one({"_id":user_id})
    if user:
        user_step = user["step"]
        if user_step == "home":
            
            await bot.send_message(chat_id=user_id, text="قد خود را وارد کنید:")
            users.update_one({"_id":user_id},{"$set":{"step":"get_height"}})
            
        elif user_step == "get_height":
            
            try:
                height = float(text)
            except:
                await bot.send_message(chat_id=user_id, text="لطفا قد خود را با فرمت صحیح ارسال کنید!")
            else:
                users.update_one({"_id":user_id},{"$set":{"height":height}})
                users.update_one({"_id":user_id},{"$set":{"step":"get_weight"}})
                await bot.send_message(chat_id=user_id, text="وزن خود را وارد کنید:")

        elif user_step == "get_weight":
            
            try:
                weight = float(text)
            except:
                await bot.send_message(chat_id=user_id, text="لطفا وزن خود را با فرمت صحیح ارسال کنید!")
            else:  
                users.update_one({"_id":user_id},{"$set":{"weight":weight}})
                users.update_one({"_id":user_id},{"$set":{"step":"home"}})
                user = users.find_one({"_id":user_id})
                height = user["height"]
                weight = user["weight"]
                result = calculator(height=height, weight=weight)
                await bot.send_message(chat_id=user_id, text=f"BMI شما:\n\n{result}\n\nبرای بازگشت به منوی اصلی /start را بزنید")                