from flask import *
from ServerSide.DBClasses.DBWrapper import DBWrapper
import os
import secrets
import random
from flask import render_template, url_for, flash, redirect, request
from ServerSide.DBClasses.forms import RegistrationForm, LoginForm, ProfileForm
from ServerSide.DBClasses.User import User 
from ServerSide.DBClasses.Post import Post
from ServerSide.DBClasses.Profile import Profile
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

# Initializations and callbacks
app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.fetch_userid(int(user_id))

def image_path(profile_pic):
    hexed = secrets.token_hex(8)
    file, extension = os.path.splitext(profile_pic.filename)
    image_file = hexed + extension
    image_paths = os.path.join(app.root_path, 'static/res', image_file)
    profile_pic.save(image_paths)
    return image_paths

def fetch_pic(username):
        DBWrapper.cursor.execute('''
            SELECT * FROM PROFILE WHERE username=(%s);
        ''', (username,))
        
        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None
        return rec[7]

# Routes
@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET','POST'])
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
def home():
    return render_template('login.html', title='Home')


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = image_path(form.image.data)
            picture_url = picture_file

        num_friends = random.randint(3,1000)
        username = current_user.password
        profile = Profile(username, form.name.data, form.status.data, form.age.data, form.lives.data, form.place.data, num_friends, picture_url)

        if profile.user_exists():
            profile.update_values(username)
            return redirect(url_for('profile'))
        else:
            profile.upload()
            return redirect(url_for('profile'))

    fetched = fetch_pic(current_user.password)
    url = 'res/' + fetched[-20:]
    picture_url = url_for('static', filename=url) 
    return render_template('profile.html', title='Profile', current_user=current_user, form=form, image_file=picture_url)

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        # Creating password hash with default salt of 12
        hashed = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user1 = User(request.form['username'], hashed, request.form['email'])
        user1.upload()
        flash(f'Account created for {form.username.data}! Now log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About', current_user=current_user)

@app.route("/about_l")
def about_l():
    return render_template('about.html', title='About', current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("register"))

app.run(debug=True)






