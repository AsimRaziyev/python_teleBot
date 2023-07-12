from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command

from models.product_user_cart import User
from database.postgresql_db import add_user, get_user_id
from utils.create_bot import dp


class FSMUser(StatesGroup):
    username = State()
    email = State()
    password = State()
    phone_number = State()
    address = State()


@dp.message_handler(Command('Зарегистрироваться'), state=None)
async def start_registration(message: types.Message, state: FSMContext):
    telegram_user_id = message.from_user.id
    if telegram_user_id == get_user_id(telegram_user_id):
        await message.answer('Вы уже зарегистрированы')
        return
    async with state.proxy() as data:
        data['id'] = telegram_user_id
    await FSMUser.username.set()
    await message.reply('Введите Имя')


@dp.message_handler(state=FSMUser.username)
async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await FSMUser.next()
    await message.reply('Введите эл. почту')


@dp.message_handler(state=FSMUser.email)
async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await FSMUser.next()
    await message.reply('Введите пароль')


@dp.message_handler(state=FSMUser.password)
async def load_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await FSMUser.next()
    await message.reply('Введите номер телефона')


@dp.message_handler(state=FSMUser.phone_number)
async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = int(message.text)
    await FSMUser.next()
    await message.reply('Введите адрес')


@dp.message_handler(state=FSMUser.address)
async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    async with state.proxy() as data:
        add_user(data['id'], data['username'], data['email'], data['password'], data['phone_number'], data['address'])
    await message.answer('Вы успешно зарегистрировались!')
    await state.finish()


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start_registration, state=None)
    dp.register_message_handler(load_username, state=FSMUser.username)
    dp.register_message_handler(load_email, state=FSMUser.email)
    dp.register_message_handler(load_password, state=FSMUser.password)
    dp.register_message_handler(load_phone_number, state=FSMUser.phone_number)
    dp.register_message_handler(load_address, state=FSMUser.address)