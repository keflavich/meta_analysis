import json
import os
from mtgo_daily import daterange
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from standard_cardlist import get_standard_legal

deck_guess = {
    'UW Panharmonicon': {'Panharmonicon':4, 'Cloudblazer':4, 'Glint-Nest Crane':4, 'Eldrazi Displacer':4, 'Drowner of Hope':2},
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UB Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Grasp of Darkness':4,
                   'Liliana, the Last Hope':4, 'Sunken Hollow':4,},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4,
                   'Void Shatter':4, 'Anticipate':4, 'Negate':4, 'Galvanic Bombardment':4, 'Dynavolt Tower':1},
    'Jeskai Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                       'Blessed Alliance':2, 'Port Town':2, 'Stasis Snare':2, 'Radiant Flames':4,
                       'Fumigate':2,
                       'Aether Hub': 4,
                       'Nahiri, the Harbinger': 2,
                       'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4,
                       'Void Shatter':4, 'Anticipate':4, 'Negate':4, 'Galvanic Bombardment':4},
    'UR Spells': {'Lightning Axe':4, 'Tormenting Voice':4, 'Highland Lake':4, 'Spirebluff Canal':4, 'Thermo-Alchemist':4,
                  'Stormchaser Mage':4, 'Galvanic Bombardment':4, 'Collective Defiance':4, 'Fiery Temper':4, 'Thing in the Ice':2},
    'GW Aggro': {"Archangel Avacyn":4, "Gideon, Ally of Zendikar": 4, "Tireless Tracker": 4, "Sylvan Advocate": 4,
                 'Declaration in Stone': 2, 'Fortified Village': 2, 'Thraben Inspector':4, 'Selfless Spirit':2,
                 'Verdurous Gearhulk': 2,
                 "Smuggler's Copter":4},
    'RB Aggro': {'Fiery Temper':4, 'Bomat Courier':4, 'Unlicensed Disintegration':4,
                 "Smuggler's Copter":4},
    'RG Energy Aggro': {'Servant of the Conduit':4, 'Attune with Aether':4,
                        'Longtusk Cub':4, 'Voltaic Brawler':4,
                        'Bristling Hydra':4},
    'Grixis Graveyard Emerge': {'Elder Deep-Fiend':4, "Kozilek's Return":4,
                                "Prized Amalgam":4, "Cathartic Reunion":4,
                                "Haunted Dead":4, "Wretched Gryff":1},
    'BG Delirium Control': {"Liliana, the Last Hope":4, 'Grim Flayer':4,
                            'Ishkanah, Grafwidow':4,
                            'Grasp of Darkness':4, 'Vessel of Nascency':4,
                            'Emrakul, the Promised End': 2,
                            'Grapple with the Past': 4,
                            "Pilgrim's Eye":1,
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'BG Delirium Aggro': {"Smuggler's Copter":4, 'Grim Flayer':4,
                          'Ishkanah, Grafwidow':4,
                          "Liliana, the Last Hope":4,
                          'Grasp of Darkness':4, 'Gnarlwood Dryad':4,
                          'Sylvan Advocate': 2,
                          'Dead Weight':2,
                          'Scrapheap Scrounger':2,
                          'Mindwrack Demon':2,
                          'Tireless Tracker':2,
                          'Hissing Quagmire':2,
                          'Verdurous Gearhulk':2,
                          'Blossoming Defense':2,
                          'Noose Constrictor':2,
                         },
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Selfless Spirit": 4,
                         "Declaration in Stone":4,
                         "Veteran Motorist":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Veteran Motorist":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
    'RG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Forest':8, 'Mountain':4, 'Game Trail':4,
                              "Woodweaver's Puzzleknot":4,
                             },
    'Temur Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                                 'Whirler Virtuoso': 4, 'Botanical Sanctum': 3, 'Spirebluff Canal': 3,
                                 'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                                 'Island':1, 'Forest': 5, 'Mountain':2,
                                 "Woodweaver's Puzzleknot":4,
                                 "Confiscation Coup":1,
                                 "Evolving Wilds":1,
                             },
    'UG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Botanical Sanctum': 3,
                              'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Island':1, 'Forest': 5,
                              "Woodweaver's Puzzleknot":4,
                              "Glimmer of Genius":4,
                              "Lumbering Falls":4,
                              "Confiscation Coup":1,
                              "Glassblower's Puzzleknot":1,
                              "Evolving Wilds":1,
                             },
    'BG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Forest':8, 'Swamp':4,
                              'To the Slaughter':2, 'Noxious Gearhulk':2, 'Grasp of Darkness':2, 'Blooming Marsh':2,
                              "Servant of the Conduit":2,
                              "Woodweaver's Puzzleknot":4,
                             },
    'Bux Graveyard': {'Haunted Dead':4, 'Prized Amalgam':4, 'Voldaren Pariah':4, 'Cryptbreaker':4,
                     },
    'Metalwork Colossus': {'Metalwork Colossus':4,
                           'Glint-Nest Crane':4,
                           'Sanctum of Ugin':4,
                           "Inventors' Fair":4,
                           "Metalspinner's Puzzleknot":4,
                           "Hedron Archive":4,
                           "Skysovereign, Consul Flagship":1,
                           "Foundry Inspector":2,
                           "Spatial Contortion":2,
                           "Cultivator's Caravan":2,
                           "Elder Deep-Fiend":2,
                           "Prophetic Prism":4,
                          },
    #'BW': {"Ayli, Eternal Pilgrim": 4, "Shambling Vent":4, "Forsaken Sanctuary": 2, "Concealed Courtyard": 4,},
    'BW Control': {"Kalitas, Traitor of Ghet": 4, "Shambling Vent":4,  "Concealed Courtyard": 4,
                   'Anguished Unmaking':3, 'Grasp of Darkness':2, 'Gideon, Ally of Zendikar': 2, 'Ruinous Path':2,
                   'Liliana, the Last Hope': 2, 'Sorin, Grim Nemesis':2, 'Fumigate':1,
                  },
    'Mardu Control': {'Liliana, the Last Hope':4, 'Mountain':4, 'Swamp':4, 'Smoldering Marsh':2, 'Kalitas, Traitor of Ghet':2,
                      'Noxious Gearhulk':2, 'Goblin Dark-Dwellers':2, 'Nahiri, the Harbinger':2, 'Grasp of Darkness':2,
                      'Chandra, Torch of Defiance':2, 'Ruinous Path':2,},
}


def do_clustering(alldecks, prefix="MTGTOP8"):
    
    standard_legal = [x.lower() for x in get_standard_legal()]

    card_namespace = set(card.lower()
                         for dailies in alldecks.values()
                         for deck in dailies.values()
                         for card in deck['mainboard'] if card.lower() in standard_legal)

    lowercase_decks = {date: {key:
                              {board: ({card.lower():deck[board][card] for card in deck[board]}
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
                raise ValueError("Card {0} is not real".format(card))
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


    timestep=7
    week_starts = [day for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=timestep)]

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
    pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pl.savefig("{prefix}_meta.png".format(prefix=prefix))

    def get_deck(num):
        deck = pd.loc[num]
        return deck[deck!=0]

    return pd, get_deck, deck_50_pct, deck_ids, deck_top20s, deck_counts
