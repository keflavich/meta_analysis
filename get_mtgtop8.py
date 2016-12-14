import requests
from bs4 import BeautifulSoup

def get_all_deck_urls():
    all_hrefs = []

    base_url = "http://mtgtop8.com/search"

    for ii in range(1000):

        payload = {'date_start':'01/10/2016',
                   'format':'ST',
                   'compet_check[P]':1,
                   'compet_check[M]':1,
                   'compet_check[C]':1,
                   'compet_check[R]':1,
                   'current_page':ii,
                   }

        rslt = requests.post(base_url, data=payload)
        soup = BeautifulSoup(rslt.content, 'lxml')

        s11s = soup.findAll('td', class_='S11')

        # once we're past the last page
        if not s11s:
            break

        hrefs = [xx.find('a').get('href') for xx in s11s if xx.find('a')]

        all_hrefs += hrefs

    return all_hrefs

def get_deck(url, base_url="http://mtgtop8.com/event"):

    rslt = requests.get(base_url+url)

    return rslt

if __name__ == '__main__':
    all_hrefs = get_all_deck_urls()
    print(all_hrefs)
