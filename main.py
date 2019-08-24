import datetime
from PIL import Image
import os
import secrets
import random
import json

from ServerSide.DBClasses.DBWrapper import DBWrapper
from ServerSide.DBClasses.forms import RegistrationForm, LoginForm, ProfileForm, PostForm, PageForm
from ServerSide.DBClasses.User import User 
from ServerSide.DBClasses.Post import Post
from ServerSide.DBClasses.Profile import Profile
from ServerSide.DBClasses.Page import Page
from ServerSide.DBClasses.Comment import Comment

from ServerSide.AI.sentiment_analyzer import predict

from flask import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO

# Initializations and callbacks
app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.fetch_userid(int(user_id))

def image_path(profile_pic):
    hexed = secrets.token_hex(8)
    file, extension = os.path.splitext(profile_pic.filename)
    image_file = hexed + extension
    image_paths = os.path.join(app.root_path, 'static/res', image_file)

    output_size = (164, 164)
    images = Image.open(profile_pic)
    images.thumbnail(output_size)
    images.save(image_paths)

    return image_paths

def fetch_pic(username):
        DBWrapper.cursor.execute('''
            SELECT * FROM PROFILE WHERE username=(%s);
        ''', (username,))
        
        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None
        return rec[7]

def update_profile_pic(pic):
        username = current_user.username
        DBWrapper.cursor.execute('''
            UPDATE USERS
            SET profile_pic = (%s)
            WHERE username = (%s);
        ''', (pic, username))

# Routes
@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Check if password hashes match
        user = User.fetch(form.email.data)

        if user:
            validate = bcrypt.check_password_hash(user.password, form.password.data)
            if validate:
                login_user(user)
                return redirect(url_for('profile'))
            else:
                flash(f'Password incorrect. Login unsuccessful', 'danger')
                return redirect(url_for('login'))

        else:
            flash(f'User does not exist', 'danger')
            return redirect(url_for('register'))
    else:
        return render_template("login.html", title='Login', form=form)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    user_profile = fetch_profile(current_user.username)
    status = fetch_status(current_user.username)
    posts = fetch_posts()
    comments = Comment.fetch_all()
    celebs = fetch_celebs()
    sentiments = fetch_sentiment()
    vals = [(i, j) for i, j in zip(posts, sentiments)]
    if status:
        stat = status
    else:
        stat = 'PostgreSQL Psycopg2 Flask JS' 

    if posts and len(posts) > 0:
        post = posts

    else:
        post = 'None to show!'

    if comments is None or len(comments) == 0:
        comments = "None"
    return render_template('timeline.html', title='Home', current_user=current_user, stat=stat, user_profile=user_profile, post=post, comments=comments, celebs=celebs, vals=vals)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = image_path(form.image.data)
            picture_url = picture_file

        num_friends = random.randint(3, 1000)
        username = current_user.username
        profile = Profile(username, form.name.data, form.status.data, form.age.data, form.lives.data, form.place.data, num_friends, picture_url)

        if profile.user_exists():
            profile.update_values(username)
            return redirect(url_for('profile'))
        else:
            profile.upload()
            return redirect(url_for('profile'))

    username = current_user.username
    fetched = fetch_pic(username)
    status = fetch_status(username)
    posts = personal_posts(username)

    if fetched:
        url = 'res/' + fetched[-20:]
    else:
        url = 'res/default.jpg'
    picture_url = url_for('static', filename=url)
    update_profile_pic(picture_url)
    update_pic_post(picture_url)

    if status:
        stat = status
    else:
        stat = 'Getting it from PostgreSQL' 

    if posts:
        post = posts
    else:
        post = 'None to show!'
    return render_template('profile.html', title='Profile', current_user=current_user, form=form, image_file=picture_url, stat=stat, post=post)

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        # Creating password hash with default salt of 12
        hashed = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user1 = User(request.form['username'], hashed, request.form['email'], 'default.jpg')
        user1.upload()
        flash(f'Account created for {form.username.data}! Now log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About', current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = image_path(form.picture.data)
            pic = 'res/' + picture_file[-20:]
            url = url_for('static', filename=pic)
        else:
            url = ''

        now = datetime.datetime.now().strftime("%H:%M %d-%m-%y")
        post = Post(current_user.username, form.title.data, form.content.data, now, url, current_user.profile_pic)
        post.upload()
        socketio.emit("newPost", include_self=True)
        return redirect(url_for('home'))

    return render_template('post.html', title='Post', form=form)

@app.route("/post/quick", methods=['GET', 'POST'])
@login_required
def quick_create():
    now = datetime.datetime.now().strftime("%H:%M %d-%m-%y")
    content = request.get_json()['content']
    print(content)
    post = Post(current_user.username, "Status Update", content, now, '', current_user.profile_pic)
    post.upload()
    socketio.emit("newPost")
    return redirect(url_for('home')), 200

@app.route("/celebrity/<name>", methods=['GET', 'POST'])
def celebrity(name):
    celeb = fetch_page(name)

    if celeb is None:
        return redirect('/home')
    else:
        return render_template('celeb.html', title=name, celeb=celeb)


@app.route("/create_celeb", methods=['GET', 'POST'])
@login_required
def create_celeb():
    form = PageForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = image_path(form.image.data)
            pic = 'res/' + picture_file[-20:]
            url = url_for('static', filename=pic)
        else:
            url = ''

        if form.banner.data:
            i = image_path(form.banner.data)
            picture = 'res/' + i[-20:]
            pic_url = url_for('static', filename=picture)
        else:
            pic_url = ''

        friends = random.randint(300000,1000000)
        page = Page(current_user.username, form.create_for.data, form.company.data, friends, form.content.data, form.place.data, url, pic_url)
        page.upload()
        return redirect(url_for('home'))

    return render_template('celeb_form.html', title='Celeb Register', form=form)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    content = request.get_json()
    cmnt = Comment(current_user.username, content['content'], content['post_id'])
    cmnt.upload()
    socketio.emit('comment', json.dumps({'username': content['username'], 'content': content['content'], 'post_id': content['post_id'], 'posted_by': current_user.username}))
    return '', 200

def fetch_status(username):
    DBWrapper.cursor.execute('''
            SELECT * FROM PROFILE WHERE username=(%s);
        ''', (username,))

    rec = DBWrapper.cursor.fetchone()
    if rec is None:
        return None
    return rec[2]


def fetch_profile(username):
    DBWrapper.cursor.execute('''
            SELECT * FROM PROFILE WHERE username=(%s);
        ''', (username,))

    rec = DBWrapper.cursor.fetchone()
    if rec is None:
        return None

    return Profile(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7])


def fetch_posts():
    DBWrapper.cursor.execute('''
        SELECT * FROM POST
        ORDER BY post_id DESC;
    ''')
    val = DBWrapper.cursor.fetchall()
    if (val is None) or (len(val) == 0):
        return None
    return val


def image_path(profile_pic):
    hexed = secrets.token_hex(8)
    file, extension = os.path.splitext(profile_pic.filename)
    image_file = hexed + extension
    image_paths = os.path.join(app.root_path, 'static/res', image_file)

    output_size = (750, 750)
    images = Image.open(profile_pic)
    images.thumbnail(output_size)
    images.save(image_paths)

    return image_paths


def personal_posts(username):
    DBWrapper.cursor.execute('''
        SELECT * FROM POST WHERE username=(%s);
    ''', (username,))

    val = DBWrapper.cursor.fetchall()
    if val is None:
        return None
    return val

def fetch_page(name):
    DBWrapper.cursor.execute('''
        SELECT * FROM PAGE WHERE create_for=(%s);
    ''', (name,))

    val = DBWrapper.cursor.fetchone()
    if val is None:
        return None

    return Page(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7])

def update_pic_post(pic):
    username = current_user.username
    DBWrapper.cursor.execute('''
        UPDATE POST
        SET profile_pic = (%s)
        WHERE username = (%s);
    ''', (pic, username))

def fetch_celebs():
    DBWrapper.cursor.execute('''
        SELECT * FROM PAGE;
    ''')

    val = DBWrapper.cursor.fetchall()
    
    return val

@app.route("/delete", methods=['GET', 'POST'])
def delete():

    DBWrapper.cursor.execute('''
        DELETE FROM PROFILE WHERE username=(%s); 

        DELETE FROM USER WHERE username=(%s);
    ''',(current_user.username, current_user.username))

    return redirect('logout')

def fetch_sentiment():
    DBWrapper.cursor.execute('''
        SELECT sentiment_score, sentiment FROM POST order by post_id desc;
    ''')

    val = DBWrapper.cursor.fetchall()
    
    return val


socketio.run(app, debug=True, host='0.0.0.0')
