from aiogram import types
from create_bot import bot
from aiogram import Dispatcher

async def command_start(message : types.message):
    await bot.send_message(message.from_user.id, "Здравствуйте")
    await message.delete()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])