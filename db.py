import pymongo

database = pymongo.Connection()["football_dev"]

def create_indexes():
    database.users.create_index("email")
    database.games.create_index("game_id")
    database.games.create_index("week")

create_indexes()

def new_user(email, password_hash, name):
    database.users.insert({"email": email,
                           "password_hash": password_hash,
                           "name": name}, safe=True)

def save_fiesta_id_for_user(email, fiesta_id):
    database.users.update({"email": email}, {"$set": {"fiesta_id": fiesta_id}}, safe=True)

def num_users():
    return database.users.count()

def user_from_email(email):
    return database.users.find_one({"email": email})

def new_game(game_id, week, game_time, away_id, home_id):
    database.games.insert({"game_id": game_id, "week": week,
                           "game_time": game_time,
                           "away_team": away_id, "away_score": 0,
                           "home_team": home_id, "home_score": 0,
                           "time_left": ""}, safe=True)

def game_from_id(game_id):
    return database.games.find_one({"game_id": game_id})

def games_for_week(week):
    return list(database.games.find({"week": week}))

def save_access_token(access_token):
    database.meta.insert({"access_token": access_token}, safe=True)

def get_access_token():
    return database.meta.find_one({"access_token": {"$exists": True}})['access_token']

def save_group_id(group_id):
    database.meta.insert({"group_id": group_id})

def get_group_id():
    return database.meta.find_one({"group_id": {"$exists": True}})['group_id']
