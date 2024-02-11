checkDeletePacket = (elem, packID) => {
    const submit = document.getElementById('submit'+String(packID));
    const deletePacket = document.getElementById('deletePacket'+String(packID)).value;
    console.log(deletePacket)
    if(deletePacket != "delete"){
        submit.disabled = true;
        console.log('true')
    } else {
        submit.disabled = false;
        console.log('false')
    }
}
