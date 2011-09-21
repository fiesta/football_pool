import db
import game
import model

class User(model.Model):
    
    @classmethod
    def from_email(cls, email):
        return cls(db.user_from_email(email))

    def total_record(self):
        wins = 0
        losses = 0
        return wins, losses

    def record_for_week(self, week):
        wins = 0
        losses = 0
        return wins, losses

    def picks_for_week(self, week):
        return [Pick.get_pick(self.email, game_obj.game_id) \
                    for game_obj in game.Game.games_for_week(week)]

class Pick(model.Model):
    @classmethod
    def get_pick(cls, user_id, game_id):
        doc = db.get_pick(user_id, game_id)
        if not doc:
            return NonPick({"user_id": user_id, "game_id": game_id})

        return cls(doc)

    @staticmethod
    def from_js_args(js_args):
        user_id, _, game_id = js_args.partition('|')
        return Pick.get_pick(user_id, game_id)

    @property
    def game(self):
        return game.Game.from_id(self.mongo_document['game_id'])

    @property
    def js_args(self):
        return '%s|%s' % (self.mongo_document['user_id'],
                          self.mongo_document['game_id'])

    

class NonPick(Pick):
    pass
