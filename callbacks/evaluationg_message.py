from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from messages import TEXT_FEEDBACK
from keyboards.inline import keyboard_thanks
from data import database_message

router = Router()

@router.callback_query(F.data.in_(['ib_heart','ib_broken_heart']))
async def evaluationg_message(callback: CallbackQuery, bot: Bot):
    evaluation_response = True if callback.data  == 'ib_heart' else False
    
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, 
                                        message_id=callback.message.message_id, 
                                        reply_markup=keyboard_thanks)
    await callback.message.answer(TEXT_FEEDBACK)
    await database_message.update_message(evaluation_response, callback.message.chat.id, callback.message.reply_to_message.message_id)
    await callback.answer()