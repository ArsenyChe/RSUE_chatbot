from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import database_message, database_admin_log
from messages import TEXT_START, TEXT_ADMIN_HELP, TEXT_PERMISSION_ERROR
import time
from os import getenv
from dotenv import load_dotenv
from neural_network.dataset_modification import JSONFileManager 
from neural_network.neural_network_training import NeuralNetworkTraining

load_dotenv()

router = Router()

admin_username: list[str] = [getenv('ADMIN_USERNAME')]

JSON_file_manager = JSONFileManager("data.json")

class IsAdmin(BaseFilter):
    def __init__(self, admin_username: list[str]) -> None:
        self.admin_username = admin_username

    async def __call__(self, message: Message) -> bool:
        return message.from_user.username in self.admin_username

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.username } {message.from_user.full_name}, '+ TEXT_START)
    await message.delete()

@router.message(IsAdmin(admin_username), Command("showquestions"))
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
    else: await message.answer('Команда написана неправильно. /showquestions <дата начала> <дата окончания> <реакция на ответ нейросети>	Выводит вопросы абитуриентов с положительной/отрицательной оценкой за определенный период времени')

@router.message(IsAdmin(admin_username), Command("addadmin"))
async def cmd_add_administrators(message: Message, command: CommandObject):
    command_len = 7
    if len(message.text.split()) == command_len:
        username, phone_number, email, name, surname, patronymic = command.args.split()
        await database_admin_log.add_admin(username, phone_number, email, name, surname, patronymic)
        await message.answer(f"Новый администратор {username} добавлен")
    else: await message.answer('Команда написана неправильно. /addadmin <ник в Telegram> <номер телефона> <электронная почта> <имя> <фамилия> <отчество>	Добавляет администратора в БД')

@router.message(IsAdmin(admin_username), Command("deladmin"))
async def cmd_delete_administrators(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        username = command.args
        await database_admin_log.delete_admin(username)
        await message.answer(f"Администратор {username} удален")
    else: await message.answer('Команда написана неправильно. /deladmin <ник в Telegram>	Удаляет администратора из БД')

@router.message(IsAdmin(admin_username), Command("showtags"))
async def cmd_show_tags(message: Message):
    await message.answer(JSON_file_manager.show_tags())

@router.message(IsAdmin(admin_username), Command("showpatterns"))
async def cmd_show_patterns(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.show_patterns(tag))
    else: await message.answer('Команда написана неправильно. /showpatterns <тема> Выводит все значения шаблонов по теме вопросов из датасета')

@router.message(IsAdmin(admin_username), Command("showresponses"))
async def cmd_show_responses(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.show_responses(tag))
    else: await message.answer('Команда написана неправильно. /showresponses <тема> Выводит все значения ответов по теме из датасета')

@router.message(IsAdmin(admin_username), Command("trainingnn"))
async def cmd_nn_training(message: Message):
    nn = NeuralNetworkTraining("data.json")
    nn.read_data()
    X_train, Y_train = nn.preprocess_data()
    nn.build_model()
    info = nn.train_model(X_train, Y_train, 5, 130)
    await message.answer(f"Модель обучилась: {info}")

@router.message(IsAdmin(admin_username), Command("addintent"))
async def cmd_add_intent(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.add_intent(tag))
    else: await message.answer('Команда написана неправильно. /addintent <тема> Добавляет тему с пустыми шаблонами вопросов и ответами на вопросы')


@router.message(IsAdmin(admin_username), Command("delintent"))
async def cmd_delete_intent(message: Message, command: CommandObject):
    command_len = 2
    if len(message.text.split()) == command_len:
        tag = command.args
        await message.answer(JSON_file_manager.delete_intent(tag))
    else: await message.answer('Команда написана неправильно. /delintent <тема> Удаляет тему с пустыми шаблонами вопросов и ответами на вопросы')

@router.message(IsAdmin(admin_username), Command("editintent"))
async def cmd_edit_intent(message: Message, command: CommandObject):
    command_len = 3
    if len(message.text.split()) == command_len:
        tag, new_tag = command.args.split(" ",1)
        await message.answer(JSON_file_manager.edit_intent(tag, new_tag))
    else: await message.answer('/editintent <тема> <новыое наименование темы> Изменяет тему  с пустыми шаблонами вопросов и ответами на вопросы')

@router.message(IsAdmin(admin_username), Command("addpattern"))
async def cmd_add_pattern(message: Message, command: CommandObject):
    tag, pattern = command.args.split(" ",1)
    await message.answer(JSON_file_manager.add_pattern(tag, pattern))

@router.message(IsAdmin(admin_username), Command("delpattern"))
async def cmd_delete_pattern(message: Message, command: CommandObject):
    tag, pattern = command.args.split(" ",1)
    await message.answer(JSON_file_manager.delete_pattern(tag, pattern))

@router.message(IsAdmin(admin_username), Command("addresponse"))
async def cmd_add_response(message: Message, command: CommandObject):
    tag, response = command.args.split(" ",1)
    await message.answer(JSON_file_manager.add_response(tag, response))

@router.message(IsAdmin(admin_username), Command("delresponse"))
async def cmd_delete_response(message: Message, command: CommandObject):
    tag, response = command.args.split(" ",1)
    await message.answer(JSON_file_manager.delete_pattern(tag, response))

@router.message(IsAdmin(admin_username), Command("help"))
async def cmd_help(message: Message):
    admin_rights = True
    await message.answer(TEXT_ADMIN_HELP) if admin_rights else await message.answer(TEXT_PERMISSION_ERROR)