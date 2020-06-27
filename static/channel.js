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

  //join channel
  socket.on("joined_channel", (data) => {
    console.log("joined_channel", { data });
    if (!localStorage.getItem("channelName"))
      localStorage.setItem("channelName", data.channelName);
    const channelName = localStorage.getItem("channelName");
    console.log(`You have already joined the channel ${channelName}`);
  });

  //leave the channel
  socket.on("leave", (data) => {
    console.log("leave_channel", { data });
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
    const createTime = document.createElement("small");
    createTime.innerText = ` ${data.created_at}  `;
    const from = document.createElement("strong");
    from.innerText = `${data.from}: `;
    const msg = document.createElement("span");
    msg.innerText = data.msg;
    msgLi.append(from, msg, createTime);
    messageList.append(msgLi);
    messageList.scrollTop = messageList.scrollHeight;
  });

  socket.on("new_channel_created", (data) => {
    console.log("new_channel_create", { data });
    const channelName = `${data.channel}`;
    channelLi = document.createElement("li");
    channelLi.innerHTML = `<button
      class="btn btn-link channel-button"
      data-channel-name="${channelName}"
      id="${channelName}">
        <span data-feather="home"></span>
        ${channelName}
      </button>`;
    const channelLists = document.getElementById("channel-lists");
    channelLists.append(channelLi);
    setUpChannelButtons(socket);
    console.log(channelLists);
  });

  socket.on("left_channel", (data) => {
    console.log("left_channel", { data });
    localStorage.removeItem("channelName");
    messageList.innerHTML = "";
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

  rejoinPreviousChannel(socket);
  setUpChannelButtons(socket);
  setUpCreateChannelForm(socket);
  setUpExitChannel(socket);
}

function rejoinPreviousChannel(socket) {
  const channelName = localStorage.getItem("channelName");
  if (channelName) {
    console.log("Re-joining previous channel", { channelName });
    socket.emit("join_channel", { channelName });
  }
}

function setUpChannelButtons(socket) {
  console.log("setUpChannelButtons");
  const channelButtons = document.querySelectorAll(".channel-button");
  channelButtons.forEach((btn) => {
    btnClone = btn.cloneNode(true);
    btnClone.addEventListener("click", () => {
      const channelName = btn.dataset.channelName;
      console.log("Joining channel", { channelName });
      socket.emit("join_channel", { channelName });
    });
    btn.parentNode.replaceChild(btnClone, btn);
  });
  console.log("setUpChannelButtons done");
}

function setUpExitChannel(socket) {
  console.log("setUpExitChannel");
  const exitBtn = document.querySelector("#exit-btn");
  exitBtn.addEventListener("click", () => {
    const channelName = localStorage.getItem("channelName");
    console.log("exitChannel", { channelName });
    localStorage.removeItem("channelName");
    socket.emit("leave", { channelName });
  });
  console.log("setUpExitChannel done");
}

function setUpCreateChannelForm(socket) {
  console.log("setUpCreateChannelForm");
  const createChannelForm = document.querySelector("#channel_creation");
  createChannelForm.addEventListener("submit", (event) => {
    console.log("createChannelForm.submit", { event });
    event.preventDefault();
    const channelName = document.querySelector("#channel_name").value;
    console.log({ channelName });
    socket.emit("join_channel", { channelName });
    $("#createChannelModal").modal("hide");
  });
  console.log("setUpCreateChannelForm done");
}

document.addEventListener("DOMContentLoaded", runChat);
