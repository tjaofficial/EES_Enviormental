const packetID = localStorage.obs_dashboard
const fsData = JSON.parse(document.getElementById('fsData').dataset.data.replaceAll("'", '"'));
const fsID = document.getElementById('fsID').dataset.data
for (let key in fsData) {
    if (fsData.hasOwnProperty(packetID)) {
        document.getElementById('formCustomName').innerHTML = fsData[packetID].replace(' ', '');
        console.log(fsData[packetID])
    } else {
        document.getElementById('formCustomName').innerHTML = fsID;
    }
  }