from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
router = Router()



@router.message(Command("ru"))
@router.message(F.text.lower() == "русский")
async def cmd_ru(message: types.Message):
    services_ru = InlineKeyboardMarkup(inline_keyboard=[])

    buy_ticket_button = InlineKeyboardButton(text='Купить билет на поезд🚅, самолет✈️, автобус🚍', callback_data='buy_ticket1')

    negotiation_course_button = InlineKeyboardButton(text='Онлайн-курс "ПЕРЕГОВОРЫ И ЛИДЕРСТВО"👩‍🎓👨‍🎓', callback_data='negotiation_course')

    services_ru = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [buy_ticket_button], [negotiation_course_button]
    ])
    await message.reply("Спасибо, что выбрали русский язык! 🇷🇺\nЧем я могу быть полезен:", reply_markup=services_ru)


@router.callback_query(lambda query: query.data == "buy_ticket1")
async def services_ru(callback_query: types.CallbackQuery):
    service_ru = InlineKeyboardMarkup(row_width=1,inline_keyboard=[
        [InlineKeyboardButton(text='Билеты на поезд🚅',web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ru/RailwayTickets/Index/'))],
        [InlineKeyboardButton(text='Билеты на автобус🚍',web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ru/Bus/Index/'))],
        [InlineKeyboardButton(text='Авиабилеты✈️',web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ru/'))]])
    await callback_query.message.answer("Отличный выбор!\nКакие именно билеты вам нужны?", reply_markup=service_ru)
