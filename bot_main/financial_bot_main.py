from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, BoundFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

import config
from db_utils import db_start, create_user, edit_expenses, get_general_data, get_data_current_month, \
    get_data_choosen_month, get_note_for_del, del_note_from_db
from keyboards import yes_no_keyboard, help_keyboard, start_using_keyboard, income_expense_inline_keyboard, \
    income_expense_inline_keyboard2, menu_keyboard, get_data_keyboard, button, months_inline_keyboard, \
    year_inline_keyboard

storage = MemoryStorage()
bot = Bot(config.TOKEN_API)
dp = Dispatcher(bot, storage=storage)

HELP = """
/commands - list of commands
/descriptions - descriptions about me
"""
DESCRIPTION = """
Я бот, созданный как помощник для контроля расходов.
Надеюсь, что я помогу Вам стать более осведомленными о Ваших расходах.
Я буду модернизироваться со временем, дальше больше!
"""
CREATOR = 448040700


class ReplyFilterBot(BoundFilter):
    async def check(self, msg: types.Message):
        try:
            float(msg.text)
            return True
        except Exception:
            return False


class ProductsStatesGroup(StatesGroup):
    amount = State()
    yes_no = State()
    description = State()


class DateStatesGroup(StatesGroup):
    year = State()
    month = State()


class ReviewStatesGroup(StatesGroup):
    text = State()


class DeleteStatesGroup(StatesGroup):
    group = State()
    amount = State()
    year = State()
    month = State()
    day = State()
    yes_no = State()


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit):
        super().__init__()
        self.last_time = {}
        self.limit = limit

    async def on_pre_process_message(self, message, data):
        if message.from_user.id not in self.last_time:
            self.last_time[message.from_user.id] = {}
            self.last_time[message.from_user.id]['date'] = message.date
            self.last_time[message.from_user.id]['text'] = message.text
            return
        if int((message.date - self.last_time[message.from_user.id]['date']).total_seconds()) < self.limit and \
                self.last_time[message.from_user.id]['text'] == message.text:
            await bot.send_message(chat_id=message.from_user.id, text='Слишком много запросов',
                                   reply_markup=start_using_keyboard())
            raise CancelHandler()
        self.last_time[message.from_user.id]['date'] = message.date
        self.last_time[message.from_user.id]['text'] = message.text


async def on_startup(_):
    await db_start()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await create_user(user_id=message.from_user.id, name=message.from_user.first_name,
                      nick_name=message.from_user.username)
    await bot.send_message(chat_id=message.from_user.id, text=DESCRIPTION,
                           reply_markup=start_using_keyboard())
    await message.delete()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'cancel', state='*')
async def cancel_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    if state is None:
        return
    await callback.message.answer('Отменено', reply_markup=menu_keyboard())
    await state.finish()


@dp.message_handler(Text(equals='Главное меню'))
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Главное меню:', reply_markup=start_using_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='Книга жалоб и предложений'))
async def review_msg_handler(message: types.Message):
    await message.reply("Оставьте свой отзыв:")
    await ReviewStatesGroup.text.set()


@dp.message_handler(state=ReviewStatesGroup.text)
async def review_msg_handler(message: types.Message, state: FSMContext):
    review = message.text
    if message.from_user.username:
        sender = message.from_user.username
    else:
        sender = message.from_user.id
    reply = f"Оставили отзыв в боте:\n{review}\nот @{sender}"
    await bot.send_message(chat_id=CREATOR, text=reply)
    await state.finish()
    await message.reply('Спасибо! Отзыв отправлен создателю бота, ему очень важно знать ваше мнение!',
                        reply_markup=start_using_keyboard())


# @dp.message_handler(Text(equals='Описание'))
# async def cmd_description(message: types.Message):
#     await bot.send_message(chat_id=message.from_user.id, text=DESCRIPTION, reply_markup=start_using_keyboard())
#     await message.delete()


@dp.message_handler(Text(equals='Начать использовать'), state='*')
async def star_using_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Меню:',
                           reply_markup=menu_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='Ввести данные'))
async def star_using_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Что вы хотите ввести?',
                           reply_markup=income_expense_inline_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='Удалить'))
async def delete_cb_handler(message: types.Message, ):
    await DeleteStatesGroup.group.set()
    await bot.send_message(chat_id=message.from_user.id, text='Удалить в какой группе?',
                           reply_markup=income_expense_inline_keyboard2())


@dp.callback_query_handler(state=DeleteStatesGroup.group)
async def delete_item_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = callback.data
    await DeleteStatesGroup.next()
    await callback.message.answer('введите сумму:')


@dp.message_handler(ReplyFilterBot(), state=DeleteStatesGroup.amount)
async def delete_amount_msg_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer('Выберите год:', reply_markup=year_inline_keyboard())
    await DeleteStatesGroup.next()


@dp.callback_query_handler(state=DeleteStatesGroup.year)
async def delete_year_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = callback.data[5:]
    await callback.message.answer('Выберите месяц:', reply_markup=months_inline_keyboard())
    await DeleteStatesGroup.next()


@dp.callback_query_handler(state=DeleteStatesGroup.month)
async def delete_month_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if len(callback.data[5:]) == 1:
            data['month'] = f"0{callback.data[5:]}"
        else:
            data['month'] = callback.data[5:]
    await callback.message.answer('Введите день:')
    await DeleteStatesGroup.next()


@dp.message_handler(ReplyFilterBot(), state=DeleteStatesGroup.day)
async def delete_day_msg_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text) == 1:
            data['day'] = f"0{message.text}"
        else:
            data['day'] = message.text
        data['date'] = f"{data['year']}-{data['month']}-{data['day']}"
    db_data = await get_note_for_del(user_id=message.from_user.id, data=data)
    reply = ""
    if len(db_data) == 0:
        reply = 'Данных не найдено. Проверьте правильность введенных данных'
        await message.answer(text=reply, reply_markup=income_expense_inline_keyboard())
        await state.finish()
    else:
        for i in db_data:
            reply += f"Вы хотите удалить:\n{button[i[0]]}: суммa {i[1]}, дата {i[2][8:]}-{i[2][5:7]}-{i[2][0:4]} {i[3]}\n"
    # reply += f"Вы хотите удалить: {db_data['amount_sum']}"
    await message.answer(text=reply, reply_markup=yes_no_keyboard())
    await DeleteStatesGroup.next()


@dp.message_handler(Text(equals='Нет'), state=DeleteStatesGroup.yes_no)
async def delete_no_msg_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено', reply_markup=income_expense_inline_keyboard())


@dp.message_handler(Text(equals='Да'), state=DeleteStatesGroup.yes_no)
async def delete_yes_msg_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await del_note_from_db(user_id=message.from_user.id, data=data)
    await state.finish()
    await message.reply('Удалено', reply_markup=menu_keyboard())


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_from_ikb')
async def back_f_ikb_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Меню:', reply_markup=menu_keyboard())
    await state.finish()


@dp.callback_query_handler(lambda callback: callback.data == 'expense')
async def income_cb_handler(callback: types.CallbackQuery):
    await callback.message.answer('Группы расходы', reply_markup=income_expense_inline_keyboard2())
    await callback.message.delete()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('grp'))
async def item_cb_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = callback_query.data
    await callback_query.message.answer('Введите сумму:')
    await ProductsStatesGroup.amount.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('year'), state=DateStatesGroup.year)
async def date_cb_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = callback_query.data[7:]
    await callback_query.message.answer(text='Выберите период', parse_mode='HTML',
                                        reply_markup=months_inline_keyboard())
    await DateStatesGroup.next()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('mnth_'), state=DateStatesGroup.month)
async def months_cb_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = callback_query.data[5:]
    db_data = await get_data_choosen_month(callback_query.from_user.id, data)
    reply = ''
    await state.finish()
    if len(db_data['main']) == 0:
        reply = 'Данных пока нету'
    else:
        for i in db_data['main']:
            reply += f"{button[i[0]]}: суммa {i[1]}, дата {i[2][8:]}-{i[2][5:7]}-{i[2][0:4]} {i[3]}\n"
        reply += f"Общая сумма расходов: {db_data['amount_sum']}"
    await bot.send_message(chat_id=callback_query.from_user.id, text=reply, parse_mode='HTML',
                           reply_markup=menu_keyboard())


@dp.message_handler(ReplyFilterBot(), state=ProductsStatesGroup.amount)
async def amount_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.reply('Хотите оставить комментарий?', reply_markup=yes_no_keyboard())
    await ProductsStatesGroup.next()


@dp.message_handler(Text(equals='⬅️ Назад'))
async def back_f_kb_handler(message: types.Message):
    await message.answer('Меню:', reply_markup=menu_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='Да'), state=ProductsStatesGroup.yes_no)
async def data_yes_handler(message: types.Message):
    await message.reply('Коментарий:')
    await ProductsStatesGroup.next()


@dp.message_handler(state=ProductsStatesGroup.description)
async def data_description_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['description'] = message.text
    await edit_expenses(state)
    await message.reply('Расход записан', reply_markup=income_expense_inline_keyboard())
    await state.finish()


@dp.message_handler(Text(equals='Нет'), state=ProductsStatesGroup.yes_no)
async def data_no_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['description'] = ''
    await edit_expenses(state)
    await message.reply('Расход записан', reply_markup=income_expense_inline_keyboard())
    await state.finish()


@dp.message_handler(Text(equals='Посмотреть итоги'))
async def get_msg_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Выберите данные которые хотите получить:',
                           reply_markup=get_data_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='За все время'))
async def get_general_month_data_msg_handler(message: types.Message):
    data = await get_general_data(message.from_user.id)
    reply = ''
    if len(data['main']) == 0:
        reply = 'Данных пока нету'
    else:
        for i in data['main']:
            reply += f"{button[i[0]]}: суммa {i[1]}, дата {i[2][8:]}-{i[2][5:7]}-{i[2][0:4]} {i[3]}\n"
        reply += f"Общая сумма расходов: {data['amount_sum']}"
    await bot.send_message(chat_id=message.from_user.id, text=reply, parse_mode='HTML',
                           reply_markup=get_data_keyboard())


@dp.message_handler(Text(equals='За текущий месяц'))
async def get_current_month_data_msg_handler(message: types.Message):
    data = await get_data_current_month(message.from_user.id)
    reply = ''
    if len(data['main']) == 0:
        reply = 'Данных пока нету'
    else:
        for i in data['main']:
            reply += f"{button[i[0]]}: суммa {i[1]}, дата {i[2][8:]}-{i[2][5:7]}-{i[2][0:4]} {i[3]}\n"
        reply += f"Общая сумма расходов: {data['amount_sum']}"
    await bot.send_message(chat_id=message.from_user.id, text=reply, parse_mode='HTML',
                           reply_markup=get_data_keyboard())


@dp.message_handler(Text(equals='Выбрать период'))
async def choose_period_msg_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Выберите год', parse_mode='HTML',
                           reply_markup=year_inline_keyboard())
    await DateStatesGroup.year.set()
    await message.delete()


if __name__ == '__main__':
    dp.middleware.setup(AntiFloodMiddleware(30))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
