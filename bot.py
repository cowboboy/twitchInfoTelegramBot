from create_bot import bot, dp
from aiogram import executor

async def on_startup(_):
    print("[BOT] Connected.")

from handlers import client

client.register_handlers_client(dp)

print("test")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)