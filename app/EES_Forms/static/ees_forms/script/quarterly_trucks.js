window.onload = function initialDisplay() {
    let list = [[1,5],[2,6],[3,7],[4,9]];
    for (number in list){
        const formTruck = document.getElementById('id_observer_' + list[number][1] + '_' + list[number][0]).value;
        console.log(list[number])
        if(!formTruck){
            if (number == 0) {
                changeTab1()
            } else if (number == 1) {
                changeTab2()
            } else if (number == 2) {
                changeTab3()
            } else if (number == 3) {
                changeTab4()
            } else if (number == 4) {
                changeTab5()
            }
            break;
        }
    }
}

document.getElementById("tab1Cont").addEventListener("click", changeTab1);
document.getElementById("tab2Cont").addEventListener("click", changeTab2);
document.getElementById("tab3Cont").addEventListener("click", changeTab3);
document.getElementById("tab4Cont").addEventListener("click", changeTab4);

function changeTab1() {
    document.getElementById('truck1Card').style.display = 'block';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';

    document.getElementById('tab1Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab1Cont').style.color = 'black';

    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
}
function changeTab2() {
    document.getElementById('truck2Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';
    document.getElementById('tab2Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab2Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
}
function changeTab3() {
    document.getElementById('truck3Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck4Card').style.display = 'none';

    document.getElementById('tab3Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab3Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab4Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab4Cont').style.color = 'white';
}
function changeTab4() {
    document.getElementById('truck4Card').style.display = 'block';
    document.getElementById('truck1Card').style.display = 'none';
    document.getElementById('truck2Card').style.display = 'none';
    document.getElementById('truck3Card').style.display = 'none';

    document.getElementById('tab4Cont').style.backgroundColor = '#dfe5e9';
    document.getElementById('tab4Cont').style.color = 'black';
    
    document.getElementById('tab1Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab3Cont').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1Cont').style.color = 'white';
    document.getElementById('tab2Cont').style.color = 'white';
    document.getElementById('tab3Cont').style.color = 'white';
}

function truckFinished(){
    let list = [[1,5],[2,6],[3,7],[4,9]];
    for (let item=0; item < list.length; item++){
        const tNumber = list[item];
        const observer = document.getElementById('id_observer_'+ tNumber[1] + '_' + tNumber[0]).value;
        const date = document.getElementById('id_date_'+ tNumber[1] + '_' + tNumber[0]).value;
        const time = document.getElementById('id_time_'+ tNumber[1] + '_' + tNumber[0]).value;
        const rearGate = document.getElementById('id_rear_gate_'+ tNumber[1] + '_' + tNumber[0]).value;
        const boxInt = document.getElementById('id_box_interior_'+ tNumber[1] + '_' + tNumber[0]).value;
        const boxExt = document.getElementById('id_box_exterior_'+ tNumber[1] + '_' + tNumber[0]).value;
        const exhaust = document.getElementById('id_exhaust_'+ tNumber[1] + '_' + tNumber[0]).value;
        const comments = document.getElementById('id_comments_'+ tNumber[1] + '_' + tNumber[0]).value;

        if (observer && date && time && rearGate && boxInt && boxExt && exhaust) {
            document.getElementById('tab' + tNumber[0] + 'Cont').style.textDecoration = 'line-through'; 
        }
    }
}
truckFinished();

function if_one_then_all(){
    let list = [[1,5],[2,6],[3,7],[4,9]];
    const input_group = ['observer', 'date', 'time', 'rear_gate', 'box_interior', 'box_exterior', 'exhaust', 'comments'];
    for (pair in list) {
        var pass = false;
        for (item in input_group) {
            const input = input_group[item];
            console.log('id_' + input + '_' + String(list[pair][1]) + '_' + String(list[pair][0]))
            const input_check = document.getElementById('id_' + input + '_' + String(list[pair][1]) + '_' + String(list[pair][0])).value;
            if (input_check) {
                pass = true;
                
            }
        }
        if (pass) {
            document.getElementById('id_observer_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_date_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_time_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_rear_gate_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_box_interior_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_box_exterior_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_exhaust_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
            document.getElementById('id_comments_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = true;
        } else {
            document.getElementById('id_observer_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_date_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_time_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_rear_gate_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_box_interior_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_box_exterior_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_exhaust_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
            document.getElementById('id_comments_' + String(list[pair][1]) + '_' + String(list[pair][0])).required = false;
        }
    } 
}
if_one_then_all()