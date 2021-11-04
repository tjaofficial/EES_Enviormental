/* Sample data set

{"data": [
    {
        oven: number
        location: [String, String, String]
    },
    {
        oven: number
        location: [String, String, String]
    },

]

}


{"data":[
    {"location":"D","oven":"1"},
    {"location":"C","oven":"1"},
    {"oven":"1"},
    {},
    {}]
} 


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
    console.log('The Event Listeners should be added once per table rebuild.')
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
    let resultInputAttr = elem.dataset.resultinput; //Index 0 - n of row in table (-1 if Data Hasnt been entered in that row)
    const resultKeyAttr = elem.dataset.resultkey; // Key of Column Effected
    const elemValue = elem.value; //Value entered into effected Input
    const input_Target = elem.dataset.targetinput; //Table JSON Data the Input Targets

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
    console.log(key)
    let new_Object = {};
    if(key === "oven"){
        new_Object[key] = value;
    }
    else if(key === "location"){
        console.log("test2");
        //check if array is set
        let locationSet = new_Object[key] ? true : false
        console.log(locationSet);
        if(locationSet){
            console.log("penis");
            new_Object[key].push(value);
            console.log(`this -> ${new_Object[key]}`)
        }
        else{
            new_Object[key] = [value];
        }
            

    }
    
    const result_Array = parsed_Result.data ? parsed_Result.data : [];

    result_Array.push(new_Object);
    parsed_Result.data = result_Array;
    console.log(parsed_Result)
    targeted_input_DOM.value = JSON.stringify(parsed_Result);
    createHTMLString(parsed_Result, target);
    addResultEventListeners();

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
        addResultEventListeners();
    }
    
    

    

}

/*****************************************
Updates the HTML based on the stored JSON
*****************************************/


// Takes array of Objects and builds the string of HTML
function createHTMLString(dataJSON, input_ID){
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

// Takes objects whether should be empty and data to return string of html
// Template for Table Rows
function htmlLayout(empty, data, target){
    console.log(data.location)
    const lidArray = data.location?data.location:[];
    let locationhtml=""
    let locationIndex=0;
    lidArray.forEach((elem)=>{
        locationhtml = locationhtml + `<select data-resultInput="${elem? -1: i}" data-resultKey="location" data-targetinput="${target}" data-locationindex="${locationIndex}">
                                                <option value="" ${elem? 'selected': ''}>--</option>
                                                <option value="D" ${!elem && data.location === "D"? 'selected': ''}>D</option>
                                                <option value="C" ${!elem && data.location === "C"? 'selected': ''}>C</option>
                                                <option value="M" ${!elem && data.location === "M"? 'selected': ''}>M</option>
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




/*****************************************
Saves Entrys into local storage to allow 
for Temporary Save
*****************************************/


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


/*****************************************
Initiates the Tables on JS load
*****************************************/
initate_Result_Table()