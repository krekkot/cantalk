from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from aiogram import types
from handlers.common import users_with_free_lessons
router = Router()


print("Список користувачів з безкоштовними уроками:")
print(users_with_free_lessons)


# Ініціалізація об'єкта для роботи з Google Spreadsheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
worksheet_name = "Уроки"
worksheet = client.open_by_url(spreadsheet_url).worksheet(worksheet_name)



@router.callback_query(lambda query: query.data == 'handle_free_lessons')
async def handle_free_lessons(callback_query: types.CallbackQuery):
    buttons5 = []
    back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])
    buttons5 = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons5)
    user_id = callback_query.from_user.id
    print(user_id, users_with_free_lessons)
    user_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}" if callback_query.from_user.last_name else callback_query.from_user.first_name
    # Перевірка, чи користувач вже отримував безкоштовні уроки
    if user_id in users_with_free_lessons:
        await callback_query.message.answer('Вибачте,але Ви вже отримували безкоштовні уроки.',reply_markup=back)
    else:
        # Генерування трьох випадкових уроків
        random_lessons = random.sample(range(2, 58), 3)

        # Надсилання користувачеві посилань на уроки
        for lesson_number in random_lessons:
            lesson_url = worksheet.cell(lesson_number, 3).value  # Рядки A2:A57
            await callback_query.message.answer(f"Безкоштовний урок: {lesson_url}",reply_markup=back)

        # Додавання користувача до списку тих, хто вже отримав безкоштовні уроки
        users_with_free_lessons.add(user_id)
        try:
            # Отримання таблиці на сторінці "Безкоштовні уроки"
            worksheet_arg = client.open_by_url(spreadsheet_url).worksheet("Безкоштовні уроки")

            # Перевірка, чи користувач вже є в таблиці (за допомогою унікального ідентифікатора)
            # І додавання інформації про користувача, якщо він відсутній
            user_record = {
                'user_id': user_id,
                'user_name':user_name
                # Додайте інші дані користувача, які вам потрібні
            }
            existing_users = worksheet_arg.col_values(1)  # Перевірка існуючих користувачів за першим стовпчиком
            if str(user_id) not in existing_users:
                user_data_list = [user_record.get('user_id', ''), user_record.get('user_name', '')]  # Вставте всі дані про користувача
                worksheet_arg.append_row(user_data_list)  # Додавання користувача до таблиці
            else:
                await callback_query.message.answer("Ви вже отримували безкоштовні уроки.",reply_markup=back)

        except Exception as e:
            print(f"Помилка при оновленні таблиці: {str(e)}")

@router.callback_query(lambda query: query.data =='back')
async def process_back_button2(callback_query: types.CallbackQuery):
    await handle_free_lessons(callback_query)


