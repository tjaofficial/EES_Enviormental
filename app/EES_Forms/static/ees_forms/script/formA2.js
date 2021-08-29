// Get Required Input Fields


function updateCalcs(){

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