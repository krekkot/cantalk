import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
gsheet = client.open_by_url(sheet_url).sheet1

# Установка токена бота
bot = telebot.TeleBot('6337428893:AAFFWOQRUTi-3U_FVM_TE4Izz-VJpRuH6ws')

languages = {'ru': 'Русский', 'uk': 'Українська'}

# Определение пакетов
packages = {
    'basic': {
        'name': 'Пакет LIFE',
        'description': 'Індивідуальний робочий кабінет\n 100 відеоуроків,\n 8 домашніх завдань (без перевірки),\n 7 тестувань з перевіркою,\n 3 вебінари,\n Усі матеріали тренінгу доступні у записі 1 місяць,\n Доступ до закритої Facebook групи на 8 тижнів',
        'price': 115.00,
    },
    'standard': {
        'name': 'Пакет BUSINESS',
        'description': 'Все, що входить до пакета “Life” +\n Індивідуальний робочий кабінет із терміном доступу 3 місяці.\n Симуляція реальних переговорів на платформі iDG (Harvard, MIT platform)\n Аналіз вашого «переговорного почерку» та патернів поведінки з постійним зворотним зв’язком партнерів та тренера\n  18 ігрових практикумів та відео/аудіо записи за вашою участю\n Розбір 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою)\n Доступ до закритої Facebook та Viber групи на 3 місяці\n  БОНУС: 50% знижки на онлайн кембридзький тестування Belbin Team Roles',
        'price': 487.00,
    },
    'premium': {
        'name': 'Пакет PREMIUM',
        'description': 'Все, що входить до пакета “Business” + \n Індивідуальний графік занять впродовж 6 місяців\nОнлайн кембріджське тестування Belbin Team Roles та індивідуальна аналітична сесія\n Ігрові спаринги з найсильнішими партнерами – Переможцями попередніх потоків \n Особисте супроводження тренера при виконанні всіх завдань – 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою)\n Персональна підтримка 24/7 у переговорних кейсах\n Три 60-хвилинні skype-сесії з тренером для відпрацювання практичних кейсів \n Підбір спеціальних практикумів та розбір кейсів з урахуванням Ваших актуальних життєвих та професійних завдань',
        'price': 932.00,
    }
}

# Список пользователей, получивших бесплатные уроки
users_with_free_lessons = set()

# Обработка команды /start
def create_language_keyboard():
    markup = types.InlineKeyboardMarkup()
    for code, language in languages.items():
        button = types.InlineKeyboardButton(text=language, callback_data=code)
        markup.add(button)
    return markup

# Створення Inline-клавіатури для вибору пакету
def create_package_keyboard():
    markup = types.InlineKeyboardMarkup()
    for package_key, package_info in packages.items():
        button_text = f"Дізнатись про {package_info['name']}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=f"package_{package_key}")
        markup.add(button)
    return markup

# Обробка команди /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Створення Inline-клавіатур
    language_markup = create_language_keyboard()
    package_markup = create_package_keyboard()

    bot.send_message(chat_id, f"Привіт, {message.from_user.first_name} {message.from_user.last_name}!\nЯ бот для продажу онлайн-курсу 'ПЕРЕГОВОРИ I ЛIДЕРСТВО' !\nОберіть,,будь ласка,мову:", reply_markup=language_markup)


@bot.callback_query_handler(func=lambda call: call.data in languages)
def handle_language_selection(call):
    chat_id = call.message.chat.id
    language = call.data
    if language == 'ru':
        bot.send_message(chat_id, "Вибачте, але поки я не розмовляю мовою окупанта.")
    else:
        # Тут ви можете зберегти вибір мови користувача в базі даних, якщо потрібно.
        bot.send_message(chat_id, f"Дякую,що вибрали {languages[language]}")

@bot.message_handler(func=lambda message: message.text == f'🇺🇦 {languages["ua"]}')
def handle_ukrainian_language(message):
    bot.send_message(message.chat_id, f"Що саме Вас цікавить? {languages[language]}",
                     reply_markup=package_markup)



# Обработка команд для каждого пакета
@bot.callback_query_handler(func=lambda call: call.data.startswith("package_"))
def handle_package_selection(call):
    user_id = call.from_user.id
    package_key = call.data.split("_")[1]
    selected_package = packages.get(package_key)

    if selected_package:
        bot.send_message(user_id, f"{selected_package['name']}\n\n{selected_package['description']}\n\nЦена: {selected_package['price']}")

@bot.message_handler(func=lambda message: message.text == "Отримати 3 випадкових уроки з курсу безплатно")
def handle_free_lessons(message):
    user_id = message.from_user.id

    # Проверка, получал ли пользователь уже бесплатные уроки
    if user_id in users_with_free_lessons:
        bot.send_message(user_id, "Ви вже отримували безплатні уроки.")
    else:
        # Генерация трех случайных уроков
        random_lessons = random.sample(range(2, 58), 3)  # Строки B2:B57

        # Отправка пользователю ссылок на уроки
        for lesson_number in random_lessons:
            lesson_url = gsheet.cell(lesson_number, 3).value  # Строки A2:A57
            bot.send_message(user_id, f"Безкоштовний урок : {lesson_url}")

        # Добавление пользователя в список тех, кто уже получал бесплатные уроки
        users_with_free_lessons.add(user_id)

# TODO: Добавьте обработку оплаты через Portmone

# Запуск бота
bot.polling()
