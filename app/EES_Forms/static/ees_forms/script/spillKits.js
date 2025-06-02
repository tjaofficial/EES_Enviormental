const spill_kits_group = ['_tag_on', '_serial', '_complete', '_report', '_comment'];
const selector = document.getElementById("selector").dataset.selector;
const totalSK = document.getElementById("total").dataset.total;
function rows_true() {
    for(var i = 0; i < parseInt(totalSK); i++){
        const tag_on = document.getElementById(`id_sk-${i}-tag_on`);
        const serial = document.getElementById(`id_sk-${i}-serial`);
        const complete = document.getElementById(`id_sk-${i}-complete`);
        const report = document.getElementById(`id_sk-${i}-report`);
        const comment = document.getElementById(`id_sk-${i}-comment`);
        
        if (tag_on.value || serial.value || complete.value || report.value || comment.value) {
            tag_on.required = true;
            serial.required = true;
            complete.required = true;
            report.required = true;
            comment.required = true;
        } else {
            tag_on.required = false;
            serial.required = false;
            complete.required = false;
            report.required = false;
            comment.required = false;
        }
    }
}

function showInventorySK(elem) {
    const month = document.getElementById("linkMonth").dataset.month;
    const iList = JSON.parse(document.getElementById('iColor').dataset.inventory);
    const fsID = document.getElementById('fsID').dataset.fsid;
    const form26_fsID = document.getElementById('form26_fsID').dataset.form26fsid;
    if (!elem){
        for(var i=0, x=1; i<parseInt(totalSK); i++, x++) {
            if (selector == "form"){
                console.log(document.getElementById(`id_sk-${i}-tag_on`))
                var tagOn = document.getElementById(`id_sk-${i}-tag_on`).value;
            } else {
                var tagOn = document.getElementById('tagOn'+String(i)).firstChild.nodeValue.trim();
            }
            if (String(tagOn) == "No" && iList[i]) {
                console.log("CHECK 1")
                var linkSel = iList[i][1];
                document.getElementById(`kit${x}`).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${i+1}/${linkSel}'>Complete</a>`
                document.getElementById(`kit${x}`).style.backgroundColor = "green"
                break
            } else if (String(tagOn) == "No") {
                console.log("CHECK 2")
                // if (){
                    
                // }
                console.log(document.getElementById(`kit${x}`))
                document.getElementById(`kit${x}`).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${i+1}/form'>Incomplete</a>`
                document.getElementById(`kit${x}`).style.backgroundColor = "yellow"
                break
            } else {
                console.log("CHECK 3")
                document.getElementById(`kit${x}`).innerHTML = "N/A"
                document.getElementById(`kit${x}`).style.backgroundColor = "white"
                break
            }
        }
    } else {
        const counter = elem.parentNode.id.slice(5);
        const sk_number = elem.id[6];
        if (selector == "form"){
            var tagOn = document.getElementById(`id_sk-${sk_number}-tag_on`).value;
        } else {
            var tagOn = document.getElementById(`tagOn${counter}`).firstChild.nodeValue.trim();
        }
        if (String(tagOn) == "No" && iList[sk_number]) {
            console.log("CHECK 1")
            var linkSel = iList[sk_number][1];
            document.getElementById(`kit${counter}`).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${sk_number}/${linkSel}'>Complete</a>`
            document.getElementById(`kit${counter}`).style.backgroundColor = "green"
        } else if (String(tagOn) == "No") {
            console.log("CHECK 2")
            document.getElementById(`kit${counter}`).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${sk_number}/form'>Incomplete</a>`
            document.getElementById(`kit${counter}`).style.backgroundColor = "yellow"
        } else {
            console.log("CHECK 3")
            document.getElementById(`kit${counter}`).innerHTML = "N/A"
            document.getElementById(`kit${counter}`).style.backgroundColor = "white"
        }
    }
}
showInventorySK(false);
function showInventorySKUT() {
    const month = document.getElementById("linkMonth").dataset.month;
    const iList = JSON.parse(document.getElementById('iColor').dataset.inventory);
    const fsID = document.getElementById('fsID').dataset.fsid;
    const form26_fsID = document.getElementById('form26_fsID').dataset.form26fsid;
    for(var i=22; i<=26; i++) {
        if (selector == "form"){
            var tagOn = document.getElementById('id_skut' + String(i) + '_tag_on').value;
        } else {
            var tagOn = document.getElementById("tagOn" + String(i)).firstChild.nodeValue.trim();
        }
        if(String(tagOn) == "No" && iList[i-1]) {
            var linkSel = iList[i-1][1];
            document.getElementById("kit" + String(i)).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${i+1}/${linkSel}'>Complete</a>`
            document.getElementById("kit" + String(i)).style.backgroundColor = "green"
        } else if (String(tagOn) == "No") {
            document.getElementById("kit" + String(i)).innerHTML = `<a href='../../26/inventory/${form26_fsID}/${month}/${i+1}/form'>Incomplete</a>`
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