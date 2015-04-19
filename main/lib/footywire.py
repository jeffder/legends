# Utility class for extracting and saving results from Footywire

import http.cookiejar
import urllib.request

from bs4 import BeautifulSoup, element


class NoSupercoachScoresError(Exception):
    pass


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

    def _is_empty(self, obj):
        """
        Check if obj is empty.
        """
        if isinstance(obj, element.Tag):
            return obj.is_empty_element
        elif isinstance(obj, element.NavigableString):
            return obj.isspace()
        else:
            return obj.isspace()

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

    def get_supercoach_scores(self, link, teams):
        scores = {}

        home = teams[0]
        away = teams[1]

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
                try:
                    score = int(cols[13].string.strip())
                except IndexError:
                    raise NoSupercoachScoresError
                scores[club].append({'player': player, 'score': score})
        return scores

    def get_results(self):
        """
        Retrieve the Footywire fixture data for this round.
        """
        num_games = self.round.num_games

        # Format the round's start date so that we can start the search
        start_str = self.round.start_time.strftime('%a %d %b')
        _day, _date, _month = start_str.split()
        if _date.startswith('0'):
            start_str = ' '.join((_day, _date[1], _month))

        url = 'http://www.footywire.com/afl/footy/ft_match_list'
        soup = self._get_soup(url)

        start = soup.find(attrs={'class': 'data'}, text=start_str)
        search_start = start.find_parent('tr')
        games = [search_start]
        games.extend(search_start.find_next_siblings('tr', limit=num_games - 1))
        for game in games:
            cols = [c for c in game.children if not self._is_empty(c)]

            home_score, away_score, link = self.get_scores(cols[4])
            if link is None:
                continue
            teams = self.get_teams(cols[1])
            crowd = self.get_crowd(cols[3])
            # Sometimes Footywire dosen't have the Supercoach scores so skip the
            # game. The idea is that sooner or later they'll include them.
            try:
                sc_scores = self.get_supercoach_scores(link, teams)
            except NoSupercoachScoresError:
                continue

            self.data[teams] = {
                'crowd': crowd,
                'home_score': home_score,
                'away_score': away_score,
                'sc_scores': sc_scores
            }

        return self.data
