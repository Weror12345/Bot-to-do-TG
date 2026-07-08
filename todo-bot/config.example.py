import os

BOT_TOKEN = "************************************"
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в переменной окружения BOT_TOKEN")