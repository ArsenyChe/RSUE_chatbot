from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from messages import TEXT_START

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.full_name}, '+ TEXT_START)
    await message.delete()