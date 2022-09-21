function freeboard_check(truck) {
    const freeboard = document.getElementById('id_freeboard' + truck).value;
    if (freeboard == 'Yes') {
        document.getElementById('id_wetted' + truck).value = 'N/A';
    } else if (freeboard == '') {
        document.getElementById('id_wetted' + truck).value = '';
    }
}
function freeboard_1() {
    freeboard_check(1);
    if_one_then_all();
}
function freeboard_2() {
    freeboard_check(2);
    if_one_then_all();
}
function freeboard_3() {
    freeboard_check(3);
    if_one_then_all();
}
function freeboard_4() {
    freeboard_check(4);
    if_one_then_all();
}
function freeboard_5() {
    freeboard_check(5);
    if_one_then_all();
}

function if_one_then_all(){
    const input_group = ['observer', 'truck_id', 'date', 'time', 'contents', 'freeboard', 'wetted', 'comments'];
    for (let i=1; i < 6; i++) {
        var pass = false;
        for (item in input_group) {
            const input = input_group[item];
            const input_check = document.getElementById('id_' + input + String(i)).value;
            if (input_check) {
                pass = true;
                
            }
        }
        if (pass) {
            document.getElementById('id_observer' + String(i)).required = true;
            document.getElementById('id_truck_id' + String(i)).required = true;
            document.getElementById('id_date' + String(i)).required = true;
            document.getElementById('id_time' + String(i)).required = true;
            document.getElementById('id_contents' + String(i)).required = true;
            document.getElementById('id_freeboard' + String(i)).required = true;
            document.getElementById('id_wetted' + String(i)).required = true;
            document.getElementById('id_comments' + String(i)).required = true;
        } else {
            document.getElementById('id_observer' + String(i)).required = false;
            document.getElementById('id_truck_id' + String(i)).required = false;
            document.getElementById('id_date' + String(i)).required = false;
            document.getElementById('id_time' + String(i)).required = false;
            document.getElementById('id_contents' + String(i)).required = false;
            document.getElementById('id_freeboard' + String(i)).required = false;
            document.getElementById('id_wetted' + String(i)).required = false;
            document.getElementById('id_comments' + String(i)).required = false;
        }
    } 
    console.log(document.getElementById('id_time3').required)
}

if_one_then_all()