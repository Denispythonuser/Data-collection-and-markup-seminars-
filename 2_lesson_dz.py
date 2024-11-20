import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
books_data = []

def scrape_books(url):
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все книги на странице
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text

            # Получаем информацию о наличии
            availability = book.find('p', class_='instock availability').text.strip()
            in_stock = 'In stock' in availability  # Проверка наличия

            # Переходим на страницу книги для получения описания
            detail_page = book.h3.a['href']
            detail_url = f"http://books.toscrape.com/catalogue/{detail_page}"

            # Получим детали книги
            detail_response = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            # Попытка извлечения описания
            description_meta = detail_soup.find('meta', attrs={'name': 'description'})
            description = description_meta['content'].strip() if description_meta else 'Описание отсутствует'  # Установка значения по умолчанию

            book_data = {
                'title': title,
                'price': price,
                'availability': availability,
                'in_stock': in_stock,
                'description': description
            }
            books_data.append(book_data)

        # Переход к следующей странице, если она существует
        next_button = soup.find('li', class_='next')
        if next_button:
            next_url = next_button.a['href']
            url = f"http://books.toscrape.com/catalogue/category/books_1/{next_url}"
        else:
            url = None

    # Сохранение данных в файл
    with open('books_data.json', 'w', encoding='utf-8') as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)

scrape_books(base_url)
