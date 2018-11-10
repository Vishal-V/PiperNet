from flask import *
from ServerSide.DBClasses.User import User
from flask import render_template, url_for, flash, redirect, request
from ServerSide.DBClasses.forms import RegistrationForm, LoginForm
from ServerSide.DBClasses.User import User 
from ServerSide.DBClasses.Post import Post
from flask_bcrypt import Bcrypt


app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'
bcrypt = Bcrypt(app)

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
                flash('Credentials Valid. Login successful', 'success')
                return redirect(url_for('register'))
            else:
                flash(f'Password incorrect. Login unsuccessful', 'danger')
                return redirect(url_for('register'))

        else:
            flash(f'User does not exist', 'danger')
            return redirect(url_for('register'))
    else:
        return render_template("login.html", title='Login', form=form)
    
@app.route("/home", methods=['GET', 'POST'])
def timeline():
    return render_template('index.html', title='Home')

@app.route("/profile")
def profile():
    return render_template('profile.html', title='Profile')

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
    return render_template('about.html', title='About')

app.run(debug=True)






