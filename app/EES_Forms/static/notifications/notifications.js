const websocketProtocol = window.location.protocol === "https" ? "wss" : "ws";
const facility = JSON.parse(document.getElementById('facility').textContent).replaceAll(" ","_")

let url = `${websocketProtocol}://${window.location.host}/ws/notifications/${facility}/`

const notifSocket = new WebSocket(url)

notifSocket.onmessage = function(event) {
    let messageData = JSON.parse(event.data)
    console.log(messageData)
    // showNotificationFunction(messageData.count)
};

// function showNotificationFunction(notificationHTML) {
//     const notificationsContainer = document.getElementById("alertNotif");
//     notificationsContainer.innerHTML = notificationHTML;
// };

function setNotificationHover(e) {
    elementID = e.children[0]
    elementID.style.backgroundColor = '';
    notifSocket.send(JSON.stringify({
        'notifID': e.id,
        'selector': 'hover'
    }))
    console.log('Hovered Notif')
}
function setNotificationClick(e) {
    notifSocket.send(JSON.stringify({
        'notifID': e.id,
        'selector': 'click'
    }))
    console.log('Clicked Notif')
}

notifSocket.onopen = (event) => {
    console.log("WebSocket connection opened!");
};

notifSocket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};