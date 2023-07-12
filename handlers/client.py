from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from handlers.cart_item import view_cart_item
from handlers.catalog import catalog
from handlers.user import start_registration
from utils.create_bot import dp, bot
from keyboards import kb_client


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать в наш магазин!', reply_markup=kb_client)
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему \nhttps://t.me/Python_asimo_bot')


@dp.message_handler(Command('Режим-работы'))
async def open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим работы: Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


@dp.message_handler(Command('Расположение'))
async def place_command(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, 'Расположение: г.Алматы ул.Абая 555')


@dp.message_handler(Command('Продукты'))
async def catalog_command(message: types.Message):
    await message.delete()
    await catalog(message)


@dp.message_handler(Command('Зарегистрироваться'))
async def registration_command(message: types.Message):
    await message.delete()
    await start_registration(message)


@dp.message_handler(Command('Корзина'))
async def cart_command(message: types.Message):
    await message.delete()
    await view_cart_item(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command)
    dp.register_message_handler(open_command)
    dp.register_message_handler(place_command)
    dp.register_message_handler(catalog_command)
    dp.register_message_handler(cart_command)
