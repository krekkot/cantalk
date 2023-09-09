import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Установка токена бота
bot = telebot.TeleBot('6337428893:AAFFWOQRUTi-3U_FVM_TE4Izz-VJpRuH6ws')

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
gsheet = client.open_by_url(sheet_url).sheet1

# Определение пакетов
packages = {
    'basic': {
        'name':'Пакет LIFE',
        'description': 'Індивідуальний робочий кабінет\n 100 відеоуроків,\n  8 домашніх завдань (без перевірки),\n 7 тестувань з перевіркою,\n 3 вебінари,\n Усі матеріали тренінгу доступні у записі 1 місяць,\n Доступ до закритої Facebook групи на 8 тижнів',
        'price': 115.00,
    },
    'standard': {
        'name':'Пакет BUSINESS',
        'description': 'Все, що входить до пакета “Life” +\n Індивідуальний робочий кабінет із терміном доступу 3 місяці.\n Симуляція реальних переговорів на платформі iDG (Harvard, MIT platform)\n Аналіз вашого «переговорного почерку» та патернів поведінки з постійним зворотним зв’язком партнерів та тренера\n  18 ігрових практикумів та відео/аудіо записи за вашою участю\n Розбір 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою)\n Доступ до закритої Facebook та Viber групи на 3 місяці\n  БОНУС: 50% знижки на онлайн кембридзький тестування Belbin Team Roles',
        'price': 487.00,
    },
    'premium': {
        'name':'Пакет PREMIUM',
        'description': 'Все, що входить до пакета “Business” + \n Індивідуальний графік занять впродовж 6 місяців\nОнлайн кембріджське тестування Belbin Team Roles та індивідуальна аналітична сесія\n Ігрові спаринги з найсильнішими партнерами – Переможцями попередніх потоків \n Особисте супроводження тренера при виконанні всіх завдань – 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою)\n Персональна підтримка 24/7 у переговорних кейсах\n Три 60-хвилинні skype-сесії з тренером для відпрацювання практичних кейсів \n Підбір спеціальних практикумів та розбір кейсів з урахуванням Ваших актуальних життєвих та професійних завдань',
        'price': 932.00,
    }
}

# Список пользователей, получивших бесплатные уроки
users_with_free_lessons = set()

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Отримання ідентифікатора користувача
    user_id = message.from_user.id
    chat_id = message.chat.id
    # Створення клавіатури для виведення кнопок
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Додавання кнопок для кожного пакету
    for package_key, package_info in packages.items():
        # Формування тексту кнопок на основі інформації про пакет
        button_text = f"Узнать о {package_info['name']}"
        markup.add(telebot.types.KeyboardButton(button_text))
    # Відправляємо повідомлення з клавіатурою
    bot.send_message(chat_id, f"Оберіть пакет:", reply_markup=markup)


    # Добавление кнопки для генерации бесплатных уроков
    markup.add(telebot.types.KeyboardButton("Получить бесплатные уроки"))

    bot.send_message(user_id, "Привет! Я бот для продажи курсов по переговорам. Выберите интересующий вас пакет:",
                     reply_markup=markup)

# Обработка команд для каждого пакета
for package_key, package_info in packages.items():
    @bot.message_handler(func=lambda message, key=package_key: message.text == f"Узнать о {packages[key]['name']}")
    def handle_package(message):
        user_id = message.from_user.id
        package_info = packages[package_key]
        bot.send_message(user_id, f"{package_info['name']}\n\n{package_info['description']}\n\nЦена: {package_info['price']}")

# Обработка команды для генерации бесплатных уроков
@bot.message_handler(func=lambda message: message.text == "Получить бесплатные уроки")
def handle_free_lessons(message):
    user_id = message.from_user.id

    # Проверка, получал ли пользователь уже бесплатные уроки
    if user_id in users_with_free_lessons:
        bot.send_message(user_id, "Вы уже получали бесплатные уроки.")
    else:
        # Генерация трех случайных уроков
        random_lessons = random.sample(range(2, 58), 3)  # Строки B2:B57

        # Отправка пользователю ссылок на уроки
        for lesson_number in random_lessons:
            lesson_url = gsheet.cell(lesson_number, 2).value  # Строки A2:A57
            bot.send_message(user_id, f"Бесплатный урок {lesson_number}: {lesson_url}")

        # Добавление пользователя в список тех, кто уже получал бесплатные уроки
        users_with_free_lessons.add(user_id)

# TODO: Добавьте обработку оплаты через Portmone

# Запуск бота
bot.polling()





