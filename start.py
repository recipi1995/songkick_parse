
from bs4 import BeautifulSoup
import requests

list_of_result = []
data_dict = dict.fromkeys(['country','city','date', 'group_name', 'Venue', 'details_title', 'place_details', 'Lineup_title', 'Lineup_text', 'last_time', 'trailer'])
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_city_url(city_val, country):
    city_val = city_val
    country = country
    text_url = f'https://www.songkick.com/search?page=1&per_page=10&query={city_val}%2C+{country}&type=locations'
    print(text_url)
    html = get_html(text_url)
    if html:
        try:
            print()
            soup = BeautifulSoup(html, 'html.parser')
            all_city = soup.find('li', class_='small-city').find_all('p', class_='summary')
            for city in all_city:
                url =f"https://www.songkick.com{city.find('a')['href']}" 
                name_city = city.find('strong').text
            return url, name_city
        except AttributeError:
            print('Такого города на сайте нет')
            url = False
            return url 

def concert_data(concert_url):
    html = get_html(concert_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            data_dict['date'] = soup.find('div', class_='date-and-name').find('p').text
        except:
            print('Нет поля Дата')
        try:
            data_dict['group_url'] = f"https://www.songkick.com{soup.find('h1', class_='h0 summary').find('a')['href']}"
        except:
            print('Нет поля URL группы')
        try:
            data_dict['group_name'] = soup.find('h1', class_='h0 summary').find('a').text
        except:
            print('Нет поля имя группы')
        try:
            Venue = soup.find('div', class_='component venue-info').find('h2').text
        except:
            print('Нет поля Заголовок коонцертного зала')
        try:
            data_dict['Venue'] = Venue + soup.find('p', class_='venue-hcard').text
        except:
            print('Нет поля контакнтных данных концертный зал')
        try:
            details_title = soup.find('div', class_='component additional-details').find('h2').text
        except:
            print('Нет поля Доп детали')
        try:
            place_details = soup.find('div', class_='additional-details-container').find_all('p')
            for char in place_details:
                details_title = details_title + char.text
            data_dict['place_details'] = details_title
        except:
            print('Нет поля детали')
        try:
            Lineup_title = soup.find('div', class_='component expanded-lineup-details').find('h2').text
        except:
            print('Нет поля Детали состава')
        try:
            Lineup_details = soup.find('div', class_='component expanded-lineup-details').find_all('li')
            for char in Lineup_details:
                Lineup_title = Lineup_title + char.text
            Lineup_title = ' '.join(Lineup_title.split())
            data_dict['Lineup_details'] = Lineup_title
        except:
            print('Нет поля Детали состава')
        try:
            data_dict['trailer'] = soup.find('div', class_='video-standfirst').find('iframe')['data-src'][2:]
        except:
            print('Нет поля трейлер')
        list_of_result.append(data_dict)

def get_city_data(city_val, country):
    city_val = city_val
    country = country
    url = get_city_url(city_val, country)
    html=True
    page=0
    while html is not False and url is not False:
        page+=1
        html = get_html(f"{url[0]}?page={page}#metro-area-calendar")
        print("-"*200)
        print('page: ', page)
        print("-"*200)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                all_data = soup.find('ul', class_='component metro-area-calendar-listings dynamic-ad-container').find_all('li', class_='event-listings-element')
                n=0
                for data in all_data:
                    concert_url = f"https://www.songkick.com{data.find('a', class_='event-link chevron-wrapper')['href']}"
                    concert_data(concert_url)
                    #print(data.find('a', class_='event-link chevron-wrapper')['href'])
                    print("="*200)
                    print(concert_url)
                    print("="*200)
            except AttributeError: html=False     


DICT_CITIES = {
    'Russian Federation': ['Moscow', 'Saint-Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Kazan', 'Nizhniy-Novgorod', 'Chelyabinsk', 'Samara', 'Omsk', 'Rostov-on-Don', 'Krasnoyarsk', 
            'Voronezh', 'Perm', 'Volgograd', 'Krasnodar', 'Saratov', 'Tyumen', 'Togliatti', 'Izhevsk', 'Kaliningrad', 'Ufa'],
    'Italy': ['Venice', 'Verona', 'Messina', 'Padua', 'Trieste', 'Taranto', 
            'Brescia', 'Prato', 'Parma', 'Modena']
}

for country in DICT_CITIES:
    for city_val in DICT_CITIES[country]:
        #print(city_val, country)
        get_city_data(city_val, country)
        print(list_of_result)