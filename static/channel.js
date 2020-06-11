document.addEventListener("DOMContentLoaded", () => {
  var channelName = document.getElementById("channel_name_header").dataset
    .channelName;

  console.log("connecting with socket.io");
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );
  socket.on("connect", () => {
    console.log("socket.io connected");
    console.log("joining", channelName);
    socket.emit("join_channel", channelName);
    console.log("joined", channelName);
  });
});
