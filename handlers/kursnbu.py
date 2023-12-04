import requests
import asyncio  # Додайте цей імпорт
from datetime import datetime
from aiogram import Router
import time
import schedule
router = Router()


def get_exchange_rate(currency_code):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_exchange_rate(currency_code))


async def fetch_exchange_rate(currency_code):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&valcode={currency_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['rate']
    else:
        print(f"Error {response.status_code}: {response.text}")

    return None

async def update_exchange_rate():
    while True:
        # Перевіряємо, чи зараз робочий час (від 10:00 до 17:00)
        current_hour = datetime.now().hour
        if 10 <= current_hour < 17:
            # Оновлюємо курс валюти
            usd_exchange_rate = await get_exchange_rate("USD")
            print(f"Курс долара США: {usd_exchange_rate}")

            # Додайте тут код для відправлення оновленого курсу користувачам чи іншої логіки
        schedule.every(30).minutes.do(update_exchange_rate)

        await asyncio.sleep(30 * 60)



# Пример использования для получения курса доллара США (USD)
usd_exchange_rate = get_exchange_rate("USD")
print(f"Курс доллара США: {usd_exchange_rate}")

previous_usd_exchange_rate = None

async def update_usd_exchange_rate():
    global previous_usd_exchange_rate

    # Отримуємо новий курс валюти
    new_usd_exchange_rate = await get_exchange_rate("USD")

    # Перевіряємо, чи курс змінився
    if previous_usd_exchange_rate is not None and new_usd_exchange_rate != previous_usd_exchange_rate:
        print(f"Курс долара США змінився: {new_usd_exchange_rate}")
        # Додайте тут код для відправлення оновленого курсу користувачам чи іншої логіки

    # Зберігаємо нове значення курсу як попереднє для майбутніх порівнянь
    previous_usd_exchange_rate = new_usd_exchange_rate
