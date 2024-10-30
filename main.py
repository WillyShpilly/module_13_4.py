from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


api = "Enter your key from botfather"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = "Calories")
async def set_age(message):
    await message.answer(f'Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=float(message.text))
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=float(message.text))
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=float(message.text))
    data = await state.get_data()
    womenresult = (10*data['third']) + (6.25*data['second']) - (5*data['first']) - 161
    await message.answer( f'результат подсчета необходимого количества :{womenresult} каллорий')
    await state.finish()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)