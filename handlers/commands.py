from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import database_message, database_admin_log
from messages import TEXT_START, TEXT_ADMIN, TEXT_PERMISSION_ERROR
import time
from os import getenv
from dotenv import load_dotenv
from neural_network.dataset_modification import JSONFileManager 
from neural_network.neural_network_training import NeuralNetworkTraining

load_dotenv()

router = Router()

admin_username: list[str] = [getenv('ADMIN_USERNAME')]

JSON_file_manager = JSONFileManager("data.json")

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

@router.message(IsAdmin(admin_username), Command("show_ques"))
async def cmd_show_questions(message: Message, command: CommandObject):
    command_len = 4
    if len(message.text.split()) == command_len:
        date, to_date, evaluation_response = command.args.split()
        try:
            time.strptime(date, "%Y-%m-%d")
            time.strptime(to_date, "%Y-%m-%d")
            questions = await database_message.show_questions(date, to_date, evaluation_response)
            await message.answer('\n'.join(map(str, questions))) if len(questions) != 0 else await message.answer('Пусто')
        except (ValueError, TypeError):
            await message.answer('Формат даты должен быть таким: %Y-%m-%d')
    else: await message.answer('Команда написана неправильно. /show_questions [ОТ ДАТЫ] [ДО ДАТЫ] [РЕАКЦИЯ НА ОТВЕТ НЕЙРОСЕТИ]')

@router.message(IsAdmin(admin_username), Command("add_adm"))
async def cmd_add_administrators(message: Message, command: CommandObject):
    command_len = 7
    if len(message.text.split()) == command_len:
        username, phone_number, email, name, surname, patronymic = command.args.split()
        await database_admin_log.add_admin(username, phone_number, email, name, surname, patronymic)
        await message.answer(f"Новый администратор {username} добавлен")
    else: await message.answer('Команда написана неправильно. /add_adm')

@router.message(IsAdmin(admin_username), Command("del_adm"))
async def cmd_delete_administrators(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        username = command.args
        await database_admin_log.delete_admin(username)
        await message.answer(f"Администратор {username} удален")
    else: await message.answer('Команда написана неправильно. /del_adm')

@router.message(IsAdmin(admin_username), Command("show_tags"))
async def cmd_show_tags(message: Message):
    await message.answer(JSON_file_manager.show_tags())

@router.message(IsAdmin(admin_username), Command("show_pat"))
async def cmd_show_patterns(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.show_patterns(tag))
    else: await message.answer('Команда написана неправильно. /show_patterns [ТЕГ]')

@router.message(IsAdmin(admin_username), Command("show_resp"))
async def cmd_show_responses(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.show_responses(tag))
    else: await message.answer('Команда написана неправильно. /show_responses [ТЕГ]')

@router.message(IsAdmin(admin_username), Command("training_nn"))
async def cmd_nn_training(message: Message):
    nn = NeuralNetworkTraining("data.json")
    nn.read_data()
    X_train, Y_train = nn.preprocess_data()
    nn.build_model()
    nn.train_model(X_train, Y_train)
    await message.answer("Модель обучилась")

@router.message(IsAdmin(admin_username), Command("add_inte"))
async def cmd_add_intent(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.add_intent(tag))
    else: await message.answer('Команда написана неправильно. /add_intent [ТЕГ]')


@router.message(IsAdmin(admin_username), Command("del_inte"))
async def cmd_delete_intent(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.delete_intent(tag))
    else: await message.answer('Команда написана неправильно. /delete_intent [ТЕГ]')

@router.message(IsAdmin(admin_username), Command("edit_inte"))
async def cmd_edit_intent(message: Message, command: CommandObject):
    command_len = 3
    if len(message.text.split()) == command_len:
        tag, new_tag = command.args.split(" ",1)
        await message.answer(JSON_file_manager.edit_intent(tag, new_tag))
    else: await message.answer('Команда написана неправильно. /edit_intent [ТЕГ] [НОВЫЙ ТЕГ]')

@router.message(IsAdmin(admin_username), Command("output_data"))
async def cmd_output_dataset(message: Message, command: CommandObject):
    pass

@router.message(IsAdmin(admin_username), Command("add_patt"))
async def cmd_add_pattern(message: Message, command: CommandObject):
    tag, pattern = command.args.split(" ",1)
    print(tag)
    print(pattern)
    await message.answer(JSON_file_manager.add_pattern(tag, pattern))

@router.message(IsAdmin(admin_username), Command("del_patt"))
async def cmd_delete_pattern(message: Message, command: CommandObject):
    tag, pattern = command.args.split(" ",1)
    await message.answer(JSON_file_manager.delete_pattern(tag, pattern))

@router.message(IsAdmin(admin_username), Command("add_resp"))
async def cmd_add_response(message: Message, command: CommandObject):
    tag, response = command.args.split(" ",1)
    await message.answer(JSON_file_manager.add_response(tag, response))

@router.message(IsAdmin(admin_username), Command("del_resp"))
async def cmd_delete_response(message: Message, command: CommandObject):
    tag, response = command.args.split(" ",1)
    await message.answer(JSON_file_manager.delete_pattern(tag, response))

@router.message(IsAdmin(admin_username), Command("help"))
async def cmd_help(message: Message):
    admin_rights = True
    await message.answer(TEXT_ADMIN) if admin_rights else await message.answer(TEXT_PERMISSION_ERROR)
    await message.delete()