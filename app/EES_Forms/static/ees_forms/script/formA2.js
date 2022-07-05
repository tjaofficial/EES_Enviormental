// Get Required Input Fields

/*
function updateCalcs() {
    // Push Side

    const pushSide_startTime_value  = document.getElementById('pushSide_startTime').value;
    const pushSide_endTime_value = document.getElementById('pushSide_endTime').value;
    const pushSide_tempBlocked_min_value = document.getElementById('pushSide_tempBlocked_min').value;
    const pushSide_tempBlocked_max_value = document.getElementById('pushSide_tempBlocked_max').value;
    const pushSide_traverseTime_value_min = document.getElementById('pushSide_traverseTime_min').value;
    const pushSide_traverseTime_value_second = document.getElementById('pushSide_traverseTime_second').value;
    
    pushSide_startTime_array = getTimeArray(pushSide_startTime_value);
    pushSide_endTime_array = getTimeArray(pushSide_endTime_value);

    pushSide_timeDelta = timeDelta(pushSide_startTime_array, pushSide_endTime_array);
    
    
    document.getElementById('pushSide_traverseTime_min').value = pushSide_timeDelta[1];
    document.getElementById('pushSide_traverseTime_second').value = pushSide_timeDelta[2];

    // coke Side

    const cokeSide_startTime_value  = document.getElementById('cokeSide_startTime').value;
    const cokeSide_endTime_value = document.getElementById('cokeSide_endTime').value;
    //const cokeSide_tempBlocked_min_value = document.getElementById('cokeSide_tempBlocked_min').value;
    //const cokeSide_tempBlocked_max_value = document.getElementById('cokeSide_tempBlocked_max').value;
    const cokeSide_traverseTime_value_min = document.getElementById('cokeSide_traverseTime_min').value;
    const cokeSide_traverseTime_value_second = document.getElementById('cokeSide_traverseTime_second').value;
    
    cokeSide_startTime_array = getTimeArray(cokeSide_startTime_value);
    cokeSide_endTime_array = getTimeArray(cokeSide_endTime_value);

    cokeSide_timeDelta = timeDelta(cokeSide_startTime_array, cokeSide_endTime_array);
    
    
    document.getElementById('cokeSide_traverseTime_min').value = cokeSide_timeDelta[1];
    document.getElementById('cokeSide_traverseTime_second').value = cokeSide_timeDelta[2];
    
    //Total Traverse Time
    traverseTime_total = 60*(pushSide_timeDelta[1]+cokeSide_timeDelta[1])+pushSide_timeDelta[2]+cokeSide_timeDelta[2];
    document.getElementById('total_traverseTime').value = traverseTime_total;
}


// takes a time string 'hh:mm:ss' and returns a int array [hh, mm, ss]
const getTimeArray = (timeString) => {
    let timeArray = timeString.split(":");
    let intTimeArray = [parseInt(timeArray[0]),parseInt(timeArray[1]),parseInt(timeArray[2])];
    return intTimeArray;
}

// takes a 2 int arrays (mil time) [hh, mm, ss] and returns the time difference in a int array [hh, mm, sss]
const timeDelta = (startTimeArray,endTimeArray) => {
    let hourDelta = endTimeArray[0] - startTimeArray[0];
    let minuteDelta = endTimeArray[1] - startTimeArray[1];
    let secondDelta = endTimeArray[2] - startTimeArray[2];
    
    if (secondDelta < 0){
        minuteDelta--;
        secondDelta = 60-Math.abs(secondDelta);
    }
    
    if (minuteDelta < 0){
        hourDelta--;
        minuteDelta = 60-Math.abs(minuteDelta);
    }

    if(hourDelta < 0){
        prevDayTimeDelta = 24 - startTimeArray[0];
        currentDayTimeDelta = endTimeArray[0];
        hourDelta = prevDayTimeDelta + currentDayTimeDelta;
        // 3 - 16 = -13
    }

    
    
    

    

    deltaArray = [hourDelta, minuteDelta, secondDelta];
    return deltaArray;    
    
}
*/

/*****************************************
Adding Rows to Table
*****************************************/

function initate_Result_Table(){
    const query_Tables = document.querySelectorAll("[data-resulttable]");
    const result_Table_DOM_Array = Array.from(query_Tables)
    result_Table_DOM_Array.forEach((elem)=>{
        let parsedJSON = JSON.parse(elem.value)
        createHTMLString(parsedJSON, elem.id);
        intiateResultEventListeners();
    })
}


// Takes array of Objects and builds the string of HTML
function createHTMLString(dataJSON, input_ID){
    //console.log(`${JSON.stringify(dataJSON)} - ${input_ID}`);    
    let tableHTML = "";

    if(dataJSON.data){
        const dataArray = dataJSON.data;
        if(dataArray.length > 0){
            for(i=0; i<dataArray.length; i++){
                let data = dataArray[i];
                tableHTML = tableHTML+htmlLayout(false, data, input_ID);
            }
        }
    }

    //adds empty row at end of table
    tableHTML = tableHTML+htmlLayout(true, {}, input_ID);

    document.getElementById(`${input_ID}_ctableBody`).innerHTML = tableHTML;
    


}


function intiateResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");
    for(i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('input', handle_Table_Input)
        resultElement[i].addEventListener('input', update_Temp_Save)
        resultElement[i].addEventListener('input', total_leaking_doors)
        resultElement[i].addEventListener('input', allowed_time)


        // resultElement[i].addEventListener('input',(event)=>{
        //     let elem = event.target;
            
        //     handle_Table_Input(elem);
        //     //update_Temp_Save();
            
        // })
        
    }
}


function handle_Table_Input(event){
    const elem = event.target;
    let resultInputAttr = elem.dataset.resultinput;
    const resultKeyAttr = elem.dataset.resultkey;
    const elemValue = elem.value; 
    const input_Target = elem.dataset.targetinput;

    if(parseInt(resultInputAttr) === -1){
        addToResultArray(input_Target, resultKeyAttr, elemValue);
    }
    else{
        updateResultArray(input_Target, resultInputAttr, resultKeyAttr, elemValue);
    }
}

function addToResultArray(target, key, value){

    const targeted_input_DOM = document.getElementById(target);
    const parsed_Result = JSON.parse(targeted_input_DOM.value);
    
    let new_Object = {};
    new_Object[key] = value;
    const result_Array = parsed_Result.data ? parsed_Result.data : [];

    result_Array.push(new_Object);
    parsed_Result.data = result_Array;
    
    targeted_input_DOM.value = JSON.stringify(parsed_Result);
    createHTMLString(parsed_Result, target);
    intiateResultEventListeners();

}

function updateResultArray(target, array_Position, key, value){

    const targeted_input_DOM = document.getElementById(target);
    const parsed_Result = JSON.parse(targeted_input_DOM.value);
    const result_Array = parsed_Result.data;
    if(result_Array[array_Position]){
        let changed_Object = result_Array[array_Position];
        if(value){
            changed_Object[key] = value;
        }
        else{
            delete changed_Object[key];
        }

        if (Object.keys(changed_Object).length === 0 && changed_Object.constructor === Object){
            result_Array.splice(array_Position,1);
        }
        else{result_Array[array_Position] = changed_Object;}
        
        parsed_Result.data = result_Array;
    
        targeted_input_DOM.value = JSON.stringify(parsed_Result);
        createHTMLString(parsed_Result, target);
        intiateResultEventListeners();
    }
    
    

    

}

//createHTMLString(pushResultDataJSON);




// Takes objects whether should be empty and data to return string of html
// Template for Table Rows
function htmlLayout(empty, data, target){

    const htmlStr= `<tr>
                        <td class="boxa6" colspan="1">
                            <input type="number" ${!empty? 'value="'+data.oven+'"': ''} data-resultInput="${empty? -1: i}" data-resultKey="oven" data-targetinput="${target}"/>
                        </td>
                        <td class="boxa6" colspan="1">
                            <select data-resultInput="${empty? -1: i}" data-resultKey="location" data-targetinput="${target}">
                                <option value="" ${empty? 'selected': ''}>--</option>
                                <option value="D" ${!empty && data.location === "D"? 'selected': ''}>D</option>
                                <option value="C" ${!empty && data.location === "C"? 'selected': ''}>C</option>
                                <option value="M" ${!empty && data.location === "M"? 'selected': ''}>M</option>
                            </select>
                        </td>
                        <td class="boxa6" colspan="1">
                            <select data-resultInput="${empty? -1: i}" data-resultKey="zone" data-targetinput="${target}">
                                <option value="" ${empty? 'selected': ''}>--</option>
                                <option value="1" ${!empty && data.zone === "1"? 'selected': ''}>1</option>
                                <option value="2" ${!empty && data.zone === "2"? 'selected': ''}>2</option>
                                <option value="3" ${!empty && data.zone === "3"? 'selected': ''}>3</option>
                                <option value="4" ${!empty && data.zone === "4"? 'selected': ''}>4</option>
                                <option value="5" ${!empty && data.zone === "5"? 'selected': ''}>5</option>
                                <option value="6" ${!empty && data.zone === "6"? 'selected': ''}>6</option>
                                <option value="7" ${!empty && data.zone === "7"? 'selected': ''}>7</option>
                                <option value="8" ${!empty && data.zone === "8"? 'selected': ''}>8</option>
                            </select>
                        </td>
                    </tr>`;
    return htmlStr;



}

function update_Temp_Save(){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;
    target_Input_Field_Id = elem.dataset.targetinput;


    formTempData.data[target_Input_Field_Id] = document.getElementById(target_Input_Field_Id).value;


    localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
}

initate_Result_Table()



function timecheck_pushDoors() {
    
    
    const start = document.getElementById('p_start').value,
          end = document.getElementById('p_stop').value;

    if (end == false) {
        var popup = document.getElementById("pushTime_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("pushTime_popup").style.visibility = 'visible';
        document.getElementById("p_start").style.backgroundColor = "white";
        document.getElementById("p_stop").style.backgroundColor = "white";
    }
    else{
        var popup = document.getElementById("pushTime_popup").style.visibility = 'hidden';
        document.getElementById("p_start").style.backgroundColor = "#3c983c85";
        document.getElementById("p_stop").style.backgroundColor = "#3c983c85";
    }
}

function timecheck_cokeDoors() {
    
    
    const start = document.getElementById('c_start').value,
          end = document.getElementById('c_stop').value;

    if (end == false) {
        var popup = document.getElementById("cokeTime_popup").style.visibility = 'hidden';
    }
    else if (start >= end) {
        document.getElementById("cokeTime_popup").style.visibility = 'visible';
        document.getElementById("c_start").style.backgroundColor = "white";
        document.getElementById("c_stop").style.backgroundColor = "white";
    }
    else{
        var popup = document.getElementById("cokeTime_popup").style.visibility = 'hidden';
        document.getElementById("c_start").style.backgroundColor = "#3c983c85";
        document.getElementById("c_stop").style.backgroundColor = "#3c983c85";
    }
}

//Get total of doors not observed
function pc_doors_not_observed() {
    const push_from = document.getElementById('p_temp_block_from').value,
          push_to = document.getElementById('p_temp_block_to').value,
          coke_from = document.getElementById('c_temp_block_from').value,
          coke_to = document.getElementById('c_temp_block_to').value,
          inop_numbs = document.getElementById('inop_numbs').value;
    
    //Gets an array of all inoperable doors
    let remove_spaces = inop_numbs.split(' ').join(""),
    select_numbers = remove_spaces.split(',');

    //Push Side - Checks if the inoperable oven are listed in the total not observed doors and then subtracts those doors, if any
    if (parseInt(push_from) || parseInt(push_to) >= 0) {
        let push_blocked = Math.abs(parseInt(push_from) - parseInt(push_to)) +1,
        x = 0;
        // push side check and subtract
        if(parseInt(push_from) < parseInt(push_to)){
            for(o=parseInt(push_from); o<=parseInt(push_to); o++){
                for(i=0; i<select_numbers.length; i++){
                    console.log("Comparing Ovens " + o + " AND Ovens " + select_numbers[i])
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                        console.log("Push Side has " + x + " Oven(s) the same.")
                    }
                }
            }
        }
        else {
            for(o=parseInt(push_to); o<=parseInt(push_from); o++){
                for(i=0; i<select_numbers.length; i++){
                    console.log("Comparing Ovens " + o + " AND Ovens " + select_numbers[i])
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                        console.log("Push Side has " + x + " Oven(s) the same.")
                    }
                }
            }
        }
        var push_block_total = parseInt(push_blocked) - parseInt(x);
    }
    else {
        var push_block_total = 0;
    }
// coke side check and subtract
    if (parseInt(coke_from) || parseInt(coke_to) >= 0) {
        let coke_blocked = Math.abs(parseInt(coke_from) - parseInt(coke_to)) +1,
        y = 0;
        

        if(parseInt(coke_from) < parseInt(coke_to)){
            for(i=parseInt(coke_from); i<=parseInt(coke_to); i++){
                if(parseInt(i) === parseInt(inop_numbs)){
                    y += 1;
                }
            }
        }
        else {
            for(i=parseInt(coke_to); i<=parseInt(coke_from); i++){
                if(parseInt(i) === parseInt(inop_numbs)){
                    y += 1;
                }
            }
        }
        var coke_block_total = parseInt(coke_blocked) - parseInt(y);
    }
    else {
        var coke_block_total = 0;
    }
//add both sides together to get the total not observed
    const not_observed = parseInt(push_block_total) + parseInt(coke_block_total);
    
    document.getElementById('doors_not_observed').value = not_observed;
    
}

function inoperable_ovens() {
    const inop = document.getElementById('inop_ovens').value;
    
    document.getElementById('inop_doors_eq').value = parseInt(inop) * 2;
}

inoperable_ovens()

function total_leaking_doors() {
    const p_elem = document.querySelector(['#pushSide']),
          c_elem = document.querySelector(['#cokeSide']);
    
    const p_array = JSON.parse(p_elem.value).data,
          c_array = JSON.parse(c_elem.value).data;
    if (typeof p_array === 'undefined') {
        var p_len = 0;
    }
    else {
        var p_len = p_array.length;
    }
    if (typeof c_array === 'undefined') {
        var c_len = 0;
    }
    else {
        var c_len = c_array.length;
    }
    const total_doors = p_len + c_len;
    
    document.getElementById('leaking_doors').value = total_doors;
}
total_leaking_doors()

function total_traverse() {
    const push_traverse_min = document.getElementById('id_p_traverse_time_min').value,
          push_traverse_sec = document.getElementById('id_p_traverse_time_sec').value,
          coke_traverse_min = document.getElementById('id_c_traverse_time_min').value,
          coke_traverse_sec = document.getElementById('id_c_traverse_time_sec').value;
    
    
    console.log(push_traverse_sec);
    if (push_traverse_min == '') {
        console.log('push minutes are empty');
        if(push_traverse_sec == '') {
            var push_secs = 0;
            console.log('push seconds are empty');
        }
    }
    else {
        var push_secs = (parseInt(push_traverse_min) * 60) + parseInt(push_traverse_sec);
    }
    
    if (coke_traverse_min == '') {
        console.log('coke minutes are empty');
        if(coke_traverse_sec == '') {
            var coke_secs = 0;
            console.log('coke seconds are empty');
        }
    }
    else {
        var coke_secs = (parseInt(coke_traverse_min) * 60) + parseInt(coke_traverse_sec);
    }
    
  //  const push_secs = (parseInt(push_traverse_min) * 60) + parseInt(push_traverse_sec);
          
    
    let total_secs = parseInt(push_secs) + parseInt(coke_secs);
    
    document.getElementById('total_traverse_time').value = total_secs;
}

function equation() {
    const leaks = document.getElementById('leaking_doors').value,
          inops = document.getElementById('inop_doors_eq').value,
          not_obs = document.getElementById('doors_not_observed').value;
    
    const equate = (parseInt(leaks) * 100)/(170 - parseInt(inops) - parseInt(not_obs));
    
    document.getElementById('id_percent_leaking').value = parseFloat(equate).toFixed(3);
    
}

function allowed_time() {
    const leaks = document.getElementById('leaking_doors').value;
    
    const equate_time = 680 + (10 * parseInt(leaks));
    
    document.getElementById('allowed_traverse_time').value = equate_time;
          
}

