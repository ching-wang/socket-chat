import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from markupsafe import escape

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


# Configure flask login
# login = LoginManager(app)
# login.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# @log.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# show the home page
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/join", methods=["POST"])
def join():
    # save display name in session
    session['display_name'] = request.form.get("display_name")
    # render a template showing list of chats and form to create new one
    return redirect("/main")


@app.route("/main", methods=["GET"])
def main():
    return render_template('main.html')

# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
