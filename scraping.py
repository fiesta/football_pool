import datetime
import re
import urllib

from BeautifulSoup import BeautifulSoup
import pytz

import db
import game
import util

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
        in_progress = False
        game_id = dom_game['id'].partition('-')[0]
        time = dom_game.fetch('div', {'class':'game-status'})
        if False: #if len(time) == 0: #Game in Progress/Done
            """
            time_left = dom_game.fetch('td', {'class':'teamTop_inGame'})[0].renderContents().strip()
            scores = dom_game.fetch('td',{'class':'tScoreLine'})
            """

            #away_score = int(scores[0].renderContents())
            #home_score = int(scores[1].renderContents())
            #in_progress = True
            #game_time = None
        else:
            game_time = time[0].text

        team_href_re = re.compile('.*clubhouse.*')
        away_team = dom_game.fetch('a', {'href': team_href_re})[0].text
        home_team = dom_game.fetch('a', {'href': team_href_re})[1].text

        game_date = dom_game.findPrevious('h4', {'class': 'games-date'}).text

        away = util.teams_by_name[away_team]
        home = util.teams_by_name[home_team]

        game_obj = game.Game.from_game_id(game_id)
        if not game_obj:
            db.new_game(game_id, week, get_gametime(game_date, game_time), 
                        away.id, home.id)
            game_obj = game.Game.from_game_id(game_id)
        
        if in_progress:
            game_obj.update_score(away_score, home_score, time_left)

if __name__ == '__main__':
    get_games(1)
