from db import db
from flask import session
import secrets
from werkzeug.security import check_password_hash, generate_password_hash

def new_user(username, password, type): # type 0 = user, 1 = admin
    sql1 = 'select id, username from users where username=:username'
    result = db.session.execute(sql1, {'username':username})
    user = result.fetchone()
    if user:
        return False
    else:
        hash_value = generate_password_hash(password)
        sql2 = 'insert into users (username, password, type) values (:username, :password, :type)'
        db.session.execute(sql2, {'username':username, 'password':hash_value, 'type':type})
        db.session.commit()
        return True

def find_user(username, password):
    sql = 'select id, username, password, type from users where username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user['password']
        if check_password_hash(hash_value, password):
            session['id'] = user.id
            session['username'] = user.username
            session['role'] = user.type
            session['csrf_token'] = secrets.token_hex(16)
            return True
        return False

def get_user_id():
    return session.get('id', 0)

def delete_session():
    del session['id']
    del session['username']
    del session['role']
    del session['csrf_token']