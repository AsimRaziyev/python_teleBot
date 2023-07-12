from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import session

from models.product_user_cart import Product
from utils.create_bot import dp

from database.postgresql_db import add_product_to_cart_item, \
    get_user_cart, delete_product_from_cart, get_user_id


class FSMCart(StatesGroup):
    quantity = State()


@dp.callback_query_handler(lambda x: x.data.startswith('Добавить_в_корзину:'))
async def add_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if user_id == get_user_id(user_id):
        callback_data = callback_query.data
        product_id = int(callback_data.split(':')[1])

        await callback_query.answer('Введите количество продукта:')
        await state.update_data(user_id=user_id, product_id=product_id)
        await FSMCart.quantity.set()
    else:
        await callback_query.answer('Прошу зарегистрироваться')


@dp.message_handler(state=FSMCart.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        data = await state.get_data()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        add_product_to_cart_item(user_id, product_id, quantity)

        await message.answer('Продукт успешно добавлен в корзину.')
        await state.finish()
    except ValueError:
        await message.answer('Ошибка! Пожалуйста, введите число.')



@dp.callback_query_handler(lambda x: x.data.startswith('Удалить_из_корзины:'))
async def delete_callback_run(callback_query: types.CallbackQuery):
    cart_id = int(callback_query.data.split(':')[1])
    if cart_id:
        delete_product_from_cart(cart_id)
        await callback_query.answer('Продукт успешно удален из корзины')
    else:
        await callback_query.answer('Произошла ошибка при удалении продукта из корзины')

@dp.message_handler(Command('Корзина'))
async def view_cart_item(message: types.Message):
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    if cart_items:
        await message.answer('Список товаров в корзине:')
        for cart_item in cart_items:
            product_name = cart_item.product.name
            quantity = cart_item.quantity
            await message.answer(f'Товар: {product_name}, Количество: {quantity}')
            delete_kb = InlineKeyboardMarkup(row_width=1)
            delete_kb.add(InlineKeyboardButton(f'Удалить', callback_data=f'Удалить_из_корзины:{cart_item.id}'))
            await message.answer(f'Удалить из корзины', reply_markup=delete_kb)
    else:
        await message.answer('Ваша корзина пуста')


def register_handlers_cart_item(dp: Dispatcher):
    dp.register_message_handler(add_callback_run)
    # dp.register_message_handler(delete_callback_run)
    dp.register_message_handler(view_cart_item)
