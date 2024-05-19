from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import database
from messages import TEXT_START, TEXT_ADMIN, TEXT_PERMISSION_ERROR
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

router = Router()

admin_username: list[str] = [getenv('ADMIN_USERNAME')]

# фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_username: list[str]) -> None:
        self.admin_username = admin_username

    async def __call__(self, message: Message) -> bool:
        return message.from_user.username in self.admin_username


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.username } {message.from_user.full_name}, '+ TEXT_START)
    await message.delete()

@router.message(IsAdmin(admin_username), Command("show_questions"))
async def cmd_show_questions(message: Message, command: CommandObject):
    command_len = 4
    if len(message.text.split()) == command_len:
        date, to_date, evaluation_response = command.args.split()
        try:
            time.strptime(date, "%Y-%m-%d")
            time.strptime(to_date, "%Y-%m-%d")
            questions = await database.show_questions(date, to_date, evaluation_response)
            await message.answer('\n'.join(map(str, questions))) if questions is not None else await message.answer('Пусто')
        except (ValueError, TypeError):
            await message.answer('Формат даты должен быть таким: %Y-%m-%d')
    else: await message.answer('Команда написана неправильно. /show_questions [ОТ ДАТЫ] [ДО ДАТЫ] [РЕАКЦИЯ НА ОТВЕТ НЕЙРОСЕТИ]')

@router.message(IsAdmin(admin_username), Command("show_patterns"))
async def cmd_show_patterns(message: Message, command: CommandObject):
    pass

@router.message(IsAdmin(admin_username), Command("nn_training"))
async def cmd_nn_training(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("add_intent"))
async def cmd_add_intent(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("delete_intent"))
async def cmd_delete_intentt(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("output_dataset"))
async def cmd_output_dataset(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("add_pattern"))
async def cmd_add_pattern(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("delete_pattern"))
async def cmd_delete_pattern(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("add_response"))
async def cmd_add_response(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("delete_response"))
async def cmd_delete_response(message: Message):
    pass

@router.message(IsAdmin(admin_username), Command("help"))
async def cmd_help(message: Message):
    admin_rights = True
    await message.answer(TEXT_ADMIN) if admin_rights else await message.answer(TEXT_PERMISSION_ERROR)
    await message.delete()