import json
import os
from mtgo_daily import daterange
from get_magicleague import get_alldecks, get_all_event_info, get_matchups
import datetime
import numpy as np
import pandas
import pylab as pl
import scipy.cluster
from do_clustering import do_clustering, deck_guess

import re

record_re = re.compile("_([0-9])-([0-9])-([0-9])_")
player_re = re.compile("(.*)_[0-9]-[0-9]-[0-9]_")

if __name__ == "__main__":

    event_info = get_all_event_info(use_cached=False)

    event_info = {key: value for key,value in event_info.items() if value['Description'] == 'Standard'}

    alldecks = get_alldecks(event_info)

    pd, get_deck, deck_50_pct, deck_ids, deck_top20s, deck_counts = do_clustering(alldecks, prefix='mtg-league')

    records = [record_re.search(x.decode()).groups() for x in pd['ID']]
    playernames = np.array([player_re.search(ID.decode()).groups()[0] for ID in pd['ID']])
    pd.ix[:,'Player'] = playernames
    player_records = {player: [0,0,0] for player,(wins,losses,ties) in zip(playernames,records)}
    for player,(wins,losses,ties) in zip(playernames,records):
        player_records[player][0] += int(wins)
        player_records[player][1] += int(losses)
        player_records[player][2] += int(ties)


    pd['Wins'] = [int(wins) for wins,losses,ties in records]
    pd['Losses'] = [int(losses) for wins,losses,ties in records]
    pd['Ties'] = [int(ties) for wins,losses,ties in records]
    pd['Matches'] = pd['Wins']+pd['Losses']+pd['Ties']

    for archetype in set(pd['Archetype']):
        Wins = pd['Wins'][pd['Archetype']==archetype].sum()
        Losses = pd['Losses'][pd['Archetype']==archetype].sum()
        Matches = pd['Matches'][pd['Archetype']==archetype].sum()
        print("{3:30s} Win pct: {4:6.2f} Total wins: {0:3d} losses: {1:3d} matches: {2:3d}".format(Wins, Losses, Matches, archetype, Wins/Matches))

    timestep=7
    week_starts = [day for day in daterange(datetime.date(year=2016,month=10,day=1), datetime.date.today(), step=timestep)]

    undefeatedfraction_weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())

    dates = pandas.to_datetime([x.decode() for x in pd.Date])
    dates = np.array([datetime.date(year=2000+int(x[6:8]), month=int(x[3:5]), day=int(x[0:2]))
                      for x in pd.Date])

    for week_start in week_starts:
        week_end = week_start + datetime.timedelta(timestep)
        date_matches = (dates>=week_start) & (dates < week_end)
        for deck in deck_guess:
            deck_matches = (pd.Archetype == deck) & date_matches
            if any(deck_matches):
                undefeatedfraction_weekly_summary[deck][week_start] = (pd['Losses'][deck_matches] == 0).sum() / pd['Matches'][deck_matches].sum()

    undefeatedfraction_weekly_summary.plot(style=[x+'o'+y for x,y in
                                                  zip('rgbcmykrgbcmykrgbcmyk',
                                                      ['-']*7 + ['--']*7 +
                                                      [':']*7)],
                                           figsize=[24,20])
    pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pl.xlabel("First date in week")
    pl.ylabel("Fraction of decks that went undefeated")
    pl.savefig("{prefix}_undefeatedfraction.png".format(prefix='mtg-leagues'))



    winfraction_weekly_summary = pandas.DataFrame(index=week_starts, columns=deck_guess.keys())

    dates = pandas.to_datetime([x.decode() for x in pd.Date])
    dates = np.array([datetime.date(year=2000+int(x[6:8]), month=int(x[3:5]), day=int(x[0:2]))
                      for x in pd.Date])

    for week_start in week_starts:
        week_end = week_start + datetime.timedelta(timestep)
        date_matches = (dates>=week_start) & (dates < week_end)
        for deck in deck_guess:
            deck_matches = (pd.Archetype == deck) & date_matches
            if any(deck_matches):
                winfraction_weekly_summary[deck][week_start] = (pd['Wins'][deck_matches]).sum() / pd['Matches'][deck_matches].sum()

    winfraction_weekly_summary.plot(style=[x+'o'+y for x,y in
                                           zip('rgbcmykrgbcmykrgbcmyk', ['-']*7
                                               + ['--']*7 + [':']*7)],
                                    figsize=[24,20])
    pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pl.xlabel("First date in week")
    pl.ylabel("Fraction of games won")
    pl.savefig("{prefix}_winfraction.png".format(prefix='mtg-leagues'))



    game_results = get_matchups(event_info)


    def name_id_to_deck(name, eventid):
        playermatch = playernames == name
        eventmatch = pd['EventID'] == int(eventid)
        mask = eventmatch & playermatch
        if mask.sum() == 1:
            archetype = pd['Archetype'][mask].values[0]
            return archetype
        elif mask.sum() == 0:
            return name
        else:
            raise ValueError()

    archetype_results = {eventid: {matchid: [(name_id_to_deck(player, eventid), result) for player, result in match.items()]
                                   for matchid, match in event.items()}
                         for eventid, event in game_results.items()
                        }

    archetypes = list(set(pd['Archetype']))
    #archetypes = ['RW Vehicle Aggro', 'BG Delirium Control']
    archresults_pd = pandas.DataFrame(index=archetypes, columns=archetypes)
    archresults_pd[:] = 0
    for eventid, event in archetype_results.items():
        for matchid, matchresults in event.items():
            if len(matchresults) < 3:
                continue
            mr = [k for k in matchresults if k[0] != 'eventid']
            player1, player2 = [k[0] for k in mr]
            if player1 in archetypes and player2 in archetypes:
                #if player1 != player2:
                #    print(mr)
                # player 1 vs player 2
                archresults_pd.ix[player1,player2] += mr[0][1]['wins']
                archresults_pd.ix[player2,player1] += mr[0][1]['losses']

                #archresults_pd.ix[player2,player1] += mr[1][1]['wins']
                #archresults_pd.ix[player1,player2] += mr[1][1]['losses']

    archresults_pd_pct = pandas.DataFrame(index=archetypes, columns=archetypes)
    archresults_pd_pct[:] = 0
 
    for arch1 in archetypes:
        for arch2 in archetypes:
            wins = archresults_pd.ix[arch1, arch2]
            losses = archresults_pd.ix[arch2, arch1]
            if (np.isnan(wins+losses)) or wins+losses != int(wins+losses):
                #already done
                continue
            if wins+losses > 0:
                winpct = wins / (wins+losses)
                losspct = losses / (wins+losses)
                archresults_pd_pct.ix[arch1,arch2] = winpct
                archresults_pd_pct.ix[arch2,arch1] = losspct
            else:
                archresults_pd_pct.ix[arch1,arch2] = np.nan

    with open('archresults.html','w') as fh:
        fh.write(archresults_pd.to_html())
    with open('archresults_pct.html','w') as fh:
        fh.write(archresults_pd_pct.to_html())
