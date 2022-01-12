from bs4 import BeautifulSoup
import requests
a=[]
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

data_dict = dict.fromkeys(['city','date', 'group_name', 'Venue', 'details_title', 'place_details', 'Lineup_title', 'Lineup_text', 'last_time', 'trailer'])

def concert_data(concert_url):
    html = get_html(concert_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            data_dict['date'] = soup.find('div', class_='date-and-name').find('p').text
        except:
            print('Нет данного поля')
        try:
            data_dict['group_url'] = f"https://www.songkick.com{soup.find('h1', class_='h0 summary').find('a')['href']}"
        except:
            print('Нет данного поля')
        try:
            data_dict['group_name'] = soup.find('h1', class_='h0 summary').find('a').text
        except:
            print('Нет данного поля')
        try:
            Venue = soup.find('div', class_='component venue-info').find('h2').text
        except:
            print('Нет данного поля')
        try:
            data_dict['Venue'] = Venue + soup.find('p', class_='venue-hcard').text
        except:
            print('Нет данного поля')
        try:
            details_title = soup.find('div', class_='component additional-details').find('h2').text
        except:
            print('Нет данного поля')
        try:
            place_details = soup.find('div', class_='additional-details-container').find_all('p')
            for char in place_details:
                details_title = details_title + char.text
            data_dict['place_details'] = details_title
        except:
            print('Нет данного поля')
        try:
            Lineup_title = soup.find('div', class_='component expanded-lineup-details').find('h2').text
        except:
            print('Нет данного поля')
        try:
            Lineup_details = soup.find('div', class_='component expanded-lineup-details').find_all('li')
            for char in Lineup_details:
                Lineup_title = Lineup_title + char.text
            Lineup_title = ' '.join(Lineup_title.split())
            data_dict['Lineup_details'] = Lineup_title
        except:
            print('Нет данного поля')
        try:
            data_dict['trailer'] = soup.find('div', class_='video-standfirst').find('iframe')['data-src'][2:]
        except:
            print('Нет данного поля')
        a.append(data_dict)
for i in range(5):
    concert_data('https://www.songkick.com/concerts/40117831-bulent-ersoy-at-jolly-joker-private')
print(a)
print(len(a))
