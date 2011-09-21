import db
import game
import util

from BeautifulSoup import BeautifulSoup
import pytz

import datetime
import re
import sys
import urllib

months = { 'September' : 9 , 'October' : 10 , 'November' : 11 , 'December' : 12 , 'January' : 1 }
est_tz = pytz.timezone('US/Eastern')
def get_gametime(game_date, game_time):
    splits = game_date.split()
    month = months[splits[1]]
    day = int(splits[2].strip(','))
    year = int(splits[3])

    if not game_time:
        return datetime.datetime(year, month, day, tzinfo=est_tz)

    time = game_time.split()[0]
    hour_min = time.split(':')
    hour = int(hour_min[0]) + 12
    min = int(hour_min[1])

    return datetime.datetime(year, month, day, hour, min, tzinfo=est_tz)

def get_games(week=None):
    if week is None:
        week = get_week()

    scoreboard = BeautifulSoup(urllib.urlopen(util.get_espn_scoreboard_url(week)))
    games = scoreboard.fetch('div', {'id':re.compile('\d+-gameContainer')})

    for dom_game in games:
        game_id = dom_game['id'].partition('-')[0]
        time_node = dom_game.fetch('div', {'class': 'game-status'})[0]
        if 'Qtr' in time_node.text or 'Final' in time_node.text:
            away_score = int(dom_game.fetch('li', {'id': game_id + '-aTotal'})[0].text)
            home_score = int(dom_game.fetch('li', {'id': game_id + '-hTotal'})[0].text)
            game_time = None
            time_left = time_node.text
        else:
            game_time = time_node.text
            time_left = None

        team_href_re = re.compile('.*clubhouse.*')
        away_team = dom_game.fetch('a', {'href': team_href_re})[0].text
        home_team = dom_game.fetch('a', {'href': team_href_re})[1].text

        game_date = dom_game.findPrevious('h4', {'class': 'games-date'}).text

        away = util.teams_by_name[away_team]
        home = util.teams_by_name[home_team]

        game_obj = game.Game.from_id(game_id)
        if not game_obj:
            db.new_game(game_id, week, get_gametime(game_date, game_time), 
                        away.id, home.id)
            game_obj = game.Game.from_id(game_id)
        
        if time_left:
            game_obj.update_score(away_score, home_score, time_left)

    return games

if __name__ == '__main__':
    week = int(sys.argv[-1])
    games = get_games(week)
