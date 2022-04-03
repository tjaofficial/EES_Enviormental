"use strict"

window.addEventListener("load", ()=> {
    insertHTMLString([])
    updateEventListeners();
});

function updateEventListeners(){
    const resultElement = document.querySelectorAll("[data-dynamicInputs]");

    for(let i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('change', handle_Table_Input)
        resultElement[i].addEventListener('change', update_Temp_Save)
        
    }
}

function handle_Table_Input(event){
    const elem = event.target;
    
    //query information from input
    let elementRowAttr = parseInt(elem.dataset.locationindex); //Index 0 - n of row in table (-1 if Data Hasnt been entered in that row)
    const elementColumnKeyAttr = elem.dataset.resultkey; // Key of Column Effected
    const elementValue = elem.value; //Value entered into effected Input

    //query data from targeted input dom storing the data and parse the infromation
    const hiddenFormDom = document.getElementById("gooseNeckData");
    const parsedDomValue = JSON.parse(hiddenFormDom.value);
    const hiddenFormValueArray = parsedDomValue.data ? parsedDomValue.data : [];
    let updatedFormValueArray = []

    

    if(elementRowAttr === -1){
        updatedFormValueArray = addArrayData(hiddenFormValueArray, elementColumnKeyAttr, elementValue);
    }
    else{
        if(hiddenFormValueArray[elementRowAttr]){

            updatedFormValueArray = updateArrayData(hiddenFormValueArray, elementRowAttr, elementColumnKeyAttr, elementValue);
        }

        else{
            console.log("error: Inproper key")
        }
    }

    parsedDomValue.data = updatedFormValueArray;
    hiddenFormDom.value = JSON.stringify(parsedDomValue);

    
    insertHTMLString(updatedFormValueArray);
    updateEventListeners();

}


//Utility Functions


function addArrayData(array, columnKey, value){
    let new_Object = {};
    new_Object[columnKey] = value;
    array.push(new_Object);

    return array;
}

function updateArrayData(array, location, columnKey, value){
    let data = array[location];
    let valueEmpty = value == "" ? true : false;
    
    let dataEmpty = dataEmptyCheck(data, columnKey);

    if(valueEmpty && dataEmpty){
        array.splice(location, 1);
    }
    else{
        data[columnKey] = value;
    }

    return array;
}

function dataEmptyCheck(data, columnKey){
    let empty = true;
    for (const [key, value] of Object.entries(data)) {
        if(key != columnKey){
            if(value != ""){
                empty = false;
            }
        }
    }

    return empty;
}

function insertHTMLString(array){
    let dynamicInputContainer = document.getElementById('gooseNeckInputContainer')
    let htmlString = "";
    array.forEach((item, index)=>{
        htmlString = htmlString + htmlTemplate(item, index);
    })

    htmlString = htmlString + htmlTemplate({}, -1);

    dynamicInputContainer.innerHTML = htmlString;

}

function htmlTemplate(data, index) {
        let html = `
        <tr>
            <th colspan="1" id="formE_box2">
                <input type="text" data-locationIndex="${index}" data-resultKey="oven" data-dynamicInputs value="${data.oven? data.oven: ''}" data-targetinput="gooseNeckData"/>
            </th>
            <th colspan="1" id="formE_box2">
                <input type="time" data-locationIndex="${index}" data-resultKey="time" data-dynamicInputs value="${data.time? data.time: ''}" data-targetinput="gooseNeckData"/>
            </th>
            <th colspan="1" id="formE_box2">
                <select data-locationIndex="${index}" data-resultKey="source" data-dynamicInputs data-targetinput="gooseNeckData"/>
                    <option value="" ${data.source? 'selected': ''}>--</option>
                    <option value="I" ${data.source === "I"? 'selected': ''}>I</option>
                    <option value="G" ${data.source === "G"? 'selected': ''}>G</option>
                    <option value="F" ${data.source === "F"? 'selected': ''}>F</option>
                    <option value="J" ${data.source === "J"? 'selected': ''}>J</option>
                </select>
            </th>
            <th colspan="1" id="formE_comments">
                <input type="text" data-locationIndex="${index}" data-resultKey="comment" data-dynamicInputs value="${data.comment? data.comment: ''}" data-targetinput="gooseNeckData"/>
            </th>
        </tr>
        `;
        return html
}

function update_Temp_Save(event){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;
    let target_Input_Field_Id = elem.dataset.targetinput;


    formTempData.data[target_Input_Field_Id] = document.getElementById(target_Input_Field_Id).value;


    localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
}

