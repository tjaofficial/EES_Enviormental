const arrayOfInputs = Array.prototype.slice.call(document.getElementsByTagName('input'),0);
const arrayOfRadios = Array.from(document.querySelectorAll("input[type=radio]"));
const arrayOfSelects = Array.prototype.slice.call(document.getElementsByTagName('select'),0);
const arrayOfTextareas = Array.prototype.slice.call(document.getElementsByTagName('textarea'),0);
const input_select_textarea_combined_array = arrayOfInputs.concat(arrayOfSelects, arrayOfTextareas, arrayOfRadios);
//console.log(input_select_textarea_combined_array)

const formName = document.getElementById('formName').dataset.form
const tempSaveKey = formName+"_tempFormData";
const currentDate = Date.now();
const tempSave_fsID = document.getElementById('tempSave_fsID').dataset.tempsavefsid;

clearStorage(currentDate, tempSaveKey);
inputEventListener(input_select_textarea_combined_array);
//fillForm(tempSaveKey);

function inputEventListener(array) {
    if (!Array.isArray(array)) {
        console.error("inputEventListener was passed a non-array value:", array);
        return;
    }
    array.forEach(item => {
        if (item.id || item.type === "radio") { // Handle radios properly
            item.addEventListener("input", saveToLocal);
        }
    });
}

function saveToLocal(event){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;

    if (!(tempSave_fsID in formTempData.data)){
        formTempData.data[tempSave_fsID] = {};   
    }
    formTempData.data[tempSave_fsID][elem.id] = elem.value;

    //formTempData.data[elem.id] = elem.value;
    console.log(formTempData.data[tempSave_fsID][elem.id])
    console.log(elem.id)
    localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
}

function clearStorage(tempSaveKey, currentDate){
    const formattedcurrentDate = new Date(currentDate);
    const formTempData = localStorage.getItem(tempSaveKey);
    if(formTempData){
        const parsedExperation = JSON.parse(formTempData).Experation
        const expDate = new Date(parsedExperation);
        if (formattedcurrentDate.getMonth() != expDate.getMonth() || formattedcurrentDate.getDate() != expDate.getDate() || formattedcurrentDate.getFullYear() != expDate.getFullYear() ){
            localStorage.removeItem(tempSaveKey);
        }  
    } 
}

function fillForm(tempSaveKey){
    const formTempData = localStorage.getItem(tempSaveKey);
    if(formTempData){
        const object = JSON.parse(formTempData);
        dataObject = object.data[tempSave_fsID];
        console.log(dataObject)
        for(let key in dataObject) {
            if(dataObject[key]){ 
                let element = document.getElementById(key);
                console.log(element)
                if (element) {
                    if(element.type === "radio") {
                        let baseName = key.replace(/_\d+$/, '').replace("id_",""); // 🔥 Remove trailing _0, _1, _2
                        let radios = document.getElementsByName(baseName);

                        console.log(baseName)
                        radios.forEach(radio => {
                            if (radio.value === dataObject[key]) {
                                radio.checked = true;
                            }
                        });
                    } else {
                        let inputValue = document.getElementById(key).value 
                        if(!inputValue || inputValue != {}){
                            document.getElementById(key).value = dataObject[key];
                        }
                    }
                } else {
                    if(dataObject[key] == "OK"){
                        var parseBaseName = "id_" + key + "_0"
                    } else {
                        var parseBaseName = "id_" + key + "_1"
                    }
                    let element = document.getElementById(parseBaseName);
                    if(element?.type && element.type === "radio") {
                        let baseName = key.replace(/_\d+$/, '').replace("id_",""); // 🔥 Remove trailing _0, _1, _2
                        let radios = document.getElementsByName(baseName);

                        console.log(baseName)
                        radios.forEach(radio => {
                            if (radio.value === dataObject[key]) {
                                radio.checked = true;
                            }
                        });
                    }
                }
            }
        }
    }
}

function intiate_TempSave(){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();

    clearStorage(tempSaveKey, currentDate);
    inputEventListener(input_select_textarea_combined_array);
    fillForm(tempSaveKey);
    
}

intiate_TempSave()
//for testing set exporation
// function setExperation(tempSaveKey){
//     const datevalue = document.getElementsByClassName('dateChanger')[0].value;
//     const dateArray = datevalue.split('-');
//     console.log(dateArray[0]+" "+dateArray[1]+" "+dateArray[2])
//     const date = new Date(parseInt(dateArray[0]), parseInt(dateArray[1])-1, parseInt(dateArray[2]));
//     const formTempData = localStorage.getItem(tempSaveKey);
//     if(formTempData){
//         const object = JSON.parse(formTempData);
//         console.log(date);
//         object.Experation = date;
//         localStorage.setItem(tempSaveKey, JSON.stringify(object));
//     }
// }

// document.getElementsByClassName('dateChanger')[0].addEventListener('change', ()=>{ setExperation(tempSaveKey)});
