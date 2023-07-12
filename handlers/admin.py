from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import Command
from aiogram import exceptions

from handlers.catalog import catalog
from utils.create_bot import dp, bot
from database.postgresql_db import add_product, get_all_products, delete_product
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(Command('moderator'), is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что нужно сделать?', reply_markup=admin_kb.button_case_admin)
    try:
        await message.delete()
    except exceptions.MessageCantBeDeleted as e:
        print(f"Не удалось удалить сообщение: {e}")


# @dp.message_handler(commands=['moderator'])
# async def make_changes_command(message: types.Message):
#     global ID
#     ID = message.from_user.id
#     if message.chat.type == 'private':
#         await bot.send_message(message.chat.id, 'Что нужно сделать?', reply_markup=admin_kb.button_case_admin)
#     else:
#         await message.reply('Команда доступна только в личных сообщениях бота.')
#
#     try:
#         await message.delete()
#     except exceptions.MessageCantBeDeleted as e:
#         print(f"Не удалось удалить сообщение: {e}")


@dp.message_handler(Command('Добавить'), state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.answer('Для завершении напишите "отмена"')
        await message.reply('Загрузите фото')


@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        try:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply('Теперь введите название')
        except:
            await message.answer('Фото не загружено')


@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание')


@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажите цену')


@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        async with state.proxy() as data:
            add_product(data['photo'], data['name'], data['description'], data['price'])
        await message.answer('Продукт успешно добавлен!')
        await state.finish()


@dp.callback_query_handler(lambda x: x.data.isdigit(), state='*')
async def del_callback_run(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data)
    delete_product(product_id)
    await callback_query.answer('Продукт успешно удален')


@dp.message_handler(Command('Удалить'))
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        products = get_all_products()
        if products:
            await message.answer('Список продуктов:')
            for product in products:
                caption = f'Название: {product.name}\n' \
                          f'Описание: {product.description}\n' \
                          f'Цена: {product.price}'
                await message.answer_photo(product.photo, caption=caption)
                keyboard = InlineKeyboardMarkup(row_width=1)
                keyboard.add(InlineKeyboardButton(f'Удалить', callback_data=str(product.id)))
                await message.answer(f'Удалить продукт: {product.name}', reply_markup=keyboard)
        else:
            await message.answer('Список продуктов пуст')


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


@dp.message_handler(Command('Список_пользователей'))
async def registration_command(message: types.Message):
    await message.answer("скоро появится возможность удалить пользователя ")



def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, state=None)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler)
    dp.register_message_handler(cancel_handler)
    dp.register_message_handler(make_changes_command)
