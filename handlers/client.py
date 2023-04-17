from aiogram import types
from create_bot import bot, connection
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from keyboards import kb_client
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from matplotlib import pyplot as plt
import time

conditions = ["Время просмотра", "Время в эфире", "Пиковый онлайн", "Средний онлайн", "Подписчики"]

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
    streamer_name = message.text
    streamer_info = connection.get_row_by_name(streamer_name)
    response = ""
    if streamer_info:
        fields = ["Имя: ", "Общее время просмотра: ", "Общее время в эфире: ", "Пиковые просмотры: ",
                  "Среднее количество просмотров: ", "Подписчики"]
        for i in range(len(fields)):
            response += fields[i] + str(streamer_info[i]) + '\n'
    else:
        response = "Нет данных. Попробуйте еще."
    await bot.send_message(message.from_user.id, response, reply_markup=kb_client.kb_menu)
    await state.finish()

async def cancel_streamer(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(message.from_user.id, "Успешно!", reply_markup=kb_client.kb_menu)
    await state.finish()

class FSMRating(StatesGroup):
    """
    Получает условие, по которому будет составляться рейтинг
    """
    condition = State()

async def rating_start(message : types.Message):
    kb_ratingConditions = ReplyKeyboardMarkup(resize_keyboard=True)
    for condition in conditions:
        kb_ratingConditions.insert(KeyboardButton(str(condition)))
    kb_ratingConditions.add(kb_client.b_cancel)
    await bot.send_message(message.from_user.id, "Выберите признак составления рейтинга:", reply_markup=kb_ratingConditions)
    await message.delete()
    await FSMRating.condition.set()

async def get_condition(message : types.Message, state : FSMContext):
    rating_condition = message.text
    fields = dict(zip(conditions, ['viewingTime', 'airTime', 'peakViews', 'averageVies', 'subscribers']))
    numeric_fields = dict(zip(conditions, range(1, 6)))
    response = ""
    if rating_condition in conditions:
        rating = connection.get_rating_by_field(fields[rating_condition])
        if rating:
            for i in range(1, 11):
                response += str(i) + ')' + str(rating[i-1][0]) + '\n'
        else:
            response = "Нет данных. Попробуйте еще."
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot()
        ax.pie([rat[numeric_fields[rating_condition]] for rat in rating], labels=[str(rat[0]) for rat in rating])
        name = "static/" + str(rating[0][0]) + str(time.time_ns()) + ".png"
        plt.savefig(name)
        await bot.send_photo(message.from_user.id, caption=response, reply_markup=kb_client.kb_menu, photo=open(name, "rb"))
    else:
        response = "Нет такой категории. Попробуйте еще."
        await bot.send_message(message.from_user.id, response, reply_markup=kb_client.kb_menu)
    await state.finish()

async def cancel_rating(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(message.from_user.id, "Успешно.", reply_markup=kb_client.kb_menu)
    await state.finish()

async def command_start(message : types.message):
    await bot.send_message(message.from_user.id, "Здравствуйте.", reply_markup=kb_client.kb_menu)
    await message.delete()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cancel_streamer, state="*", commands="Отмена")
    dp.register_message_handler(cancel_rating, state="*", commands="Отмена")

    dp.register_message_handler(command_start, commands=["start", "help", "помощь", "начало"])

    dp.register_message_handler(streamer_start, Text(equals="Узнать о стримере"), state=None)
    dp.register_message_handler(get_name, state=FSMStreamer.name)

    dp.register_message_handler(rating_start, Text(equals="Рейтинг стримеров"), state=None)
    dp.register_message_handler(get_condition, state=FSMRating.condition)