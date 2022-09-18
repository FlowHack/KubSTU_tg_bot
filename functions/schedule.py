import calendar
from datetime import datetime

from base_data import DayWeek
from settings import WEEKDAYS, WEEKDAYS_ANSWER


async def get_parity_week(day: int, month: int, year: int):
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    day = None

    for index, week in enumerate(days_by_week):
        if str_day in week:
            day = index + 1
            break

    return False if day % 2 == 1 else True


async def get_schedule(session, date=datetime.now()):
    parity = await get_parity_week(date.day, date.month, date.year)
    weekday = WEEKDAYS[date.weekday()]

    result = session.query(
        DayWeek
    ).filter(
        DayWeek.name == weekday
    ).filter(
        DayWeek.parity == parity
    ).first()
    if result is None:
        return None

    return {
        'couples': result.couples,
        'weekday': weekday,
        'parity': parity
    }


async def get_schedule_week(session, parity):
    return session.query(DayWeek).filter(DayWeek.parity == parity).all()


async def get_schedule_on_day_answer(weekday, parity, schedule, REQUESTS):
    answer = REQUESTS['schedule_day'].format(
        weekday=WEEKDAYS_ANSWER[weekday],
        parity='Чётная' if parity is True else 'Нечётная',
    )
    for couple in schedule:
        lecture_hall = couple.lecture_hall
        answer += REQUESTS['schedule_day_couple'].format(
            couple_num=couple.couple_num, time_from=couple.time_from,
            time_to=couple.time_to, title=couple.title,
            university_building=couple.university_building,
            lecture_hall=lecture_hall if lecture_hall is not None else '',
            teacher=couple.teacher if couple.teacher is not None else '-',
            period=couple.period, type_of_occupation=couple.type_of_occupation,
            lecture_stream='Да' if couple.lecture_stream is True else 'Нет'
        )

    return answer


def requests_count(count, null=False, plus=True):
    if plus:
        return count + 1
    if null:
        return 0
