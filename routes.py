from app import app
from users import new_user, find_user
from flask import redirect, render_template, request, session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['get','post'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user(username, password, 0)
        return redirect('/')

@app.route('/signin', methods=['post'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if not find_user(username, password):
        return render_template('error.html', message='Invalid username or password.')
    session['username'] = username
    return redirect('/')

@app.route('/signout')
def signout():
    del session['username']
    return redirect('/')