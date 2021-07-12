const arrayOfInputs = document.getElementsByTagName('input');
const formName = document.getElementById('formName').dataset.form
const tempSaveKey = formName+"_tempFormData";
const currentDate = Date.now();

function inputEventListener(array, tempSaveKey, currentDate){
    
    //console.log(arrayOfInputs)
    for(let elem in array) {  
        item = array[elem];
        if(item.id){
            console.log("test")
            document.getElementById(item.id).addEventListener("input", () => {saveToLocal(array, tempSaveKey, currentDate)});
        }
    }
}

function saveToLocal(array, tempSaveKey, currentDate){
  
    const saveDateObject = {"Experation":currentDate, data:{}};
        
    for(let elem in array) {  
        item = array[elem];
        if(item.id){
            saveDateObject.data[item.id] = item.value;
        }
    }

    localStorage.setItem(tempSaveKey, JSON.stringify(saveDateObject));
    

}

function clearStorage(currentDate, tempSaveKey){

    const formattedcurrentDate = new Date(currentDate);
    const formTempData = localStorage.getItem(tempSaveKey);
    if(formTempData){
        const expDate = new Date(JSON.parse(formTempData).Experation);
        console.log(formattedcurrentDate);
        console.log(expDate);
        if (formattedcurrentDate.getMonth() != expDate.getMonth() && formattedcurrentDate.getDate() != expDate.getDate() && formattedcurrentDate.getFullYear() != expDate.getFullYear() ){
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

clearStorage(currentDate, tempSaveKey);
inputEventListener(arrayOfInputs, tempSaveKey, currentDate);
fillForm(tempSaveKey);

