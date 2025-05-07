const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const facility = JSON.parse(document.getElementById('facility').textContent).replaceAll(" ","_")
const notifSettings = JSON.parse(document.getElementById('notifSettings').textContent);
let url = `${websocketProtocol}://${window.location.host}/ws/notifications/`

const notifSocket = new WebSocket(url)

notifSocket.onmessage = function(event) {
    let messageData = JSON.parse(event.data)
    console.log(messageData);
    let facilityID = messageData['facID'];
    let notif_type = messageData['notif_type'];
    const notifCheck = notifSettings[facilityID]['notifications'][notif_type]['methodplus'];
    
    if (!notifCheck) return;
    
    if (messageData.type === 'notification') {
        if (messageData.html) {
            appendNotificationToDropdown(messageData.html, facilityID);
        }
        fetch('/ajax/notification-count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById("alertNotif");
                if (badge) {
                    badge.innerHTML = data.count;
                    badge.style.display = data.count > 0 ? "block" : "none";
                }
            })
            .catch(err => {
                console.error("Error fetching updated notif count", err);
            });
    }
};

function appendNotificationToDropdown(notifHTML, facilityID) {
    const dropdown = document.getElementById(`facilityID_${facilityID}`);
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = notifHTML.trim();

    const newNotif = tempDiv.firstElementChild;

    const noNotifElement = Array.from(dropdown.children).find(child =>
        child.textContent.includes("No Notifications")
    );

    if (noNotifElement) {
        noNotifElement.remove();
    }
    dropdown.parentNode.insertBefore(newNotif, dropdown.nextSibling);
}

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