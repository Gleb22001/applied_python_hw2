from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message#, ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
#from aiogram.utils import executor
from config import TOKEN
from config import API_URL

class Form(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity_level = State()
    city = State()
    calorie_goal = State()
    additional_parameters = State()
    first_dish=State()
    second_dish=State()
    drink=State()
    cake=State()
    WATER_GOAL=State()
    calories1=State()
    calories2=State()
    calories3=State()
    calories4=State()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Заполнить профиль", callback_data="btn1")],
    ]
)

keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ввести план на день", callback_data="btn2")],
    ]
)



# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Я бот, который будет помогать тебе рассчитывать калории. \n"
    "Чтобы продолжить работу, нажмите 'Заполнить профиль'.", reply_markup=keyboard1)

# Обработчик
@dp.callback_query(lambda cb: cb.data == "btn1")
async def handle_btn1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Убираем уведомление о нажатии кнопки
    await set_profile_command(callback_query.message, state)


@dp.message(Command("set_profile"))
async def set_profile_command(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(Form.weight)

@dp.message(Form.weight)
async def set_weight(message: types.Message, state: FSMContext):
    weight = message.text
    await state.update_data(weight=weight)
    await message.answer("Введите ваш рост (в см):")
    await state.set_state(Form.height)

@dp.message(Form.height)
async def set_height(message: types.Message, state: FSMContext):
    height = message.text
    await state.update_data(height=height)
    await message.answer("Введите ваш возраст:")
    await state.set_state(Form.age)



@dp.message(Form.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    await message.answer("В каком городе вы находитесь (на английском)?")
    await state.set_state(Form.city)
@dp.message(Form.city)
async def set_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    user_data = await state.get_data()
    CITY_NAME =  user_data.get('city', 'Не указано')

    

    response = (
        "<b>Ваши данные:</b>\n"
        f"Вес: {user_data['weight']} кг\n"
        f"Рост: {user_data['height']} см\n"
        f"Возраст: {user_data['age']} лет\n"
        #f"Уровень активности: {user_data['activity_level']} минут в день\n"
        f"Город: {user_data['city']}\n"

    )
    
    await message.answer(response, parse_mode='HTML', reply_markup=keyboard2)
    await state.finish()








@dp.callback_query(lambda cb: cb.data == "btn2")
async def handle_btn2(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Убираем уведомление о нажатии кнопки
    await set_data_command(callback_query.message, state)


@dp.message(Command("set_data"))
async def set_data_command(message: types.Message, state: FSMContext):
    await message.answer("Введите цель калорий (по умолчанию будет рассчитана, оставьте пустым для автоподсчета):")
    await state.set_state(Form.calorie_goal)



@dp.message(Form.calorie_goal)
async def set_calorie_goal(message: types.Message, state: FSMContext):
    calorie_goal = message.text
    await state.update_data(calorie_goal=calorie_goal)
    await message.answer("Укажите минуты активности:")
    await state.set_state(Form.activity_level)



@dp.message(Form.activity_level)
async def set_activity_level(message: types.Message, state: FSMContext):
    activity_level = message.text
    await state.update_data(activity_level=activity_level)
    await message.answer("Первое блюдо (на английском)")
    await state.set_state(Form.first_dish)


@dp.message(Form.first_dish)
async def set_first_dish(message: types.Message, state: FSMContext):
    global first_dish
    first_dish = message.text
    await state.update_data(first_dish=first_dish)
    await message.answer("Второе блюдо (на английском)")
    await state.set_state(Form.second_dish)



@dp.message(Form.second_dish)
async def set_second_dish(message: types.Message, state: FSMContext):
    global second_dish
    second_dish = message.text
    await state.update_data(second_dish=second_dish)
    await message.answer("Напиток (на английском)")
    await state.set_state(Form.drink)


@dp.message(Form.drink)
async def set_second_dish(message: types.Message, state: FSMContext):
    global drink
    drink = message.text
    await state.update_data(drink=drink)
    await message.answer("Десерт (на английском)")
    await state.set_state(Form.cake)

@dp.message(Form.cake)
async def set_cake(message: types.Message, state: FSMContext):
    global cake
    cake = message.text
    await state.update_data(cake=cake)

    user_data = await state.get_data()

    import requests

    def get_current_temperature(city_name, api_key):
        # URL для получения текущей погоды
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            return temperature
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None


    API_KEY = "57b4e3fcf695f44922abddd25d5e79e8"
    CITY_NAME = user_data.get('city', 'Не указано')

    temperature = get_current_temperature(CITY_NAME, API_KEY)

    if temperature>25:
        water_goal=float(user_data['weight'])*30+500*float(user_data['activity_level'])/30+500+1000
    else:
        water_goal=float(user_data['weight'])*30+500*float(user_data['activity_level'])/30+500

    global WATER_GOAL
    WATER_GOAL = water_goal
    await state.set_state(Form.WATER_GOAL)
    await state.update_data(WATER_GOAL=WATER_GOAL)
    user_data = await state.get_data()

    def get_product_calories(product_name):
        # URL для поиска продукта по имени
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&json=1"
    
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            if data['products']:  # Проверяем, есть ли результаты
                product = data['products'][0]  # Берем первый продукт из списка
                calories = product.get('nutriments', {}).get('energy-kcal', None)  # Получаем калории
            
                if calories is not None:
                    return calories
                else:
                    print("Калорийность не найдена.")
                    return None
            else:
                print("Продукты не найдены.")
                return None
        else:
            print(f"Ошибка: {response.status_code}")
            return None

    global calorie_goal
    global calories1
    global calories2
    global calories3
    global calories4


    calorie_goal=user_data.get('calorie_goal', '')
    if not calorie_goal:
        calorie_goal=10*float(user_data.get('weight', 'Не указано'))+6.25*float(user_data.get('height', 'Не указано'))-5*float(user_data.get('age', 'Не указано'))+400*float(user_data.get('activity_level', 'Не указано'))/60 #+400 ккал за каждый час активности

    
    # Пример использования
    
    calories1 = get_product_calories(user_data.get('first_dish', 'Не указано'))
    calories2 = get_product_calories(user_data.get('second_dish', 'Не указано'))
    calories3 = get_product_calories(user_data.get('drink', 'Не указано'))
    calories4 = get_product_calories(user_data.get('cake', 'Не указано'))

    await state.set_state(Form.calories1)
    await state.update_data(calories1=calories1)

    await state.set_state(Form.calories2)
    await state.update_data(calories2=calories2)

    await state.set_state(Form.calories3)
    await state.update_data(calories3=calories3)

    await state.set_state(Form.calories4)
    await state.update_data(calories4=calories4)
    
    #Считаем, что все каллории распределяем так 30% на первое блюдо, 40% на второе блюдо, 25% на десерт и 5% на напиток
    weight_1=0.3*float(calorie_goal)/float(calories1)
    weight_2=0.4*float(calorie_goal)/float(calories2)
    weight_3=0.05*float(calorie_goal)/float(calories3)
    weight_4=0.25*float(calorie_goal)/float(calories4)



    response = (
        "<b>Ваши данные:</b>\n"
        f"Уровень активности:{user_data['activity_level']} минут в день\n"
        f"Цель калорий: {user_data['calorie_goal'] if user_data['calorie_goal'] else 'будет рассчитана'}\n"
        f"Первое блюдо: {user_data['first_dish']}\n"
        f"Второе блюдо: {user_data['second_dish']}\n"
        f"Напиток: {user_data['drink']}\n"
        f"Десерт: {user_data['cake']}\n"
        f"Вам необходимо за день выпить {int(water_goal)} мл воды\n"
        f"Вам необходимо за день съесть {int(weight_1)} г первого блюда\n"
        f"Вам необходимо за день съесть {int(weight_2)} г второго блюда\n"
        f"Вам необходимо за день съесть {int(weight_3)} г десерта\n"
        f"Вам необходимо за день выпить {int(weight_4)} г напитка\n\n"
        f"<b>Чтобы следить за тем, сколько осталось выпить воды:</b>\n"
        f"Введите комманду /log_water, а через пробел число миллилитров випитого.\n"
        "<b>Чтобы оценить, сколько каллорий осталось:</b>\n"
        f"Введите команду /log_cal через пробел продукт на английском и ещё через пробел количество грамм."
    )

    
    
    await message.answer(response, parse_mode='HTML')
    await state.finish()

# Пользовательские данные: может быть реализовано более гибко
user_water_data = {}

# Норма воды (в мл)


@dp.message(Command("log_water"))
async def log_water_command(message: types.Message):
    # Получаем текст команды
    command_text = message.text.strip()

    # Разделим текст по пробелам и извлечем аргументы
    components = command_text.split()

    # Убедимся, что мы имеем аргумент
    if len(components) != 2 or not components[1].isdigit():
        await message.answer("Пожалуйста, укажите количество воды, например: /log_water 300")
        return

    volume = int(components[1])  # Получаем количество воды из аргументов
    user_id = message.from_user.id

    # Сохраняем данные о пользователе (если нет, создаем новую запись)
    if user_id not in user_water_data:
        user_water_data[user_id] = 0

    # Обновляем количество выпитой воды
    user_water_data[user_id] += volume

    # Рассчитываем, сколько осталось до нормы
    remaining = WATER_GOAL- user_water_data[user_id]

    if remaining > 0:
        await message.answer(f"Вы выпили {volume} мл воды. Осталось {remaining} мл до нормы.")
    else:
        await message.answer(f"Вы выпили мл воды. Норма достигнута!")




# Пользовательские данные: может быть реализовано более гибко
user_cal_data = {}



@dp.message(Command("log_cal"))
async def log_cal_command(message: types.Message):
    # Получаем текст команды
    command_text = message.text.strip()

    # Разделим текст по пробелам и извлечем аргументы
    components = command_text.split()
    
    # Убедимся, что мы имеем аргумент
    if len(components) != 3 or not components[2].isdigit():
        await message.answer("Пожалуйста, укажите количество воды, например: /log_cal 300")
        return

    volume = int(components[2])  # Получаем количество воды из аргументов
    user_id = message.from_user.id

    # Сохраняем данные о пользователе (если нет, создаем новую запись)
    if user_id not in user_cal_data:
        user_cal_data[user_id] = 0

    # Обновляем количество выпитой воды
    if components[2]==first_dish:
        user_cal_data[user_id] += volume*float(calories1)
    elif components[2]==second_dish:
        user_cal_data[user_id] += volume*float(calories2)
    elif components[2]==drink:
        user_cal_data[user_id] += volume*float(calories3)
    else:
        user_cal_data[user_id] += volume*float(calories4)
        


    # Рассчитываем, сколько осталось до нормы
    
        
    remaining = float(calorie_goal) - user_cal_data[user_id]

    if remaining > 0:
        await message.answer(f"Вы съели {volume} г {components[2]}. Осталось {remaining} ккал до нормы.")
    else:
        await message.answer(f"Вы съели все калории. Норма достигнута!")







async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main()) 



