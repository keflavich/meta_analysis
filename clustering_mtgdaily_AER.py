from mtgo_daily import get_alldecks, daterange
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster

from deck_guess_AER import deck_guess

bad_cards = ('Collected Company', "Nissa's Pilgrimage",
             "Knight of the White Orchid", "Smuggler's Copter",
             "Emrakul, the Promised End",
             "Reflector Mage",
             "Ojutai's Command", "Tragic Arrogance")

start_date = datetime.date(year=2017,month=1,day=25)

alldecks = get_alldecks(start_date=start_date)

alldecks = {date: results for date, results in alldecks.items()
            if not any(bad in deck['mainboard'] for deck in results.values() for bad in bad_cards)}



card_namespace = set(card
                     for dailies in alldecks.values()
                     for deck in dailies.values() if not any(x in {**deck['mainboard'], **deck['sideboard']} for x in bad_cards)
                     for card in {**deck['mainboard'], **deck['sideboard']})

deckcount = sum(len(x) for x in alldecks.values())

array = np.recarray(deckcount, dtype=[('ID','S20'),('Date','S10'),("Archetype","S25")]+[(name, np.int16) for name in card_namespace])

ii = 0
for date,daily in alldecks.items():
    for deckname,deck in daily.items():
        array['ID'][ii] = deckname.encode('ascii')
        array['Date'][ii] = date

        for card in card_namespace:
            if card in deck['mainboard']:
                array[card][ii] = int(deck['mainboard'][card])+10
            else:
                array[card][ii] = 0

        ii = ii+1

pd = pandas.DataFrame(array)

# get rid of the id column and date column
justdata = pd.T[3:]


distortions = []



# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        if card not in pd.columns:
            print("Deck {0} is not represented in the meta".format(deckname))
            #raise ValueError("Card {0} is not real".format(card))
        guess_array[ii,justdata.T.keys() == card] = deck[card] + 10


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

pd['Distortion'] = dist

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}
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
    card_match_fraction = {dk:top20_match(k in deck.keys()[-20:] for k in ks)
                           for dk,ks in deck_guess.items()}
    bestfrac = 0
    for dk, frac in card_match_fraction.items():
        if frac > bestfrac:
            bestfrac = frac
            name = dk
    if bestfrac < 0.8:
        print("Deck {0}  has bad matches {1}".format(ii, bestfrac))
        name = None
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
        deck_ids[ii]=ii
        deck_50_pct[ii] = mask.sum()/len(mask)
        pd.ix[mask, 'Archetype'] = "Other "+str(ii)
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
            pd.ix[mask, 'Archetype'] = name + str(ii)
        else:
            pd.ix[mask, 'Archetype'] = name
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
        deck_ids[name]=ii
        #pd['Archetype'][mask] = name
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)


final = pandas.DataFrame.from_dict(list(deck_50_pct.items()))
final.sort_values(by=1, inplace=True)
print(final.sort_values(by=1))


timestep=3
week_starts = [day for day in daterange(start_date, datetime.date.today(), step=timestep)]

weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())

dates = pandas.to_datetime(pd.Date.str.decode('ascii'))

for week_start in week_starts:
    week_end = week_start + datetime.timedelta(timestep)
    date_matches = (dates>=week_start) & (dates < week_end)
    for deck in deck_guess:
        deck_matches = (pd.Archetype == deck) & date_matches
        weekly_summary[deck][week_start] = deck_matches.sum() / date_matches.sum()

weekly_summary.plot(style=[x+'o'+y for x,y in zip('rgbcmykrgbcmykrgbcmyk', ['-']*7 + ['--']*7 + [':']*7)],
                    figsize=[24,20])
pl.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
pl.xlabel("First date in week")
pl.ylabel("Fraction of 5-0 decks in that week")
pl.savefig("MTGO_5-0_meta.png")


def get_deck(num):
    deck = pd.loc[num]
    return deck[deck!=0]
