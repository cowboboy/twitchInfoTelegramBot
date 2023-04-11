from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from processor import dataprocessor_service
import os

storage = MemoryStorage()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
service = dataprocessor_service.DataProcessorService(datasource="twitchdata-update.csv", \
                                                             db_connection_url="sqlite:///test.db")
connection = service.get_database()