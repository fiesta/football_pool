import db
import model
import util

from datetime import datetime

class Game(model.Model):

    @classmethod
    def from_id(cls, game_id):
        return cls(db.game_from_id(game_id))

    @classmethod
    def games_for_week(cls, week):
        return map(cls, db.games_for_week(week))

    @property
    def result(self):
        if '_result' not in dir(self):
            self._result = GameResult.for_game_id(self.game_id)

        return self._result

    @property
    def game_id(self):
        return self.mongo_document['game_id']

    @property
    def home_team(self):
        return util.teams[self.mongo_document['home_team']]

    @property
    def away_team(self):
        return util.teams[self.mongo_document['away_team']]

    @property
    def home_score(self):
        return self.mongo_document['home_score']

    @property
    def away_score(self):
        return self.mongo_document['away_score']

    @property
    def home_spread(self):
        return self.mongo_document['home_spread']

    @property
    def away_spread(self):
        return self.mongo_document['away_spread']

    @property
    def game_time(self):
        return self.mongo_document['game_time']

    @property
    def time_left(self):
        return self.mongo_document['time_left']

    def started(self):
        return datetime.now() >= self.mongo_document['game_time']

    def update_score(self, away_score, home_score, time_left):
        db.update_score(self.game_id, away_score, home_score, time_left)


class GameResult(model.Model):

    @classmethod
    def for_game_id(cls, game_id):
        return cls(db.game_result_from_id(game_id))
