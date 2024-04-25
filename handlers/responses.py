import neuronBot
from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import keyboard_dislike_like
from datetime import datetime as dt
from data import database

router = Router()

@router.message(F.text.lower())
async def response_message(message: Message):
    LSTM_text = message.text.lower()
    await message.reply(LSTM_text,
                        reply_markup=keyboard_dislike_like)
    formatted_date = dt.strftime(message.date,"%Y-%m-%d")
    await database.add_message(message.chat.id, message.message_id, message.text.lower(), LSTM_text.lower(), formatted_date)