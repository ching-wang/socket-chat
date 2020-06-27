# Project 2 - Flack

Web Programming with Python and JavaScript

## Getting Started

Python 3.6 or higher installed

To run this Flask application:

Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages (Flask and Flask-SocketIO, for instance) are installed.

```bash
pip install -r requirements.txt
flask run
```

## Features

- Choose display name
- Create new channels
- Live update of new channel names
- Join existing channels
- See last 100 messages when joining a channel
- Channel joining and leaving announcements
- Send messages in channel
- Delete own messages from a channel; deletes on server and in other users' clients
- Remembers display name and previous channel when returning

## Structure

### application.py

Backend server application using Flask and SocketIO

### layout.html

navbar and script header

### index.html

Root page, where a user inputs their desired display name

### main.html

main.html is a chatting dashboard which shows the chatting room and creating channel button.

### channel.js

Frontend client application that communicates with the backend and manipulates the DOM.
