from flask import *
from ServerSide.DBClasses.User import User


app = Flask("__app__", template_folder='Site')


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


app.run("0.0.0.0", 8080)
