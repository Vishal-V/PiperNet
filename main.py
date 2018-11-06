from flask import *

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

    print(data)
    if "un" in data:
        if data["un"] == "test":
            return make_response(jsonify({'text': "Failure"}), 200)

    else:
        print("absent")

    return make_response(jsonify({'text': "Failure"}), 200)


app.run("0.0.0.0", 8080)
