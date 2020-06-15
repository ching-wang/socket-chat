console.log("Starting");

const messageList = document.querySelector("#messages");
const messageForm = document.querySelector("#message-form");
const messageField = document.querySelector("#message-field");

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
    localStorage.setItem("channelName", data.channelName);
  });

  socket.on("message", (data) => {
    console.log("message", { data });
  });

  socket.on("server_msg", (data) => {
    console.log("server_msg", { data });
    const msgLi = document.createElement("li");
    msgLi.innerText = data.msg;
    messageList.append(msgLi);
    messageList.scrollTop = messageList.scrollHeight;
  });

  socket.on("chat_msg", (data) => {
    console.log("chat_msg", { data });
    if (!data.msg || !data.from) {
      return;
    }
    const msgLi = document.createElement("li");
    const from = document.createElement("strong");
    from.innerText = `${data.from}: `;
    const msg = document.createElement("span");
    msg.innerText = data.msg;
    msgLi.append(from, msg);
    messageList.append(msgLi);
    messageList.scrollTop = messageList.scrollHeight;
  });

  messageForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const msg = messageField.value;
    const sendMessage = {
      msg,
      channelName: localStorage.getItem("channelName"),
    };
    console.log("Sending chat message", { sendMessage });
    socket.emit("send_chat_msg", sendMessage);
    messageField.value = "";
    console.log("Sent chat message", { sendMessage });
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
