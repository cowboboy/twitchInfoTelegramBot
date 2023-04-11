from create_bot import bot, dp, service
from aiogram import executor

async def on_startup(_):
    global connection
    print("[BOT] Connected.")
    try:
        service.run_service()
        #print("[DataProcessor] Connected.")
    except:
        print("[DataProcessor] Failed.")

from handlers import client

client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)