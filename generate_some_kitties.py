import random
import requests
import logging
from http import HTTPStatus
from webcolors import CSS3_HEX_TO_NAMES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

ENDPOINT = 'http://127.0.0.1:8000/cats/'

NUMBER_OF_CATS = 10

INIT_DATA = {
    'name': ['Соня', 'Клеопатра', 'Цунами', 'Забияка', 'Матильда', 'Кнопка',
             'Масяня', 'Царапка', 'Серсея', 'Ворсинка', 'Амели', 'Наоми',
             'Маркиза', 'Изольда', 'Гарфилд', 'Том', 'Гудвин', 'Рокки',
             'Ленивец', 'Пушок', 'Спорти', 'Бегемот', 'Пират', 'Гудини',
             'Зорро', 'Саймон', 'Альбус', 'Базилио', 'Леопольд', 'Нарцисс',
             'Атос', 'Каспер', 'Валли', 'Барсик', 'Масик', 'Вельзевул',
             'Лапочка', 'Уголек', 'Царапка', 'Джонни', 'Борис', 'Пушистик',
             'Геродот'],

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


def generate_data(sprint_lesson: int = 0,
                  number_of_cats: int = NUMBER_OF_CATS) -> list:
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
                    'color': random.choice(INIT_DATA['color']),
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
    """Delete all entries from data base."""
    response = requests.get(ENDPOINT)
    entries = []
    for entry in response.json():
        entries.append(entry.get('id'))
    for entry in entries:
        requests.delete(endpoint + str(entry))


def main() -> None:
    """Main function."""
    if check_server(ENDPOINT):
        data = generate_data(3)
        deploy(ENDPOINT, data)


if __name__ == '__main__':
    main()
