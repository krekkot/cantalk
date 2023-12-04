#from database.database import *
from random import randint
from aiogram.types import Message
from aiogram import F, Router


router_ads = Router()

@router_ads.message(F.text == '/send')
async def sendall(message: Message):
  if message.chat.type == 'private' or message.chat.type == 'supergroup' or message.chat.type == 'group':
    if message.from_user.id == 1240754158:
      text = message.text[6:].strip()
      db = Database('database/game.db')  # Створюємо об'єкт класу Database
      telegram_ids, group_ids = db.get_users()  # Викликаємо метод get_users() на створеному об'єкті
      for row in telegram_ids + group_ids:
        try:
          await message.answer(text=text)  # Викликаємо метод send_message з передачею chat_id та text як ключових аргументів
          if row[1] is not None and int(row[1]) != 1:
            db.set_active(row[0], 1)  # Викликаємо метод set_active() на створеному об'єкті
        except Exception as e:
          logging.error(f'Error sending message to user {row[0]}: {e}')
          db.set_active(row[0], 0)  # Викликаємо метод set_active() на створеному об'єкті
      await message.answer(text="Готово")

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM ads WHERE telegram_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO ads (telegram_id) VALUES (?)", (user_id,))

    def set_active(self, user_id, active):
        with self.connection:
            self.cursor.execute("UPDATE ads SET active = ? WHERE telegram_id = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            telegram_ids = self.cursor.execute("SELECT telegram_id, active FROM ads").fetchall()
            group_ids = self.cursor.execute("SELECT group_id, active FROM ads").fetchall()
            return telegram_ids, group_ids
