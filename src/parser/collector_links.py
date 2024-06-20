import logging
import aiohttp
import requests
from bs4 import BeautifulSoup

year_for_searching = 2023  # год, до какого включительно будем искать


def check_date(date: str, year: int) -> bool:
    """Проверяем до какого года включительно нам нужны бюллетени"""
    if int(date.split('.')[2]) < year:
        return False
    return True


async def get_request_to_page(url: str) -> str:
    """Отправляет get запрос асинхронно и возвращает ответ в виде тееста страницы"""

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except requests.exceptions.ConnectTimeout:
            logging.error(f'Время ожидания вышло. Невозможно получить ответ от страницы {url}')
            raise requests.exceptions.ConnectTimeout
        except requests.exceptions.ConnectionError:
            logging.error(f'Невозможно получить ответ от страницы {url}')
            raise requests.exceptions.ConnectionError
        except requests.exceptions.RequestException:
            logging.error(f'Страничка {url} не ответила на запрос.')
            raise requests.exceptions.RequestException


async def collector_links_from_page(url: str) -> (list[tuple[str, str]], bool):
    """Собирает ссылки с одной страницы.
    Принимает ссылку на страницу.
    Отдает список с данными и флаг для остановки/продолжения цикла"""

    tm_links = []
    stop_loop = False

    html_content = await get_request_to_page(url)

    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.find_all(
            'a',
            class_='accordeon-inner__item-title link xls')[:10]:
        tm_links.append(f'https://spimex.com{link.get("href")}')
    counter = -1
    for div in soup.find_all('div', class_='accordeon-inner__item-inner__title')[:10]:
        counter += 1
        for span in div.find_all('span'):
            date = span.get_text(strip=True)

        if not check_date(date, year_for_searching):
            del tm_links[counter:]
            stop_loop = True
            break

        else:
            tm_links[counter] = (tm_links[counter], date)

    return tm_links, stop_loop


async def collector_links() -> list[tuple[str, str]]:
    """Собирает все ссылки на xls формы только за 2024 год,
     со всех страниц, возвразает список с кортежами,
    в каждом из которых: ссылка в виде строки и дата в виде строки"""

    num = 0
    stop_loop = False

    total_links = []
    while not stop_loop:
        num += 1
        url = f'https://spimex.com/markets/oil_products/trades/results/?page=page-{num}'
        try:
            tm_links, stop_loop = await collector_links_from_page(url)
        except Exception:
            break

        total_links.extend(tm_links)

    return total_links
