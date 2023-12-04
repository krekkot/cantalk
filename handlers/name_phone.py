from aiogram import Router, types, Dispatcher
from aiogram.types import LabeledPrice, SuccessfulPayment
from aiogram.methods import SendInvoice
from config_reader import payment_token
from handlers.peregovorshik import show_package_description
import re
from aiogram import Bot
from aiogram.types import LabeledPrice
from aiogram.methods import SendInvoice
from aiogram import F
router = Router()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, SuccessfulPayment
from config_reader import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from aiogram import types
from handlers.common import users_with_free_lessons
from aiogram.types import ReplyKeyboardRemove


# Ініціалізація об'єкта для роботи з Google Spreadsheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
worksheet_name = "Уроки"
worksheet = client.open_by_url(spreadsheet_url).worksheet(worksheet_name)


#@router.message(Command('ok'))




# async def start_data_collection(message: types.Message):
#     await ask_for_data(message, 'ім\'я')
#
# async def ask_for_data(message: types.Message, data_type: str):
#     await message.answer(f"Введіть свій {data_type}:")
#     await process_data_step.set(data_type=data_type)
#
# @router.message(F.data_type=='ім\'я')
# async def process_data_step(message: types.Message):
#     data_type = data_type(message)
#     data = message.text
#     user_id = message.from_user.id
#
#     # Тут ви можете використовувати data та user_id для обробки даних, наприклад, додавання до гугл таблиці.
#
#     await message.answer(f"Ваш {data_type}: {data}")
#
#     if data_type == "ім'я":
#         await ask_for_data(message, 'телефон')
#     elif data_type == 'телефон':
#         await ask_for_data(message, 'емейл')
#     elif data_type == 'емейл':
#         await message.answer("Дякуємо за надану інформацію!")
#         await process_data_step.finish()




