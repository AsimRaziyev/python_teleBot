from aiogram import executor

from utils.create_bot import dp
from database.postgresql_db import create_db_engine
from handlers import client, admin, other, cart_item, user

engine = create_db_engine()


async def on_startup(_):
    print('Бот успешно был запущен!')
    client.register_handlers_client(dp)
    admin.register_handlers_admin(dp)
    other.register_handlers_other(dp)
    cart_item.register_handlers_cart_item(dp)
    user.register_handlers_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
