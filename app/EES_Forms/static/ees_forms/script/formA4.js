
/*****************************************
Initial Page Load Setup
*****************************************/
// Run once on js load only
function initate_Result_Table(){
    const query_Table = document.querySelector("[data-resulttable]");
    let parsedJSON = JSON.parse(query_Table.value)
    createHTMLString(parsedJSON);
    addResultEventListeners();
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
    //let locationIndexAttr = parseInt(elem.dataset.locationindex); //Index 0 - n of the location (-1 if Data Hasnt been entered in that row)
    const resultKeyAttr = elem.dataset.resultkey; // Key of Column Effected
    const elemValue = elem.value; //Value entered into effected Input
    //const input_Target = elem.dataset.targetinput; //Table JSON Data the Input Targets

    //query data from targeted input dom storing the data and parse the infromation
    const targeted_input_DOM = document.getElementById("pushSide");
    const parsed_Result = JSON.parse(targeted_input_DOM.value);
    const result_Array = parsed_Result.data ? parsed_Result.data : [];


    if(resultInputAttr === -1){
        let new_Object = {};
        new_Object[resultKeyAttr] = elemValue;

        result_Array.push(new_Object);
    }
    else{
        if(result_Array[resultInputAttr]){
            let rowData = result_Array[resultInputAttr];
                // 1. update the data
                
            rowData[resultKeyAttr] = elemValue;

            //delete row if both objects are empty
            
            let ovenHasData = rowData.oven && rowData.Oven != "" ? true : false;
            let timeHasData = rowData.time && rowData.time != "" ? true : false;
            let tempSealedHasData = rowData.tempSealed && rowData.tempSealed != "" ? true : false;
            let tempSealedByHasData = rowData.tempSealedBy && rowData.tempSealedBy != "" ? true : false;
            let repairInitHasData = rowData.repairInit && rowData.repairInit != "" ? true : false;
            let repairCompleteHasData = rowData.repairComplete && rowData.repairComplete != "" ? true : false;
            let repairByHasData = rowData.repairBy && rowData.repairBy != "" ? true : false;
            
            if(!ovenHasData && !timeHasData && !tempSealedHasData && !tempSealedByHasData && !repairInitHasData && !repairCompleteHasData && !repairByHasData){
                result_Array.splice(resultInputAttr, 1);
            }
        }

        else{
            console.log("error: Inproper key")
        }
    }

    parsed_Result.data = result_Array;
    targeted_input_DOM.value = JSON.stringify(parsed_Result);

    createHTMLString(parsed_Result);
    addResultEventListeners();
}





/*****************************************
Updates the HTML based on the stored JSON
*****************************************/


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

    //adds empty row at end of table
    tableHTML = tableHTML+htmlLayout(true, {});
    document.getElementById(`pushSide_tableBody`).innerHTML = tableHTML;

}

// Takes objects determines whether should be empty and data to return string of html
// Template for Table Rows



function htmlLayout(empty, data){
    const htmlStr= `<tr>
                        <th id="A4ovens">
                            <input type="number" style="width:50px; text-align: center;" value="${!empty && data.oven ? data.oven : ""}" data-resultKey="oven" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="time" style="width: 120px;" value="${!empty && data.time ? data.time : ''}" data-resultKey="time" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="datetime-local" style="" value="${!empty && data.tempSealed ? data.tempSealed : ''}" data-resultKey="tempSealed" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="text" style="width:120px; text-align: center;" value="${!empty && data.tempSealedBy ? data.tempSealedBy : ''}" data-resultKey="tempSealedBy" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="datetime-local" style="" value="${!empty && data.repairInit ? data.repairInit : ''}" data-resultKey="repairInit" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="datetime-local" style="" value="${!empty && data.repairComplete ? data.repairComplete : ''}" data-resultKey="repairComplete" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>
                        <th id="formA5_box1">
                            <input type="text" style="width:120px; text-align: center;" value="${!empty && data.repairBy ? data.repairBy : ''}" data-resultKey="repairBy" data-resultInput="${empty? -1: i}" data-targetinput="pushSide"/>
                        </th>

                    </tr>`;
    return htmlStr;

}

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
