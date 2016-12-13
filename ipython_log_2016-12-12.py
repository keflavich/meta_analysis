########################################################
# Started Logging At: 2016-12-12 16:33:23
########################################################

########################################################
# # Started Logging At: 2016-12-12 16:33:24
########################################################
import requests
rslt = requests.get('http://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info')
rslt
rslt.content
requests.get('http://magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-2016-12-10')
rslt = requests.get('http://magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-2016-12-10')
rslt.content
print(rslt.content)
rslt.content.split("\n")
rslt.text.split("\n")
[x for x in rslt.text.split("\n") if 'Gracias' in x]
rslt = requests.get('http://magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-2016-12-12')
[x for x in rslt.text.split("\n") if 'Gracias' in x]
from bs4 import BeautifulSoup
soup = BeautifulSoup(rslt.content)
soup = BeautifulSoup(rslt.content, 'html5')
soup = BeautifulSoup(rslt.content, 'html')
soup = BeautifulSoup(rslt.content, 'lxml')
soup.findAll('h4')
get_ipython().magic('history ')
import datetime
datetime.timedelta(1)
datetime.date(year=2016, month=11, day=1)
datetime.date.today()
get_ipython().magic('pwd ')
get_ipython().magic('mv /Users/adam/mtgo_daily.py .')
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('mv /Users/adam/mtgo_daily.py .')
get_ipython().magic('run mtgo_daily.py')
5+True
get_ipython().magic('run mtgo_daily.py')
day.year
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('run mtgo_daily.py')
soup.findAll('h4')
[x.text for x in soup.findAll('h4')]
[x for x in rslt.text.split("\n") if 'Gracias' in x]
soup.findAll('meta')
soup.findAll('meta', name='description')
soup.findAll('meta', name_='description')
soup.findAll('meta', property='og:description')
soup.findAll('meta', name_='description')
soup.findAll('meta', _name='description')
[x for x in rslt.text.split("\n") if 'Otklover' in x]
soup.findAll('div', class='deck-list-text')
soup.findAll('div', class_='deck-list-text')
soup.findAll('div', class_='deck-list-text')[:5]
soup.findAll('div', class_='deck-list-text')[:1]
soup.findAll('span', class_='deck-meta')
#soup.findAll('div', class_='deck-list-text')[:1]
soup.findAll('div', class_='deck-list-text')[0]
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-count')
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-name')
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-name').text
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-name')[0]
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-name')[0].text
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-count')
soup.findAll('div', class_='deck-list-text')[0].findAll('span', class_='card-count')[0].text
start_date = end_date = datetime.date.today()
get_ipython().magic('paste')
# http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date, include_end=True):
    for n in range(int((end_date - start_date).days)+include_end):
        yield start_date + datetime.timedelta(n)

decklist_url = 'http://magic.wizards.com/decklist'

def parse_html_decklist(decklist):
    names = [x.text for x in decklist.findAll('span', class_='card-name')]
    counts = [x.text for x in decklist.findAll('span', class_='card-count')]

    return dict(zip(names,counts))

alldecks = {}

for day in daterange(start_date, end_date):

    ymd = '{year:04d}-{month:02d}-{day:02d}'.format(year=day.year, month=day.month, day=day.day)
    baseurl = ('http://magic.wizards.com/en/articles/archive/mtgo-standings/competitive-standard-constructed-league-{0}'
               .format(ymd))

    print(baseurl)

    rslt = requests.get(baseurl)
    soup = BeautifulSoup(rslt.content, 'lxml')

    decknames = [x.text for x in soup.findAll('h4')]
    decklists = soup.findAll('div', class_='deck-list-text')

    alldecks[ymd] = dict(zip(decknames, decklists))
alldecks
decknames
decklists
get_ipython().magic('run mtgo_daily.py')
all
alldecks
get_ipython().magic('mkdir data')
import json
json.dump
get_ipython().magic('pinfo json.dump')
fp()
json.dump({1:2}, 'test')
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('ls data/')
alldecks
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('run mtgo_daily.py')
alldecks
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('ls data/')
alldecks
alldecks['2016-11-01']
get_ipython().magic('run mtgo_daily.py')
alldecks.values()
alldecks.values()[0]
list(alldecks.values())[0]
get_ipython().magic('run mtgo_daily.py')
alldecks = get_alldecks()
card_namespace = set(card for dailies in alldecks.values() for deck in dailies.values() for card in deck)
card_namespace
deckcount = sum(len(x) for x in alldecks.values)
deckcount = sum(len(x) for x in alldecks.values())
deckcount
get_ipython().magic('pinfo np.recarray')
array = np.recarray(deckcount, dtype=['int' for n in range(len(card_namespace))], names=card_namespace)
['int' for n in range(len(card_namespace))]
np.int16
array = np.recarray(deckcount, dtype=[np.int16 for n in range(len(card_namespace))], names=card_namespace)
array = np.recarray(deckcount, dtype=[(name, np.int16) for name in card_namespace])
array
get_ipython().magic('run clustering.py')
get_ipython().magic('debug')
deckname
deckname.encode('ascii')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
array['Heir of Falkenrath')
array['Heir of Falkenrath']
array['Heir of Falkenrath'][5]
array['Heir of Falkenrath',5]
get_ipython().magic('run clustering.py')
array
get_ipython().magic('run clustering.py')
array[0]
array[5]
decklists[0]
[x for x in rslt.text.split("\n") if 'Sideboard' in x]
get_ipython().magic('rm data/2016-12-12')
get_ipython().magic('run clustering.py')
alldecks
get_ipython().magic('run mtgo_daily.py')
alldecks = get_alldecks()
alldecks
['2016-12-12']
alldecks['2016-12-12']
alldecks['2016-12-12']['yuhy (5-0)']
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('rm data/2016-12-12')
alldecks = get_alldecks()
alldecks['2016-12-12']['yuhy (5-0)']
date
day
baseurl
get_ipython().magic('paste')
print(baseurl)

rslt = requests.get(baseurl)
soup = BeautifulSoup(rslt.content, 'lxml')

decknames = [x.text for x in soup.findAll('h4')]
#decklists = soup.findAll('div', class_='deck-list-text')
decklists = soup.findAll('div', class_='sorted-by-overview-container')
sideboards = soup.findAll('div', class_='sorted-by-sideboard-container')
decklists
sideboards
decks = ({'mainboard':parse_html_decklist(x),
          'sideboard':parse_html_decklist(y)}
         for x,y in zip(decklists, sideboards))
decks
alldecks[ymd] = dict(zip(decknames, decks))
ymd
alldecks['2016-12-12']['yuhy (5-0)']
get_ipython().magic('run mtgo_daily.py')
get_ipython().magic('rm data/*')
get_ipython().magic('run mtgo_daily.py')
#alldecks = get_alldecks()
get_ipython().magic('run mtgo_daily.py')
alldecks = get_alldecks()
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
array
array['Heir of Falkenrath',5]
array['Heir of Falkenrath'][5]
array['Heir of Falkenrath']
import skfuzzy
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(array, 10, 2)
cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(array, 10, 2)
cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(array, 10, 2, error=0.005, maxiter=100)
array.shape
array.astype('int')
array[x for x in array.dtype.names if x != 'ID']
array[[x for x in array.dtype.names if x != 'ID']]
array[[x for x in array.dtype.names if x != 'ID']].astype('int')
import pandas
pandas.DataFrame(array)
pd = pandas.DataFrame(array)
pd.swapaxes()
pd.swapaxes(0,1)
pd.swapaxes(0,1)[1:].swapaxes(0,1)
pd.swapaxes(0,1)[1:].swapaxes(0,1).columns
cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(justdata, 10, 2, error=0.005, maxiter=100)
justdata = pd.swapaxes(0,1)[1:].swapaxes(0,1)
cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(justdata, 10, 2, error=0.005, maxiter=100)
cntr
cntr.shape
pl.plot(cntr)
import pylab as pl
pl.plot(cntr)
pl.plot(cntr.T)
pl.clf()
pl.plot(cntr.T)
get_ipython().magic('pinfo skfuzzy.cluster.cmeans')
np.r_[2:11]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    data=justdata, c=4, m=2, error=0.005, maxiter=1000, init=None)
u.shape
u0.shape
pl.plot(u.T)
pl.clf()
pl.plot(u.T)
pl.plot(u0.T)
jm.shape
jm
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    data=justdata, c=4, m=2, error=0.005, maxiter=1000, init=None)
p.shape
p
fpc
cntr.shape
cnt[0]
cntr
cluster_membership = np.argmax(u, axis=0)
cluster_membership==0
pd[cluster_membership==0]
pd.T[cluster_membership==0].T
get_ipython().magic('paste')
# get rid of the id column
justdata = pd.T[1:]


import pylab as pl
import skfuzzy as fuzz
# Set up the loop and plot
fig1, axes1 = pl.subplots(3, 3, figsize=(8, 8))
fpcs = []

for ncenters, ax in enumerate(axes1.reshape(-1), 2):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

    # Store fpc values for later
    fpcs.append(fpc)

#    # Plot assigned clusters, for each data point in training set
    cluster_membership = np.argmax(u, axis=0)
#    for j in range(ncenters):
#        ax.plot(xpts[cluster_membership == j],
#                ypts[cluster_membership == j], '.', color=colors[j])
#
#    # Mark the center of each fuzzy cluster
#    for pt in cntr:
#        ax.plot(pt[0], pt[1], 'rs')
#
#    ax.set_title('Centers = {0}; FPC = {1:.2f}'.format(ncenters, fpc))
#    ax.axis('off')
#
#fig1.tight_layout()

fig2, ax2 = pl.subplots()
ax2.plot(np.r_[2:11], fpcs)
ax2.set_xlabel("Number of centers")
ax2.set_ylabel("Fuzzy partition coefficient")


cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    data=justdata, c=4, m=2, error=0.005, maxiter=1000, init=None)
cluster_membership
pd[cluster_membership==0]
pd[cluster_membership==4]
pd[cluster_membership==4].columns
pd[cluster_membership==4].sum(axis=0)
len(card_namespace)
card_namespace = set(card
                     for dailies in alldecks.values()
                     for deck in dailies.values() if 'Collected Company' not in deck['mainboard']
                     for card in deck['mainboard'])
len(card_namespace)
pd[cluster_membership==4].sum(axis=0)
deck4 = pd[cluster_membership==4].sum(axis=0)
deck4.sort()
get_ipython().magic('pinfo deck4.sort')
deck4.sort([1])
deck4[1:]
deck4[1:].sort()
deck4_ =deck4[1:]
deck4_
deck4_.sort()
deck4_
#deck4 = pd[cluster_membership==4].sum(axis=0)
justdata[cluster_membership==ii].sum(axis=0)
justdata[cluster_membership==ii].sum(axis=1)
justdata.T[cluster_membership==ii].sum(axis=1)
justdata.T[cluster_membership==ii].sum(axis=0)
deck = justdata.T[cluster_membership==ii].sum(axis=0)
deck.sort()
dec
deck
ii=4
deck = justdata.T[cluster_membership==ii].sum(axis=0)
deck
deck.sort()
deck
deck[-10:]
deck[-10:][0]
deck[-10:].columns
deck.columns
deck.keys
deck.keys()
deck.keys()[-10:]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
ax2.plot(range(2,20), fpcs)
ax2.set_xlabel("Number of centers")
ax2.set_ylabel("Fuzzy partition coefficient")
'Panharmonicon' in deck.keys()[-10:]
deck[-10:]
get_ipython().magic('run clustering.py')
np.nonzero(justdata.T[mask])
(justdata.T[mask])
justdata.T[mask]
justdata.T[mask] > 0
(justdata.T[mask] > 0).sum(axis=0)
deck.sort()
deck
(justdata.T[mask] > 0).sum(axis=0)
blah = (justdata.T[mask] > 0).sum(axis=0)
blah.sort()
get_ipython().magic('pinfo blah.sort')
blah.sort_values(inplace=True)
deck = (justdata.T[mask] > 0).sum(axis=0)
deck.sort_values(inplace=True)
deck
get_ipython().magic('run clustering.py')
justdata
justdata['Metalwork Colossus']
justdata.T['Metalwork Colossus']
justdata.T['Metalwork Colossus'] != 0
sum(justdata.T['Metalwork Colossus'] != 0)
cluster_membership
cluster_membership[(justdata.T['Metalwork Colossus'] != 0)]
import scipy
import scipy.cluster
scipy.cluster.vq
scipy.cluster.vq.kmeans(justdata)
scipy.cluster.vq.kmeans(justdata, 5)
scipy.cluster.vq.kmeans(np.array(justdata, dtype='int'), 5)
scipy.cluster.vq.kmeans(np.array(justdata, dtype='float'), 5)
scipy.cluster.vq.kmeans(np.array(justdata, dtype='float'), 5).shape
a,b=scipy.cluster.vq.kmeans(np.array(justdata, dtype='float'), 5)
a.shape
b
scipy.cluster.vq.vq(justdata, a)
scipy.cluster.vq.vq(np.array(justdata, dtype='int'), a)
code, dist =scipy.cluster.vq.vq(np.array(justdata, dtype='int'), a)
code.shape
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
code
dist
pl.plot(code,dist)
pl.clf()
pl.plot(code,dist,'.')
code
get_ipython().magic('paste')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
fpcs.append(distortions)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)
    if any(k in deck.keys()[-10:] for k in easy_decks):
        for k in easy_decks:
            if k in deck.keys()[-10:]:
                name = k
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    else:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    print(deck[-10:])
distortions = []
get_ipython().magic('paste ')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
fpcs.append(distortions)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)
    if any(k in deck.keys()[-10:] for k in easy_decks):
        for k in easy_decks:
            if k in deck.keys()[-10:]:
                name = k
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    else:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    print(deck[-10:])
get_ipython().magic('pinfo pl.subplots')
pl.subplots(figure=2)
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('paste')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

deck_50_pct = {}

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    print(deck[-20:])

print(deck_50_pct)
get_ipython().magic('paste')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

deck_50_pct = {}

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    print(deck[-20:])

print(deck_50_pct)
get_ipython().magic('paste')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), ncenters)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

deck_50_pct = {}

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    print(deck[-20:])

print(deck_50_pct)
get_ipython().magic('run clustering.py')
len(deck_50_pct)
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
justdata
justdata.shape
justdata.columns
justdata.keys()
justdata.T.keys()
justdata.T.keys() == 'Sunken Hollow'
any(justdata.T.keys() == 'Sunken Hollow')
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,deck in enumerate(deck_guess):
        for card in deck:
                guess_array[justdata.T.keys() == card] = deck[card]
        
get_ipython().magic('paste')
deck_guess = {
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4},
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
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
}

# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,deck in enumerate(deck_guess):
    for card in deck:
        guess_array[justdata.T.keys() == card] = deck[card]
justdata.T.keys()==card
guess_array
guess_array.shape
get_ipython().magic('paste')
for ii,deck in enumerate(deck_guess):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]
guess_array
deck
get_ipython().magic('paste')
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]
guess_array
guess_array.max(axis=0)
guess_array.max(axis=1)
get_ipython().magic('paste')
codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

print()
print("Nclusters = {0}".format(ncenters))
print()

deck_50_pct = {}

for ii in range(ncenters):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)
codebook.shape
code
get_ipython().magic('paste')
# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)
get_ipython().magic('paste')
deck_guess = {
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4},
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
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
    'RG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Forest':8, 'Mountain':4, 'Game Trail':4,
                             },
    'Temur Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                                 'Whirler Virtuoso': 4, 'Botanical Sanctum': 3, 'Spirebluff Canal': 3,
                                 'Island':1, 'Forest': 5, 'Mountain':2,
                             },
}

# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_class.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)
get_ipython().magic('paste')
# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    name = None
    for dk,ks in deck_guess.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)
get_ipython().magic('paste')
deck_50_pct = {}
deck_top20s = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    deck_top20s[ii] = deck

    name = None
    for dk,ks in deck_guess.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)
deck_top20s[1]
get_ipython().magic('paste')
deck_guess = {
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4},
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
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
    'RG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Forest':8, 'Mountain':4, 'Game Trail':4,
                             },
    'Temur Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                                 'Whirler Virtuoso': 4, 'Botanical Sanctum': 3, 'Spirebluff Canal': 3,
                                 'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                                 'Island':1, 'Forest': 5, 'Mountain':2,
                             },
}
get_ipython().magic('paste')
# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}
deck_top20s = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    deck_top20s[ii] = deck

    name = None
    for dk,ks in deck_guess.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)







deck[1]
deck_top20s[1]
get_ipython().magic('paste')
deck_guess = {
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4},
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
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
    'RG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Forest':8, 'Mountain':4, 'Game Trail':4,
                             },
    'Temur Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                                 'Whirler Virtuoso': 4, 'Botanical Sanctum': 3, #'Spirebluff Canal': 3,
                                 'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                                 'Island':1, 'Forest': 5, 'Mountain':2,
                             },
}

# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}
deck_top20s = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    deck_top20s[ii] = deck

    name = None
    for dk,ks in deck_guess.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)


deck_top20s[6]
get_ipython().magic('paste')
deck_guess = {
    'UW Control': {'Torrential Gearhulk':4, 'Glimmer of Genius':4,
                   'Immolating Glare':2, 'Blessed Alliance':2, 'Prairie Stream':4},
    'UR Control': {'Torrential Gearhulk':2, 'Glimmer of Genius':4,
                   'Harnessed Lightning':4, 'Spirebluff Canal':4, 'Wandering Fumarole':4},
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
                            'Noxious Gearhulk':1, 'Ruinous Path':1},
    'UW Flash': {'Reflector Mage':4, "Gideon, Ally of Zendikar":4,
                 "Smuggler's Copter":4, "Thraben Inspector":4,
                 "Prairie Stream":4},
    'RW Vehicle Aggro': {"Smuggler's Copter":4, "Inspiring Vantage":4,
                         "Pia Nalaar":4, "Toolcraft Exemplar":4,
                         "Thraben Inspector":4},
    'Mardu Vehicle Aggro': {"Cultivator's Caravan":3, "Concealed Courtyard":4,
                            "Scrapheap Scrounger":4, "Smuggler's Copter":4,
                            "Inspiring Vantage":4, "Toolcraft Exemplar":4,
                            "Thraben Inspector":4},
    'RG Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                              'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                              'Forest':8, 'Mountain':4, 'Game Trail':4,
                             },
    'Temur Aetherworks Marvel': {'Aetherworks Marvel':4, 'Emrakul, the Promised End':4, 'Ulamog, the Ceaseless Hunger':2,
                                 'Whirler Virtuoso': 4, 'Botanical Sanctum': 3, 'Spirebluff Canal': 3,
                                 'Harnessed Lightning':4, 'Attune with Aether':4, 'Vessel of Nascency':4,
                                 'Island':1, 'Forest': 5, 'Mountain':2,
                             },
    'Bux Graveyard': {'Haunted Dead':4, 'Prized Amalgam':4, 'Voldaren Pariah':4, 'Cryptbreaker':4,
                     },
}

# +1 for the "others"
guess_array = np.zeros([len(deck_guess)+1, justdata.shape[0]])
for ii,(deckname, deck) in enumerate(deck_guess.items()):
    for card in deck:
        guess_array[ii,justdata.T.keys() == card] = deck[card]


codebook, distortion = scipy.cluster.vq.kmeans(np.array(justdata.T, 'float'), guess_array)
code, dist = scipy.cluster.vq.vq(np.array(justdata.T, 'int'), codebook)
#cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#    data=justdata, c=ncenters, m=2, error=0.005, maxiter=1000, init=None)

# Store fpc values for later
distortions.append(distortion)

cluster_membership = code

deck_50_pct = {}
deck_top20s = {}

for ii in range(len(deck_guess)+1):
    mask = cluster_membership==ii
    deck = (justdata.T[mask] > 0).sum(axis=0)
    deck.sort_values(inplace=True)

    deck_top20s[ii] = deck

    name = None
    for dk,ks in deck_guess.items():
        if all(k in deck.keys()[-20:] for k in ks):
            name = dk
    if name is None:
        print("Deck {0}: {1} matches, {2}%".format(ii, mask.sum(), mask.sum()/len(mask)))
    else:
        if name in deck_50_pct:
            print("**********DUPLICATE**********")
        deck_50_pct[name] = mask.sum()/len(mask)
        print("Deck {0}={2}: {1} matches, {3}%".format(ii, mask.sum(), name, mask.sum()/len(mask)))
    #print(deck[-20:])

print(len(deck_50_pct), deck_50_pct)




get_ipython().magic('run clustering.py')
deck_top20s[0]
deck_top20s[1]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('debug')
get_ipython().magic('run clustering.py')
deck_top20s[1]
deck_top20s[6]
deck_top20s[10]
get_ipython().magic('run clustering.py')
list(zip(deck_top20s[10], deck_top20s[0]))
list(zip(deck_top20s[10].keys(), deck_top20s[0],keys()))
deck_top20s[0]
deck_top20s[0].keys()
list(zip(deck_top20s[10].keys(), deck_top20s[0].keys()))
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
list(zip(deck_top20s[7].keys(), deck_top20s[1].keys()))
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_top20s[12]
get_ipython().magic('run clustering.py')
deck_top20s[13]
get_ipython().magic('run clustering.py')
pandas.DataFrame(deck_50_pct)
pandas.DataFrame(deck_50_pct, 0)
pandas.DataFrame(deck_50_pct, 1)
pandas.DataFrame.from_dict(deck_50_pct)
pandas.DataFrame.from_dict(deck_50_pct)
deck_50_pct
pandas.DataFrame.from_dict(deck_50_pct.items())
pandas.DataFrame(deck_50_pct.items())
pandas.DataFrame.from_dict(list(deck_50_pct.items()))
pandas.DataFrame.from_dict(list(deck_50_pct.items()))
final = pandas.DataFrame.from_dict(list(deck_50_pct.items()))
final.sort(1)
final
final.sort_values()
final.sort_values(by=1)
final = pandas.DataFrame.from_dict(list(deck_50_pct.items()))
final.sort_values(by=1)
final
final.sort_values(by=1)
list(zip(deck_top20s[5].keys(), deck_top20s[3].keys()))
final.sort_values(by=1)
deck_50_pct
deck_top20s
deck_top20s[0]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_ids
deck_ids
get_ipython().magic('run clustering.py')
deck_ids
ii=6
mask = cluster_membership==ii
deck = (justdata.T[mask] > 0).sum(axis=0)
deck
cards_in_uw = deck != 0
cards_in_uw
justdata[cards_in_uw]
justdata[cards_in_uw].sum(axis=0)
justdata[cards_in_uw].sum(axis=1)
justdata[cards_in_uw].sum(axis=0).min()
justdata[cards_in_uw].sum(axis=0) > 0
justdata[cards_in_uw].T[justdata[cards_in_uw].sum(axis=0) > 0]
justdata[cards_in_uw][justdata[cards_in_uw].sum(axis=0) > 0]
justdata[cards_in_uw].T[justdata[cards_in_uw].sum(axis=0) > 0]
justdata[cards_in_uw].sum(axis=0) > 0
(justdata[cards_in_uw].sum(axis=0) > 0).shape
justdata[cards_in_uw].T.shape
justdata[cards_in_uw].T[np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool')]
justdata[cards_in_uw].T[np.nonzero(np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool'))]
np.nonzero(np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool'))
just_data[np.nonzero(np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool'))]
justdata[np.nonzero(np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool'))]
justdata[np.nonzero(np.array(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool')),:]
justdata[justdata>0]
get_ipython().magic('pinfo justdata.where')
justdata.where(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool'))
justdata.where(justdata[cards_in_uw].sum(axis=0) > 0, dtype='bool')
justdata.where(justdata[cards_in_uw].sum(axis=0) > 0)
justdata.T.where(justdata[cards_in_uw].sum(axis=0) > 0)
justdata.where(justdata[cards_in_uw].sum(axis=0) > 0)
get_ipython().magic('pinfo justdata.where')
#justdata.where(justdata[cards_in_uw].sum(axis=0) > 0)
justdata[cards_in_uw].sum(axis=0) > 0
uw_mask = justdata[cards_in_uw].sum(axis=0) > 0
justdata[uw_mask]
justdata.where(uw_mask)
justdata[cards_in_uw].sum(axis=0) > 0
justdata[cards_in_uw].any(axis=0)
get_ipython().magic('pinfo justdata.query')
justdata.query(uw_mask)
np.array(justdata)
arr = np.array(justdata)
arr.shape
arr[:,uw_mask]
arr[:,uw_mask].shape
uw_mask.sum()
uw_mask = justdata[cards_in_uw].any(axis=0)
uw_mask.sum()
deck_ids
get_ipython().magic('run clustering.py')
deck_ids
deck_top20s[6]
deck_top20s[6].nonzero()
len(deck_top20s[6].nonzero())
len(deck_top20s[6].nonzero()[0])
uw_mask = deck_top20s[6] > 0
justdata[cards_in_uw]
#uw_mask = justdata[cards_in_uw].any(axis=0)
cards_in_uw
cards_in_uw = deck != 0
#deck = (justdata.T[mask] > 0).sum(axis=0)
mask
deck
uw_mask
uw_mask.sum()
uw_mask = justdata[cards_in_uw].any(axis=0)
cards_in_uw
cards_in_uw.sum()
cards_in_uw = deck != 0
deck = justdata.T[cluster_membership==ii].sum(axis=0)
ii
deck
ii = deck_ids['UW Flash']
ii
deck = justdata.T[cluster_membership==ii].sum(axis=0)
deck
(deck>0).sum()
cards_in_uw = deck != 0
cards_in_uw.sum()
justdata[cards_in_uw]
justdata[cards_in_uw]
justdata[cards_in_uw]['Wastes']
justdata['Wastes'][cards_in_uw]
justdata
justdata['Wastes']
justdata.T['Wastes']
justdata.T['Wastes'][card_in_uw]
justdata.T['Wastes'][cards_in_uw]
cards_in_uw
justdata.T['Wastes'].T[cards_in_uw]
justdata.T['Wastes'].T
justdata.T['Wastes'].sum()
justdata.T['Wastes']*cards_in_uw
justdata.T['Wastes'][cards_in_uw]
justdata.T['Wastes'][cards_in_uw.astype('bool')]
cards_in_uw.astype('bool')
np.array(cards_in_uw, dtype='bool')
uw_mask = np.array(cards_in_uw, dtype='bool')
justdata.T['Wastes'][uw_mask]
justdata.T['Wastes'][uw_mask].shape
justdata.T['Wastes'][uw_mask].sum()
justdata[uw_mask]
justdata[uw_mask].shape
np.array(justdata[uw_mask])
justdata[uw_mask].columns
justdata[uw_mask].T.columns
len(justdata[uw_mask].T.columns)
justdata[uw_mask]
justdata[uw_mask].sum(axis=0)
justdata[uw_mask].sum(axis=1)
justdata[uw_mask]
justdata[uw_mask].max(axis=0)
justdata[uw_mask].max(axis=0).min()
uw_decks = justdata[uw_mask].max(axis=0) > 0 
uw_decks.sum()
justdata
(justdata[uw_mask].max(axis=0) > 0).sum()
(justdata[uw_mask].max(axis=1) > 0).sum()
justdata[uw_mask][617]
justdata[uw_mask][616]
justdata
justdata[uw_mask][616]
justdata[uw_mask][615]
justdata[uw_mask][614]
justdata[uw_mask][500]
get_ipython().magic('run clustering.py')
deck_ids[9]
deck_top20s[9]
get_ipython().magic('run clustering.py')
deck_top20s[13]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_top20s[14]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_top20s[10]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_top20s[10]
deck_top20s[10]
get_ipython().magic('run clustering.py')
get_ipython().magic('run clustering.py')
deck_top20s[10]
deck_top20s[10][-20:]
deck_top20s[10][-25:]
get_ipython().magic('run clustering.py')
deck_top20s[10][-25:]
ds
pd
pd.columns
"Reckless Bushwhacker" in pd.columns
get_ipython().magic('run clustering.py')
deck_top20s[10][-25:]
get_ipython().magic('run clustering.py')
deck_top20s[14][-25:]
mask
mask.shape
pd['Archetype'] = [" "*25 for ii in range(mask.size)]
pd
pd.columns
#pd['Archetype'] = [" "*25 for ii in range(mask.size)
get_ipython().magic('run clustering.py')
pd['Archetype']
pd.hist('Archetype')
pd.apply(pandas.value_counts).plot(kind='bar', subplots=True)
pd['Date','Archetype'].apply(pandas.value_counts).plot(kind='bar', subplots=True)
pl.close(16)
pd['Date']
pd['Date', 'Archetype']
pd[['Date', 'Archetype']]
pd[['Date','Archetype']].apply(pandas.value_counts).plot(kind='bar', subplots=True)
pd['Archetype'].apply(pandas.value_counts).plot(kind='bar', subplots=True)
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7)):
    print(day)
    
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7):
    print(day)
    
get_ipython().magic('pinfo range')
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7):
    print(day)
    
get_ipython().magic('pinfo range')
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7):
    print(day)
    
list(range(0, int((end_date - start_date).days)+include_end, step))
list(range(0,50,7))
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7):
    print(day)
    
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), 7):
    print(day)
    
list(range(0,80,7))
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=7):
    print(day)
    
get_ipython().magic('run mtgo_daily.py')
for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=7):
    print(day)
    
week_starts = [day for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=7)]
week_starts
weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())
weekly_summary
df
ds
pd.Date
day
pd.Date < day
pd.Date.astype(pandas.DatetimeIndex)
pd.Date.to_datetime()
pandas.to_datetime(pd.Date)
pandas.to_datetime(pd.Date) < day
pandas.to_datetime(pd.Date) < day
weekly_summary
weekly_summary['RG Aetherworks']
weekly_summary['2016-11-19']['RG Aetherworks']
weekly_summary['2016-11-19']
weekly_summary.columns
weekly_summary['BW']
weekly_summary['BW']['2016-10-01']
weekly_summary['BW'][pd.to_datetime('2016-10-01]
weekly_summary['BW'][pandas.to_datetime('2016-10-01')]
weekly_summary
weekly_summary['BW'][pandas.Timestamp('2016-10-01')]
pd[0]
weekly_summary[0]
weekly_summary.index
weekly_summary.index[0]
weekly_summary['BW'][datetime.date(2016,10,1)]
get_ipython().magic('paste')
week_starts = [day for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=7)]

weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())

dates = pandas.to_datetime(pd.Date)

for week_start in week_starts:
    week_end = week_start + datetime.timedelta(7)
    date_matches = (dates>=week_start) & (dates < week_end)
    for deck in deck_guess:
        deck_matches = (pd.Archetype == deck) & date_matches
        weekly_summary[deck][week_start] = deck_matches.sum()
weekly_summary
weekly_summary.plot()
get_ipython().magic('pinfo weekly_summary.plot')
weekly_summary.plot(colors='rgbcmykrgbcmykr', linestyles=['--',':','-']*5)
weekly_summary.plot(style=[x+y for x,y in zip('rgbcmykrgbcmykr',['--',':','-']*5)])
get_ipython().magic('paste')
for week_start in week_starts:
    week_end = week_start + datetime.timedelta(7)
    date_matches = (dates>=week_start) & (dates < week_end)
    for deck in deck_guess:
        deck_matches = (pd.Archetype == deck) & date_matches
        weekly_summary[deck][week_start] = deck_matches.sum() / date_matches.sum()
weekly_summary.plot(style=[x+y for x,y in zip('rgbcmykrgbcmykr',['--',':','-']*5)])
for ii in pl.get_fignums(): pl.close(ii)
weekly_summary.plot(style=[x+y for x,y in zip('rgbcmykrgbcmykr', '-'*5 + '--'*5 + ':'*5)])
pl.xlabel("First date in week")
pl.ylabel("Fraction of 5-0 decks in that week")
for ii in pl.get_fignums(): pl.close(ii)
weekly_summary.plot(style=[x+y for x,y in zip('rgbcmykrgbcmykr', ['-']*5 + ['--']*5 + [':']*5)])
pl.xlabel("First date in week")
pl.ylabel("Fraction of 5-0 decks in that week")
get_ipython().system('open 8png')
get_ipython().system('open *png')
get_ipython().magic('ls -rt')
get_ipython().system('open *png')
