import argparse
import json
import logging
import random
import sys
from http import HTTPStatus
from logging import DEBUG, ERROR, INFO
from typing import Tuple
from urllib.parse import ParseResult, urlparse

import requests

from webcolors import CSS3_HEX_TO_NAMES

SCHEMA = ['http', 'https']
ADDRESS = '127.0.0.1'
PORT = '8000'
RESOURCE = 'cats/'
NUMBER_OF_CATS = 10
LESSON_NUMBER = (0, 1, 2, 3)
VERBOSITY = {0: ERROR,
             1: INFO,
             3: DEBUG}

INIT_DATA = {
    'name': ['Аврора', 'Агат', 'Агата', 'Адам', 'Адель', 'Айвори', 'Айк',
             'Айова', 'Айс', 'Айсик', 'Алекса', 'Алиса', 'Алмаз', 'Альбус',
             'Альф', 'Аляска', 'Амели', 'Амон', 'Амор', 'Амур', 'Анора',
             'Анун', 'Арни', 'Арнольд', 'Артур', 'Арчи', 'Ассоль', 'Астер',
             'Астра', 'Атос', 'Аурика', 'Багира', 'Базилио', 'Байрон', 'Бакс',
             'Балу', 'Барби', 'Барни', 'Барон', 'Барс', 'Барса', 'Барсик',
             'Баунти', 'Баффи', 'Бегемот', 'Бейонсе', 'Белка', 'Белла',
             'Берри', 'Бетти', 'Билли', 'Блейд', 'Бонни', 'Борис', 'Босс',
             'Бостон', 'Бренди', 'Бритни', 'Бруно', 'Бука', 'Бумер', 'Бун',
             'Бунси', 'Буян', 'Бьянка', 'Бэмби', 'Бэт', 'Вайт', 'Валли',
             'Ванда', 'Ваниль', 'Ватсон', 'Вегас', 'Вельзевул', 'Веснушка',
             'Виви', 'Виски', 'Ворсинка', 'Гамлет', 'Ганди', 'Гарфилд',
             'Гельд', 'Геральт', 'Герда', 'Геродот', 'Гита', 'Глори', 'Глюк',
             'Грей', 'Грейс', 'Грим', 'Гричо', 'Гроза', 'Гудвин', 'Гудини',
             'Гуччи', 'Дайна', 'Дакота', 'Даллас', 'Дана', 'Дао', 'Дарси',
             'Дарт Вейдер', 'Дая', 'Джеки', 'Джексон', 'Джерри', 'Джерси',
             'Джеси', 'Джина', 'Джокер', 'Джонни', 'Дилан', 'Диско', 'Долли',
             'Дольче', 'Донна', 'Дори', 'Дуглас', 'Дымка', 'Дымок', 'Дюна',
             'Ева', 'Жужа', 'Забияка', 'Зена', 'Зефир', 'Зея', 'Злата',
             'Зорро', 'Иззи', 'Изольда', 'Изюм', 'Инки', 'Ирис', 'Ириска',
             'Исида', 'Каир', 'Кай', 'Кайли', 'Ками', 'Камун', 'Канзас',
             'Капоне', 'Карри', 'Каспер', 'Кей', 'Кесси', 'Кетти', 'Кики',
             'Кира', 'Китти', 'Кия', 'Клайд', 'Клахан', 'Клео', 'Клеопатра',
             'Клепа', 'Кнопка', 'Коко', 'Коржик', 'Кортни', 'Космос', 'Кулап',
             'Купер', 'Курт', 'Куся', 'Кэнти', 'Кэсси', 'Лайма', 'Лайт',
             'Лаки', 'Лакки', 'Лакрица', 'Лана', 'Лапочка', 'Лара', 'Ларри',
             'Ларси', 'Ласка', 'Леди', 'Лейла', 'Лек', 'Лекс', 'Лексус',
             'Ленивец', 'Леннон', 'Лео', 'Леон', 'Леопольд', 'Лепа', 'Лиззи',
             'Линкольн', 'Локи', 'Лорд', 'Луксор', 'Лулу', 'Луна', 'Лунтик',
             'Лучано', 'Лэйла', 'Люк', 'Люси', 'Лючия', 'Ляля', 'Мадонна',
             'Май', 'Майами', 'Макс', 'Малай', 'Малыш', 'Мальвина', 'Мани',
             'Мао', 'Марго', 'Маркиз', 'Маркиза', 'Маркус', 'Марли', 'Марс',
             'Марсель', 'Марси', 'Масик', 'Масяня', 'Матильда', 'Мачо',
             'Микки', 'Милана', 'Милка', 'Мими', 'Мисси', 'Мисти', 'Мия',
             'Молли', 'Монтана', 'Морфей', 'Мотя', 'Муза', 'Мускат', 'Мушка',
             'Мышка', 'Най', 'Найт', 'Нала', 'Нана', 'Нану', 'Наоми', 'Нари',
             'Нарцисс', 'Невада', 'Нейт', 'Нелли', 'Немо', 'Неро', 'Ника',
             'Нил', 'Нима', 'Ниран', 'Ной', 'Нокс', 'Нола', 'Норд', 'Норман',
             'Ночка', 'Нуар', 'Нэйла', 'Нэнси', 'Нюша', 'Огайо', 'Оззи', 'Ола',
             'Олаф', 'Олли', 'Оникс', 'Онурис', 'Осирис', 'Оскар', 'Остин',
             'Ося', 'Панда', 'Пантера', 'Пегги', 'Пеппер', 'Персик', 'Петти',
             'Пикси', 'Пинки', 'Пират', 'Плут', 'Плюша', 'Пресли', 'Принц',
             'Пума', 'Пунш', 'Пушистик', 'Пушок', 'Ради', 'Ракета', 'Рамзес',
             'Расти', 'Рианна', 'Рик', 'Рикко', 'Ринго', 'Ричард', 'Ричи',
             'Ричмонд', 'Риччи', 'Роза', 'Роки', 'Рокки', 'Рокси', 'Россо',
             'Руби', 'Руфус', 'Рысь', 'Рэйчел', 'Рэми', 'Рюрик', 'Саба',
             'Саймон', 'Сальса', 'Самон', 'Самсон', 'Сандер', 'Санни', 'Санта',
             'Сахар', 'Свити', 'Сенди', 'Серена', 'Серж', 'Серсея', 'Сима',
             'Симба', 'Скраппи', 'Смоки', 'Снежок', 'Сомбун', 'Сомчай', 'Соня',
             'Спорти', 'Спотти', 'Стелла', 'Стефан', 'Страйк', 'Стрелка',
             'Сэйлем', 'Сэни', 'Сюзи', 'Тайгер', 'Тайлер', 'Тара', 'Тарзан',
             'Тедди', 'Техас', 'Тигра', 'Тина', 'Тиша', 'Тоби', 'Том', 'Томас',
             'Тори', 'Тэрри', 'Уголек', 'Уинстон', 'Уитни', 'Файлин', 'Фанни',
             'Фараон', 'Фауст', 'Феликс', 'Фелиция', 'Феникс', 'Фея', 'Фиона',
             'Фисташка', 'Флейк', 'Флинн', 'Фокси', 'Фортуна', 'Фредди',
             'Фрости', 'Фунтик', 'Хани', 'Ханна', 'Хапу', 'Холмс', 'Царапка',
             'Цунами', 'Чеддер', 'Честер', 'Чикаго', 'Шай', 'Шанель', 'Шани',
             'Шанти', 'Шарлотт', 'Шеда', 'Шер', 'Шерлок', 'Шерри', 'Шиншилла',
             'Шкода', 'Шнапс', 'Шоки', 'Шрея', 'Шу', 'Шума', 'Шура', 'Элтон',
             'Эмбер', 'Эми', 'Эрби', 'Эш', 'Юджин', 'Юки', 'Юса', 'Юта'],

    'color': (('Gray', 'Серый'),
              ('Black', 'Чёрный'),
              ('White', 'Белый'),
              ('Ginger', 'Рыжий'),
              ('Mixed', 'Смешанный')),

    'birth_year': (2010, 2023),
    'owner': 1,
    'achievements': ['Зассыка 100%', 'Уронил вазу', 'Поймал мышку',
                     'Напал из-за угла', 'Рылся в мусорке',
                     'Гонялся за птицами', 'Воровал колбасу',
                     'Рыбачил в аквариуме', 'Тыгыдакал в жесть утра',
                     'Уронил елку'],
}

parser = argparse.ArgumentParser(
    prog='python3 gensk.py',
    description='Script for generate and deploy kitties data via API'
)

parser.add_argument('-v', '--verbosity', nargs='?', type=int,
                    choices=VERBOSITY,
                    const=VERBOSITY[1],
                    default=VERBOSITY[1],
                    help='Set verbosity level for logging'
                    )

group_url_parts = parser.add_argument_group('URL configuration')
group_url_parts.add_argument('-s', '--schema', choices=SCHEMA,
                             default=SCHEMA[0],
                             help=('Select schema to use.')
                             )
group_url_parts.add_argument('-a', '--address', nargs='?', default=ADDRESS,
                             help='Specify address.')
group_url_parts.add_argument('-p', '--port', nargs='?', default=PORT,
                             help='Specify port number.')
group_url_parts.add_argument('-r', '--resource', nargs='?', default=RESOURCE,
                             help='Specify API resource of endpoint.')
group_url_parts.add_argument('-u', '--url', nargs='?', type=str,
                             const='', default='',
                             help='Fully specified URL to API.')

group_generating = parser.add_argument_group('Generating kitties')
group_generating.add_argument('-g', '--generate', action='store_true',
                              help='Generate kitties and print in stdout.')
group_generating.add_argument('-l', '--lesson-number', nargs='?', type=int,
                              choices=LESSON_NUMBER,
                              const=LESSON_NUMBER[0],
                              default=LESSON_NUMBER[0],
                              help=('0: `Урок 5/15` 1: `Урок 9/15`'
                                    '2: `Урок 10/15` 3: `Урок 12/15`.')
                              )
group_generating.add_argument('-n', '--number-of-cats',
                              nargs='?', type=int,
                              const=NUMBER_OF_CATS,
                              default=NUMBER_OF_CATS,
                              help=('Number of kitties to generate.')
                              )

group_actions = parser.add_argument_group(
    'API actions').add_mutually_exclusive_group(required=False)
group_actions.add_argument('-c', '--check-server', action='store_true',
                           help='Basic check for endpoint availability.')
group_actions.add_argument('-d', '--deploy', action='store_true',
                           help='Deploy generated data via `POST` method.')
group_actions.add_argument('-e', '--cleanup-db', action='store_true',
                           help='Delete all entries in database via `DELETE` '
                                 'method.'
                           )

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

logging.basicConfig(
    level=args.verbosity,
    format=('%(asctime)s - [%(levelname)s] - %(name)s - '
            '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
)


def url_validator(url: str) -> Tuple[bool, ParseResult, str]:
    """Simple URL validator."""
    try:
        if not url.endswith('/'):
            url += '/'
        result = urlparse(url)
        if result.scheme not in SCHEMA:
            url = SCHEMA[0] + '://' + url
            result = urlparse(url)
            logging.debug(f'Schema not known. Set to `http://{url}`')
        return all([result.scheme, result.netloc, result.path]), result, url
    except Exception as e:
        logging.error(e)
        return False


def pretty_json(data: list) -> json:
    """Prepare list to json."""
    return json.dumps(data,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': ')
                      )


def generate_data(sprint_lesson: int, number_of_cats: int) -> list:
    """Generate cats data according sprint lesson.

    Meaning:
        0: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 5/15'
            Необходимые поля `name`, `color`, `birth_year`

        1: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 9/15'
            Необходимые поля: `name`, `color`, `birth_year`,
                              `owner`, `achievements`
            `color` указывается в шестнадцатеричном виде #00abc1

        2: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 10/15'
            Необходимые поля: `name`, `color`, `birth_year`,
                              `owner`, `achievements`
            `achievemens` = {`achievement_name`: ...}
            Изменено отображение с использованием source=
                `achievement_name = serializers.CharField(source='name')`

        3: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 12/15'
            Необходимые поля: `name`, `color`, `birth_year`,
                              `owner`, `achievements`
            `color` выбирается из списка выбора:
                'Gray', 'Black', 'White', 'Белый', 'Ginger', 'Mixed'
                `color = models.CharField(max_length=16, choices=CHOICES)`
    """
    cats = []

    for _ in range(number_of_cats):
        cats.append(
            {
                'name': random.choice(INIT_DATA.get('name')),
                'color': random.choice(INIT_DATA.get('color'))[0],
                'birth_year': random.randint(INIT_DATA.get('birth_year')[0],
                                             INIT_DATA.get('birth_year')[1]),
            }
        )
    if sprint_lesson == 0:
        return cats

    for cat in cats:
        cat['owner'] = INIT_DATA.get('owner')
        cat['color'] = random.choice(list(CSS3_HEX_TO_NAMES))
        cat['achievements'] = random.choice(
            [
                [],
                [{'name': random.choice(INIT_DATA.get('achievements'))}]
            ]
        )
    if sprint_lesson == 1:
        return cats

    for cat in cats:
        cat['achievements'] = random.choice(
            [
                [],
                [
                    {'achievement_name': random.choice(
                        INIT_DATA.get('achievements'))}
                ]
            ]
        )
    if sprint_lesson == 2:
        return cats

    for cat in cats:
        cat['color'] = random.choice(INIT_DATA.get('color'))[0]
    if sprint_lesson == 3:
        return cats


def check_server(url: str) -> bool:
    """Check server availability."""
    try:
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            logging.warning(response.status_code)
            return False
        logging.debug(response)
        logging.info(f'Successful response from: {url}')
        return True
    except Exception as e:
        logging.error(e)


def deploy(url: str, cats: list) -> None:
    """Deploy data to server via POST method."""
    try:
        if cats:
            for cat in cats:
                response = requests.post(url, json=cat)
                if response.status_code != 201:
                    logging.error(f'{response.status_code} -> {response.text}')
        else:
            logging.warning('Cats list is empty.')
    except Exception as e:
        logging.error(e)


def cleanup_db(url: str) -> None:
    """Delete all entries from database."""
    try:
        response = requests.get(url)
        entries = []
        for entry in response.json():
            entries.append(entry.get('id'))

        logging.info(f'Entries in database: {len(entries)}')

        for entry in entries:
            requests.delete(url + str(entry))

        logging.info('Cleanup successfuly done.')

    except Exception as e:
        logging.error(e)


def main() -> None:
    """Main function."""
    logging.debug(f'\n{args}')

    args_url_parts = ('-s', '--schema', '-a', '--address', '-p', '--port',
                      '-r', '--resource')
    if any([arg in args_url_parts for arg in sys.argv[1:]]) and not any(
            [args.check_server, args.deploy, args.cleanup_db]):
        parser.error(
            'You may use this option only with [-c | --check-server], '
            '[-d | --deploy] or with [-e | --cleanup-db].\n'
            'Like: gensk.py -c -p 80\n'
            '      gensk.py --deploy --lesson-number 3 --number-of-cats 5'
        )
    elif args.url:
        valide_url = url_validator(args.url)
        if valide_url[0]:
            url = valide_url[2]
    else:
        url = f'{args.schema}://{args.address}:{args.port}/{args.resource}'

    args_gen_or_deploy = ('-l', '--lesson-number', '-n', '--number-of-cats')
    if any([arg in args_gen_or_deploy for arg in sys.argv[1:]]) and not any(
            [args.generate, args.deploy]):
        parser.error(
            'You may use this option only with [-g | --generate] or with '
            '[-d | --deploy].\n'
            'Like: gensk.py -g -l 3 -n 20\n'
            '      gensk.py --deploy --lesson-number 3 --number-of-cats 5'
        )

    if args.generate:
        print(
            pretty_json(generate_data(args.lesson_number,
                                      args.number_of_cats))
        )

    if args.check_server:
        check_server(url)

    if args.deploy:
        if check_server(url):
            data = generate_data(args.lesson_number, args.number_of_cats)
            deploy(url, data)
            logging.debug(f'Deployed data: {pretty_json(data)}')

    if args.cleanup_db:
        if check_server(url):
            cleanup_db(url)


if __name__ == '__main__':
    main()
