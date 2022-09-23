from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def new_user(username, password, type): # type 0 = user, 1 = admin
    hash_value = generate_password_hash(password)
    sql = 'insert into users (username, password, type) values (:username, :password, :type)'
    db.session.execute(sql, {'username':username, 'password':hash_value, 'type':type})
    db.session.commit()

def find_user(username, password):
    sql = 'select id, username, password from users where username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        False
    else:
        hash_value = user['password']
        if check_password_hash(hash_value, password):
            return True
        return False