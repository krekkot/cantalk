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
worksheet = client.open_by_url(sheet_url).worksheet("Безкоштовні уроки")

# Установка токена бота
bot = telebot.TeleBot('6337428893:AAFFWOQRUTi-3U_FVM_TE4Izz-VJpRuH6ws')

languages = {'ru': 'Русский', 'uk': 'Українська'}
selected_user_packages = {}
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
    markup.add(telebot.types.InlineKeyboardButton('Сайт курсу', url='https://cantalk.com.ua/'))
    markup.add(telebot.types.InlineKeyboardButton('Отримати 3 випадкових уроки з курсу безплатно', callback_data='handle_free_lessons'))
    return markup



# Обробка команди /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Створення Inline-клавіатур
    language_markup = create_language_keyboard()
    package_markup = create_package_keyboard()

    bot.send_message(chat_id, f"Привіт, {message.from_user.first_name} {message.from_user.last_name}!\nЯ бот для продажу онлайн-курсу 'ПЕРЕГОВОРИ I ЛIДЕРСТВО' !\nОберіть, будь ласка, мову:", reply_markup=language_markup)

# @bot.callback_query_handler(func=lambda call: call.data in languages)
@bot.callback_query_handler(func=lambda call: call.data in languages)
def handle_language_selection(call):
    chat_id = call.message.chat.id
    language = call.data
    if language == 'ru':
        bot.send_message(chat_id, "Вибачте, але поки я не розмовляю мовою окупанта.\nВиберіть, будь ласка, іншу мову", reply_markup=create_language_keyboard())
    else:
        # Тут ви можете зберегти вибір мови користувача в базі даних, якщо потрібно.
        bot.send_message(chat_id, f"Дякую, що вибрали Українську!\n Що саме Вас цікавить?", reply_markup=create_package_keyboard())

# Обработка команд для каждого пакета
def return_keyboard(package_key):
    markup = types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Назад', callback_data=f"back_{package_key}"))
    return markup
@bot.callback_query_handler(func=lambda call: call.data.startswith("package_"))
def handle_package_selection(call):
    user_id = call.from_user.id
    package_key = call.data.split("_")[1]
    selected_user_packages[user_id] = package_key  # Зберегти вибір користувача
    selected_package = packages.get(package_key)

    if selected_package:
        bot.send_message(user_id, f"{selected_package['name']}\n\n{selected_package['description']}\n\nЦена: {selected_package['price']}", reply_markup=return_keyboard(package_key))

@bot.callback_query_handler(func=lambda call: call.data.startswith("back_"))
def handle_back_button(call):
    user_id = call.from_user.id
    package_key = call.data.split("_")[1]
    package_markup = create_package_keyboard()
    bot.send_message(user_id, "Виберіть, будь ласка, пакет:", reply_markup=package_markup)


@bot.callback_query_handler(func=lambda call: call.data == "handle_free_lessons")
def handle_free_lessons(call):
    user_id = call.from_user.id

    # Перевірка, чи користувач вже отримував безкоштовні уроки
    if user_id in users_with_free_lessons:
        bot.send_message(user_id, "Ви вже отримували безкоштовні уроки.")
    else:
        # Генерування трьох випадкових уроків
        random_lessons = random.sample(range(2, 58), 3)  # Рядки B2:B57

        # Надсилання користувачеві посилань на уроки
        for lesson_number in random_lessons:
            lesson_url = gsheet.cell(lesson_number, 3).value  # Рядки A2:A57
            bot.send_message(user_id, f"Безкоштовний урок: {lesson_url}")

        # Додавання користувача до списку тих, хто вже отримав безкоштовні уроки
        users_with_free_lessons.add(user_id)

        # Оновлення таблиці Google-документа для відзначення користувача
        try:
            # Отримання таблиці на сторінці "Безкоштовні уроки"
            worksheet = client.open_by_url(sheet_url).worksheet("Безкоштовні уроки")

            # Перевірка, чи користувач вже є в таблиці (за допомогою унікального ідентифікатора)
            # І додавання інформації про користувача, якщо він відсутній
            user_record = {
                'user_id': user_id,
                # Додайте інші дані користувача, які вам потрібні
            }
            existing_users = worksheet.col_values(1)  # Перевірка існуючих користувачів за першим стовпчиком
            if str(user_id) not in existing_users:
                user_data_list = [user_record.get(key, '') for key in ['user_id']]  # Вставте всі дані про користувача
                worksheet.append_row(user_data_list)  # Додавання користувача до таблиці
            else:
                print(f"Користувач {user_id} вже отримував безкоштовні уроки.")
                bot.send_message(user_id, "Ви вже отримували безкоштовні уроки.")

        except Exception as e:
            print(f"Помилка при оновленні таблиці: {str(e)}")


# TODO: Добавьте обработку оплаты через Portmone

# Запуск бота
bot.polling()

print