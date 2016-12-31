import json
import os
from mtgo_daily import daterange
from get_mtgtop8 import get_alldecks, get_event_info
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from do_clustering import do_clustering


def get_deck(num):
    deck = pd.loc[num]
    return deck[deck!=0]

if __name__ == "__main__":

    if not os.path.exists('data/mtgtop8/eventinfo.json'):
        event_info = get_event_info()
        print(event_info)
        with open('data/mtgtop8/eventinfo.json','w') as fh:
            json.dump(event_info, fh)
    else:
        with open('data/mtgtop8/eventinfo.json','r') as fh:
            event_info = json.load(fh)

    alldecks = get_alldecks(event_info)

    pd, get_deck, deck_50_pct, deck_ids, deck_top20s, deck_counts = do_clustering(alldecks, prefix='MTGTOP8')
