from db import db

def new_category(category):
    sql = 'insert into categories (category) values (:category)'
    db.session.execute(sql, {'category':category})
    db.session.commit()

def show_categories():
    sql = 'select * from categories'
    return db.session.execute(sql).fetchall()

def get_name(id):
    sql = 'select category from categories where id=:id'
    return db.session.execute(sql, {'id':id}).fetchone()[0]

def delete_category(id):
    sql = 'delete from categories where id=:id'
    db.session.execute(sql, {'id':id})
    db.session.commit()
