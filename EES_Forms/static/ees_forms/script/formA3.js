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

    document.getElementById(`${input_ID}_tableBody`).innerHTML = tableHTML;
    


}










function intiateResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");
    const locationElement = document.querySelectorAll("[data-locationindex]");

    for(i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('input', handle_Table_Input)
        resultElement[i].addEventListener('input', update_Temp_Save)
        
    }
    for(i=0; i<locationElement.length; i++){
        locationElement[i].addEventListener('input', handle_location_Input)
        
    }
}

function handle_location_Input(event){
    const elem = event.target;
    let resultInputAttr = elem.dataset.resultinput;
    const resultKeyAttr = elem.dataset.resultkey;
    const elemValue = elem.value; 
    const input_Target = elem.dataset.targetinput;

    if(parseInt(resultInputAttr) === -1){
        addToResultArray(input_Target, resultKeyAttr, elemValue);
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
    if(key === "oven"){
        new_Object[key] = value;
    }
    else{
        new_Object[key] = [value];
    }
    
    const result_Array = parsed_Result.data ? parsed_Result.data : [];

    result_Array.push(new_Object);
    parsed_Result.data = result_Array;
    console.log(parsed_Result)
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

    const lidArray = data.location;
    let locationhtml=""
    let locationIndex=0;
    lidArray.forEach((elem)=>{
        locationhtml = locationhtml + `<select data-resultInput="${empty? -1: i}" data-resultKey="location" data-targetinput="${target}" data-locationindex="${locationIndex}">
                                                <option value="" ${empty? 'selected': ''}>--</option>
                                                <option value="D" ${!empty && data.location === "D"? 'selected': ''}>D</option>
                                                <option value="C" ${!empty && data.location === "C"? 'selected': ''}>C</option>
                                                <option value="M" ${!empty && data.location === "M"? 'selected': ''}>M</option>
                                            </select>`;
        locationIndex++
    })
    const htmlStr= `<tr>
                        <td class="boxa6" colspan="1">
                            <input type="number" ${!empty? 'value="'+data.oven+'"': ''} data-resultInput="${empty? -1: i}" data-resultKey="oven" data-targetinput="${target}"/>
                        </td>
                        <td class="boxa6" colspan="1">
                            ${locationIndex}
                            <select data-resultInput="${empty? -1: i}" data-resultKey="location" data-targetinput="${target}" data-locationindex="-1">
                                <option value="" ${empty? 'selected': ''}>--</option>
                                <option value="D" ${!empty && data.location === "D"? 'selected': ''}>D</option>
                                <option value="C" ${!empty && data.location === "C"? 'selected': ''}>C</option>
                                <option value="M" ${!empty && data.location === "M"? 'selected': ''}>M</option>
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