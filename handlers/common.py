from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
router = Router()

languages = {"ru": 'Русский', "ua": 'Українська'}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1WWmBw7LSUg8WHrQjbVMfSNl_2EA8NYUcE6Zpg2LiBto/edit?usp=sharing"
worksheet_name = "Безкоштовні уроки"
worksheet = client.open_by_url(spreadsheet_url).worksheet(worksheet_name)


users_with_free_lessons = set()


def load_users_with_free_lessons():
    global users_with_free_lessons
    users_with_free_lessons = set()
    worksheet = client.open_by_url(spreadsheet_url).worksheet("Безкоштовні уроки")

    # Отримати всі значення в першому стовпці (ідентифікатори користувачів)
    user_ids = worksheet.col_values(1)

    # Починаючи з другого рядка (перший рядок - заголовки), переберіть кожний рядок
    for user_id in user_ids[1:]:
        if user_id.strip():  # Перевірка, чи рядок не порожній
            try:
                users_with_free_lessons.add(int(user_id))
            except ValueError:
                print(f"Неправильний формат даних: {user_id}")

    return users_with_free_lessons


users_with_free_lessons = load_users_with_free_lessons()

print("Список користувачів з безкоштовними уроками:")
print(users_with_free_lessons)


@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    button_ru = KeyboardButton(text="Русский")
    button_ua = KeyboardButton(text="Українська")
    user = message.from_user
    user_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name

    # Встановлення параметрів resize_keyboard та keyboard_button_height
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_ru, button_ua]],
        resize_keyboard=True,  # Зробить кнопки меншими
        keyboard_button_height=2  # Задає висоту кнопок (в цьому випадку 2)
    )

    await message.answer(f"Привіт, {user_name}!🙃\nРаді бачити Вас у Transavia Group🤗!\nОберіть, будь ласка, мову:", reply_markup=keyboard)




# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)
