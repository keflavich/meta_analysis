import urllib
import json
import re
import os
import requests
from bs4 import BeautifulSoup
import datetime

def get_all_event_info(fmt='Standard', max_pages=10,
                       savefile='data/mtg-leagues/meta.json',
                       earliest_date=datetime.datetime(year=2016, month=10, day=1),
                      ):

    if os.path.exists(savefile):
        with open(savefile, 'r') as fh:
            event_info = json.load(fh)
    else:
        event_info = {}

    base_url = "http://magic-league.com/tourney_list.php"

    for ii in range(max_pages):

        print("Loading deck lists for page {0}".format(ii))
        payload = {'start': ii*50, }

        rslt = requests.get(base_url, params=payload)
        soup = BeautifulSoup(rslt.content, 'lxml')
        

        maintable = soup.find('div', class_='MainText').find('table')

        rows = maintable.findAll('tr')

        if len(rows) < 2:
            raise ValueError("No entries")

        stop = False
        start_recording = False
        for row in rows:
            if not start_recording and all(x in str(row)
                                           for x in ["ID", "Time",
                                                     "Description", "Category",
                                                     "Max", "Tourney", "Type",
                                                     "Rating", "restr.", "TC",
                                                     "Status",
                                                     "Current", "Round"]):
                print("Started recording {0}".format(ii))
                start_recording = True
                colnames = [x.get_text() for x in row.findAll('th')]
                assert colnames
            elif start_recording:
                cols = row.findAll('td')
                this_event = {nm: col.get_text() for nm,col in zip(colnames, cols)
                              if nm}

                if this_event['Description'] != fmt:
                    # skip non-matching formats
                    continue

                date = datetime.datetime.strptime(this_event['Time'],
                                                  "%H:%M %m/%d/%y")
                if date < earliest_date:
                    print("Ending search because date {0} is before first "
                          "date {1}".format(date, earliest_date))
                    stop = True
                    break

                href = cols[0].find('a').get('href')
                _,_,eventid = re.compile("[?=&]").split(href)

                if eventid in event_info:
                    continue

                decks = get_decks(eventid)

                this_event['decks'] = decks

                event_info[eventid] = this_event

        if stop:
            break

    if savefile:
        with open(savefile, 'w') as fh:
            json.dump(event_info, fh)

    return event_info


player_re = re.compile("Played by: (.*) \|")
record_re = re.compile("Record: ([-0-9]*)")
deck_re = re.compile("deck=([0-9]{6})")

def get_player(tbl):
    search = player_re.search(str(tbl))
    if search:
        return search.groups()[0]
    else:
        return ""

def get_record(tbl):
    search = record_re.search(str(tbl))
    if search:
        return search.groups()[0]
    else:
        return ""

def get_decks(eventid):

    base_url = "http://magic-league.com/"
    tournament_url = os.path.join(base_url, "tournament/info.php")

    decks_and_records = {}

    for page in range(1,5):
        payload = {'id': eventid,
                   'view': 'decks',
                   'page': page,
                  }

        rslt = requests.get(tournament_url, params=payload)
        soup = BeautifulSoup(rslt.content, 'lxml')

        decks = [hr for hr in soup.findAll('a')
                 if 'decks/download' in hr.get('href')]
        if len(decks) == 0:
            break
        elif page > 1:
            print("On page {0} for event {1}".format(page, eventid))

        tables_ = soup.find('div', class_='MainText').findAll('table', class_='deck')

        #tables = {get_player(tbl): tbl for tbl in tables_ if get_player(tbl)}
        tds_ = [tbl.find('td', class_='small') for tbl in tables_]
        tds = [td for td in tds_ if get_player(td)]
        #records = {get_player(td): get_record(td) for td in tds if get_player(td)}

        assert len(decks) == len(tds)

        decks_and_records.update({deck_re.search(deck.get('href')).groups()[0]:
                                  {'player': get_player(td),
                                   'record': get_record(td),
                                   'deckid': deck_re.search(deck.get('href')).groups()[0]}
                                  for deck,td in zip(decks, tds)
                                 })
        assert len(decks_and_records) == len(set([dk['player'] for dk in decks_and_records.values()]))

    return decks_and_records

def download_deck(deckid, eventid, save=True, path='data/mtg-leagues',
                  overwrite=False, verbose=False):

    savepath = os.path.join(path, "{0}_{1}".format(eventid, deckid))
    if os.path.exists(savepath) and not overwrite:
        if verbose:
            print("Skipping {0}:{1} because it exists".format(eventid,deckid))
        return
    else:
        rslt = requests.get("http://magic-league.com/decks/download.php",
                            params={'deck':deckid})

        playername = urllib.parse.unquote(rslt.url).split()[-1][:-4]

        with open(savepath, 'w') as fh:
            fh.write("// player event deck\n".format(playername, eventid, deckid))
            fh.write("// {0} {1} {2}\n".format(playername, eventid, deckid))
            fh.write(rslt.text)
        if verbose:
            print("Successfully wrote {0}:{1} to {2}".format(eventid,deckid,savepath))

def get_alldecks(event_info, basepath='data/mtg-leagues/'):
    alldecks = {}

    for eventid,eventmeta in event_info.items():
        for deckid, deckmeta in eventmeta['decks'].items():
            time = datetime.datetime.strptime(eventmeta['Time'],
                                              "%H:%M %m/%d/%y")
            date = time.strftime("%d-%m-%y")
            deckname = deckmeta['player']+"_"+deckmeta['record']+"_"+deckmeta['deckid']

            deck_fn = os.path.join(basepath,
                                   "{0}_{1}".format(eventid,
                                                    deckid))
            if not os.path.exists(deck_fn):
                download_deck(deckid, eventid, verbose=True)

            deck_contents = read_deck(deck_fn)
            deck_contents['record'] = deckmeta['record']
            deck_contents['eventid'] = eventid

            if date in alldecks:
                alldecks[date][deckname] = deck_contents
            else:
                alldecks[date] = {deckname:deck_contents}

    return alldecks

def read_deck(fn):
    with open(fn,'r') as fh:
        mainboard,sideboard = {},{}
        in_sb = False
        for row in fh.readlines():
            if "This deck doesn't exist!" in row:
                return {'mainboard':[], 'sideboard':[]}
            if 'Sideboard' in row:
                in_sb=True
                continue
            if "//" in row:
                continue
            
            if 'SB:' in row:
                row = row[3:]

            count, cardname = int(row.split()[0]), " ".join(row.split()[1:])
            if not in_sb:
                mainboard[cardname] = int(count)
            else:
                sideboard[cardname] = int(count)
            
    return {'mainboard':mainboard, 'sideboard': sideboard}

def get_matchups(event_info, savefile='data/mtg-leagues/matchups.json'):

    base_url = "http://magic-league.com/"
    tournament_url = os.path.join(base_url, "tournament/info.php")

    if os.path.exists(savefile):
        with open(savefile, 'r') as fh:
            game_results = json.load(fh)
    else:
        game_results = {}

    player_ids = set([deck['player']
                      for event in event_info.values()
                      for deck in event['decks'].values()])

    for eventid in event_info:
        if eventid in game_results:
            continue
        else:
            game_results[eventid] = {}
        print("Loading event {0}: ".format(eventid), end="")
        for round in range(1,12):
            rslt = requests.get(tournament_url,
                                params={'id': eventid,
                                        'round': round}
                               )
            soup = BeautifulSoup(rslt.content, 'lxml')
            result_tables = [tbl for tbl in soup.findAll('table')
                             if (tbl.find('th') and
                                 "Round {0} results".format(round)
                                 in tbl.find('th').text)]
            if len(result_tables) == 1:
                result_table = result_tables[0]
            elif len(result_tables) > 1:
                raise ValueError("multiple matches")
            elif len(result_tables) == 0:
                # done with tournament
                print()
                break
            else:
                raise ValueError("impossible value...")

            print("{0}, ".format(round), end="")

            for row in result_table.findAll('tr'):
                tds = row.findAll('td')
                if len(tds) == 6:
                    matchid,player1,_,player2,result,flip = [td.text
                                                             for td in tds]

                    if 'Bye' in (player1, player2):
                        # skip all byes
                        continue

                    player1id_left, player1id_right = player1.split()
                    player1id_right = player1id_right.strip("()")
                    if player1id_right in player_ids:
                        player1id = player1id_right
                    elif player1id_left in player_ids:
                        player1id = player1id_left
                    else:
                        # no valid players
                        if 'Bye' not in player1:
                            print("Skipping {0}: {1} vs {2} w/{3}".format(matchid, player1, player2, result))
                            raise
                        continue

                    player2id_left, player2id_right = player2.split()
                    player2id_right = player2id_right.strip("()")
                    if player2id_right in player_ids:
                        player2id = player2id_right
                    elif player2id_left in player_ids:
                        player2id = player2id_left
                    else:
                        # no valid players
                        if 'Bye' not in player2:
                            print("Skipping {0}: {1} vs {2} w/{3}".format(matchid, player1, player2, result))
                            raise
                        continue


                    if flip:
                        p1wins,p2wins = 0,0
                    else:
                        p1wins,p2wins = map(int, result.split("-"))

                    game_results[eventid][matchid] = \
                            {player1id: {'wins':p1wins, 'losses':p2wins,
                                         'round':round},
                             player2id: {'wins':p2wins, 'losses':p1wins,
                                         'round':round},
                             'eventid': eventid,
                            }

    if savefile:
        with open(savefile, 'w') as fh:
            json.dump(game_results, fh)

    return game_results
