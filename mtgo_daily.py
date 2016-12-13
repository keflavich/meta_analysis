import os
import datetime
from bs4 import BeautifulSoup
import requests
import json



# http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date, include_end=True, step=1):
    ndays = int((end_date - start_date).days)+include_end
    for n in range(0, ndays, step):
        yield start_date + datetime.timedelta(n)

decklist_url = 'http://magic.wizards.com/decklist'

def parse_html_decklist(decklist):
    names = [x.text for x in decklist.findAll('span', class_='card-name')]
    counts = [x.text for x in decklist.findAll('span', class_='card-count')]

    return dict(zip(names,counts))

def get_alldecks(start_date=datetime.date(year=2016, month=10, day=1),
                 end_date=datetime.date.today(), ):

    alldecks = {}

    for day in daterange(start_date, end_date):

        ymd = '{year:04d}-{month:02d}-{day:02d}'.format(year=day.year, month=day.month, day=day.day)
        baseurl = ('http://magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-{0}'
                   .format(ymd))

        jsonpath = ('data/{0}'.format(ymd))
        if os.path.exists(jsonpath):
            with open(jsonpath, 'r') as fh:
                alldecks[ymd] = json.load(fh)
            continue
        else:

            print(baseurl)

            rslt = requests.get(baseurl)
            soup = BeautifulSoup(rslt.content, 'lxml')

            decknames = [x.text for x in soup.findAll('h4')]
            #decklists = soup.findAll('div', class_='deck-list-text')
            decklists = soup.findAll('div', class_='sorted-by-overview-container')
            sideboards = soup.findAll('div', class_='sorted-by-sideboard-container')

            decks = ({'mainboard':parse_html_decklist(x),
                      'sideboard':parse_html_decklist(y)}
                     for x,y in zip(decklists, sideboards))

            alldecks[ymd] = dict(zip(decknames, decks))

            print("{0}: {1} decks".format(ymd, len(alldecks[ymd])))

            with open(jsonpath, 'w') as fh:
                json.dump(alldecks[ymd], fh)

    return alldecks
