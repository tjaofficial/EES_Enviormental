



const arrayOfInputs = Array.prototype.slice.call(document.getElementsByTagName('input'),0);

const arrayOfSelects = Array.prototype.slice.call(document.getElementsByTagName('select'),0);
const arrayOfTextareas = Array.prototype.slice.call(document.getElementsByTagName('textarea'),0);
const input_select_textarea_combined_array = arrayOfInputs.concat(arrayOfSelects, arrayOfTextareas);



const formName = document.getElementById('formName').dataset.form
const tempSaveKey = formName+"_tempFormData";
const currentDate = Date.now();



clearStorage(currentDate, tempSaveKey);
inputEventListener(input_select_textarea_combined_array);
fillForm(tempSaveKey);


function inputEventListener(array){
    

    
    for(let elem in array) {  
        item = array[elem];
        if(item.id){
            //console.log("test")
            document.getElementById(item.id).addEventListener("input", saveToLocal);
        }
    }
}

function saveToLocal(event){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;


    formTempData.data[elem.id] = elem.value;


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
        dataObject = object.data;
        for(let key in dataObject) {
            if(dataObject[key]){  
                document.getElementById(key).value = dataObject[key];
            }
            
        }
    }
}

function intiate_TempSave(){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    
    clearStorage(tempSaveKey, currentDate);
    inputEventListener();
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
