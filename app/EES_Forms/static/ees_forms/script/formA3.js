const submitButton = document.getElementById('submit');
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
        resultElement[i].addEventListener('change', total_leaking_doors)
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


    if(parseInt(resultInputAttr) === -1){
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

    console.log(`${JSON.stringify(dataJSON)} - ${input_ID}`);    
    let tableHTML = "";

    if(dataJSON.data){
        const dataArray = dataJSON.data;
        if(dataArray.length > 0){
            for(i=0; i<dataArray.length; i++){
                let data = dataArray[i];
                tableHTML = tableHTML+htmlLayout(false, data, input_ID);
            }
            if(input_ID === "lid"){
                let l_insert_in_form = document.getElementById('l_leak_json').value = JSON.stringify(dataJSON);
                let total_lid_leaks = 0;

                for(a=0; a<dataArray.length; a++){
                    if(dataArray[a]["location"]){
                        if(dataArray[a]["location"][0] !== "dampered_off"){
                            total_lid_leaks++
                        }
                    }
                }
                let total_lid_leak_insert = document.getElementById('l_leaks').value = total_lid_leaks;
                let total_lid_not_obs = document.getElementById('l_not_observed').value = dataArray.length *4;
            }
            if(input_ID === "offtake"){
                let om_insert_in_form = document.getElementById('om_leak_json').value = JSON.stringify(dataJSON);
                let total_om_leaks = 0;

                for(b=0; b<dataArray.length; b++){
                    if(dataArray[b]["location"]){
                        if(dataArray[b]["location"][0] !== "dampered_off"){
                            total_om_leaks++
                        }
                    }
                }
                let total_om_leak_insert = document.getElementById('om_leaks').value = total_om_leaks;
                let total_om_not_obs = document.getElementById('om_not_observed').value = dataArray.length *2;
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
    if(target == 'offtakes'){
        var htmlTempate = `<select oninput="check_dampered_inoperable(this, '${target}', 'inputted');" data-locationIndex="${locationIndex}" data-resultKey="location" data-targetinput="${target}" data-resultInput="${resultInput}" style="margin-bottom:3px;">
                                <option value="" ${value? 'selected': ''}>--</option>
                                <option value="dampered_off" ${value === "dampered_off"? 'selected': ''}>D</option>
                                <option value="cap" ${value === "cap"? 'selected': ''}>C</option>
                                <option value="flange" ${value === "flange"? 'selected': ''}>F</option>
                                <option value="slip_joint" ${value === "slip_joint"? 'selected': ''}>S</option>
                                <option value="base" ${value === "base"? 'selected': ''}>B</option>
                                <option value="piping" ${value === "piping"? 'selected': ''}>P</option>
                                <option value="other" ${value === "other"? 'selected': ''}>O</option>
                                <option value="mini_standpipe" ${value === "mini_standpipe"? 'selected': ''}>MS</option>
                            </select>`;
    } else {
        var htmlTempate = `<select oninput="check_dampered_inoperable(this, '${target}', 'inputted')" data-locationIndex="${locationIndex}" data-resultKey="location" data-targetinput="${target}" data-resultInput="${resultInput}" style="margin-bottom:3px;">
                                <option value="" ${value? 'selected': ''}>--</option>
                                <option value="dampered_off" ${value === "dampered_off"? 'selected': ''}>D</option>
                                <option value="1" ${value === "1"? 'selected': ''}>1</option>
                                <option value="2" ${value === "2"? 'selected': ''}>2</option>
                                <option value="3" ${value === "3"? 'selected': ''}>3</option>
                                <option value="4" ${value === "4"? 'selected': ''}>4</option>
                            </select>`;
    }
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
                        <td class="boxa6" colspan="1" style="text-align: center; width: 84px;">
                            <input type="number" oninput="check_dampered_inoperable(this, '${target}', 'inputted')" style="text-align: center; width: 45px; margin-bottom:3px;" ${!empty? 'value="'+data.oven+'"': ''} data-resultInput="${empty? -1: i}" data-resultKey="oven" data-targetinput="${target}"/>
                        </td>
                        <td class="boxa6" colspan="1" style="width:90px; margin-bottom:3px;">
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


function total_leaking_doors() {
    const o_elem = document.querySelector(['#offtakes']),
          l_elem = document.querySelector(['#lids']);
    
    const o_array = JSON.parse(o_elem.value).data,
          l_array = JSON.parse(l_elem.value).data;
    if (typeof o_array === 'undefined') {
        var o_len = 0;
    } else {
        var x = 0;
        for (let i=0; i < o_array.length; i+=1) {
            if (o_array[i]['location'] == 'dampered_off'){
                x +=1;
            }
        }
        var o_len = o_array.length;
        const o_damper = x;
        const o_other = o_len - x;
        document.getElementById('om_leaks').value = o_other;
        document.getElementById('om_leaks2').value = o_other;
        document.getElementById('om_not_observed').value = o_damper * 2;
        om_equation();
    }
    if (typeof l_array === 'undefined') {
        var l_len = 0;
    } else {
        var y = 0;
        for (let c=0; c < l_array.length; c+=1) {
            if (l_array[c]['location'] == 'dampered_off'){
                y +=1;
            }
        }
        var l_len = l_array.length;
        const l_damper = y;
        const l_other = l_len - y;
        document.getElementById('l_leaks').value = l_other;
        document.getElementById('l_leaks2').value = l_other;
        document.getElementById('l_not_observed').value = l_damper * 4;
        l_equation();
    }
}
total_leaking_doors()

function total_time(observed){
    if(observed == "offtakes"){
        const om_traverse_time_min = document.getElementById('id_om_traverse_time_min').value;
        const om_traverse_time_sec = document.getElementById('id_om_traverse_time_sec').value;
        const om_total_sec = document.getElementById('id_om_total_sec');
        const om_total = minutesToSeconds(om_traverse_time_min)+parseInt(om_traverse_time_sec? om_traverse_time_sec: 0);
        om_total_sec.value = om_total;
    } else {
        const l_traverse_time_min = document.getElementById('id_l_traverse_time_min').value;
        const l_traverse_time_sec = document.getElementById('id_l_traverse_time_sec').value;
        const l_total_sec = document.getElementById('id_l_total_sec');
        const l_total = minutesToSeconds(l_traverse_time_min)+parseInt(l_traverse_time_sec? l_traverse_time_sec: 0);
        l_total_sec.value = l_total;
    }
}
total_time('offtakes');
total_time('lids');

function minutesToSeconds(minutes){
    let total_seconds = minutes*60
    return parseInt(total_seconds)
}

function l_equation() {
    const l_leaks = document.getElementById('l_leaks2').value,
          l_inops = document.getElementById('inop_ovens').value,
          l_not_obs = document.getElementById('l_not_observed').value;
    
    const equate = (parseInt(l_leaks) * 100)/(4*(85 - parseInt(l_inops)) - parseInt(l_not_obs));
    
    document.getElementById('l_percent_leaking').value = parseFloat(equate).toFixed(3);
}

function om_equation() {
    const om_leaks = document.getElementById('om_leaks2').value,
          om_inops = document.getElementById('inop_ovens').value,
          om_not_obs = document.getElementById('om_not_observed').value;
    
    const equate = (parseInt(om_leaks) * 100)/(2*(85 - parseInt(om_inops)) - parseInt(om_not_obs));
    
    document.getElementById('om_percent_leaking').value = parseFloat(equate).toFixed(3);
}

function one_pass_func() {
    const checked = document.getElementById('id_one_pass').checked;
    const om_start = document.getElementById('id_om_start').value;
    const om_stop = document.getElementById('id_om_stop').value;
    const om_traverse_time_min = document.getElementById('id_om_traverse_time_min').value;
    const om_traverse_time_sec = document.getElementById('id_om_traverse_time_sec').value;
    const om_total_sec = document.getElementById('id_om_total_sec').value;
    console.log(checked);
    if (checked) {
        document.getElementById('id_l_start').value = om_start;
        document.getElementById('id_l_stop').value = om_stop;
        document.getElementById('id_l_traverse_time_min').value = om_traverse_time_min;
        document.getElementById('id_l_traverse_time_sec').value = om_traverse_time_sec;
        document.getElementById('id_l_total_sec').value = om_total_sec;
    }
}
one_pass_func();
/*****************************************
 Initiates the Tables on JS load
 *****************************************/
setTimeout(
    initate_Result_Table(),
    1000
    )
    
function check_dampered_inoperable(elem, observed, action) {
    const inop_numbers = document.getElementById('inop_numbs').value.replaceAll(' ','').split(',');
    var noOvensMatch1offtakes = true;
    var noOvensMatchlids = true;
    if (elem.id == 'inop_numbs') {
        var offtakesList = document.getElementById('offtakes_tableBody').children;
        var lidsList = document.getElementById('offtakes_tableBody').children;
        for(let v=0;v<inop_numbers.length;v++){
            let inopOvenNumber = inop_numbers[v];
            for(var w=0;w<offtakesList.length;w++){
                var offtakeOven = offtakesList[w].children[0].children[0].value;
                console.log(offtakeOven)
                console.log(inopOvenNumber)
                if (parseInt(offtakeOven) == parseInt(inopOvenNumber)){
                    console.log('check 1')
                    var offtakeSelections = offtakesList[w].children[1].children;
                    for(var g=0;g<offtakeSelections.length;g++){
                        var offtakesSingleSelection = offtakeSelections[g].value;
                        if (offtakesSingleSelection == 'dampered_off'){
                            console.log('check 2');
                            noOvensMatch1offtakes = false;
                        }
                    }
                }
            }
        }
        for(let v=0;v<inop_numbers.length;v++){
            let inopOvenNumber = inop_numbers[v];
            for(var w=0;w<lidsList.length;w++){
                var lidOven = lidsList[w].children[0].children[0].value;
                if (parseInt(lidOven) == parseInt(inopOvenNumber)){
                    console.log('check 3')
                    var lidSelections = lidsList[w].children[1].children;
                    for(var g=0;g<lidSelections.length;g++){
                        var lidSingleSelection = lidSelections[g].value;
                        if (lidSingleSelection == 'dampered_off'){
                            console.log('check 4')
                            noOvensMatchlids = false;
                        }
                    }
                }
            }
        }
        if(noOvensMatch1offtakes){
            document.getElementById('om_damperPopup').style.display = 'none';
            submitButton.disabled = false;
            console.log('No Ovens Match the Inoperable')
        } else {
            document.getElementById('om_damperPopup').style.display = 'block';
            submitButton.disabled = true;
            console.log('found one')
        }
        if(noOvensMatchlids){
            document.getElementById('l_damperPopup').style.display = 'none';
            submitButton.disabled = false;
            console.log('No Ovens Match the Inoperable')
        } else {
            document.getElementById('l_damperPopup').style.display = 'block';
            submitButton.disabled = true;
            console.log('found one')
        }
    } else {
        if(observed == 'offtakes'){
            var ovenData = JSON.parse(document.querySelectorAll("[id='offtakes']")[0].value)['data'];
            var idAttachment = 'om'
        } else {
            var ovenData = JSON.parse(document.querySelectorAll("[id='lids']")[0].value)['data'];
            var idAttachment = 'l'
        }
        var noOvensMatch1 = true;
        if(action == "inputted"){
            const tableAnswers = elem.parentNode.parentNode.parentNode.children;
            for(var y=0;y<tableAnswers.length;y++){
                var element = tableAnswers[y].children[0].children[0].value;
                for(let x=0;x<inop_numbers.length;x++){
                    let inopOvenNumber = inop_numbers[x];
                    if(parseInt(inopOvenNumber) == parseInt(element)){
                        console.log('check 1')
                        for (var z=0;z<tableAnswers[y].children[1].children.length;z++){
                            var locationValue = tableAnswers[y].children[1].children[z].value;
                            if(locationValue == "dampered_off"){
                                noOvensMatch1 = false;
                                console.log('chcek 2')
                            }
                        }
                    }
                }
            }
            if(noOvensMatch1){
                document.getElementById(idAttachment + '_damperPopup').style.display = 'none';
                submitButton.disabled = false;
                console.log('No Ovens Match the Inoperable')
            } else {
                document.getElementById(idAttachment + '_damperPopup').style.display = 'block';
                submitButton.disabled = true;
                console.log('found one')
            }
        } else {
            try{
                var noOvensMatch2 = true;
                for(var x=0;x<inop_numbers.length;x++){
                    var inopOvenNumber = inop_numbers[x];
                    for(var i=0;i<ovenData.length;i++){
                        var damperedOvenNumber = ovenData[i]['oven'];
                        if(parseInt(inopOvenNumber) == parseInt(damperedOvenNumber || parseInt(inputValue) == parseInt(inopOvenNumber))){
                            if(ovenData[i]['location'] == "dampered_off"){
                                noOvensMatch2 = false;
                                console.log('found one in ' + observed)
                            }
                        }
                    }
                }
                if(noOvensMatch2){
                    document.getElementById(idAttachment + '_damperPopup').style.display = 'none';
                    submitButton.disabled = false;
                    console.log('No Ovens Match')
                } else {
                    submitButton.disabled = true;
                    document.getElementById(idAttachment + '_damperPopup').style.display = 'block';
                }
            } catch(err) {
                document.getElementById(idAttachment + '_damperPopup').style.display = 'none';
                submitButton.disabled = false;
                console.log("No Data Inputed for " + observed)
            }
        }
    }
}
check_dampered_inoperable(false, 'offtakes', 'initial');
check_dampered_inoperable(false, 'lids', 'initial');

function inoperable_ovens() {
    const inop = document.getElementById('inop_ovens').value;
    
    document.getElementById('l_inop_ovens').value = parseInt(inop);
    document.getElementById('om_inop_ovens').value = parseInt(inop);
    l_equation();
    om_equation();

    const inop_numbs_input = document.getElementById('inop_numbs');
    var length_of_inop_numbers = inop_numbs_input.value.replace(' ', '').split(',').length
    const inop_message = document.getElementById('inop_message');
    if (inop_numbs_input.value == "-" && +inop == 0){
        inop_message.style.display = "none";
    } else if (length_of_inop_numbers != inop){
        console.log('Error message')
        inop_message.style.display = "block";
        submitButton.disabled = true;
    } else {
        var blank = false;
        for(let x=0;x<length_of_inop_numbers;x++){
            const oven_number = inop_numbs_input.value.replace(' ', '').split(',')[x];
            if (!oven_number || +oven_number == 0 || isNaN(+oven_number)) {
                var blank = true;
                console.log("you got it")
            }
        }
        if (blank) {
            inop_message.style.display = "block";
            submitButton.disabled = true;
        } else {
            inop_message.style.display = "none";
            submitButton.disabled = false;
        }
    }
}
inoperable_ovens();
