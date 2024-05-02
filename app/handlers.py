from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import app.keyboards as kb
import app.states as st
import app.api.response as api_res

router = Router()


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
async def create_keyboard(items):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        keyboard.add(KeyboardButton(item['name']))
    return keyboard


#Старт
@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(f'Привет👋\nВыбери пункт из меню🔍',
                        reply_markup=kb.start)


#Парсирование===========================================================================================


@router.message(lambda message: message.text == "Парсировать")
async def parsing_start(message: Message):
    await message.answer('Выберите пункт из меню', reply_markup=kb.quantity_selection)

@router.message(lambda message: message.text == "Продолжить")
async def pasring_continuation(message: Message):
    response, error = api_res.parsing(None)
    if response:
        await message.answer(f'✅{response}', reply_markup=kb.start)
    elif error:
        await message.answer(f'❗{error}', reply_markup=kb.start)

@router.message(lambda message: message.text == "Указать количество")
async def get_products_count_start(message: Message, state: FSMContext):
    await message.answer('Укажите количество', reply_markup=kb.cancel)
    await state.set_state(st.Parsing.wait_products_count)
    

@router.message(st.Parsing.wait_products_count)
async def get_products_count(message: Message, state: FSMContext):
    try:
        products_count = int(message.text)
        if 0 < products_count <= 50:
            response, error = api_res.parsing(products_count)
            if response:
                await message.answer(f'✅{response}', reply_markup=kb.start)
                await state.clear()
            elif error:
                await message.answer(f'❗{error}', reply_markup=kb.start)
        else:
            await message.answer('Введите число от 1 до 50', reply_markup=kb.cancel)
    except ValueError:
        await message.answer('Введите число', reply_markup=kb.cancel)


#Получение списка===========================================================================================


@router.message(lambda message: message.text == "Получить список")
async def get_products_list(message: Message):
    
    products_list = api_res.get_products_list()
    if products_list is not None:
        if products_list != []:
            await message.answer("🛒*Товары:*\n\n", parse_mode="Markdown", reply_markup=await kb.inline_products(products_list))
        else:
            await message.answer("*🔎Дежурств не обнаружено*", parse_mode="Markdown")
    else:
        await message.answer("❗Не удалось получить список товаров. Попробуйте позже.")

@router.callback_query(lambda query: query.data.startswith('product_'))
async def select_product(call: CallbackQuery, bot: Bot):
    product_id = call.data.split('_')[1]
    
    product = api_res.get_product(product_id)
    if product:
        msg = '🛒*Товар:*\n\n' + f"*№{product['id']}* {product['name']} 💸*{product['price']}₽* 📉*{product['discount']}*"
        try:
            await call.message.answer_photo(photo=f"{product['image']}", caption=msg, parse_mode="Markdown")
        except:
            await call.message.answer(msg, parse_mode="Markdown")
    else:
        await call.message.answer(f'❗Не удалось получить товар. Попробуйте позже.')

    await call.answer()

    
@router.callback_query(F.data == 'cancel')
async def catalog(callback:CallbackQuery, state: FSMContext):
    await state.clear() #Очищение состояний
    await callback.message.edit_text('✅Отменено')


