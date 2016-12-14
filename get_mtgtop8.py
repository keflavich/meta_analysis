import os
import requests
from bs4 import BeautifulSoup

def get_all_deck_urls():
    all_hrefs = []

    base_url = "http://mtgtop8.com/search"

    for ii in range(1000):

        print("Loading deck lists for page {0}".format(ii))
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

#def get_deck(url, base_url="http://mtgtop8.com/export_files/deck{0}.mwDeck"):
def get_deck(deckid, base_url="http://mtgtop8.com/mtgo?d={0}"):

    rslt = requests.get(os.path.join(base_url.format(deckid)))

    return rslt

def download_deck(deckid, save=True, path='data/mtgtop8', overwrite=False):
    rslt = get_deck(deckid)
    savepath = os.path.join(path, str(deckid))
    if os.path.exists(savepath) and not overwrite:
        return
    else:
        with open(savepath, 'w') as fh:
            fh.write(rslt.content)

if __name__ == '__main__':
    all_hrefs = get_all_deck_urls()
    print(all_hrefs)

    for hr in all_hrefs:
        download_deck(hr[16:22])

    
