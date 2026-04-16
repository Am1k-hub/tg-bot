import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ТВОЙ ТОКЕН - ЗАМЕНИ!!!
TOKEN = "8765796060:AAGRvCegUHdxfgBvvKm8N-j0BRk0iH3nBF8"

# Создаем бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Тут будем хранить что нажал каждый пользователь
user_data = {}

# ========== КНОПКИ ==========
def get_buttons():
    """Просто создаем кнопки"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="7", callback_data="7"),
                InlineKeyboardButton(text="8", callback_data="8"),
                InlineKeyboardButton(text="9", callback_data="9"),
                InlineKeyboardButton(text="/", callback_data="/"),
            ],
            [
                InlineKeyboardButton(text="4", callback_data="4"),
                InlineKeyboardButton(text="5", callback_data="5"),
                InlineKeyboardButton(text="6", callback_data="6"),
                InlineKeyboardButton(text="*", callback_data="*"),
            ],
            [
                InlineKeyboardButton(text="1", callback_data="1"),
                InlineKeyboardButton(text="2", callback_data="2"),
                InlineKeyboardButton(text="3", callback_data="3"),
                InlineKeyboardButton(text="-", callback_data="-"),
            ],
            [
                InlineKeyboardButton(text="0", callback_data="0"),
                InlineKeyboardButton(text=".", callback_data="."),
                InlineKeyboardButton(text="=", callback_data="="),
                InlineKeyboardButton(text="+", callback_data="+"),
            ],
            [
                InlineKeyboardButton(text="ОЧИСТИТЬ", callback_data="C"),
                InlineKeyboardButton(text="УДАЛИТЬ", callback_data="DEL"),
            ],
        ]
    )
    return keyboard

# ========== КОМАНДА СТАРТ ==========
@dp.message(Command("start"))
async def start(message: Message):
    user_data[message.from_user.id] = ""  # Очищаем историю пользователя
    await message.answer(
        "🧮 КАЛЬКУЛЯТОР\n\nНажимай на кнопки:",
        reply_markup=get_buttons()
    )

# ========== ОБРАБОТЧИК НАЖАТИЙ ==========
@dp.callback_query()
async def on_click(callback: CallbackQuery):
    user_id = callback.from_user.id
    button = callback.data  # Что нажал пользователь
    current = user_data.get(user_id, "")  # Что уже набрано
    
    # Если нажали "="
    if button == "=":
        try:
            # Считаем пример
            result = eval(current)
            # Убираем лишние нули
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
            user_data[user_id] = str(result)
            text = f"{current} = {result}"
        except:
            text = f"Ошибка в примере: {current}"
            user_data[user_id] = ""
    
    # Если нажали "ОЧИСТИТЬ"
    elif button == "C":
        user_data[user_id] = ""
        text = "Очищено. Вводи новый пример:"
    
    # Если нажали "УДАЛИТЬ"
    elif button == "DEL":
        user_data[user_id] = current[:-1]
        text = f"📝 {user_data[user_id] or 'Пусто'}"
    
    # Если нажали цифру или операцию
    else:
        user_data[user_id] = current + button
        text = f"📝 {user_data[user_id]}"
    
    # Обновляем сообщение
    await callback.message.edit_text(
        text,
        reply_markup=get_buttons()
    )
    await callback.answer()

# ========== ЕСЛИ ПИШУТ ТЕКСТ ==========
@dp.message()
async def any_text(message: Message):
    await message.answer("Нажимай на кнопки, не пиши текст!", reply_markup=get_buttons())

# ========== ЗАПУСК ==========
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())