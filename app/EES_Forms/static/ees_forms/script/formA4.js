
document.getElementById("leaksYN").addEventListener('change', leak_appear);

function leak_appear(){
    const leaksYN = document.getElementById('leaksYN').value,
    leakCont = document.getElementById('leakCont'),
    leakCont2 = document.getElementById('leakCont2');
    if (leaksYN == 'yes'){
        leakCont.hidden = false;
    } else if (leaksYN == 'no'){
        leakCont.hidden = true;
    }
}

leak_appear()



/*****************************************
Initial Page Load Setup
*****************************************/
// Run once on js load only
function initate_Result_Table(){
    const query_Table = document.querySelectorAll("[data-resulttable]");
    const result_Table_DOM_Array = Array.from(query_Table);
    result_Table_DOM_Array.forEach((elem)=>{
        let parsedJSON = JSON.parse(elem.value)
        createHTMLString(parsedJSON, elem.id);
        intiateResultEventListeners();
    })
}

/*****************************************
Add event Listeners
*****************************************/
//This adds the event listeners every Time the Table is rebuilt
function intiateResultEventListeners(){
    const resultElement = document.querySelectorAll("[data-resultInput]");
    console.log(resultElement[0].value)
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
    const input_Target = elem.dataset.targetinput;
    console.log(input_Target)

    if(parseInt(resultInputAttr) === -1){
        addToResultArray(input_Target, resultKeyAttr, elemValue);
    }
    else{
        updateResultArray(input_Target, resultInputAttr, resultKeyAttr, elemValue);
    }
}

function addToResultArray(target, key, value){
    //query data from targeted input dom storing the data and parse the infromation
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
        if (value){   
            // 1. update the data
            changed_Object[key] = value;
        } else {
            //delete row if both objects are empty
            delete changed_Object[key];
        }
        
        if (Object.keys(changed_Object).length === 0 && changed_Object.constructor === Object){
            result_Array.splice(array_Position,1);
        } else {result_Array[array_Position] = changed_Object;}
        
        parsed_Result.data = result_Array;

        targeted_input_DOM.value = JSON.stringify(parsed_Result);
        createHTMLString(parsed_Result, target);
        intiateResultEventListeners();
    }
}





/*****************************************
Updates the HTML based on the stored JSON
*****************************************/


// Takes array of Objects and builds the string of HTML
function createHTMLString(dataJSON, input_ID){
   
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
    console.log(tableHTML)
    document.getElementById(`${input_ID}_ctableBody`).innerHTML = tableHTML;

}

// Takes objects determines whether should be empty and data to return string of html
// Template for Table Rows



function htmlLayout(empty, data, target){
    const htmlStr= `<tr>
                        <td class="rowsMiddle" colspan="1">
                            <input type="number" style="width:50px; text-align: center;" ${!empty? 'value="'+data.oven+'"': ''} data-resultKey="oven" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle" colspan="1">
                            <input type="time" style="width: 120px;" value="${!empty && data.time ? data.time : ''}" data-resultKey="time" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle" colspan="1">
                            <input type="datetime-local" style="" value="${!empty && data.tempSealed ? data.tempSealed : ''}" data-resultKey="tempSealed" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle">
                            <input type="text" style="width:120px; text-align: center;" value="${!empty && data.tempSealedBy ? data.tempSealedBy : ''}" data-resultKey="tempSealedBy" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle">
                            <input type="datetime-local" style="" value="${!empty && data.repairInit ? data.repairInit : ''}" data-resultKey="repairInit" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle">
                            <input type="datetime-local" style="" value="${!empty && data.repairComplete ? data.repairComplete : ''}" data-resultKey="repairComplete" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
                        <td class="rowsMiddle">
                            <input type="text" style="width:120px; text-align: center;" value="${!empty && data.repairBy ? data.repairBy : ''}" data-resultKey="repairBy" data-resultInput="${empty? -1: i}" data-targetinput="collection" data-targetinput="${target}"/>
                        </td>
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
initate_Result_Table();
