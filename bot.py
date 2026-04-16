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

user_expressions = {} # хранилище 

def get_keyboard(): # сама клавиатура 
    """Возвращает клавиатуру с кнопками калькулятора"""
    
    row_brackets = [
        InlineKeyboardButton(text="(", callback_data="("),
        InlineKeyboardButton(text=")", callback_data=")"),
    ]
    
    row1 = [
        InlineKeyboardButton(text="7", callback_data="7"),
        InlineKeyboardButton(text="8", callback_data="8"),
        InlineKeyboardButton(text="9", callback_data="9"),
        InlineKeyboardButton(text="/", callback_data="/"),
    ]
    
    row2 = [
        InlineKeyboardButton(text="4", callback_data="4"),
        InlineKeyboardButton(text="5", callback_data="5"),
        InlineKeyboardButton(text="6", callback_data="6"),
        InlineKeyboardButton(text="*", callback_data="*"),
    ]
    
    row3 = [
        InlineKeyboardButton(text="1", callback_data="1"),
        InlineKeyboardButton(text="2", callback_data="2"),
        InlineKeyboardButton(text="3", callback_data="3"),
        InlineKeyboardButton(text="-", callback_data="-"),
    ]
    
    row4 = [
        InlineKeyboardButton(text="0", callback_data="0"),
        InlineKeyboardButton(text=".", callback_data="."),
        InlineKeyboardButton(text="=", callback_data="="),
        InlineKeyboardButton(text="+", callback_data="+"),
    ]
    
    row5 = [
        InlineKeyboardButton(text="C", callback_data="C"),
        InlineKeyboardButton(text="←", callback_data="DEL"),
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        row_brackets,
        row1, 
        row2, 
        row3, 
        row4, 
        row5
    ])
    return keyboard

@dp.message(Command("start")) # команда старт
async def start_command(message: Message):
    # Запоминаем, что у этого пользователя пустое выражение
    user_expressions[message.from_user.id] = ""
    
    await message.answer(
        reply_markup=get_keyboard()
    )

@dp.callback_query() # обрабатывает нажатие всех кнопок
async def handle_click(callback: CallbackQuery):
    user_id = callback.from_user.id
    button = callback.data
    current = user_expressions.get(user_id, "")
    
    
    if button == "=": # кнопка равно 
        try:
            result = eval(current)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            user_expressions[user_id] = str(result)
            text = f"📊 {current} = {result}"
        except Exception:
            text = f"❌ Ошибка в выражении: {current}\n💡 Проверь скобки!"
            user_expressions[user_id] = ""
    

    elif button == "C": # кнопка для очистки всего
        user_expressions[user_id] = ""
        text = "✅ Очищено. Вводи новый пример со скобками!"
    
    elif button == "DEL": # кнопка для удаления последнего символа
        user_expressions[user_id] = current[:-1]
        text = f"📝 {user_expressions[user_id] or 'пусто'}"
    
    else:
        user_expressions[user_id] = current + button
        text = f"📝 {user_expressions[user_id]}"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_keyboard()
    )
    
    await callback.answer()

@dp.message()
async def any_text(message: Message):
    await message.answer(
        reply_markup=get_keyboard()
    )

async def main():
    print("Бот запущен!")
    print("Скобки добавлены в отдельный ряд!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())