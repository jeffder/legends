# Utility class for extracting and saving results from Footywire

import http.cookiejar
import urllib.request

from bs4 import BeautifulSoup


class Footywire(object):

    def __init__(self, rnd):
        self.round = rnd

        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj))
        self.data = {}
        self.round_name = self.round.name.lower().replace(' ', '_')

    def _get_soup(self, url):
        request = urllib.request.Request(url)
        response = self.opener.open(request)

        return BeautifulSoup(response)

    def get_teams(self, html):
        contents = html.contents
        home = contents[1].string.strip()
        away = contents[3].string.strip()

        return home, away

    def get_crowd(self, html):
        crowd = html.contents
        if not crowd:
            return 0

        return int(crowd[0].string.strip())

    def get_scores(self, html):
        contents = html.contents
        if contents:
            home_score, away_score = contents[0].string.strip().split('-')
            home_score, away_score = int(home_score), int(away_score)
            link = contents[0]['href']
        else:
            home_score, away_score, link = None, None, None

        return home_score, away_score, link

    def get_supercoach_scores(self, link, home, away):
        scores = {}

        url = 'http://www.footywire.com/afl/footy/{}'.format(link)
        soup = self._get_soup(url)

        start_tags = soup.find_all(attrs={'name': 't1'})
        for tag, club in zip(start_tags, (home, away)):
            scores[club] = []
            grandparent = tag.find_parents('tr', limit=2)[1]
            header = grandparent.find_next_sibling('tr').find_next('tr')
            rows = header.find_next_siblings('tr')
            for row in rows:
                cols = [c for c in row.children if c != u'\n']
                player = cols[0].string.strip()
                score = int(cols[13].string.strip())
                scores[club].append({'player': player, 'score': score})
        return scores

    def get_results(self):
        '''
        Retrieve the Footywire fixture data for this round.
        '''
        num_games = self.round.num_games

        url = 'http://www.footywire.com/afl/footy/ft_match_list'
        soup = self._get_soup(url)

        round_header = soup.find(attrs={'name': self.round_name})
        search_start = round_header.find_parent('tr')
        games = search_start.find_next_siblings('tr', limit=num_games + 1)
        for game in games[1:]:
            cols = [c for c in game.children if c != u'\n']

            home_score, away_score, link = self.get_scores(cols[4])
            if link is None:
                continue
            teams = self.get_teams(cols[1])
            crowd = self.get_crowd(cols[3])
            sc_scores = self.get_supercoach_scores(link, teams[0], teams[1])

            self.data[teams] = {
                'crowd': crowd,
                'home_score': home_score,
                'away_score': away_score,
                'sc_scores': sc_scores
            }

    def save_result(self, fixture):
        '''
        Save the fixture's result
        '''
        # We may already have the result or the game might not have been played
        # yet
        try:
            result = self.data[(fixture.home.name, fixture.away.name)]
        except KeyError:
            return

        fixture.home_score = result['home_score']
        fixture.away_score = result['away_score']
        fixture.crowd = result['crowd']
        fixture.status = 'Provisional'
        fixture.save()

        # Save the AFL BOGs
        fixture.save_bogs(result['sc_scores'])
