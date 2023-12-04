from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
router = Router()




@router.message(Command("ua"))
@router.message(F.text.lower() == "українська")
async def cmd_ua(message: types.Message):
    services_ua = InlineKeyboardMarkup(inline_keyboard=[])

    buy_ticket_button = InlineKeyboardButton(text='Купити квиток на потяг🚅,літак✈️,автобус🚍', callback_data='buy_ticket')

    negotiation_course_button = InlineKeyboardButton(text='Онлайн-курс "ПЕРЕГОВОРИ I ЛIДЕРСТВО"👩‍🎓👨‍🎓', callback_data='negotiation_course')

    services_ua = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [buy_ticket_button],[negotiation_course_button]
    ])
    await message.reply("Дякую, що обрали українську мову! 🇺🇦 \nЧим можу бути корисним:", reply_markup=services_ua)



@router.callback_query(lambda query: query.data == "buy_ticket")
async def services_ua(callback_query: types.CallbackQuery):
    service_ua = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Квитки на потяг🚅',
                                                                   web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ua/RailwayTickets/Index/')),
                                          ],
                                          [
                                              InlineKeyboardButton(text='Квитки на автобус🚍',
                                                                   web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ua/Bus/Index/')),
                                          ],
                                          [
                                              InlineKeyboardButton(text='Авіаквитки✈️',
                                                                   web_app=WebAppInfo(url=f'https://transaviagroup.rezonuniversal.com/ua/')),
                                          ],
                                      ])
    await callback_query.message.answer("Чудовий вибір!\nЯкі саме квитки Вам потрібні?", reply_markup=service_ua)






