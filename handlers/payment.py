from aiogram import Router, types
from aiogram.types import LabeledPrice, SuccessfulPayment
from aiogram.methods import SendInvoice
from config_reader import payment_token  # Перевірте правильність назви токену
from handlers.peregovorshik import show_package_description
import re
from aiogram import Bot
from aiogram.types import LabeledPrice
from aiogram import F
router = Router()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.types import PreCheckoutQuery, SuccessfulPayment
from config_reader import config
bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")


@router.message(lambda message: message.text == "pay")
async def handle_pay(message: types.Message):
    # Викликати show_package_description, щоб отримати значення priceuah
    priceuah = await show_package_description(message)
    print(f"DEBUG: priceuah before SendInvoice: {priceuah}")

    # Використовувати HTML-розмітку для підкреслення тексту кнопки
    pay_button_text = f'<u>Придбати курс</u>'

    # Викликати функцію process_pay, передаючи параметри, включаючи об'єкт bot
    await process_pay(message, priceuah)




@router.callback_query(lambda query: query.data.startswith('pay'))
async def process_pay(callback_query: types.CallbackQuery):
    # Отримати значення priceuah з callback_data
    print(f"DEBUG: callback_query.data: {callback_query.data}")
    bot = callback_query.bot
    # Використовуйте регулярний вираз для виділення числа з рядка
    match = re.search(r'\d+', callback_query.data)
    priceuah = int(match.group()) if match else 0

    # Відправте користувача на оплату, передаючи об'єкт бота
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оплатити', pay=True)],
    ])

    # Відправити інвойс, вказавши клавіатуру

    await bot.send_invoice(
        chat_id=callback_query.message.chat.id,
        title=f'Покупка курса',
        description='Покупка курса "ПЕРЕГОВОРИ I ЛIДЕРСТВО"',
        payload='invoice',
        provider_token=payment_token,
        currency='UAH',
        prices=[LabeledPrice(label='Покупка курса', amount=priceuah*100)],
        reply_markup=keyboard,
    )


@router.callback_query(lambda query: query.data.startswith('successful_payment'))
async def success(callback_query: types.CallbackQuery):
    successful_payment_info = SuccessfulPayment(**callback_query.get_payment())
    await callback_query.answer(f'Success: {successful_payment_info.order_info}')

@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # Обробка події pre_checkout_query
    # Підтвердження платежу
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.types==types.successful_payment)
async def process_successful_payment(message: types.Message):
    # Обробка події successful_payment
    # Отримано підтвердження успішного платежу
    successful_payment_info = SuccessfulPayment(process_successful_payment)
    await message.answer(f'Success: {successful_payment_info.order_info}')

@router.callback_query(lambda query: query.data.startswith('pre_checkout_query'))
async def process_pre_checkout_query(callback_query: types.pre_checkout_query):
    # Обробка події pre_checkout_query
    # Підтвердження платежу
    pre_checkout_query_info=PreCheckoutQuery(**callback_query.get_payment())
    await callback_query.answer(f'done: {pre_checkout_query_info.order_info}')

