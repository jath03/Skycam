var ws = new WebSocket("ws://192.168.5.14:7000");
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
var keydown = false
$(document).keydown(function(event){
  console.log(event.which);
  if (!keydown) {
    keydown = true
    switch (event.which) {
      case 40:
        console.log("arrow down event");
        ws.send("tilt,1");
        break;
      case 38:
        console.log("arrow up event");
        ws.send("tilt,0");
        break;
      case 39:
        console.log("arrow right event");
        ws.send("pan,0");
        break;
      case 37:
        console.log("arrow Left event");
        ws.send("pan,1");
        break;
      case 87:
        console.log("w event");
        ws.send("drive,0");
      case 83:
        console.log("s event");
        ws.send("drive,1");
      case 32:
        ws.send("drive,2");
      default:
        return;
    }
  }
  event.preventDefault();
});

$(document).keyup(function (event) {
  keydown = false
})
