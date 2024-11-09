function zero_option_name(elem, key, name){
    if (elem.value){
        document.getElementById('areaName' + key).name = 'areaName' + key;
    } else {
        document.getElementById('areaName' + key).name = "none" + key;
    }
}

function add_areas(areaNum) {
    const areaCont = document.getElementById("areaCont" + areaNum)
    areaCont.style.display = 'block';
    for (let x=0;x<12;x+=1){
        document.getElementById('area' + areaNum + 'Read' + x).required = true;
    }
    document.getElementById('areaStartTime' + areaNum).required = true;
    document.getElementById('areaStopTime' + areaNum).required = true;
    document.getElementById('areaAverage' + areaNum).required = true;
    document.getElementById('areaLabel' + areaNum).style.display = 'none';
    document.getElementById('areaName' + areaNum).required = true;
}

function remove_area(areaNum) {
    const areaCont = document.getElementById("areaCont" + areaNum)
    areaCont.style.display = 'none';
    for (let x=0;x<12;x+=1){
        document.getElementById('area' + areaNum + 'Read' + x).required = false;
    }
    document.getElementById('areaStartTime' + areaNum).required = false;
    document.getElementById('areaStopTime' + areaNum).required = false;
    document.getElementById('areaAverage' + areaNum).required = false;
    document.getElementById('areaLabel' + areaNum).style.display = 'block';
    document.getElementById('areaName' + areaNum).required = false;
}

function startupDisplay() {
    const areasFilled = document.getElementById('areasFilled').dataset.areas;
    const areasList = JSON.parse(areasFilled.replaceAll("'",'"'))
    let theList = []
    for (let x=1; x<=4; x++){
        if (!areasList.includes(String(x))){
            theList.push(x)
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