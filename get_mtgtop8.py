import json
import re
import os
import requests
from bs4 import BeautifulSoup

def get_event_info(start_date='01/10/2016'):
    #all_hrefs = []

    event_info = {}

    base_url = "http://mtgtop8.com/search"

    for ii in range(1000):

        print("Loading deck lists for page {0}".format(ii))
        payload = {'date_start':start_date,
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

        compareform = soup.find('form', action='compare')
        if not compareform:
            break

        souptable = compareform.find('table')
        rows = souptable.findAll('tr')

        start_recording = False
        for row in rows:
            if not start_recording and all(x in str(row) for x in ['Deck', 'Player', 'Event', 'Level', 'Rank', 'Date']):
                start_recording = True
                colnames = [x.get_text() for x in row.findAll('td')]
            elif start_recording:
                if row.find('input', value='Compare Decks'):
                    start_recording = False
                    break
                cols = row.findAll('td')
                this_deck = {nm: col.get_text() for nm,col in zip(colnames, cols)
                             if nm}



                href = cols[1].find('a').get('href')
                _,_,eventid,_,deckid,_,format = re.compile("[?=&]").split(href)

                this_deck['eventid'] = eventid
                this_deck['deckid'] = deckid

                if eventid in event_info:
                    event_info[eventid][deckid] = this_deck
                else:
                    event_info[eventid] = {deckid: this_deck}

                print(this_deck)

                #deckname = cols[1].get_text()
                #player = cols[2].get_text()
                #level = cols[3].get_text()
                #event = cols[4].get_text()
                #rank = cols[5].get_text()
                #date = cols[6].get_text()
                #event_info[eventid] = {'deckid': deckid,
                #                       'href': href,
                #                       'deckname': deckname,
                #                       'player': player,
                #                       'event': event,
                #                       'rank': rank,
                #                       'date': date,
                #                       'level': level,
                #                       'eventid': eventid,
                #                      }


        #hrefs = [xx.find('a').get('href') for xx in s11s if xx.find('a')]

        #all_hrefs += hrefs

    return event_info

#def get_deck(url, base_url="http://mtgtop8.com/export_files/deck{0}.mwDeck"):
def get_deck(deckid, base_url="http://mtgtop8.com/mtgo?d={0}"):

    rslt = requests.get(os.path.join(base_url.format(deckid)))

    return rslt

def download_deck(deckid, eventid, save=True, path='data/mtgtop8',
                  overwrite=False, verbose=False):
    rslt = get_deck(deckid)
    savepath = os.path.join(path, "{0}_{1}".format(eventid, deckid))
    if os.path.exists(savepath) and not overwrite:
        if verbose:
            print("Skipping {0}:{1} because it exists".format(eventid,deckid))
        return
    else:
        with open(savepath, 'w') as fh:
            fh.write(rslt.text)
        if verbose:
            print("Successfully wrote {0}:{1} to {2}".format(eventid,deckid,savepath))

def read_deck(fn):
    with open(fn,'r') as fh:
        mainboard,sideboard = {},{}
        in_sb = False
        for row in fh.readlines():
            if 'Sideboard' in row:
                in_sb=True
                continue

            count, cardname = int(row.split()[0]), " ".join(row.split()[1:])
            if not in_sb:
                mainboard[cardname] = int(count)
            else:
                sideboard[cardname] = int(count)
            
    return {'mainboard':mainboard, 'sideboard': sideboard}

def get_alldecks(event_info, basepath='data/mtgtop8/'):
    alldecks = {}

    for eventid,decklist in event_info.items():
        for deckid,metadata in decklist.items():
            date = metadata['Date']
            deckname = metadata['Deck']+metadata['deckid']

            deck_fn = os.path.join(basepath,
                                   "{0}_{1}".format(metadata['eventid'],
                                                    metadata['deckid']))
            if not os.path.exists(deck_fn):
                download_deck(metadata['deckid'], metadata['eventid'],
                              verbose=True)

            deck_contents = read_deck(deck_fn)
            deck_contents['eventid'] = eventid

            if date in alldecks:
                alldecks[date][deckname] = deck_contents
            else:
                alldecks[date] = {deckname:deck_contents}

    return alldecks

    
    

def get_event(eventid, base_url='http://mtgtop8.com/event', format='ST'):

    url = "{base_url}?e={eventid}&f={format}".format(eventid=eventid,
                                                     base_url=base_url,
                                                     format=format)

    rslt = requests.get(url)
    soup = BeautifulSoup(rslt.content, 'lxml')

    deck_divs = soup.findAll('div',class_='W14') + soup.findAll('div',class_='S14')

    event_decks = {int(id_dd.get_text()):(deck_dd.get_text(),
                                          deck_dd.find('a').get('href')) for
                   id_dd,deck_dd in zip(deck_divs[::2], deck_divs[1::2])}



if __name__ == '__main__':
    if not os.path.exists('data/mtgtop8/eventinfo.json'):
        event_info = get_event_info()
        print(event_info)
        with open('data/mtgtop8/eventinfo.json','w') as fh:
            json.dump(event_info, fh)
    else:
        with open('data/mtgtop8/eventinfo.json','r') as fh:
            event_info = json.load(fh)

    alldecks = get_alldecks(event_info)

    #for hr in all_hrefs:
    #    _,_,eventid,_,deckid,_,format = re.compile("[?=&]").split(hr)
    #    download_deck(deckid, eventid)

    
