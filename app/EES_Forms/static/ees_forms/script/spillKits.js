const spill_kits_group = ['_tag_on', '_serial', '_complete', '_report', '_comment'];
function rows_true() {
    for(var i = 1; i <= 21; i++){
        const tag_on = document.getElementById('id_sk' + i + '_tag_on').value;
        const serial = document.getElementById('id_sk' + i + '_serial').value;
        const complete = document.getElementById('id_sk' + i + '_complete').value;
        const report = document.getElementById('id_sk' + i + '_report').value;
        const comment = document.getElementById('id_sk' + i + '_comment').value;
        
        if (tag_on || serial || complete || report || comment) {
            document.getElementById('id_sk' + i + '_tag_on').required = true;
            document.getElementById('id_sk' + i + '_serial').required = true;
            document.getElementById('id_sk' + i + '_complete').required = true;
            document.getElementById('id_sk' + i + '_report').required = true;
            document.getElementById('id_sk' + i + '_comment').required = true;
        } else {
            document.getElementById('id_sk' + i + '_tag_on').required = false;
            document.getElementById('id_sk' + i + '_serial').required = false;
            document.getElementById('id_sk' + i + '_complete').required = false;
            document.getElementById('id_sk' + i + '_report').required = false;
            document.getElementById('id_sk' + i + '_comment').required = false;
        }
    }
}

function showInventorySK() {
    const month = document.getElementById("linkMonth").dataset.month;
    for(var i=1; i<=21; i++) {
        const tagOn = document.getElementById('id_sk' + String(i) + '_tag_on').value;
        if(tagOn == "No") {
            document.getElementById("kit" + String(i)).innerHTML = "<a href='./"+month+"/"+String(i)+"/form'>Incomplete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "yellow"
        } else {
            document.getElementById("kit" + String(i)).innerHTML = "N/A"
            document.getElementById("kit" + String(i)).style.backgroundColor = "white"
        }
    }
}
showInventorySK();
function showInventorySKUT() {
    const month = document.getElementById("linkMonth").dataset.month;
    for(var i=22; i<=26; i++) {
        const tagOn = document.getElementById('id_skut' + String(i) + '_tag_on').value;
        if(tagOn == "No") {
            document.getElementById("kit" + String(i)).innerHTML = "<a href='./"+month+"/"+String(i)+"/form'>Incomplete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "yellow"
        } else {
            document.getElementById("kit" + String(i)).innerHTML = "N/A"
            document.getElementById("kit" + String(i)).style.backgroundColor = "white"
        }
    }
}
showInventorySKUT();

function iChangeColor() {
    const month = document.getElementById("linkMonth").dataset.month;
    const iList = document.getElementById('iColor').dataset.inventory;
    for(var i=1; i<=21; i++) {
        for(var q=0; q<iList.length; q++){
            let skID = iList[q];
                if (skID == i) {
                    document.getElementById("kit" + String(i)).innerHTML = "<a href='./"+month+"/"+String(i)+"/form'>Completed</a>"
                    document.getElementById("kit" + String(i)).style.backgroundColor = "green"
                }

        }
    }
}
iChangeColor();