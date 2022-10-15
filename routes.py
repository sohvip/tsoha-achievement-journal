from app import app
from categories import new_category, show_categories, get_name, delete_category
from users import new_user, find_user, delete_session, get_user_id
from posts import new_post, edit_post, show_posts, show_post, get_post, delete_post, count_posts, search_posts
from comment import new_comment, show_comments, show_comment
from likes import liked, get_likes
from flask import redirect, render_template, request, session, abort

@app.route('/', methods=['get','post'])
def index():
    if request.method == 'GET':
        categories = show_categories()
        return render_template('index.html', categories=categories)
    if request.method == 'POST':
        category = request.form['category']
        token = request.form['csrf_token']
        if session["csrf_token"] != token:
            abort(403)
        new_category(category)
        return redirect('/')

@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        search = request.form['search']
        posts = search_posts(search)
        return render_template('search.html', posts=posts)

@app.route('/category/<int:id>', methods=['get'])
def category(id):
    if request.method == 'GET':
        category = get_name(id)
        posts = show_posts(id)
        user_id = get_user_id()
        count = count_posts(id)
        return render_template('category.html', id=id, category=category, posts=posts, user_id=user_id, count=count)

@app.route('/category/<int:id>/delete', methods=['get'])
def delete(id):
    if request.method == 'GET':
        delete_category(id)
        return redirect('/')

@app.route('/category/<int:id>/<int:post_id>', methods=['get'])
def post(id, post_id):
    if request.method == 'GET':
        category = get_name(id)
        post = show_post(post_id)
        user_id = get_user_id()
        likes = get_likes(post_id)
        comment = show_comment(post_id)
        return render_template('post.html', id=id, post_id=post_id, category=category, post=post, user_id=user_id, likes=likes, comment=comment)

@app.route('/category/<int:id>/newpost', methods=['get', 'post'])
def newpost(id):
    if request.method == 'GET':
        return render_template('newpost.html', id=id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        token = request.form['csrf_token']
        if session["csrf_token"] != token:
            abort(403)
        if len(title) < 3 or len(content) < 3:
            return render_template('newpost_error.html', id=id, message='Title and content must be atleast 3 characters long.')
        if len(title) > 100 or len(content) > 5000:
            return render_template('newpost_error.html', id=id, message='Title or content is too long.')
        if len(set(title)) <= 1 and title[0] == ' ':
            return render_template('newpost_error.html', id=id, message='Title cannot contain only spaces.')
        if len(set(content)) <= 1 and content[0] == ' ':
            return render_template('newpost_error.html', id=id, message='Content cannot contain only spaces.')
        new_post(title, content, id)
        return redirect(f'/category/{id}')

@app.route('/category/<int:id>/<int:post_id>/editpost', methods=['get', 'post'])
def editpost(id, post_id):
    if request.method == 'GET':
        post = get_post(post_id)
        return render_template('editpost.html', id=id, post_id=post_id, title=post[0], content=post[1])
    if request.method == 'POST':
        content = request.form['content']
        token = request.form['csrf_token']
        if session["csrf_token"] != token:
            abort(403)
        if len(content) < 3:
            return render_template('editpost_error.html', id=id, post_id=post_id, message='Content must be atleast 3 characters long.')
        if len(set(content)) <= 1 and content[0] == ' ':
            return render_template('editpost_error.html', id=id, post_id=post_id, message='Content cannot contain only spaces.')
        edit_post(post_id, content)
        return redirect(f'/category/{id}')

@app.route('/category/<int:id>/<int:post_id>/deletepost', methods=['get'])
def deletepost(id, post_id):
    if request.method == 'GET':
        delete_post(post_id)
        return redirect(f'/category/{id}')

@app.route('/category/<int:id>/<int:post_id>/comment', methods=['get', 'post'])
def comment(id, post_id):
    if request.method == 'GET':
        return render_template('comment.html', id=id, post_id=post_id)
    if request.method == 'POST':
        comment = request.form['comment']
        if len(comment) < 3:
            return render_template('comment_error.html', id=id, post_id=post_id, message='Comment must be atleast 3 characters long.')
        if len(set(comment)) <= 1 and comment[0] == ' ':
            return render_template('comment_error.html', id=id, post_id=post_id, message='Comment cannot contain only spaces.')
        new_comment(comment, post_id)
        return redirect(f'/category/{id}/{post_id}')

@app.route('/category/<int:id>/<int:post_id>/like', methods=['get'])
def like(id, post_id):
    if request.method == 'GET':
        liked(post_id)
        return redirect(f'/category/{id}/{post_id}')

@app.route('/category/<int:id>/<int:post_id>/all_comments', methods=['get'])
def all_comments(id, post_id):
    if request.method == 'GET':
        comments = show_comments(post_id)
        if len(comments) == 0:
            comments = 0
        return render_template('all_comments.html', id=id, post_id=post_id, comments=comments)

@app.route('/signup', methods=['get','post'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            role = int(request.form['role'])
        except:
            return render_template('signup_error.html', message='Choosing a role is required in order to sign up.')
        if not 10 >= len(username) >= 3:
            return render_template('signup_error.html', message='Username must be 3 to 10 characters long.')
        if not 10 >= len(password) >= 3:
            return render_template('signup_error.html', message='Password must be 3 to 10 characters long.')
        if " " in username or " " in password:
            return render_template('signup_error.html', message='Username and password must not contain spaces.')
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
        return redirect('/')

@app.route('/signout')
def signout():
    delete_session()
    return redirect('/')