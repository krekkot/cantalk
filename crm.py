from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('6337428893:AAFFWOQRUTi-3U_FVM_TE4Izz-VJpRuH6ws')

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message ):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.KeyboardButton('Купити з/д квиток', web_app=WebAppInfo(url='https://transaviagroup.rezonuniversal.com/ru/RailwayTickets')))
    markup.add(types.KeyboardButton('Купити автобусний квиток', web_app=WebAppInfo(url='https://transaviagroup.rezonuniversal.com/ru/Bus/Index/')))
    markup.add(types.KeyboardButton('Купити авіаквиток',web_app=WebAppInfo(url='https://transaviagroup.rezonuniversal.com/')))
    await message.answer('Купи свій квиток!', reply_markup=markup)

@dp.message_handler(commands=['start'])

executor.start_polling(dp)
