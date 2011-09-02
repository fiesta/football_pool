import db, sha

db.new_user('dan', sha.sha('dan').hexdigest(), 'Daniel Gottlieb')

