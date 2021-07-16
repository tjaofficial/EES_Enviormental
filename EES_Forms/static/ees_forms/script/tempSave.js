const arrayOfInputs = document.getElementsByTagName('input');
const formName = document.getElementById('formName').dataset.form
const tempSaveKey = formName+"_tempFormData";
const currentDate = Date.now();

function inputEventListener(array, tempSaveKey, currentDate){
    
    //console.log(arrayOfInputs)
    for(let elem in array) {  
        item = array[elem];
        if(item.id){
            //console.log("test")
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

clearStorage(currentDate, tempSaveKey);
inputEventListener(arrayOfInputs, tempSaveKey, currentDate);
fillForm(tempSaveKey);

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
