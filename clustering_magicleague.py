import json
import os
from mtgo_daily import daterange
from get_magicleague import get_alldecks, get_all_event_info
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from do_clustering import do_clustering


if __name__ == "__main__":

    event_info = get_all_event_info()

    alldecks = get_alldecks(event_info)

    pd, get_deck = do_clustering(alldecks, prefix='mtg-league')
