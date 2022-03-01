
/*****************************************
Initial Page Load Setup
*****************************************/
// Run once on js load only
function initate_Result_Table(){
    const query_Tables = document.querySelectorAll("[data-resulttable]");
    const result_Table_DOM_Array = Array.from(query_Tables)
    result_Table_DOM_Array.forEach((elem)=>{
        let parsedJSON = JSON.parse(elem.value)
        createHTMLString(parsedJSON, elem.id);
        addResultEventListeners();
        
    })
}

/*****************************************
Add event Listeners
*****************************************/
//This adds the event listeners every Time the Table is rebuilt
function addResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");

    for(i=0; i<resultElement.length; i++){
        resultElement[i].addEventListener('change', handle_Table_Input)
        resultElement[i].addEventListener('change', update_Temp_Save)
        
    }

}

/*****************************************
Update JSON Values
*****************************************/

// Takes the event and Pulls required data-sets from effected Input
function handle_Table_Input(event){
    const elem = event.target;
    
    //query information from input
    let resultInputAttr = parseInt(elem.dataset.resultinput); //Index 0 - n of row in table (-1 if Data Hasnt been entered in that row)
    let locationIndexAttr = parseInt(elem.dataset.locationindex); //Index 0 - n of the location (-1 if Data Hasnt been entered in that row)
    const resultKeyAttr = elem.dataset.resultkey; // Key of Column Effected
    const elemValue = elem.value; //Value entered into effected Input
    const input_Target = elem.dataset.targetinput; //Table JSON Data the Input Targets

    //query data from targeted input dom storing the data and parse the infromation
    const targeted_input_DOM = document.getElementById(input_Target);
    const parsed_Result = JSON.parse(targeted_input_DOM.value);
    const result_Array = parsed_Result.data ? parsed_Result.data : [];


    if(resultInputAttr === -1){
        let new_Object = {};
        if(resultKeyAttr === "oven"){
            new_Object[resultKeyAttr] = elemValue;
        }
        else if(resultKeyAttr === "location"){
            new_Object[resultKeyAttr] = [elemValue];
        }
        
        
        result_Array.push(new_Object);

    }
    else{
        if(result_Array[resultInputAttr]){
            let rowData = result_Array[resultInputAttr];
            
            if(resultKeyAttr === "oven"){
                
                // 1. update the data
                
                rowData[resultKeyAttr] = elemValue;
            }

            else if(resultKeyAttr === "location"){
                // 1. add the data
                // 2. change the data
                
                if(locationIndexAttr === -1){
                    if(rowData[resultKeyAttr]){
                        rowData[resultKeyAttr].push(elemValue);
                    }
                    else{
                        rowData[resultKeyAttr] = [elemValue];
                    }
                    
                    
                }
                else{
                    let locationUnsetCheck = !elemValue ? true : false;
                    let objectData = rowData[resultKeyAttr];

                    if(locationUnsetCheck){
                        objectData.splice(locationIndexAttr, 1)
                        
                    }
                    else{
                        objectData[locationIndexAttr] = elemValue;
                    }
                }
            }
            else{
                console.log("error: Inproper key")
            }


            //delete row if both objects are empty
            let checkLocationHasData = false;
            let checkOvenHasData = false;
            const checkOvenSet = rowData.oven ? true : false;
            const checkLocationSet = rowData.location ? true : false;
            
            
            if(checkLocationSet){
                console.log(`${rowData.location.length}`);
                checkLocationHasData = rowData.location.length > 0 ? true : false;
            }

            if(checkOvenSet){
                console.log(`${rowData.oven}`);
                checkOvenHasData = rowData.oven != "" ? true : false;
            }

            if(!checkLocationHasData && !checkOvenHasData){
                result_Array.splice(resultInputAttr, 1);
            }


            

            console.log(`${checkLocationHasData} ${checkOvenHasData} -- this is a test i just enter`);

            

            
            //targeted_input_DOM.value = JSON.stringify(parsed_Result);
            //createHTMLString(parsed_Result, target);
            //addResultEventListeners();
        }
        else {console.log('this needs to read out')}
    }

    parsed_Result.data = result_Array;
    targeted_input_DOM.value = JSON.stringify(parsed_Result);

    
    createHTMLString(parsed_Result, input_Target);
    addResultEventListeners();

}




/*****************************************
Updates the HTML based on the stored JSON
*****************************************/


// Takes array of Objects and builds the string of HTML
function createHTMLString(dataJSON, input_ID){
    console.log('test');

    console.log(`${JSON.stringify(dataJSON)} - ${input_ID}`);    
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

// Takes objects determines whether should be empty and data to return string of html
// Template for Table Rows

function locationHTMLTemplate(value, target, locationIndex, resultInput){
    let htmlTempate = `<select data-locationIndex="${locationIndex}" data-resultKey="location" data-targetinput="${target}" data-resultInput="${resultInput}">
                            <option value="" ${value? 'selected': ''}>--</option>
                            <option value="D" ${value === "D"? 'selected': ''}>D</option>
                            <option value="C" ${value === "C"? 'selected': ''}>C</option>
                            <option value="M" ${value === "M"? 'selected': ''}>M</option>
                        </select>`;

    return htmlTempate
}


function htmlLayout(empty, data, target){
    const lidArray = data.location?data.location:[];
    let locationhtml=""
    let locationIndex=0;
    let locationResultInput=empty? -1: i;
    lidArray.forEach((elem)=>{
        locationhtml = locationhtml + locationHTMLTemplate(elem, target, locationIndex, locationResultInput);
        locationIndex++;
    })

    locationhtml = locationhtml + locationHTMLTemplate("", target, -1, locationResultInput);


    const htmlStr= `<tr>
                        <td class="boxa6" colspan="1">
                            <input type="number" ${!empty? 'value="'+data.oven+'"': ''} data-resultInput="${empty? -1: i}" data-resultKey="oven" data-targetinput="${target}"/>
                        </td>
                        <td class="boxa6" colspan="1">
                            ${locationhtml}
                        </td>

                    </tr>`;
    return htmlStr;

}




/*****************************************
Saves Entrys into local storage to allow 
for Temporary Save
*****************************************/


function update_Temp_Save(event){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;
    target_Input_Field_Id = elem.dataset.targetinput;


    formTempData.data[target_Input_Field_Id] = document.getElementById(target_Input_Field_Id).value;


    localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
}


/*****************************************
Initiates the Tables on JS load
*****************************************/
initate_Result_Table()