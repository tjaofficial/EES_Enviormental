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





// {
//     data:[
//         {
//             oven: "1",
//             location: "D",
//             zone: "3"
//         },
//         {
//             oven: "3",
//             location: "C",
//             zone: "6"
//         },
//         {
//             oven: "2",
//             location: "M",
//             zone: "7"
//         }
//     ]
// };



// Takes array of Objects and builds the string of HTML
function createHTMLString(dataJSON){
        
    let tableHTML = "";

    if(dataJSON.data){
        const dataArray = dataJSON.data;
        if(dataArray.length > 0){
            for(i=0; i<dataArray.length; i++){
                let data = dataArray[i];
                tableHTML = tableHTML+htmlLayout(false, data);
            }
        }
    }

    tableHTML = tableHTML+htmlLayout(true, {});
    document.getElementById('ctableBody').innerHTML = tableHTML;
    


}



function intiateResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");
    for(i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('input',(event)=>{
            let elem = event.target;
            handle_Table_Input(elem)
        })
        
    }
}


function handle_Table_Input(elem){
    let resultInputAttr = elem.dataset.resultinput;
    let resultKeyAttr = elem.dataset.resultkey;
    let elemValue = elem.value; 
    if(parseInt(resultInputAttr) === -1){
        addToResultArray(elemValue, resultKeyAttr);
    }
    else{
        updateResultArray(elemValue, resultKeyAttr, resultInputAttr);
    }
}

function addToResultArray(valueInputed, inputKey){
    const push_Side_Result = document.getElementById('pushSideResults').value;
    const parsed_Result = JSON.parse(push_Side_Result)
    
    let new_Object = {};
    new_Object[inputKey] = valueInputed;
    const result_Array = parsed_Result.data ? parsed_Result.data : [];

    result_Array.push(new_Object);
    parsed_Result.data = result_Array;
    
    document.getElementById('pushSideResults').value = JSON.stringify(parsed_Result);
    createHTMLString(parsed_Result);
    intiateResultEventListeners();

}

function updateResultArray(valueInputed, inputKey, arrayPos){
    const push_Side_Result = document.getElementById('pushSideResults').value;
    const parsed_Result = JSON.parse(push_Side_Result)
    const result_Array = parsed_Result.data;
    if(result_Array[arrayPos]){
        let changed_Object = result_Array[arrayPos];
        if(valueInputed){
            changed_Object[inputKey] = valueInputed;
        }
        else{
            delete changed_Object[inputKey];
        }

        if (Object.keys(changed_Object).length === 0 && changed_Object.constructor === Object){
            result_Array.splice(arrayPos,1);
        }
        else{result_Array[arrayPos] = changed_Object;}
        
        parsed_Result.data = result_Array;
    
        document.getElementById('pushSideResults').value = JSON.stringify(parsed_Result);
        createHTMLString(parsed_Result);
        intiateResultEventListeners();
    }
    
    

    

}

//createHTMLString(pushResultDataJSON);


function initate_Result_Table(){
    const pushResultDataJSON = document.getElementById('pushSideResults').value;
    let parsedJSON = JSON.parse(pushResultDataJSON)
    createHTMLString(parsedJSON);
    intiateResultEventListeners();

}

// Takes objects whether should be empty and data to return string of html
// Template for Table Rows
function htmlLayout(empty, data){

    const htmlStr= `<tr>
                        <td class="boxa6" colspan="1">
                            <input type="number" ${!empty? 'value="'+data.oven+'"': ''} data-resultInput="${empty? -1: i}" data-resultKey="oven" />
                        </td>
                        <td class="boxa6" colspan="1">
                            <select data-resultInput="${empty? -1: i}" data-resultKey="location" onchange()>
                                <option value="" ${empty? 'selected': ''}>--</option>
                                <option value="D" ${!empty && data.location === "D"? 'selected': ''}>D</option>
                                <option value="C" ${!empty && data.location === "C"? 'selected': ''}>C</option>
                                <option value="M" ${!empty && data.location === "M"? 'selected': ''}>M</option>
                            </select>
                        </td>
                        <td class="boxa6" colspan="1">
                            <select data-resultInput="${empty? -1: i}" data-resultKey="zone">
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

initate_Result_Table()