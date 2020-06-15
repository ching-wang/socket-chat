console.log("Starting");

const messageList = document.querySelector("#messages");

function runChat() {
  console.log("Connecting to socket");
  const socket = io();

  socket.on("connect", () => {
    console.log("Socket connected");
  });

  socket.on("confirm_connected", (data) => {
    console.log("confirm_connected", { data });
  });

  socket.on("joined_channel", (data) => {
    console.log("joined_channel", { data });
  });

  socket.on("message", (data) => {
    console.log("message", { data });
  });

  socket.on("chat_msg", (data) => {
    console.log("chat_msg", { data });
    const msgLi = document.createElement("li");
    msgLi.innerText = data.msg;
    messageList.append(msgLi);
  });

  setUpChannelButtons(socket);
}

function setUpChannelButtons(socket) {
  const channelButtons = document.querySelectorAll(".channel-button");
  channelButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const channelName = btn.dataset.channelName;
      console.log("Joining channel", { channelName });
      socket.emit("join_channel", { channelName });
    });
  });
}

document.addEventListener("DOMContentLoaded", runChat);
