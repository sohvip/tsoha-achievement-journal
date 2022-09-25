from app import app
from categories import new_category, show_categories
from users import new_user, find_user
from flask import redirect, render_template, request, session

@app.route('/', methods=['get','post'])
def index():
    if request.method == 'GET':
        categories = show_categories()
        return render_template('index.html', categories=categories)
    if request.method == 'POST':
        category = request.form['category']
        new_category(category)
        return redirect('/')

@app.route('/signup', methods=['get','post'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = int(request.form['role'])
        if not new_user(username, password, role):
            return render_template('signup_error.html', message='Username not available.')
        return redirect('/signin')

@app.route('/signin', methods=['get','post'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not find_user(username, password):
            return render_template('signin_error.html', message='Invalid username or password.')
        session['username'] = username
        return redirect('/')

@app.route('/signout')
def signout():
    del session['username']
    return redirect('/')