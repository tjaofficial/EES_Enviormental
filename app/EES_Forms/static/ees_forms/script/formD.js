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


document.getElementById("tab1Cont").addEventListener("click", changeTab1);
document.getElementById("tab2Cont").addEventListener("click", changeTab2);
document.getElementById("tab3Cont").addEventListener("click", changeTab3);
document.getElementById("tab4Cont").addEventListener("click", changeTab4);
document.getElementById("tab5Cont").addEventListener("click", changeTab5);

function changeTab1() {
    document.getElementById('truck1Card').style.display = 'block';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';
    document.getElementById('truck5Card').style.display = 'none';

    document.getElementById('tab1Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab1Cont').style.color = 'black';

    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab5Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
    document.getElementById('tab5Cont').style.color = 'white';
}
function changeTab2() {
    document.getElementById('truck2Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';
    document.getElementById('truck5Card').style.display = 'none';

    document.getElementById('tab2Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab2Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab5Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
    document.getElementById('tab5Cont').style.color = 'white';
}
function changeTab3() {
    document.getElementById('truck3Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';
    document.getElementById('truck5Card').style.display = 'none';

    document.getElementById('tab3Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab3Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab5Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
    document.getElementById('tab5Cont').style.color = 'white';
}
function changeTab4() {
    document.getElementById('truck4Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck5Card').style.display = 'none';

    document.getElementById('tab4Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab4Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab5Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab5Cont').style.color = 'white';
}
function changeTab5() {
    document.getElementById('truck5Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';

    document.getElementById('tab5Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab5Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
}