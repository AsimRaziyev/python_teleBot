from aiogram.types import ReplyKeyboardMarkup,\
    KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим-работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Продукты')
b4 = KeyboardButton('/Зарегистрироваться')
b5 = KeyboardButton('/Корзина')
# b6 = KeyboardButton('Поделиться номером', request_contact=True)
# b7 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2, b3, b4, b5) #.row(b5, b6)
