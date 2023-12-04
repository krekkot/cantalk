from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

# Клас ChatTypeFilter наслідується від BaseFilter і використовується для фільтрації повідомлень за типом чату.
class ChatTypeFilter(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        # Конструктор класу приймає параметр chat_type, який може бути строкою або списком типів чатів.
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:  # [3]
        # Метод __call__ викликається для кожного повідомлення і повертає True, якщо тип чату відповідає параметру chat_type.
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type