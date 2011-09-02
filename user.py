import db
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

class UserPicks(model.Model):
    pass

class NonPick:
    pass
