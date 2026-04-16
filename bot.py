import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения выражений каждого пользователя
выражения_пользователей = {}

# ===== КЛАВИАТУРА =====
def создать_клавиатуру():
    """Возвращает клавиатуру с кнопками калькулятора"""
    
    # Первый ряд
    ряд1 = [
        InlineKeyboardButton(text="7", callback_data="7"),
        InlineKeyboardButton(text="8", callback_data="8"),
        InlineKeyboardButton(text="9", callback_data="9"),
        InlineKeyboardButton(text="/", callback_data="/"),
    ]
    
    # Второй ряд
    ряд2 = [
        InlineKeyboardButton(text="4", callback_data="4"),
        InlineKeyboardButton(text="5", callback_data="5"),
        InlineKeyboardButton(text="6", callback_data="6"),
        InlineKeyboardButton(text="*", callback_data="*"),
    ]
    
    # Третий ряд
    ряд3 = [
        InlineKeyboardButton(text="1", callback_data="1"),
        InlineKeyboardButton(text="2", callback_data="2"),
        InlineKeyboardButton(text="3", callback_data="3"),
        InlineKeyboardButton(text="-", callback_data="-"),
    ]
    
    # Четвертый ряд
    ряд4 = [
        InlineKeyboardButton(text="0", callback_data="0"),
        InlineKeyboardButton(text=".", callback_data="."),
        InlineKeyboardButton(text="=", callback_data="="),
        InlineKeyboardButton(text="+", callback_data="+"),
    ]
    
    # Пятый ряд (кнопки управления)
    ряд5 = [
        InlineKeyboardButton(text="C", callback_data="C"),
        InlineKeyboardButton(text="←", callback_data="DEL"),
    ]
    
    # Собираем все ряды в клавиатуру
    клавиатура = InlineKeyboardMarkup(inline_keyboard=[ряд1, ряд2, ряд3, ряд4, ряд5])
    return клавиатура

# ===== КОМАНДА СТАРТ =====
@dp.message(Command("start"))
async def команда_старт(сообщение: Message):
    # Запоминаем, что у этого пользователя пустое выражение
    выражения_пользователей[сообщение.from_user.id] = ""
    
    # Отправляем сообщение с клавиатурой
    await сообщение.answer(
        "🔢 КАЛЬКУЛЯТОР\nВводи пример кнопками:",
        reply_markup=создать_клавиатуру()
    )

# ===== ОБРАБОТКА НАЖАТИЙ НА КНОПКИ =====
@dp.callback_query()
async def обработать_нажатие(нажатие: CallbackQuery):
    id_пользователя = нажатие.from_user.id
    кнопка = нажатие.data  # что нажал пользователь
    текущее = выражения_пользователей.get(id_пользователя, "")
    
    # КНОПКА "РАВНО"
    if кнопка == "=":
        try:
            результат = eval(текущее)  # вычисляем выражение
            # Убираем .0 у целых чисел
            if isinstance(результат, float) and результат.is_integer():
                результат = int(результат)
            
            выражения_пользователей[id_пользователя] = str(результат)
            текст_ответа = f"{текущее} = {результат}"
        except:
            текст_ответа = f"❌ Ошибка: {текущее}"
            выражения_пользователей[id_пользователя] = ""
    
    # КНОПКА "ОЧИСТИТЬ ВСЁ"
    elif кнопка == "C":
        выражения_пользователей[id_пользователя] = ""
        текст_ответа = "✅ Очищено"
    
    # КНОПКА "УДАЛИТЬ ПОСЛЕДНИЙ СИМВОЛ"
    elif кнопка == "DEL":
        выражения_пользователей[id_пользователя] = текущее[:-1]
        текст_ответа = f"📝 {выражения_пользователей[id_пользователя] or 'пусто'}"
    
    # ОБЫЧНЫЕ КНОПКИ (цифры и операции)
    else:
        выражения_пользователей[id_пользователя] = текущее + кнопка
        текст_ответа = f"📝 {выражения_пользователей[id_пользователя]}"
    
    # Обновляем сообщение (меняем текст и клавиатуру)
    await нажатие.message.edit_text(
        текст_ответа,
        reply_markup=создать_клавиатуру()
    )
    
    # Подтверждаем нажатие (чтобы убрать часики на кнопке)
    await нажатие.answer()

# ===== ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПИШЕТ ТЕКСТ =====
@dp.message()
async def любой_текст(сообщение: Message):
    await сообщение.answer(
        "❌ Пользуйся кнопками!",
        reply_markup=создать_клавиатуру()
    )

# ===== ЗАПУСК =====
async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())