from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, redirect
import twitter2


app = Flask(__name__)


@app.route('/createmap', methods=["POST"])
def mapcreate():
    """
    :return:
    """

    name = request.form['name']
    names, place = twitter2.get_data(name)
    twitter2.createmap(names, place)
    return redirect(url_for("static", filename="Friends.html"))


@app.route('/')
def start():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)