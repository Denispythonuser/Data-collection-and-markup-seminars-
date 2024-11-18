import requests

# Запрос к API Foursquare для поиска заведений по категории
category = input("Введите категорию заведений, которую вы ищете (например, кофейни, музеи, парки и т.д.): ")

url = 'https://api.foursquare.com/v2/venues/search'
params = {
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'v': '20220101',
    'near': 'New York',  # Можно указать нужный город или координаты
    'query': category
}

response = requests.get(url, params=params)
data = response.json()

# Получение информации о заведениях
for venue in data['response']['venues']:
    name = venue['name']
    address = venue['location']['address'] if 'address' in venue['location'] else 'Address not available'
    rating = venue['rating'] if 'rating' in venue else 'Rating not available'
    
    print(f'Название: {name}')
    print(f'Адрес: {address}')
    print(f'Рейтинг: {rating}')
    print('-------------------------------------------')