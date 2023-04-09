from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b_cancel = KeyboardButton("/Отмена")
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура для отмены действий
kb_cancel.row(b_cancel)

b_streamer = KeyboardButton("Узнать о стримере")
b_rating= KeyboardButton("Рейтинг стримеров")

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура главного меню
kb_menu.row(b_streamer, b_rating)

b_viewCondition = KeyboardButton("Просмотры")
b_subscribersCondition = KeyboardButton("Подписчики")
kb_ratingConditions = ReplyKeyboardMarkup(resize_keyboard=True) # клавиатура меню выбора признака составления рейтинга
kb_ratingConditions.row(b_viewCondition, b_subscribersCondition).add(b_cancel)