function truck_average() {
    list = [1,2,3,4,5,6,7,8,9,10,11,12]
    var truck_total = 0;
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const truck_opac  = document.getElementById('TRead' + opacities).value;
        truck_total += parseInt(truck_opac);
    }
    const truckAverage = (truck_total / 12).toFixed(3);
    document.getElementById('average_t').placeholder = truckAverage;
    const id_param = document.getElementById('average_t').id;
    stop_light(truckAverage, id_param);
}

function area_average() {
    list = [1,2,3,4,5,6,7,8,9,10,11,12]
    var area_total = 0;
    for (let i=0; i < list.length; i++){
        const opacities = list[i];
        const area_opac  = document.getElementById('ARead' + opacities).value;
        area_total += parseInt(area_opac);
    }
    const areaAverage = (area_total / 12).toFixed(3);
    document.getElementById('average_p').placeholder = areaAverage;
    const id_param = document.getElementById('average_p').id;
    stop_light(areaAverage, id_param);
}

function stop_light(average, id_param) {
    const inputAverage = document.getElementById(id_param).value;
    if (inputAverage) {
        if (parseFloat(inputAverage) == parseFloat(average)) {
            document.getElementById(id_param).style.backgroundColor = '#3c983c85';
        } else {
            document.getElementById(id_param).style.backgroundColor = '#F49B9B';
        }
    } else {
        document.getElementById(id_param).style.backgroundColor = '#FFFA8B';
    }
}

function timecheck_1() {
    "use strict";
    const start1 = document.getElementById('truck_start_time').value,
          end1 = document.getElementById('truck_stop_time').value;

    if (end1 == false) {
        
    }
    else if (start1 > end1) {
        var popup = document.getElementById("truck_popup").style.visibility = 'visible';
        document.getElementById("truck_start_time").style.backgroundColor = "#ffffff";
        document.getElementById("truck_stop_time").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("truck_popup").style.visibility = 'hidden';
        document.getElementById("truck_start_time").style.backgroundColor = "#3c983c85";
        document.getElementById("truck_stop_time").style.backgroundColor = "#3c983c85";
    }
}
function timecheck_2() {
    "use strict";
    const start1 = document.getElementById('area_start_time').value,
          end1 = document.getElementById('area_stop_time').value;

    if (end1 == false) {
        
    }
    else if (start1 > end1) {
        var popup = document.getElementById("area_popup").style.visibility = 'visible';
        document.getElementById("area_start_time").style.backgroundColor = "#ffffff";
        document.getElementById("area_stop_time").style.backgroundColor = "#ffffff";
    }
    else{
        var popup = document.getElementById("area_popup").style.visibility = 'hidden';
        document.getElementById("area_start_time").style.backgroundColor = "#3c983c85";
        document.getElementById("area_stop_time").style.backgroundColor = "#3c983c85";
    }
}