"""Парсер фильмов и сериалов сайта imdb.com по заданной ссылке"""

import requests
import os
import csv
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/chart/tvmeter?sort=us,desc&mode=simple&page=1'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
'accept': '*/*',
'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}
HOST = 'https://www.imdb.com'
FILE = 'series.csv'

def get_html(url, params=None):
    """Функция отправки get запроса."""
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    """Функция получения контента."""
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody', class_='lister-list').find_all('tr')
    films = []
    place = 0

    for item in items:
        place += 1
        films.append({
            'place': place,
            'img': item.find('a').find_next('img').get('src'),
            'title': item.find('td', class_='titleColumn').find_next('a')\
                .get_text(strip=True),
            'release_date': item.find('td', class_='titleColumn')\
                .find_next('span', class_='secondaryInfo')\
                    .get_text(strip=True).replace('(', '').replace(')', ''),
            'rating': item.find('td', class_='ratingColumn imdbRating')\
                .get_text(strip=True),
            'link': HOST + item.find('td', class_='titleColumn').find_next('a')\
                .get('href')
        })
    return films

def save_file(items, path):
    """Функция сохранения результата"""

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Место', 'Лого', 'Название', 'Дата релиза', 'Рейтинг', 'Ссылка'
            ])
        for item in items:
            writer.writerow([
                item['place'], item['img'], item['title'], item['release_date'],
                item['rating'], item['link']
                ])

def parse(URL):
    """Функция парсинга страниц."""

    html = get_html(URL)
    if html.status_code == 200:
        films = get_content(html.text)
    else:
        print('Сайт не пускает.')
    save_file(films, FILE)
    print(f'Получено {len(films)} сериалов.')
    os.startfile(FILE)

parse(URL)