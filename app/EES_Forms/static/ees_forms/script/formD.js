function freeboard_check(truck) {
    const freeboard = document.getElementById('id_freeboard' + truck).value;
    let newID = 'id_wetted' + truck
    const formName = document.getElementById('formName').dataset.form;
    var tempSaveKey = formName+"_tempFormData";
    var currentData = JSON.parse(localStorage.getItem(tempSaveKey)) || { Experation: Date.now(), data: {} };
    if (freeboard == 'Yes') {
        document.getElementById(newID).value = 'N/A';
        currentData.data[newID] = 'N/A';
        console.log("Updated Local Storage to: N/A")
    } else if (freeboard == '') {
        document.getElementById(newID).value = '';
        currentData.data[newID] = '';
        console.log("Updated Local Storage to: ''")
    }
    localStorage.setItem(tempSaveKey, JSON.stringify(currentData));
}
function freeboard(elem) {
    freeboard_check(elem.name.slice(9));
    if_one_then_all();
}
window.onload = function initialDisplay() {
    for (number=1;number<6;number+=1){
        const formTruck = document.getElementById('id_observer'+number).value;
        if(!formTruck){
            changeTab(number);
            break;
        }
    }
}
function changeTab(item){
    for (let i=1; i<=5; i++){
        if (item == i){
            document.getElementById('truck'+ String(i) +'Card').style.display = 'block';
            document.getElementById('tab'+ String(i) +'Cont').style.backgroundColor = '#dfe5e9';
            document.getElementById('tab'+ String(i) +'Cont').style.color = 'black';
        } else {
            document.getElementById('truck'+ String(i) +'Card').style.display = 'none';
            document.getElementById('tab'+ String(i) +'Cont').style.backgroundColor = '#6c7d88';
            document.getElementById('tab'+ String(i) +'Cont').style.color = 'white';
        }
    }
}
function truckFinished(){
    list = [1,2,3,4,5];
    for (let item=0; item < list.length; item++){
        const tNumber = list[item];
        const truck_id = document.getElementById('id_truck_id' + tNumber).value;
        const date = document.getElementById('id_date' + tNumber).value;
        const time = document.getElementById('id_time' + tNumber).value;
        const contents = document.getElementById('id_contents' + tNumber).value;
        const freeboard = document.getElementById('id_freeboard' + tNumber).value;
        const wetted = document.getElementById('id_wetted' + tNumber).value;
        const comments = document.getElementById('id_comments' + tNumber).value;

        if (truck_id && date && time && contents && freeboard && wetted && comments) {
            document.getElementById('tab' + tNumber + 'Cont').style.textDecoration = 'line-through'; 
        }
    }
}
truckFinished();
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
}
if_one_then_all()