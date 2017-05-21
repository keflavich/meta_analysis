import io
import json
import os
import requests
import zipfile

def get_standard_legal(savename='data/standard_legal.json',
                       forced_legal=[]):
    if os.path.exists(savename):
        with open(savename,'r') as fh:
            return json.load(fh)

    if not os.path.exists('AllSets-x.json'):
        allsetszip = requests.get('https://mtgjson.com/json/AllSets-x.json.zip')
        zf = zipfile.ZipFile(io.BytesIO(allsetszip.content))
        zf.extractall()

    with open('AllSets-x.json', 'r') as fh:
        allsets = json.load(fh)

    standard_cards = []

    for setname in allsets:

        for card in allsets[setname]['cards']:
            if 'legalities' not in card and setname not in forced_legal:
                continue
            elif setname in forced_legal:
                set_legal = True
                standard_cards.append(card['name'])
                print("Found {0} in forced_legal".format(card['name']))
            else:
                legal = [legality['legality'] == 'Legal'
                         for legality in card['legalities']
                         if legality['format'] == 'Standard']
                if legal:
                    standard_cards.append(card['name'])
                    set_legal = True
                else:
                    set_legal = False

        if not(set_legal):
            print("Set {0} is not legal in standard".format(setname))
            continue
        
    with open(savename,'w') as fh:
        json.dump(list(set(standard_cards)), fh)

    return list(set(standard_cards))
