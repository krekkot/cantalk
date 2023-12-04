from aiogram import Router, F
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.types import CallbackQuery
from aiogram import types
from handlers.ualang import cmd_ua
from aiogram.types import InputFile
from aiogram.types import PhotoSize
from aiogram.types import InputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hide_link
from handlers.kursnbu import usd_exchange_rate
router = Router()

# Ініціалізація об'єкта для роботи з Google Spreadsheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../credentials1.json", scope)
client = gspread.authorize(creds)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
worksheet_name = "Безкоштовні уроки"
worksheet = client.open_by_url(spreadsheet_url).worksheet(worksheet_name)


# Словник для української мови
ua_packages = {
    'basic': {
        'name': 'Пакет LIFE',
        'description': '-Індивідуальний робочий кабінет\n-100 відеоуроків,\n-8 домашніх завдань (без перевірки),\n-7 тестувань з перевіркою,\n-3 вебінари,\n-Усі матеріали тренінгу доступні у записі 1 місяць,\n-Доступ до закритої Facebook групи на 8 тижнів',
        'price': 115.00,
    },
    'standard': {
        'name': 'Пакет BUSINESS',
        'description': '-Індивідуальний робочий кабінет із терміном доступу 3 місяці.\n\n-Симуляція реальних переговорів на платформі iDG\n<a href="https://youtu.be/RFPj55WNR-M?si=v2bS78FBZYR6kVtz">Відео про платформу iDg</a>,\n<a href="https://cantalk.com.ua/wp-content/uploads/debrief-report-example.pdf">завантажити приклад звіту</a>\n\n-Аналіз вашого «переговорного почерку» та патерни поведінки з постійним зворотнім зв’язком партнерів та тренера\n<a href="https://cantalk.com.ua/wp-content/uploads/fragment.m4a">Фрагмент гри «Продай ручку»</a>\n\n-18 ігрових практикумів та відео/аудіо записи за вашою участю.\n<a href="https://youtu.be/y78Oau7RlO0?si=tOHwJB7848fcGCFx">Приклад запису гри 10000</a>\n\n-Розбір 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою).\n<a href="https://cantalk.com.ua/wp-content/uploads/Home_task_1_ua.pdf">Завантажити Приклад Домашнього завдання #1</a>\n\n-Доступ до закритої Facebook та Viber групи на 3 місяці\n\n-БОНУС: 50% знижки на онлайн кембриджське тестування Belbin Team Roles.\n<a href="https://drive.google.com/file/d/1yNHJgQ1Cc-40l6RjG9uyNsJOcP9A_xRe/view?usp=share_link">Що це за тест?</a><a href="https://drive.google.com/file/d/1O5z3pKlSd_EbpCRrN2kvrcIc7cOBWYE9/view">Переглянути зразок звіту</a>',
        'price': 487.00,
    },
    'premium': {
        'name': 'Пакет PREMIUM',
        'description': '-Все, що входить до пакета “Business” + \n\n-Індивідуальний графік занять впродовж 6 місяців\n\n-Онлайн кембріджське тестування Belbin Team Roles та індивідуальна аналітична сесія\n<a href="https://drive.google.com/file/d/1yNHJgQ1Cc-40l6RjG9uyNsJOcP9A_xRe/view?usp=share_link">Що це за тест?\n</a><a href="https://drive.google.com/file/d/1O5z3pKlSd_EbpCRrN2kvrcIc7cOBWYE9/view">Переглянути зразок звіту</a>\n\n-Ігрові спаринги з найсильнішими партнерами – Переможцями попередніх потоків \n\n-Особисте супроводження тренера при виконанні всіх завдань – 7 тестувань, 5 домашніх завдань, фільмів та текстів (з перевіркою)\n<a href="https://docs.google.com/forms/d/e/1FAIpQLScRnDQvmRAy7hbcZHtZS9CX3uLccgVolYisOKMi5A-DLkbOSw/viewform">Отримати зворотний зв’язок на вступну Анкету</a>\n\n-Персональна підтримка 24/7 у переговорних кейсах\n\n-Три 60-хвилинні skype-сесії з тренером для відпрацювання практичних кейсів\n<a href="https://cantalk.com.ua/wp-content/uploads/case_example_ukr.pdf">Завантажити зразок кейса.</a>\n\n-Підбір спеціальних практикумів та розбір кейсів з урахуванням Ваших актуальних життєвих та професійних завдань',
        'price': 932.00,
    }
}

# Словник для російської мови
ru_packages = {
    'basic': {
        'name': 'Пакет LIFE',
        'description': '-Индивидуальный рабочий кабинет\n-100 видеоуроков,\n-8 домашних заданий (без проверки),\n-7 тестов с проверкой,\n-3 вебинара,\n-Все материалы тренинга доступны в записи 1 месяц,\n-Доступ к закрытой Facebook группе на 8 недель',
        'price': 115.00,
    },
    'standard': {
        'name': 'Пакет BUSINESS',
        'description': '-Все, что входит в пакет "Life" +\n-Индивидуальный рабочий кабинет с сроком доступа 3 месяца.\n-Симуляция реальных переговоров на платформе iDG (Harvard, MIT platform)\n-Анализ вашего "переговорного почерка" и паттернов поведения с постоянной обратной связью партнеров и тренера\n 18 игровых практикумов и видео/аудио записи с вашим участием\n Разбор 7 тестов, 5 домашних заданий, фильмов и текстов (с проверкой)\n Доступ к закрытым Facebook и Viber группам на 3 месяца\n БОНУС: 50% скидка на онлайн кембриджское тестирование Belbin Team Roles',
        'price': 487.00,
    },
    'premium': {
        'name': 'Пакет PREMIUM',
        'description': '-Все, что входит в пакет "Business" + \n-Индивидуальное расписание занятий на протяжении 6 месяцев\n-Онлайн кембриджское тестирование Belbin Team Roles и индивидуальная аналитическая сессия\n Игровые спарринги с самыми сильными партнерами - Победителями предыдущих потоков \n Личное сопровождение тренера при выполнении всех заданий - 7 тестов, 5 домашних заданий, фильмов и текстов (с проверкой)\n Персональная поддержка 24/7 в переговорных кейсах\n Три 60-минутные skype-сессии с тренером для отработки практических кейсов \n Подбор специальных практикумов и разбор кейсов с учетом Ваших актуальных жизненных и профессиональных задач',
        'price': 932.00,
    }
}


selected_packages = {}
current_language = 'UA'  # Поточна мова користувача
if current_language == 'UA':
    selected_packages = ua_packages
else:
    selected_packages = ru_packages

package_name = selected_packages['basic']['name']
package_description = selected_packages['basic']['description']
package_price = selected_packages['basic']['price']


async def show_package_description(query: types.CallbackQuery, callback_data: dict):
    package_key = callback_data['package_key']  # Отримайте ключ пакету з callback_data
    package_info = selected_packages.get(package_key)  # Отримайте інформацію про пакет
    if package_info:
        name = package_info['name']
        price = package_info['price']
        description = package_info['description']
        priceuah = int(float(price) * usd_exchange_rate)
        message_text = f" {name}\n\n{description}\n\nЦіна: usd {price}0 (грн {priceuah})"
        pay_button = InlineKeyboardButton(text=f'Придбати курс за {priceuah} грн ', callback_data=f"pay{priceuah}")
        await query.message.answer(message_text, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back1')],[pay_button],
            ]
        ))


@router.callback_query(lambda query: query.data =='back')
async def process_back_button1(callback_query: types.CallbackQuery):
    buttons = []
    back = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='back')],
        ]
    )
    await cmd_negotiation_course(callback_query=callback_query)


@router.callback_query(lambda query: query.data =='back3')
async def process_back_button3(callback_query: types.CallbackQuery):
    buttons = []
    back = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='back3')],
        ]
    )
    # Використовуйте callback_query.message замість передачі callback_query в якості аргументу
    await cmd_ua(callback_query.message)


@router.callback_query(lambda query: query.data =='back1')
async def process_back_button2(callback_query: types.CallbackQuery):
    buttons = []
    back = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='back1')],
        ]
    )
    await package_course(callback_query=callback_query)

@router.callback_query(lambda query: query.data =="negotiation_course")
@router.callback_query(F.text =="Онлайн-курс 'переговори i лiдерство'")
async def cmd_negotiation_course(callback_query: CallbackQuery):
    buttons = []
    back5 = InlineKeyboardButton(text='Назад', callback_data='back3')
    site_button = InlineKeyboardButton(text='Сайт курсу😎', url='https://cantalk.com.ua')
    course_information_button = InlineKeyboardButton(text='Про онлайн-курс "ПЕРЕГОВОРИ I ЛIДЕРСТВО"', callback_data='course_information')
    package_button = InlineKeyboardButton(text='Вартість курсу👌', callback_data='package')
    couch_button = InlineKeyboardButton(text='Хто веде навчання ?🤗', callback_data='couch')
    quest_button = InlineKeyboardButton(text='Чому Вам варто пройти цей курс ?🤨', callback_data='why_im')
    free_lesson_button = InlineKeyboardButton(text='Бонус!🆓Отримати 3 зі 100 випадкових уроки з курсу ', callback_data='handle_free_lessons')
    buttons.append([site_button])
    buttons.append([free_lesson_button])
    buttons.append([package_button])
    buttons.append([couch_button])
    buttons.append([quest_button])
    buttons.append([course_information_button])
    buttons.append([back5])  # Додаємо back5 (InlineKeyboardMarkup) без зайвого вкладення
    buttons = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)
    await callback_query.message.answer("Раді бачити Вашу зацікавленність курсом!\nЩо саме Вас цікавить?", reply_markup=buttons)



@router.callback_query(lambda query: query.data == "package")
@router.callback_query(F.text == 'Вартість курсів')
async def package_course(callback_query: CallbackQuery):
    buttons1 = []
    back1 = InlineKeyboardButton(text='Назад', callback_data='back')

    for package_key, package_info in selected_packages.items():
        button_text = f"Дізнатись про {package_info['name']}"
        package_button = InlineKeyboardButton(text=button_text, callback_data=f"package_{package_key}")
        buttons1.append([package_button])

    buttons1.append([back1])
    buttons1 = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons1)
    await callback_query.message.answer(
        "Будемо раді розповісти Вам про наші пакети\nЧи готові ви всього за 8 тижнів тотальнио прокачати свої навички комунікації та почати отримувати бажаний результат у переговорах?",
        reply_markup=buttons1)
@router.callback_query(lambda query: query.data.startswith("package_"))
async def process_package_choice(callback_query: types.CallbackQuery):
    package_key = callback_query.data.split("_")[1]
    callback_data = {'package_key': package_key}
    await show_package_description(callback_query, callback_data)

@router.callback_query(lambda query: query.data =="course_information")
async def course_information(callback_query: CallbackQuery):
    buttons2 = []
    back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])
    buttons2 = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons2)
    await callback_query.message.answer("Вже скоро тут буде інформація",reply_markup=back)

@router.callback_query(lambda query: query.data == "couch")
async def couch_information(callback_query: CallbackQuery):
    buttons3 = []
    back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])
    buttons3 = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons3)
    await callback_query.message.answer(
        f"{hide_link('https://cantalk.com.ua/wp-content/uploads/2020/01/second_screen.jpg')}"
        f'Навчання проводить <a href=\'https://www.facebook.com/l.slobodyanyuk/\'>Людмила Слободянюк</a>\n\n-Генеральний директор «TransAvia Group»\n\n-16 років досвіду\nробота ТОП-менеджером у 3-х найбільших галузевих підприємствах СНД\n\n-Випускниця програм\nMeditate and Mediate (викладач William Uri), Negotiation and Influence (MIT Sloan School of Management), Harvard Program on Negotiation and Leadership (Harvard Law School)\n\n-Переговори\nна 35 міжнародних ринках з річним оборотом $650.000.000 в управлінні\n\n-Акредитований тренер\nBelbin Team Roles UK (2014)\n\nПредставник світової консалтингової компанії\nICF SH&E\n\n-Провідний Інструктор\nNegotiation-Pro Camp Negotiation Institute',reply_markup=back
    )


@router.callback_query(lambda query: query.data =="why_im")
async def why_im_course(callback_query: CallbackQuery):
    buttons4 = []
    back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])
    buttons4 = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons4)
    await callback_query.message.answer("💬У реальному житті ніхто та ніколи не казатиме Вам:\n-Ось тут Вас підвели міміка і жести;-Тут Ви повелися неправильно;\n-А в цей момент варто було поступитися;\n-А через ці аргументи переговори “провалилися”.\nВи не дізнаєтеся про це не через те, що хтось промовчить!\nЗазвичай люди або не усвідомлюють, що впливає на переговори, або просто не фокусують на цьому свою увагу.\n\nОтож чому Вам варто пройти цей курс:\n-Точка зростання — різниця між бажаним результатом та змістом нашого досвіду☝.☝️\n-5 годин практики на тиждень вербальної та невербальної комунікації. Про що говорять ваші жести, інтонації, підтекст?👀\nКурс допоможе дати відповіді на такі запитання:\nЯк примножити?💰\nЯк домовитись?🤝\nЯк бути собою?🙀\n-Сертифікація.📃\n-Курс пройшли 1768 учасників – керівники та підприємці.📊\n-100% повернення коштів найкращому студенту.👍",reply_markup=back)


