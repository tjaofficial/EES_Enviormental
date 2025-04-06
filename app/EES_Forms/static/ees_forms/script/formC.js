function zero_option_name(elem, key, name){
    if (elem.value){
        document.getElementById('areaName' + key).name = 'areaName' + key;
    } else {
        document.getElementById('areaName' + key).name = "none" + key;
    }
}

function add_areas(areaNum) {
    const areaCont = document.getElementById("areaCont" + areaNum);
    const areaUsed = document.getElementById(`areaUsed_${areaNum}`);
    areaUsed.value = "true"
    areaCont.style.display = 'block';
    for (let x=1;x<13;x++){
        document.getElementById("id_" + areaNum + 'Read_' + x).required = true;
    }
    document.getElementById("id_" + areaNum + '_start').required = true;
    document.getElementById("id_" + areaNum + '_stop').required = true;
    document.getElementById("id_" + areaNum + '_average').required = true;
    document.getElementById('areaLabel' + areaNum).style.display = 'none';
    var selectElement = document.getElementById("id_" + areaNum + '_selection');
    if (selectElement && selectElement.options.length === 0){
        var hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.id = selectElement.id;
        hiddenInput.name = selectElement.name;
        hiddenInput.value = "";
        hiddenInput.required = true;
        
        selectElement.parentNode.replaceChild(hiddenInput, selectElement)
    }
}

function remove_area(areaNum) {
    const areaCont = document.getElementById("areaCont" + areaNum)
    if (areaCont) {
        const areaUsed = document.getElementById(`areaUsed_${areaNum}`);
        areaUsed.value = "false"
        areaCont.style.display = 'none';
        if (selector == "form"){
            for (let x=1;x<13;x++){
                document.getElementById("id_" + areaNum + 'Read_' + x).required = false;
            }
            document.getElementById("id_" + areaNum + '_start').required = false;
            document.getElementById("id_" + areaNum + '_stop').required = false;
            document.getElementById("id_" + areaNum + '_average').required = false;
            document.getElementById('areaLabel' + areaNum).style.display = 'block';
            document.getElementById("id_" + areaNum + '_selection').required = false;
        }
    }
}

function startupDisplay() {
    const areasFilled = document.getElementById('areasFilled').dataset.areas;
    console.log(areasFilled)
    const areasList = JSON.parse(areasFilled.replaceAll("'",'"'))
    console.log(areasList)
    let theList = []
    for (let x=1; x<=4; x++){
        if (!areasList.includes(String(x))){
            theList.push(x)
        } else {
            var selectElement = document.getElementById("id_" + x + '_selection');
            if (selectElement && selectElement.options.length === 0){
                var hiddenInput = document.createElement("input");
                hiddenInput.type = "hidden";
                hiddenInput.id = selectElement.id;
                hiddenInput.name = selectElement.name;
                hiddenInput.value = "";
                hiddenInput.required = true;
                
                selectElement.parentNode.replaceChild(hiddenInput, selectElement)
            }
        }
    }
    if (theList.length != 0){
        for (let theArea in theList){
            remove_area(theList[theArea]);
        }
    }
}
const pullSelector = document.getElementById('selector').dataset.selector;
const [selector, existing] = pullSelector.split('-');
if (existing){
    startupDisplay();
}


// function display_check() {
//     const area3_start = document.getElementById('areaStartTime3').value;
//     const area4_start = document.getElementById('areaStartTime4').value;
//     const area3_stop = document.getElementById('areaStopTime3').value;
//     const area4_stop = document.getElementById('areaStopTime4').value;
//     console.log(area3_start)
//     console.log(area3_stop)
//     if (area3_start || area3_stop) {
//         add_areas();
//     } else {
//         remove_area();
//     }
//     if (area4_start || area4_stop) {
//         add_salts();
//     } else {
//         remove_salt();
//     }
// }
// display_check();