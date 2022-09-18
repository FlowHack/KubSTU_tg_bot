from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

FRAZES = {
    'parse_couples': 'Спарсить пары',
    'schedule_today': 'На сегодня',
    'back_main': 'Назад на главную',
    'schedule_tomorrow': 'На завтра',
    'schedule_parity': 'На чётную неделю',
    'schedule_none_parity': 'На нечётную неделю',
    'parity_week': 'Чётность недели',
    'new_url': 'Установить новый url'
}


def admin_panel():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(KeyboardButton(FRAZES['parse_couples']))
    keyboard.add(KeyboardButton(FRAZES['new_url']))
    keyboard.add(KeyboardButton(FRAZES['back_main']))

    return keyboard


def main_panel():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(
        KeyboardButton(FRAZES['schedule_today'], color='red'),
        KeyboardButton(FRAZES['schedule_tomorrow'])
    )
    keyboard.add(KeyboardButton(FRAZES['parity_week']))
    keyboard.add(
        KeyboardButton(FRAZES['schedule_none_parity']),
        KeyboardButton(FRAZES['schedule_parity'])
    )

    return keyboard


KEYBOARDS = {
    'admin': admin_panel(),
    'main_panel': main_panel(),
}
