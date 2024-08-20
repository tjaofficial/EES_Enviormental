checkDeletePacket = (elem, packID, selector) => {
    const submit = document.getElementById(selector + 'Submit'+String(packID));
    const deletePacket = elem.value;
    console.log(deletePacket)
    console.log(submit)
    if(deletePacket != "delete"){
        submit.disabled = true;
        console.log('true')
    } else {
        submit.disabled = false;
        console.log('false')
    }
}
