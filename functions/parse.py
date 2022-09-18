from datetime import datetime
from re import compile

import requests
from bs4 import BeautifulSoup
from urllib3 import disable_warnings

from settings import settings_json

from .models import Couple, Week

disable_warnings()


def get_week_with_couples():
    request = requests.get(settings_json.get('url'), verify=False).text
    soup = BeautifulSoup(request, 'lxml')
    return get_couples(soup)


def get_couples(soup):
    parity_false = soup.find(
        'div', attrs={
            'role': 'tabpanel',
            'id': 'collapse_n_1',
            'aria-labelledby': 'heading_n_1'
        }
    ).div
    parity_true = soup.find(
        'div', attrs={
            'role': 'tabpanel',
            'id': 'collapse_n_2',
            'aria-labelledby': 'heading_n_2'
        }
    ).div

    parity_false = parity_false.find_all(
        'div', attrs={
            'class': 'panel panel-info',
            'style': 'margin-bottom: 7px;'
        }
    )
    parity_true = parity_true.find_all(
        'div', attrs={
            'class': 'panel panel-info',
            'style': 'margin-bottom: 7px;'}
    )

    parity_false_days = get_days(parity_false)
    parity_true_days = get_days(parity_true)

    week_parity_false_couples = Week()
    week_parity_true_couples = Week()
    get_day_with_couples(parity_false_days, week_parity_false_couples)
    get_day_with_couples(parity_true_days, week_parity_true_couples, True)

    return {
        'parity': week_parity_true_couples,
        'parity_false': week_parity_false_couples
    }


def get_days(week):
    days = []
    pattern = compile('^heading_n_[0-9]_d_[0-9]$')

    for item in week:
        item_id = item.div.get('id')
        if pattern.match(item_id):
            days.append(item)

    return days


def get_day_with_couples(days, week, parity=False):
    for item in days:
        week.name = item.find(
            'span', attrs={'style': 'font-style: normal; '}
        ).text.strip()
        week.parity = parity
        week.couples = []
        couples = item.find_all(
            'div', attrs={
                'class': 'panel panel-info',
                'style': 'margin-bottom: 7px;'
            }
        )

        for couple in couples:
            coup = Couple()
            couple_name = couple.find(
                'span', attrs={
                    'style': 'font-size: 0.8em; font-weight: bold; '
                }
            ).text.strip().split('/')
            para = couple_name[0].split('(')
            coup.couple_num = int(para[0].split('пара')[0].strip())
            para_time = para[1].split(')')[0].split('-')
            coup.time_from = para_time[0].strip()
            coup.time_to = para_time[1].strip()
            coup.title = couple_name[1].strip()
            coup.type_of_occupation = couple_name[2].strip()

            couple_notes = couple.find(
                'div', attrs={
                    'class': 'panel-collapse collapse',
                    'role': 'tabpanel'
                }
            ).div.find_all('p')
            for couple_note in couple_notes:
                note = couple_note.text.split(':')
                note_name = note[0].strip()
                note_value = note[1].strip()
                if note_name == 'Преподаватель':
                    coup.teacher = note_value if note_value != '' else None
                    continue
                if note_name == 'Аудитория':
                    note_value = note_value.split('-')
                    coup.university_building = note_value[0].strip()
                    coup.lecture_hall = None if  \
                        note_value[1].strip() == '' else note_value[1].strip()
                    continue
                if note_name == 'Период':
                    coup.period = note_value
                    continue
                if note_name == 'Примечание':
                    coup.note = note_value
                    continue
                if note_name == 'В лекционном потоке':
                    coup.lecture_stream = True if note_value == 'Да' else False
                    continue

            week.couples.append(coup)

        if item != days[-1]:
            week.next = Week()
            week = week.next
