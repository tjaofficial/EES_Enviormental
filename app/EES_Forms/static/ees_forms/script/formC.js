function add_areas() {
    const group = document.getElementsByClassName('area_table');
    for (let i=0;i<group.length;i+=1){
        group[i].style.display = 'table-row';
    }
    for (let x=1;x<13;x+=1){
        document.getElementById('storage_' + x).required = true;
    }
    document.getElementById('areaStartTime3').required = true;
    document.getElementById('areaStopTime3').required = true;
    document.getElementById('areaAverage3').required = true;
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
    const area3_start = document.getElementById('areaStartTime3').value;
    const area4_start = document.getElementById('areaStartTime4').value;
    const area3_stop = document.getElementById('areaStopTime3').value;
    const area4_stop = document.getElementById('areaStopTime4').value;
    console.log(area3_start)
    console.log(area3_stop)
    if (area3_start || area3_stop) {
        add_areas();
    } else {
        remove_area();
    }
    if (area4_start || area4_stop) {
        add_salts();
    } else {
        remove_salt();
    }
}
display_check();