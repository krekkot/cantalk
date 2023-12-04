import asyncio
import logging
from aiogram.fsm.strategy import FSMStrategy
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import common
from handlers import ualang
from handlers import rulang
from handlers import peregovorshik
from handlers import handle_free_lessons
from handlers import kursnbu
from handlers import payment
from handlers import message
from handlers import name_phone
from aiogram.fsm.strategy import FSMStrategy
from handlers.kursnbu import update_exchange_rate
import aiocron
import asyncio



async def main():
    task_update_exchange_rate = asyncio.create_task(update_exchange_rate())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # Но явное лучше неявного =]
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    dp.include_router(common.router)
    dp.include_router(ualang.router)
    dp.include_router(rulang.router)
    dp.include_router(peregovorshik.router)
    dp.include_router(handle_free_lessons.router)
    dp.include_router(kursnbu.router)
    dp.include_router(payment.router)
    dp.include_router(name_phone.router)

    # сюда импортируйте ваш собственный роутер для напитков

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    # Створення циклу для іншої функції
    asyncio.run(update_exchange_rate())
    loop = asyncio.get_event_loop()
    cron = aiocron.crontab("*/30 9-17 * * 1-5", func=update_exchange_rate) #*/30 9-17 * * 1-5 визначає, що завдання повинно виконуватися кожні півгодини в проміжку від 9:00 до 17:00 з понеділка по п'ятницю
    loop.run_until_complete(cron.start())
    loop.run_forever()
    task_update_exchange_rate = loop.create_task(update_exchange_rate())
    loop.run_until_complete(asyncio.gather(main(), task_update_exchange_rate))



    # Запускаємо асинхронний цикл



