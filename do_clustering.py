import json
import os
from mtgo_daily import daterange
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from standard_cardlist import get_standard_legal

from KLD_archetypes import deck_guess as KLD_deck_guess
from deck_guess_AER import deck_guess as AER_deck_guess
from deck_guess_AKH import deck_guess as AKH_deck_guess

def do_clustering(alldecks, prefix="MTGTOP8", deck_guess=KLD_deck_guess,
                  start_date=datetime.date(year=2016,month=10,day=1),
                  timestep=7,
                  standard_set_savename='data/standard_legal.json',
                  forced_legal=[],
                  card_to_check=None,
                 ):
    
    standard_legal = [x.lower() for x in get_standard_legal(savename=standard_set_savename,
                                                            forced_legal=forced_legal)]
    if card_to_check is not None:
        assert card_to_check in standard_legal

    card_namespace = set(card.lower()
                         for dailies in alldecks.values()
                         for deck in dailies.values()
                         for card in deck['mainboard'] if card.lower() in standard_legal)

    lowercase_decks = {date: {key:
                              {board: ({(card.lower() if '/' not in card else
                                         card.lower().split("/")[0].strip()):
                                        deck[board][card]
                                        for card in deck[board]}
                                       if board not in ('eventid', 'record')
                                       else deck[board])
                               for board in deck}
                              for key,deck in results.items()}
                       for date, results in alldecks.items()}



    legaldecks = {date: results
                  for date, results in lowercase_decks.items()
                  if not any(card.lower() not in standard_legal for deck in results.values() for card in deck['mainboard'])}
    illegalcards = {date: {user: ([card for card in deck['mainboard'] if card.lower() not in standard_legal], deck['eventid'])
                           for user,deck in results.items()
                           if any([card for card in deck['mainboard'] if card.lower() not in standard_legal])
                          } for date,results in lowercase_decks.items()
                    if any(card.lower() not in standard_legal for deck in results.values() for card in deck['mainboard'])}

    deckcount = sum(len(x) for x in legaldecks.values())
    print("Found {0} decks".format(deckcount))

    array = np.recarray(deckcount,  dtype=([('ID', 'S40'), ('Date', 'S10'),
                                            ('EventID', int),
                                            ("Archetype", "S25")] +
                                           [(name, np.int16) for name in card_namespace]))

    ii = 0
    for date,daily in legaldecks.items():
        for deckname,deck in daily.items():
            array['ID'][ii] = deckname.encode('ascii', errors='replace')
            array['Date'][ii] = date
            array['EventID'][ii] = deck['eventid']

            for card in card_namespace:
                if card in deck['mainboard']:
                    array[card][ii] = int(deck['mainboard'][card])+10
                else:
                    array[card][ii] = 0

            ii = ii+1

    pd = pandas.DataFrame(array)

    # get rid of the id column and date column
    justdata = pd.T[4:]




    # import skfuzzy as fuzz
    # # Set up the loop and plot
    # #fig1, axes1 = pl.subplots(3, 3, figsize=(8, 8))
    # fpcs = []
    # 
    # 
    # for ncenters in range(2,20):
    #     cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    #         data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)
    # 
    #     # Store fpc values for later
    #     fpcs.append(fpc)
    # 
    # #    # Plot assigned clusters, for each data point in training set
    #     cluster_membership = np.argmax(u, axis=0)
    # 
    #     print()
    #     print("Nclusters = {0}".format(ncenters))
    #     print()
    # 
    #     for ii in range(ncenters):
    #         mask = cluster_membership==ii
    #         deck = (justdata.T[mask] > 0).sum(axis=0)
    #         deck.sort_values(inplace=True)
    #         if any(k in deck.keys()[-10:] for k in easy_decks):
    #             for k in easy_decks:
    #                 if k in deck.keys()[-10:]:
    #                     name = k
    #             print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #         else:
    #             print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    #         print(deck[-10:])
    # #    for j in range(ncenters):
    # #        ax.plot(xpts[cluster_membership == j],
    # #                ypts[cluster_membership == j], '.', color=colors[j])
    # #
    # #    # Mark the center of each fuzzy cluster
    # #    for pt in cntr:
    # #        ax.plot(pt[0], pt[1], 'rs')
    # #
    # #    ax.set_title('Centers = {0}; FPC = {1:.2f}'.format(ncenters, fpc))
    # #    ax.axis('off')
    # #
    # #fig1.tight_layout()
    # 
    # fig2, ax2 = pl.subplots()
    # ax2.plot(range(2,20), fpcs)
    # ax2.set_xlabel("Number of centers")
    # ax2.set_ylabel("Fuzzy partition coefficient")


    distortions = []

    deck_class = {'Panharmonicon': ['Panharmonicon'],
                  'Metalwork Colossus': ['Metalwork Colossus'],
                  'Aetherworks Marvel': ['Aetherworks Marvel'],
                  #'BG Delirium Aggro': ['Grim Flayer', ],
                  'BG Delirium Control': ["Liliana, the Last Hope", 'Grim Flayer',
                                          'Ishkanah, Grafwidow',
                                          'Grasp of Darkness', 'Vessel of Nascency',
                                          'Noxious Gearhulk', 'Ruinous Path'],
                  'UW Flash': ['Reflector Mage', "Smuggler's Copter", "Thraben Inspector", "Prairie Stream"],
                  'Bux Graveyard': ['Haunted Dead', 'Prized Amalgam', 'Voldaren Pariah', 'Cryptbreaker'],
                  'RW Vehicle Aggro': ["Smuggler's Copter", "Inspiring Vantage", "Pia Nalaar", "Toolcraft Exemplar", "Thraben Inspector"],
                  'Mardu Vehicle Aggro': ["Concealed Courtyard", "Scrapheap Scrounger", "Smuggler's Copter", "Inspiring Vantage", "Toolcraft Exemplar", "Thraben Inspector"],
                  'Wx Humans': ["Thalia's Lieutenant", "Thraben Inspector", "Town Gossipmonger", "Expedition Envoy", "Always Watching"], # has a dwarf?!
                  'RG Energy Aggro': ['Servant of the Conduit', 'Attune with Aether', 'Longtusk Cub', 'Voltaic Brawler', 'Bristling Hydra'],
                  'Grixis Graveyard Emerge': ['Elder Deep-Fiend', "Kozilek's Return", "Prized Amalgam", "Cathartic Reunion", "Haunted Dead", "Wretched Gryff"],
                  'RG Pummeler': ["Electrostatic Pummeler", 'Servant of the Conduit', 'Attune with Aether', "Blossoming Defense", "Built to Smash"],
                  'RB Aggro': ['Fiery Temper', 'Bomat Courier', 'Unlicensed Disintegration'],
                  'UR Control': ['Torrential Gearhulk', 'Glimmer of Genius', 'Harnessed Lightning', 'Spirebluff Canal', 'Wandering Fumarole'],
                  'UW Control': ['Torrential Gearhulk', 'Glimmer of Genius', 'Immolating Glare', 'Blessed Alliance'],
                  'UB Control': ['Torrential Gearhulk', 'Glimmer of Genius', 'Grasp of Darkness', 'Liliana, the Last Hope', 'Sunken Hollow'],
                 }

    easy_decks = ('Panharmonicon', 'Metalwork Colossus', 'Aetherworks Marvel')


    # +1 for the "others"
    guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
    for ii,(deckname, deck) in enumerate(deck_guess.items()):
        for card in deck:
            if card.lower() not in pd.columns:
                print("Deck {0} is not represented in the meta".format(deckname))
                #raise ValueError("Card {0} is not real".format(card))
            guess_array[ii,justdata.T.keys() == card.lower()] = deck[card] + 10


    codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
    code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
    #cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    #    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

    pd['Distortion'] = dist

    # Store fpc values for later
    distortions.append(distortion)

    cluster_membership = code

    deck_50_pct = {}
    deck_counts = {}
    deck_top20s = {}
    deck_ids = {}

    def top20_match(x):
        x = list(x)
        if len(x) == 0:
            return 0
        return np.sum(x)/len(x)

    for ii in range(len(deck_guess)+1):
        mask = cluster_membership==ii
        deck = (justdata.T[mask] > 0).sum(axis=0)
        deck.sort_values(inplace=True)

        deck_top20s[ii] = deck

        name = None
        card_match_fraction = {dk:top20_match(k.lower() in [this_key.lower() for this_key in deck.keys()[-20:]]
                                              for k in ks)
                               for dk,ks in deck_guess.items()}
        bestfrac = 0
        for dk, frac in card_match_fraction.items():
            if frac > bestfrac:
                bestfrac = frac
                name = dk
        if bestfrac < 0.7:
            print("### Deck {0} has bad matches {1}".format(ii, bestfrac))
            name = None
        if name is None:
            print("Deck {0}: {1} matches, {2:0.2f}% of total".format(ii, mask.sum(), mask.sum()/len(mask)*100))
            deck_ids[ii]=ii
            deck_50_pct[ii] = mask.sum()/len(mask)
            deck_counts[ii] = mask.sum()
            pd.ix[mask, 'Archetype'] = "Other "+str(ii)
        else:
            if name in deck_50_pct:
                print("**********DUPLICATE**********")
                pd.ix[mask, 'Archetype'] = name + str(ii)
            else:
                pd.ix[mask, 'Archetype'] = name
            deck_50_pct[name] = mask.sum()/len(mask)
            deck_counts[name] = mask.sum()
            print("Deck {0}={2}: {1} matches, {3:0.2f}% of total".format(ii, mask.sum(), name, mask.sum()/len(mask)*100))
            deck_ids[name]=ii
            #pd['Archetype'][mask] = name
        #print(deck[-20:])

    print(len(deck_50_pct), deck_50_pct)


    final = pandas.DataFrame.from_dict([(name, deck_50_pct[name], deck_counts[name]) for name in deck_50_pct])
    final.sort_values(by=1, inplace=True)
    print(final.sort_values(by=1))


    week_starts = [day for day in daterange(start_date, datetime.date.today(), step=timestep)]

    weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())

    dates = pandas.to_datetime([x.decode() for x in pd.Date])
    dates = np.array([datetime.date(year=2000+int(x[6:8]), month=int(x[3:5]), day=int(x[0:2]))
                      for x in pd.Date])

    for week_start in week_starts:
        week_end = week_start + datetime.timedelta(timestep)
        date_matches = (dates>=week_start) & (dates < week_end)
        for deck in deck_guess:
            deck_matches = (pd.Archetype == deck) & date_matches
            weekly_summary[deck][week_start] = deck_matches.sum() / date_matches.sum()

    weekly_summary.plot(style=[x+'o'+y for x,y in zip('rgbcmykrgbcmykrgbcmykrgbcmyk', ['-']*7 + ['--']*7 + [':']*7 + ['-.']*7)],
                        figsize=[24,20])
    pl.xlabel("First date in week")
    pl.ylabel("Fraction decks in that week")
    pl.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    pl.savefig("{prefix}_meta.png".format(prefix=prefix), bbox_inches='tight')

    def get_deck(num):
        deck = pd.loc[num]
        return deck[deck!=0]

    return pd, get_deck, deck_50_pct, deck_ids, deck_top20s, deck_counts
