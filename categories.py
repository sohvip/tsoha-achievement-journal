from db import db

def new_category(category):
    sql = 'insert into categories (category) values (:category)'
    db.session.execute(sql, {'category':category})
    db.session.commit()

def show_categories():
    sql = 'select category from categories'
    return db.session.execute(sql).fetchall()