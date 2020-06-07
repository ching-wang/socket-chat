import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from markupsafe import escape

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# show the home page
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/join", methods=["post", "get"])
def join():
    session['display_name'] = request.form['display_name']
    print(session['display_name'])
    return render_template('main.html')
    # save display name in session
    # render a template showing list of chats and form to create new one

# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
