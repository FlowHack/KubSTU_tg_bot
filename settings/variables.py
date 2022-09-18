from os import environ, getcwd
from os.path import join as path_join

from .functions import read_json

API_TOKEN = environ.get('TG_API_TOKEN')
ADMIN_ID = int(environ.get('TG_ADMIN_ID'))
BOT_ID = int(API_TOKEN.split(":")[0])
DB_HOST = environ.get('DB_HOST')
DB_NAME = environ.get('DB_NAME')
POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
DB_PORT = environ.get('DB_PORT')

path = getcwd()
path_settings_dir = path_join(path, 'settings')
path_settings = path_join(path_settings_dir, 'settings.json')

settings_json = read_json(path_settings)

FORMAT_TIME = '%H:%M'
WEEKDAYS = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}
WEEKDAYS_ANSWER = {
    'Понедельник': 'Понедельник',
    'Вторник': 'Вторник',
    'Среда': 'Среду',
    'Четверг': 'Четверг',
    'Пятница': 'Пятницу',
    'Суббота': 'Субботу',
    'Воскресенье': 'Воскресенье'
}
