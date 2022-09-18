from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types

from base_data import Couple, DayWeek, session
from functions import (FRAZES, KEYBOARDS, get_parity_week, get_schedule,
                       get_week_with_couples, write_all_couples_in_bd,
                       get_schedule_week, get_schedule_on_day_answer)
from settings import (ADMIN_ID, API_TOKEN, BOT_ID, path_settings,
                      settings_json, write_json)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot_api = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
REQUESTS = settings_json.get('requests')
dp = Dispatcher(bot_api)
global requests_count
requests_count = 0


async def null_requests():
    global requests_count
    requests_count = 0
    await bot_api.send_message(
        ADMIN_ID, f'Сбросил количество запросов до: {requests_count}'
    )


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    global requests_count
    requests_count += 1
    new_member = message.new_chat_members[0]

    if new_member.id == BOT_ID:
        await message.answer(
            REQUESTS['start'], reply_markup=KEYBOARDS['main_panel']
        )
        return

    await message.answer(
        'Хай, пидрила. Если нужно расписание, обращайся',
        reply_markup=KEYBOARDS['main_panel']
    )


@dp.message_handler(commands='start')
async def start(message: types.Message):
    global requests_count
    requests_count += 1
    await message.answer(
        REQUESTS['start'], reply_markup=KEYBOARDS['main_panel']
    )


async def schedule_on_week(message, parity):
    global requests_count
    requests_count += 1
    schedule = await get_schedule_week(session, parity)
    parity = 'чётную' if parity is True else 'нечётную'

    answer = f'<code>Расписание на {parity} неделю.</code>\n\n\n'
    await message.answer(answer, reply_markup=KEYBOARDS['main_panel'])

    for day in schedule:
        answer = await get_schedule_on_day_answer(
            day.name, day.parity,
            day.couples, REQUESTS
        )
        await message.answer(answer, reply_markup=KEYBOARDS['main_panel'])


@dp.message_handler(text=FRAZES['schedule_parity'])
async def schedule_week_parity(message: types.Message):
    await schedule_on_week(message, True)


@dp.message_handler(text=FRAZES['schedule_none_parity'])
async def schedule_week_none_parity(message: types.Message):
    await schedule_on_week(message, False)


async def schedule_on_day(message: types.Message, date):
    global requests_count
    requests_count += 1
    schedule = await get_schedule(session, date)
    if schedule is None:
        await message.answer(
            REQUESTS['schedule_none'], reply_markup=KEYBOARDS['main_panel']
        )
        return

    answer = await get_schedule_on_day_answer(
        schedule['weekday'], schedule['parity'],
        schedule['couples'], REQUESTS
    )

    await message.answer(answer, reply_markup=KEYBOARDS['main_panel'])


@dp.message_handler(text=FRAZES['schedule_today'])
async def schedule_today(message: types.Message):
    await schedule_on_day(message, datetime.now())


@dp.message_handler(text=FRAZES['schedule_tomorrow'])
async def schedule_tomorrow(message: types.Message):
    await schedule_on_day(message, datetime.now() + timedelta(days=1))


@dp.message_handler(text=FRAZES['parity_week'])
async def parity_week(message: types.Message):
    global requests_count
    requests_count += 1
    date = datetime.today()
    parity = await get_parity_week(date.day, date.month, date.year)
    parity = 'Чётная' if parity is True else 'Нечётная'
    await message.answer(parity, reply_markup=KEYBOARDS['main_panel'])


@dp.message_handler(commands='admin')
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            REQUESTS['admin'], reply_markup=KEYBOARDS['admin']
        )


@dp.message_handler(text=FRAZES['parse_couples'])
async def parse_couples(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if len(session.query(Couple).all()) > 0:
            session.query(Couple).filter(Couple.title is not None).delete()
        if len(session.query(DayWeek).all()) > 0:
            session.query(DayWeek).filter(DayWeek.parity is not None).delete()

        weeks = get_week_with_couples()

        parity = weeks['parity'].get_all_days()
        parity_false = weeks['parity_false'].get_all_days()
        days = list(parity + parity_false)

        write_all_couples_in_bd(session, days)

        await message.answer('Готово', reply_markup=KEYBOARDS['admin'])


@dp.message_handler(text=FRAZES['new_url'])
async def new_url(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            'Введите url в формате\n\n/admin_write_new_url\nURL',
            reply_markup=KEYBOARDS['admin']
        )


@dp.message_handler(commands='admin_write_new_url')
async def admin_write_new_url(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            url = message.text.split('\n')[1].strip()
        except IndexError:
            await message.answer('А где урл то?')
            return

        settings_json['url'] = url
        write_json(path_settings, settings_json)

        await message.answer(f'Готов\nURL={url}')


@dp.message_handler(text=FRAZES['get_requests'])
async def count_requests(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f'Количество запросов: {requests_count}')


@dp.message_handler(text=FRAZES['back_main'])
async def back_main(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            'Главная страница', reply_markup=KEYBOARDS['main_panel']
        )


if __name__ == '__main__':
    scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})
    scheduler.add_job(null_requests, 'cron', hour=0, minute=0)
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
