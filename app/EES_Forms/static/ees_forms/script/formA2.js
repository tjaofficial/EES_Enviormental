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
    //console.log(tableHTML)
    document.getElementById(`${input_ID}_ctableBody`).innerHTML = tableHTML;
}


function intiateResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");
    for(i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('change', handle_Table_Input)
        resultElement[i].addEventListener('change', update_Temp_Save)
        resultElement[i].addEventListener('change', total_leaking_doors)
        resultElement[i].addEventListener('change', allowed_time)
    }
}

function handle_Table_Input(event){
    const elem = event.target;
    let resultInputAttr = elem.dataset.resultinput;
    const resultKeyAttr = elem.dataset.resultkey;
    const elemValue = elem.value; 
    const input_Target = elem.dataset.targetinput;
    //console.log(input_Target)

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
        } else {
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

initate_Result_Table();







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
    console.log(select_numbers)
    //Push Side - Checks if the inoperable oven are listed in the total not observed doors and then subtracts those doors, if any
    if (parseInt(push_from) || parseInt(push_to) >= 0) {
        let push_blocked = Math.abs(parseInt(push_from) - parseInt(push_to)) +1,
        x = 0;
        // push side check and subtract
        if(parseInt(push_from) < parseInt(push_to)){
            for(o=parseInt(push_from); o<=parseInt(push_to); o++){
                for(i=0; i<select_numbers.length; i++){
                    //console.log("Comparing Ovens " + o + " AND Ovens " + select_numbers[i])
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                        //console.log("Push Side has " + x + " Oven(s) the same.")
                    }
                }
            }
        }
        else {
            for(o=parseInt(push_to); o<=parseInt(push_from); o++){
                for(i=0; i<select_numbers.length; i++){
                    //console.log("Comparing Ovens " + o + " AND Ovens " + select_numbers[i])
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                        //console.log("Push Side has " + x + " Oven(s) the same.")
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
        console.log(coke_blocked);

        if(parseInt(coke_from) < parseInt(coke_to)){
            for(i=parseInt(coke_from); i<=parseInt(coke_to); i++){
                for(k=0; k<select_numbers.length; k++){
                    //console.log("Comparing Ovens " + i + " AND Ovens " + select_numbers[k])
                    if(parseInt(i) === parseInt(select_numbers[k])){
                        y += 1;
                        //console.log("Coke Side has " + y + " Oven(s) the same.")
                    }
                }
            }
        }
        else {
            for(i=parseInt(coke_to); i<=parseInt(coke_from); i++){
                for(k=0; k<select_numbers.length; k++){
                    //console.log("Comparing Ovens " + i + " AND Ovens " + select_numbers[k])
                    if(parseInt(i) === parseInt(select_numbers[k])){
                        y += 1;
                        //console.log("Coke Side has " + y + " Oven(s) the same.")
                    }
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
    equation();
}
pc_doors_not_observed();

function inoperable_ovens() {
    const inop = document.getElementById('inop_ovens').value;
    
    document.getElementById('inop_doors_eq').value = parseInt(inop) * 2;
    equation();

    const inop_numbs_input = document.getElementById('inop_numbs');
    var length_of_inop_numbers = inop_numbs_input.value.replace(' ', '').split(',').length
    const inop_message = document.getElementById('inop_message');
    if (length_of_inop_numbers != inop ){
        console.log('Error message')
        inop_message.style.display = "block";
    } else {
        var blank = false;
        for(let x=0;x<length_of_inop_numbers;x++){
            const oven_number = inop_numbs_input.value.replace(' ', '').split(',')[x];
            if (!oven_number || +oven_number == 0 || isNaN(+oven_number)) {
                var blank = true;
            }
        }
        if (blank) {
            inop_message.style.display = "block";
        } else {
            inop_message.style.display = "none";
        }
    }
}
inoperable_ovens();

function total_leaking_doors() {
    const p_elem = document.querySelector(['#pushSide']),
          c_elem = document.querySelector(['#cokeSide']);
    
    const p_array = JSON.parse(p_elem.value).data,
          c_array = JSON.parse(c_elem.value).data;
          console.log(p_array);
          console.log(c_array);
    let pushList = []

    //---------------------------------------------------------------
    //-------Attempt to remove duplicates but might need to just add a popup---------
    //---------------------------------------------------------------

    // for (let i=0; i<p_array.length; i++){
    //     let singleDoor = p_array[i]['oven'];
    //     console.log(singleDoor)
    //     pushList.push(singleDoor)
    // }
    // for (let x=0; x<p_array.length; x++){
    //     let ovenDoor = p_array[x]['oven'];
    //     if (ovenDoor in pushList){
    //         p_array[x]['oven'] = "";
    //         p_array[x]['location'] = "";
    //         p_array[x]['zone'] = "";
    //         console.log(p_array)
    //         let pushJson = JSON.stringify(p_array);
    //         document.querySelector(['#pushSide']).value.data = pushJson;
    //     }
    // }
    if (typeof p_array === 'undefined') {
        var p_len = 0;
    } else {
        var p_len = p_array.length;
        console.log(p_len);
    }
    if (typeof c_array === 'undefined') {
        var c_len = 0;
    } else {
        var c_len = c_array.length;
    }
    const total_doors = p_len + c_len;
    
    document.getElementById('leaking_doors').value = total_doors;
    equation();
}
total_leaking_doors();

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

    if (total_secs == 0) {
        document.getElementById('total_traverse_time').value = total_secs;
    } else {
        document.getElementById('total_traverse_time').value = total_secs;
    }
}
total_traverse();

function equation() {
    const leaks = document.getElementById('leaking_doors').value,
          inops = document.getElementById('inop_doors_eq').value,
          not_obs = document.getElementById('doors_not_observed').value;
    
    const equate = (parseInt(leaks) * 100)/(170 - parseInt(inops) - parseInt(not_obs));
    if (isNaN(equate)) {
        document.getElementById('id_percent_leaking').value = '';
    } else {
        document.getElementById('id_percent_leaking').value = parseFloat(equate).toFixed(3);
    }
}

function allowed_time() {
    const leaks = document.getElementById('leaking_doors').value;
    
    const equate_time = 680 + (10 * parseInt(leaks));
    
    document.getElementById('allowed_traverse_time').value = equate_time;
          
}
allowed_time();
equation();