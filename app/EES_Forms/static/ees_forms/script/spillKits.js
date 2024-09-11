const spill_kits_group = ['_tag_on', '_serial', '_complete', '_report', '_comment'];
const selector = document.getElementById("selector").dataset.selector;
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
    const iList = JSON.parse(document.getElementById('iColor').dataset.inventory);
    const fsID = document.getElementById('fsID').dataset.fsid;
    for(var i=1; i<=21; i++) {
        if (selector == "form"){
            var tagOn = document.getElementById('id_sk' + String(i) + '_tag_on').value;
        } else {
            var tagOn = document.getElementById('tagOn'+String(i)).firstChild.nodeValue.trim();
        }
        if (String(tagOn) == "No" && iList[i]) {
            console.log("CHECK 1")
            var linkSel = iList[i][1];
            console.log(linkSel)
            document.getElementById("kit" + String(i)).innerHTML = "<a href='../../26/inventory/"+ fsID +"/"+month+"/"+String(i)+"/"+linkSel+"'>Complete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "green"
        } else if (String(tagOn) == "No") {
            console.log("CHECK 2")
            document.getElementById("kit" + String(i)).innerHTML = "<a href='../../26/inventory/"+ fsID +"/"+month+"/"+String(i)+"/form'>Incomplete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "yellow"
        } else {
            console.log("CHECK 3")
            document.getElementById("kit" + String(i)).innerHTML = "N/A"
            document.getElementById("kit" + String(i)).style.backgroundColor = "white"
        }
    }
}
showInventorySK();
function showInventorySKUT() {
    const month = document.getElementById("linkMonth").dataset.month;
    const iList = JSON.parse(document.getElementById('iColor').dataset.inventory);
    const fsID = document.getElementById('fsID').dataset.fsid;
    for(var i=22; i<=26; i++) {
        if (selector == "form"){
            var tagOn = document.getElementById('id_skut' + String(i) + '_tag_on').value;
        } else {
            var tagOn = document.getElementById("tagOn" + String(i)).firstChild.nodeValue.trim();
        }
        if(String(tagOn) == "No" && iList[i-1]) {
            var linkSel = iList[i-1][1];
            document.getElementById("kit" + String(i)).innerHTML = "<a href='../../26/inventory/"+ fsID +"/"+month+"/"+String(i+1)+"/"+linkSel+"'>Complete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "green"
        } else if (String(tagOn) == "No") {
            document.getElementById("kit" + String(i)).innerHTML = "<a href='../../26/inventory/"+ fsID +"/"+month+"/"+String(i+1)+"/form'>Incomplete</a>"
            document.getElementById("kit" + String(i)).style.backgroundColor = "yellow"
        } else {
            console.log("CHECK 3")
            document.getElementById("kit" + String(i)).innerHTML = "N/A"
            document.getElementById("kit" + String(i)).style.backgroundColor = "white"
        }
    }
}
showInventorySKUT();

// function iChangeColor() {
//     const month = document.getElementById("linkMonth").dataset.month;
//     const iList = JSON.parse(document.getElementById('iColor').dataset.inventory);

//     console.log(iList)
//     for(var i=1; i<=26; i++) {
//         if (iList[i]) {
//             let skID = iList[i][0];
//             if (selector == "form"){
//                 var linkSel = "form";
//             } else {
//                 var linkSel = iList[i][1];
//             }
//             if (skID == i) {
//                 console.log("CHECK 4")
//                 document.getElementById("kit" + String(i)).innerHTML = "<a href='./"+month+"/"+String(i)+"/"+linkSel+"'>Completed</a>"
//                 document.getElementById("kit" + String(i)).style.backgroundColor = "green"
//             }
//         }
//     }

// }
// iChangeColor();