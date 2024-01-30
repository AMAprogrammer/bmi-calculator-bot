from botconfig import bot
from pyrogram import filters
from pyrogram.types import Message
from keyboards import main_keyboard



@bot.on_message(filters=filters.private & filters.command(["start","cancel"]))
async def main_menu(client, message:Message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text="سلام به ربات محاسبه شاخص توده بدنی خوش آمدید",
                     reply_markup=main_keyboard)


@bot.on_message(filters=filters.private & filters.regex("محاسبه BMI من"))
async def calculate_bmi(client, message:Message):
    chat_id = message.chat.id
    