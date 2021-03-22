from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False)
main_kb.add(KeyboardButton('Сканировать'))
main_kb.add(KeyboardButton('Отменить'))
main_kb.add(KeyboardButton('Помощь'))
