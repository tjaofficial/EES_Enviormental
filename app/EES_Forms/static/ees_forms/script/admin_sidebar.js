document.getElementById('sbClient').addEventListener('click',onOFF)

function onOFF() {
    const sbClientList = document.getElementById('sbClientList').style.display;
    console.log(sbClientList)
    if (sbClientList == 'block'){
        document.getElementById('sbClientList').style.display = 'none';
    } else {
        document.getElementById('sbClientList').style.display = 'block';
    }

    
}