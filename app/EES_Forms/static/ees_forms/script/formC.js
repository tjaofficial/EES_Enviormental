


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