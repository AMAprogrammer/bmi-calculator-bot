from botconfig import bot
from pyrogram import filters
from pyrogram.types import Message
from keyboards import main_keyboard
from database_config import bmi
from tools import calculator



@bot.on_message(filters=filters.private)
async def main_menu(client, message:Message):
    text = message.text
    user_id = message.from_user.id
    users = bmi["USERS"]
    user = users.find_one({"_id":user_id})
    if user:
        user_step = user["step"]
    else:
        users.insert_one({"_id":user_id,"step":"home","bmi":None,"height":None,"weight":None})
        
    if user_step == "home":
        if text == "/start":

            bot.send_message(chat_id=user_id,
                            text="سلام به ربات محاسبه شاخص توده بدنی خوش آمدید",
                            reply_markup=main_keyboard)


        elif text == "محاسبه BMI من":
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
                
                
                
                
bot.run()