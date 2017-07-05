var ws = new WebSocket("ws://localhost:7000");
function main() {
  ws.onmessage = function(event) {
    if (event.data === "1") {
      $("#direction").html('<p id="direction">Current direction: <br/>Backward</p>');
    } else if (event.data === "0") {
      $("#direction").html('<p id="direction">Current direction: <br/>Forward</p>');
    } else if (event.data === "2") {
      $("#direction").html('<p id="direction">Current direction: <br/>Stopped</p>');
    } else {
      console.log(event.data)
    }
  }
  ws.onclose = function(event) {
    alert("Websocket connection closed");
  }
  ws.onopen = function(event) {}

  $("#forward").on("click", function() {
    ws.send("drive,0");
  });

  $("#stop").on("click", function() {
    ws.send("drive,2");
  });

  $("#backward").on("click", function() {
    ws.send("drive,1");
  });

}

$(document).ready(main)
