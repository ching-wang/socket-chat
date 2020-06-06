document.addEventListener("DOMContentLoaded", () => {
  //Connect to websocket
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  //When connected, show the chatting room.
  socket.on("connect", (socket) => {
    console.log("A user conntected!");
  });
});
