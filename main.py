from flask import *
from ServerSide.DBClasses.User import User
from flask import render_template, url_for, flash, redirect, request
from ServerSide.DBClasses.forms import RegistrationForm, LoginForm
from ServerSide.DBClasses.User import User
# from ServerSide.DBClasses.Posts import Post
from flask_bcrypt import Bcrypt


app = Flask("__app__", template_folder='Site')
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'
bcrypt = Bcrypt(app)

@app.route("/index", methods=['GET'])
@app.route("/", methods=['GET'])
def index():
    return render_template("html/login.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args

    if "username" in data:
        user = User.fetch(data["username"])
        print(user)
        if user is None:
            return make_response(jsonify({'text': "No user with username: " + data["username"]}), 200)
        elif data["password"] != user.password:
            return make_response(jsonify({'text': "Wrong password"}), 200)
        else:
            return make_response(jsonify({'text': "Logged in successfully"}), 200)


    return make_response(jsonify({'text': "Failure"}), 400)

@app.route("/home", methods=['GET', 'POST'])
def timeline():
    return render_template('html/index.html', title='Home')

@app.route("/profile")
def profile():
    return render_template('html/profile.html', title='Profile')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        #Will add full Auth. The hash is commented for now.
        user1 = USERS(request.form['username'], request.form['password'], request.form['email'], 'default.jpg')
        # db.session.add(user1)
        # db.session.commit()
        #Will update fom the methods defined. No API calls. 
        # flash(f'Account created for {form.username.data}! Now log in', 'success')
        #Needs to Auth 
        return redirect(url_for('login'))
    return render_template('html/register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template('html/about.html', title='About')

app.run(debug=True)







