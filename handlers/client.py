from aiogram import types
from create_bot import bot, connection
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from keyboards import kb_client
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class FSMStreamer(StatesGroup):
    """
    Получает имя стримера и выводит информацию по нему
    """
    name = State()
async def streamer_start(message : types.Message):
    await bot.send_message(message.from_user.id, "Введите имя стримера:", reply_markup=kb_client.kb_cancel)
    await message.delete()
    await FSMStreamer.name.set()

async def get_name(message : types.Message, state : FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id, f"Стример {data['name']} был найден.", reply_markup=kb_client.kb_menu)
    await state.finish()

async def cancel_streamer(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(message.from_user.id, reply_markup=kb_client.kb_menu)
    await state.finish()

class FSMRating(StatesGroup):
    """
    Получает условие, по которому будет составляться рейтинг
    """
    condition = State()

async def rating_start(message : types.Message):
    conditions = []
    kb_ratingConditions = ReplyKeyboardMarkup(resize_keyboard=True)
    for condition in conditions:
        kb_ratingConditions.insert(KeyboardButton(str(condition)))
    await bot.send_message(message.from_user.id, "Выберите признак составления рейтинга:", reply_markup=kb_ratingConditions)
    await message.delete()
    await FSMRating.condition.set()

async def get_condition(message : types.Message, state : FSMContext):
    await state.update_data(condition=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id, f"Статистика по условию {data['condition']}: ...", reply_markup=kb_client.kb_menu)
    await state.finish()

async def cancel_rating(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(message.from_user.id, reply_markup=kb_client.kb_menu)
    await state.finish()

async def command_start(message : types.message):
    await bot.send_message(message.from_user.id, "Здравствуйте", reply_markup=kb_client.kb_menu)
    await message.delete()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])

    dp.register_message_handler(streamer_start, Text(equals="Узнать о стримере"), state=None)
    dp.register_message_handler(get_name, state=FSMStreamer.name)

    dp.register_message_handler(rating_start, Text(equals="Рейтинг стримеров"), state=None)
    dp.register_message_handler(get_condition, state=FSMRating.condition)

    dp.register_message_handler(cancel_streamer, state="*", commands="отмена")
    dp.register_message_handler(cancel_rating, state="*", commands="отмена")