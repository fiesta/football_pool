import db
import model

class Game(model.Model):

    @classmethod
    def from_game_id(cls, game_id):
        return cls(db.game_from_id(game_id))

    @classmethod
    def games_for_week(cls, week):
        return map(cls, db.games_for_week(week))

    @property
    def result(self):
        if '_result' not in dir(self):
            self._result = GameResult.for_game_id(self.game_id)

        return self._result

class GameResult(model.Model):

    @classmethod
    def for_game_id(cls, game_id):
        return cls(db.game_result_from_id(game_id))
