from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from app import keyboards as kb
from app import database as db
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

async def on_startup(_):
    await db.db_start()
    print("Бот успешно запущен!")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMUZVCj-YOpnI9nQap5Ei4UqGTyd3EAApwVAAIcZnhLvjpdclDp8JAzBA')
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Привет {message.from_user.first_name}!', reply_markup=kb.main_admin)
    else:
        await message.answer(f'Привет {message.from_user.first_name}!', reply_markup=kb.main)

@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer("Каталог:", reply_markup=kb.catalog_list)

@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer("Корзина:", reply_markup=kb.catalog_list)

@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer("По всем вопросам: @x_why_z")

@dp.message_handler(text='Админ-панель')
async def admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Админ панель:", reply_markup=kb.admin_panel)
    else:
        await message.reply(f'Я не понимаю Вас')

@dp.message_handler(text='Главное меню')
async def main(message: types.Message):
    await message.answer(f'Главное меню:', reply_markup=kb.main)

@dp.message_handler(text='Айди')
async def check_id(message: types.Message):
    await message.reply(message.from_user.id)

@dp.message_handler(content_types=['sticker'])
async def check_sticker(message: types.Message):
    await message.answer(message.sticker.file_id)

@dp.message_handler(text=['document', 'photo'])
async def forward_message(message: types.Message):
    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply(f'Я не понимаю Вас')

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
