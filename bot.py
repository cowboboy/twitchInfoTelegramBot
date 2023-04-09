from create_bot import bot, dp
from aiogram import executor
from data_base import sqlite
from processor import dataprocessor_service

async def on_startup(_):
    print("[BOT] Connected.")
    sqlite.create_db()
    try:
        dataprocessor_service.DataProcessorService("twitchdata-update.csv").run_service()
        print("[DataProcessor] Connected.")
    except:
        print("[DataProcessor] Failed.")

from handlers import client

client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)