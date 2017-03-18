import json
import os
from mtgo_daily import daterange
from get_mtgtop8 import get_alldecks, get_event_info
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from do_clustering import do_clustering, AER_deck_guess


def get_deck(num):
    deck = pd.loc[num]
    return deck[deck!=0]

if __name__ == "__main__":

    if not os.path.exists('data/mtgtop8/eventinfo_AER.json'):
        # Jan 25, 2017 start of AER
        event_info = get_event_info(start_date='25/01/2017')
        print(event_info)
        with open('data/mtgtop8/eventinfo_AER.json','w') as fh:
            json.dump(event_info, fh)
    else:
        with open('data/mtgtop8/eventinfo_AER.json','r') as fh:
            event_info = json.load(fh)

    alldecks = get_alldecks(event_info)

    (pd, get_deck, deck_50_pct, deck_ids, deck_top20s,
     deck_counts) = do_clustering(alldecks, prefix='MTGTOP8',
                                  deck_guess=AER_deck_guess,
                                  start_date=datetime.date(year=2017,month=1,day=25),
                                  timestep=3,
                                  standard_set_savename='data/AER_standard_legal.json',
                                 )
