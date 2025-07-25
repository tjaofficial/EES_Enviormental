document.addEventListener('input', e => {
    const el = e.target;
    if (shouldTrack(el)) {
        saveToLocal({ target: el });
    }
}, true);

document.addEventListener('change', e => {
    const el = e.target;
    if (shouldTrack(el)) {
        saveToLocal({ target: el });
    }
}, true);

// Optional helper to avoid csrf or hidden fields, etc.
function shouldTrack(el) {
    if (!el.tagName) return false;
    if (el.type === 'hidden' || el.name === 'csrfmiddlewaretoken') return false;
    if (el.disabled || el.readOnly) return false;
    return ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName);
}

function saveToLocal(event){
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const currentDate = Date.now();
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    const elem = event.target;

    if (elem.tagName === 'SELECT' && elem.multiple) {
        const selectedValues = Array.from(elem.selectedOptions).map(opt => opt.value);
        formTempData.data[elem.id] = selectedValues;
    } else if (elem.type === "radio") {
        let baseName = elem.name;  // Use `name` instead of `id` to get the whole group
        formTempData.data[baseName] = elem.value; // Store by name, not full ID
    } else if (elem.type === "checkbox"){
        formTempData.data[elem.id] = elem.checked;
    } else {
        formTempData.data[elem.id] = elem.value;
    }

    //formTempData.data[elem.id] = elem.value;
    console.log("Saved field:", elem.id || elem.name, elem.value);
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
        console.log(dataObject)
        for(let key in dataObject) {
            if(dataObject[key]){ 
                let element = document.getElementById(key);
                if (!element){
                    const val = dataObject[key];
                    let element = document.getElementById(key);
                    if (!element && typeof val === 'string') {
                        element = document.getElementById(`${key}_${val.toLowerCase()}`);
                    }
                }
                //console.log(element)
                if (element) {
                    if (element.tagName === 'SELECT' && element.multiple) {
                        const savedValues = dataObject[key];

                        if (element.choicesInstance && Array.isArray(savedValues)) {
                            element.choicesInstance.setChoiceByValue(savedValues);
                        } else {
                            // fallback for plain selects
                            Array.from(element.options).forEach(opt => {
                                opt.selected = savedValues.includes(opt.value);
                            });
                        }
                    } else if (element.type === "checkbox"){
                        element.checked = dataObject[key];
                    } else if(element.type === "radio") {
                        if (['24', '25'].includes(formName)){
                            var baseName = key;
                        } else {
                            var baseName = key.replace(/_\d+$/, '').replace("id_",""); // 🔥 Remove trailing _0, _1, _2
                        }
                        let radios = document.getElementsByName(baseName);
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
    fillForm(tempSaveKey);
    
}

intiate_TempSave()
