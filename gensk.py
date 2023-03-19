import argparse
import random
import requests
import logging
import json
from http import HTTPStatus
from webcolors import CSS3_HEX_TO_NAMES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

SCHEMA = ['http', 'https']
ADDRESS = '127.0.0.1'
PORT = '8000'
ENDPOINT = 'cats/'
NUMBER_OF_CATS = 10
SPRINT_BASE = 'Спринт 8/18 → Тема 1/3: Django Rest Framework →'

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
    description='Script for generate and deploy kitties data via API',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument('-s', '--schema', choices=SCHEMA, default=SCHEMA[0],
                    help=('Select schema to use.')
                    )

parser.add_argument('-a', '--address', nargs='?', default=ADDRESS,
                    help='Specify address.')

parser.add_argument('-p', '--port', nargs='?', default=PORT,
                    help='Specify port number.')

parser.add_argument('-u', '--url', nargs='?',
                    help='Fully specified URL to API.')

parser.add_argument('-l', '--lesson-number', nargs='?', type=int, default=0,
                    help=('0: `Урок 5/15` 1: `Урок 9/15`'
                          '2: `Урок 10/15` 3: `Урок 12/15`.')
                    )

parser.add_argument('-g', '--generate', action='store_true',
                    help='Generate kitties and print in stdout.')

parser.add_argument('-n', '--number-of-cats',
                    nargs='?', type=int, default=NUMBER_OF_CATS,
                    help=('Number of kitties to generate.')
                    )

parser.add_argument('-c', '--check-server', action='store_true',
                    help='Basic check for endpoint availability.')

parser.add_argument('-d', '--deploy', action='store_true',
                    help='Deploy generated data via `POST` method.')

parser.add_argument('-r', '--cleanup-db', action='store_true',
                    help='Delete all entries in database via `DELETE` method.')

args = parser.parse_args()


def generate_data(sprint_lesson: int, number_of_cats: int) -> list:
    """Generate cats data according sprint lesson.

    Meaning:
        0: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 5/15'
        1: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 9/15'
        2: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 10/15'
        3: 'Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 12/15'
    """
    cats = []

    if sprint_lesson == 0:
        for _ in range(number_of_cats):
            cats.append(
                {
                    'name': random.choice(INIT_DATA['name']),
                    'color': random.choice(INIT_DATA['color'])[0],
                    'birth_year': random.randint(INIT_DATA['birth_year'][0],
                                                 INIT_DATA['birth_year'][1]),
                }
            )

    if sprint_lesson == 1:
        for _ in range(number_of_cats):
            cats.append(
                {
                    'name': random.choice(INIT_DATA['name']),
                    'color': random.choice(list(CSS3_HEX_TO_NAMES)),
                    'birth_year': random.randint(INIT_DATA['birth_year'][0],
                                                 INIT_DATA['birth_year'][1]),
                    'owner': INIT_DATA['owner'],
                    'achievements': [
                        {'name': random.choice(INIT_DATA['achievements'])}
                    ]
                }
            )

    if sprint_lesson == 2:
        for _ in range(number_of_cats):
            cats.append(
                {
                    'name': random.choice(INIT_DATA['name']),
                    'color': random.choice(list(CSS3_HEX_TO_NAMES)),
                    'birth_year': random.randint(INIT_DATA['birth_year'][0],
                                                 INIT_DATA['birth_year'][1]),
                    'owner': INIT_DATA['owner'],
                    'achievements': [
                        {'achievement_name':
                         random.choice(INIT_DATA['achievements'])}
                    ]
                }
            )

    if sprint_lesson == 3:
        for _ in range(number_of_cats):
            cats.append(
                {
                    'name': random.choice(INIT_DATA['name']),
                    'color': random.choice(INIT_DATA['color'])[0],
                    'birth_year': random.randint(INIT_DATA['birth_year'][0],
                                                 INIT_DATA['birth_year'][1]),
                    'owner': INIT_DATA['owner'],
                    'achievements': [
                        {'achievement_name':
                         random.choice(INIT_DATA['achievements'])}
                    ]
                }
            )
    return cats


def check_server(endpoint: str) -> bool:
    """Check server availability."""
    try:
        response = requests.get(endpoint)
        if response.status_code != HTTPStatus.OK:
            logging.warning(response.status_code)
            return False
        return True
    except requests.exceptions.ConnectionError as e:
        logging.error(e)


def deploy(endpoint: str, cats: list) -> None:
    """Deploy data to server via POST method."""
    try:
        if cats:
            for cat in cats:
                requests.post(endpoint, json=cat)
        else:
            logging.warning('Cats list is empty.')
    except Exception as e:
        logging.error(e)


def cleanup_db(endpoint: str) -> None:
    """Delete all entries from database."""
    try:
        response = requests.get(ENDPOINT)
        entries = []
        for entry in response.json():
            entries.append(entry.get('id'))

        logging.info(f'Entries in database: {len(entries)}')

        for entry in entries:
            requests.delete(endpoint + str(entry))

        logging.info('Cleanup successfuly done.')

    except Exception as e:
        logging.error(e)


def main() -> None:
    """Main function."""
    url = f'{args.schema}://{ADDRESS}:{PORT}/{ENDPOINT}'

    if args.url:
        url = args.url

    if args.generate:
        print(
            json.dumps(generate_data(args.lesson_number,
                                     args.number_of_cats),
                       sort_keys=False,
                       indent=4,
                       ensure_ascii=False,
                       separators=(',', ': '))
        )
    else:
        parser.print_help()

    if args.check_server:
        check_server(url)

    if args.deploy:
        if check_server(url):
            deploy(url, generate_data(args.lesson_number,
                                      args.number_of_cats))

    if args.cleanup_db:
        if check_server(url):
            cleanup_db()


if __name__ == '__main__':
    main()
