from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.postgresql_db import get_all_products


async def catalog(message: types.Message):
    products = get_all_products()
    if products:
        await message.answer('Список продуктов:')
        for product in products:
            caption = f'Название: {product.name}\n' \
                      f'Описание: {product.description}\n' \
                      f'Цена: {product.price}тг'
            await message.answer_photo(product.photo, caption=caption)
            cart_kb = InlineKeyboardMarkup(row_width=1)
            cart_kb.add(InlineKeyboardButton(f'Добавить', callback_data=f'Добавить_в_корзину:{product.id}'))
            await message.answer(f'Добавить в корзину: {product.name}', reply_markup=cart_kb)
    else:
        await message.answer('Список продуктов пуст')



