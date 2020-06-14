console.log("Starting");

function runChat() {
  console.log("Connecting to socket");
  const socket = io();
  socket.on("connect", function () {
    console.log("Socket connected");
  });

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
