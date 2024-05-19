from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import keyboard_dislike_like
from datetime import datetime as dt
from data import database
from neural_network.neural_network import NeuralNetwork

router = Router()

@router.message(F.text.lower())
async def response_message(message: Message):
    nn = NeuralNetwork("data.json")
    nn.read_data()
    nn.preprocess_data()
    LSTM_text = nn.get_answer(message.text)
    await message.reply(LSTM_text,
                        reply_markup=keyboard_dislike_like)
    formatted_date = dt.strftime(message.date,"%Y-%m-%d")
    await database.add_message(message.chat.id, message.message_id, message.text.lower(), LSTM_text.lower(), formatted_date)