document.addEventListener("DOMContentLoaded", () => {

  //Connect to websocket
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  //When connected, show the chatting room.
  socket.on("message-from-client", (msg) => {
    console.log(msg);
  });

  socket.emit("message-from-client", {
    greeting: "Hello from Client",
  });
});
