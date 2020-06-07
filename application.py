import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from markupsafe import escape

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


roomLists = {"ROOM_1": None}

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

    # Flash message to show login in successfully
    flash('login successfully. Please create a channel or join one to start t chart', 'success')
    return redirect('/main')


@app.route("/main", methods=["GET"])
def main():
    return render_template('main.html', rooms=roomLists)


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash('You are successfully logged out. Please create a channel or join one to start t chart', 'success')
    return render_template("index.html")


@app.route("/room/<room_name>", methods=["GET"])
def room(room_name: str):
    return render_template("room.html", room_name=room_name, rooms=roomLists)

# Create channel
@socketio.on("create channel")
def create_channel(channel_name):
    selection = data["selection"]
    channels[selection] += 1
    emit("channel lists", channels, broadcast=True)

# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
