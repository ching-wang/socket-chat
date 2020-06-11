import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from markupsafe import escape

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


channelLists = {"CHANNEL_1": None}
my_message_lists = {}

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


@app.route("/login", methods=["POST"])
def login():
    # save display name in session
    session['display_name'] = request.form.get("display_name")
    # render a template showing list of chats and form to create new one

    # Flash message to show login in successfully
    flash('login successfully. Please create a channel or join one to start t chart', 'success')
    return redirect('/main')


@app.route("/main", methods=["GET"])
def main():
    return render_template('main.html', channels=channelLists)


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash('You are successfully logged out. Please create a channel or join one to start t chart', 'success')
    return render_template("index.html")


@app.route("/channel/<channel_name>", methods=["GET", "POST"])
def channels(channel_name: str):
    session['current_channel'] = channel_name

    if request.method == "POST":
        return redirect("index.html")
    return render_template("channel.html", channel_name=channel_name, channels=channelLists)

# Join in a channel
@socketio.on("join_channel")
def join_channel(channel_name):
    join_room(channel_name)
    emit("recent_messages", my_message_lists[channel_name])

# Create channel
@socketio.on("create_channel")
def create_channel(channel_name):

    # Check if the channel name is exist
    if channel_name in channelLists.items():
        emit("error", f"{channel_name} has already been taken")

    # add it to the channel lists
    channelLists['key'] = channel_name
    my_message_lists[channel_name] = []

    join_room(channel_name)
    current_channel = channel_name
    data = {"channel_name": channel_name,
            "messages": my_message_lists[channel]}
    emit("join_channel", data)


# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
