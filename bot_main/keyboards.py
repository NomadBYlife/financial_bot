from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

button = {
    'grp_products': '🍌 Продукты',
    'grp_transport': '🚌 Транспорт',
    'grp_medicine': '💊 Медицина',
    'grp_house_goods': '🪠 Хоз товары',
    'grp_clothes': '👔 Одежда',
    'grp_child_clothes': '🧦 Детская одежда',
    'grp_entertainment': '🎉 Развлечения',
    'grp_communal': '🚻 Коммунальные платежи',
    'grp_car': '🚘 Машина',
    'grp_spouse_1': '👨‍🦲 Супруг 1',
    'grp_spouse_2': '👨‍🦲 Супруг 2',
    'grp_child': '👶 Дети',
    'grp_different': '👐 Разное',
    'grp_donate': '🎁 Подарки, пожертвования',
    'grp_school': '🏫 Школа/дет.сад',
    'grp_travel': '✈️ Поездки',
    'grp_emergency': '🆘 Экстренные расходы',
    'grp_other': '💭 Другое',
}

months = {
    'mnth_1': 'Январь',
    'mnth_2': 'Февраль',
    'mnth_3': 'Март',
    'mnth_4': 'Апрель',
    'mnth_5': 'Май',
    'mnth_6': 'Июнь',
    'mnth_7': 'Июль',
    'mnth_8': 'Август',
    'mnth_9': 'Сентябрь',
    'mnth_10': 'Октябрь',
    'mnth_11': 'Ноябрь',
    'mnth_12': 'Декабрь',
}



def yes_no_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True   )
    kb.add(KeyboardButton('Да'), KeyboardButton('Нет'))
    return kb


def help_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Описание'))
    return kb


def start_using_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('Начать использовать'))
    # KeyboardButton('ЧаВо?'))
    return kb


def income_expense_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb.add(InlineKeyboardButton(text='📈 Доход', callback_data='income'),
            InlineKeyboardButton(text='📉 Расход', callback_data='expense'),
            InlineKeyboardButton(text='⬅️ Назад', callback_data='back_from_ikb'),)
    return ikb


def menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('Ввести данные'), KeyboardButton('Получить данные'))
    return kb


def income_expense_inline_keyboard2() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text=button['grp_products'], callback_data='grp_products'),
            InlineKeyboardButton(text=button['grp_transport'], callback_data='grp_transport'),
            InlineKeyboardButton(text=button['grp_medicine'], callback_data='grp_medicine'),
            InlineKeyboardButton(text=button['grp_house_goods'], callback_data='grp_house_goods'),
            InlineKeyboardButton(text=button['grp_clothes'], callback_data='grp_clothes'),
            InlineKeyboardButton(text=button['grp_child_clothes'], callback_data='grp_child_clothes'),
            InlineKeyboardButton(text=button['grp_entertainment'], callback_data='grp_entertainment'),
            InlineKeyboardButton(text=button['grp_communal'], callback_data='grp_communal'),
            InlineKeyboardButton(text=button['grp_car'], callback_data='grp_car'),
            InlineKeyboardButton(text=button['grp_spouse_1'], callback_data='grp_spouse_1'),
            InlineKeyboardButton(text=button['grp_spouse_2'], callback_data='grp_spouse_2'),
            InlineKeyboardButton(text=button['grp_child'], callback_data='grp_child'),
            InlineKeyboardButton(text=button['grp_different'], callback_data='grp_different'),
            InlineKeyboardButton(text=button['grp_donate'], callback_data='grp_donate'),
            InlineKeyboardButton(text=button['grp_school'], callback_data='grp_school'),
            InlineKeyboardButton(text=button['grp_travel'], callback_data='grp_travel'),
            InlineKeyboardButton(text=button['grp_emergency'], callback_data='grp_emergency'),
            InlineKeyboardButton(text=button['grp_other'], callback_data='grp_other'),
            InlineKeyboardButton(text='😐 cancel', callback_data='cancel'))
    return ikb


def get_data_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    kb.add(KeyboardButton('За все время'), KeyboardButton('За текущий месяц'),KeyboardButton('Выбрать мeсяц'))
    kb.add(KeyboardButton(text='⬅️ Назад'))
    return kb

def months_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text=months['mnth_1'], callback_data='mnth_1'),
            InlineKeyboardButton(text=months['mnth_2'], callback_data='mnth_2'),
            InlineKeyboardButton(text=months['mnth_3'], callback_data='mnth_3'),
            InlineKeyboardButton(text=months['mnth_4'], callback_data='mnth_4'),
            InlineKeyboardButton(text=months['mnth_5'], callback_data='mnth_5'),
            InlineKeyboardButton(text=months['mnth_6'], callback_data='mnth_6'),
            InlineKeyboardButton(text=months['mnth_7'], callback_data='mnth_7'),
            InlineKeyboardButton(text=months['mnth_8'], callback_data='mnth_8'),
            InlineKeyboardButton(text=months['mnth_9'], callback_data='mnth_9'),
            InlineKeyboardButton(text=months['mnth_10'], callback_data='mnth_10'),
            InlineKeyboardButton(text=months['mnth_11'], callback_data='mnth_11'),
            InlineKeyboardButton(text=months['mnth_12'], callback_data='mnth_12'))
    return ikb


