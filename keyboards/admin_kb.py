from aiogram.types import ReplyKeyboardMarkup,\
    KeyboardButton

button_load = KeyboardButton('/Добавить')
button_delete = KeyboardButton('/Удалить')
button_delete_user = KeyboardButton('/Список_пользователей')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_load).add(button_delete).add(button_delete_user)
