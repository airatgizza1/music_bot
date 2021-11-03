from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

btn1 = KeyboardButton("Узнать требования")
btn2 = KeyboardButton("Отправить трек на прослушивание")
bt12 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn2).add(btn1)
bt2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn2)
btn3 = KeyboardButton("Я передумал, не отправлять")
bt3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn3)
btn4 = KeyboardButton("Продолжить")
bt4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn4)
btn5 = KeyboardButton("Отправить трек на прослушивание")
bt5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn5)
btn6 = KeyboardButton("Готово!")
bt6 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn6).add(btn3)
bt_remove = ReplyKeyboardRemove()