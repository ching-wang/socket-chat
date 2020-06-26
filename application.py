from markupsafe import escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import logging
import sys
import datetime


app = Flask(__name__)
handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


channelLists = {"CHANNEL_1": None}
my_message_lists = {}


# show the home page
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

# Display name Login
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


@socketio.on('connect')
def test_connect():
    emit('confirm_connected', {"Connected": True})


@socketio.on("join_channel")
def on_join_channel(data):
    logging.info("join_channel %s", data)
    channel_name = data["channelName"]
    join_room(channel_name)
    emit("joined_channel", {"channelName": channel_name})
    if 'channel_name' in session and session['channel_name'] == channel_name:
        pass
    else:
        emit(
            "server_msg",
            {
                "msg": f"{session['display_name']} has joined the {channel_name} channel"
            },
            room=channel_name)
    session['channel_name'] = data["channelName"]


@socketio.on("leave")
def on_leave(data):
    logging.info("leave %s", data)
    username = session['display_name']
    channel_name = data["channelName"]
    leave_room(channel_name)
    emit("left_channel", {"channel": channel_name})
    emit(
        "server_msg",
        {
            "msg": f"{username} has left the {channel_name} channel."
        },
        room=channel_name
    )


@socketio.on("send_chat_msg")
def on_send_chat_msg(data):
    logging.info("chat_msg %s", data)
    if data["msg"] and data["channelName"]:
        emit(
            "chat_msg",
            {
                "msg": data["msg"],
                "from": session["display_name"],
                "created_at": datetime.datetime.now().replace(microsecond=0).isoformat()
            },
            room=data["channelName"])

# Receiving message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
