import time
import datetime

import model

class Team(object):
    def __init__(self, id, name, abbreviation, espn_abbr):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.espn_abbr = espn_abbr

teams = {1: Team(1, "New York Giants", "NYG", "Giants"),
         2: Team(2, "Dallas Cowboys", "DAL", "Cowboys"),
         3: Team(3, "Washington Redskins", "WAS", "Redskins"),
         4: Team(4, "Philadelphia Eagles", "PHI", "Eagles"),
         5: Team(5, "Arizona Cardials", "ARI", "Cardinals"),
         6: Team(6, "San Francisco 49ers", "SF", "49ers"),
         7: Team(7, "Seattle Seahawks", "SEA", "Seahawks"),
         8: Team(8, "St. Louis Rams", "STL", "Rams"),
         9: Team(9, "Chicago Bears", "CHI", "Bears"),
         10: Team(10, "Detroit Lions", "DET", "Lions"),
         11: Team(11, "Green Bay Packers", "GB", "Packers"),
         12: Team(12, "Minnesota Vikings", "MIN", "Vikings"),
         13: Team(13, "Atlanta Falcons", "ATL", "Falcons"),
         14: Team(14, "Carolina Panthers", "CAR", "Panthers"),
         15: Team(15, "New Orleans Saints", "NO", "Saints"),
         16: Team(16, "Tampa Bay Buccaneers", "TB", "Buccaneers"),
         17: Team(17, "Buffalo Bills", "BUF", "Bills"),
         18: Team(18, "New England Patriots", "NE", "Patriots"),
         19: Team(19, "Miami Dolphins", "MIA", "Dolphins"),
         20: Team(20, "New York Jets", "NYJ", "Jets"),
         21: Team(21, "Denver Broncos", "DEN", "Broncos"),
         22: Team(22, "Kansas City Chiefs", "KC", "Chiefs"),
         23: Team(23, "Oakland Raiders", "OAK", "Raiders"),
         24: Team(24, "San Diego Chargers", "SD", "Chargers"),
         25: Team(25, "Baltimore Ravens", "BAL", "Ravens"),
         26: Team(26, "Cincinatti Bengals", "CIN", "Bengals"),
         27: Team(27, "Cleveland Browns", "CLE", "Browns"),
         28: Team(28, "Pittsburgh Steelers", "PIT", "Steelers"),
         29: Team(29, "Houston Texans", "HOU", "Texans"),
         30: Team(30, "Indianapolis Colts", "IND", "Colts"),
         31: Team(31, "Jacksonville Jaguars", "JAC", "Jaguars"),
         32: Team(32, "Tennessee Titans", "TEN", "Titans")}

teams_by_name = dict([(team.espn_abbr, team) for team in teams.values()])

_season_start = datetime.datetime(2011, 9, 7)
def get_today():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    return datetime.datetime(year, month, day)

def get_week():
    time_since_start = get_today() - _season_start
    week = time_since_start.days / 7 + 1

    return max(week, 1)

def get_year():
    """Uses the season start date to get the season year"""
    return _season_start.year

def get_espn_scoreboard_url(week=None, year=None):
    if week == None:
        week = get_week()
    if year == None:
        year = get_year()

    return 'http://scores.espn.go.com/nfl/scoreboard?weekNumber=%d&seasonYear=%d&seasonType=2' % (week, year)

class LeaderboardSnapShot(model.Model):
    pass

class CurrentStandings(model.Model):
    pass

class WeeklyWinners(model.Model):
    pass
