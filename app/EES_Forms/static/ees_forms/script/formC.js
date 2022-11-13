
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

function add_areas() {
    const group = document.getElementsByClassName('area_table');
    for (let i=0;i<group.length;i+=1){
        group[i].style.display = 'table-row';
    }
    for (let x=1;x<13;x+=1){
        document.getElementById('storage_' + x).required = true;
    }
    document.getElementById('id_sto_start_time').required = true;
    document.getElementById('id_sto_stop_time').required = true;
    document.getElementById('average_storage').required = true;
    document.getElementById('areaLabel').style.visibility = 'hidden';
}
function add_salts() {
    const group = document.getElementsByClassName('salt_table');
    for (let i=0;i<group.length;i+=1){
        group[i].style.display = 'table-row';
    }
    for (let x=1;x<13;x+=1){
        document.getElementById('salt_' + x).required = true;
    }
    document.getElementById('id_salt_start_time').required = true;
    document.getElementById('id_salt_stop_time').required = true;
    document.getElementById('average_salt').required = true;
    document.getElementById('saltLabel').style.visibility = 'hidden';
}

function remove_area() {
    const group = document.getElementsByClassName('area_table');
    for (let i=0;i<group.length;i+=1){
        group[i].style.display = 'none';
    }
    for (let x=1;x<13;x+=1){
        document.getElementById('storage_' + x).required = false;
    }
    document.getElementById('id_sto_start_time').required = false;
    document.getElementById('id_sto_stop_time').required = false;
    document.getElementById('average_storage').required = false;
    document.getElementById('areaLabel').style.visibility = 'visible';
    document.getElementById('id_sto_start_time').value = null;
}
function remove_salt() {
    const group = document.getElementsByClassName('salt_table');
    for (let i=0;i<group.length;i+=1){
        group[i].style.display = 'none';
    }
    for (let x=1;x<13;x+=1){
        document.getElementById('salt_' + x).required = false;
    }
    document.getElementById('id_salt_start_time').required = false;
    document.getElementById('id_salt_stop_time').required = false;
    document.getElementById('average_salt').required = false;
    document.getElementById('saltLabel').style.visibility = 'visible';
    document.getElementById('id_salt_start_time').value = null;
}

function display_check() {
    const storage_start = document.getElementById('id_sto_start_time').value;
    const salt_start = document.getElementById('id_salt_start_time').value;
    const storage_stop = document.getElementById('id_sto_stop_time').value;
    const salt_stop = document.getElementById('id_salt_stop_time').value;

    if (storage_start || storage_stop) {
        add_areas();
    }
    if (salt_start || salt_stop) {
        add_salts();
    }
}
display_check();