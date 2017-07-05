function main() {
  $("#header").click(function() {
    $("#header").hide();
    $("#header").fadeIn(1000);
  });
}

$(document).ready(main);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function() {
    navigator.serviceWorker.register("/sw.js").then(function(registration) {
      console.log("registration was successful with scope: ", registration.scope);
    }, function(err) {
      alert("Service worker registration error: ", err);
    });
  });
}
