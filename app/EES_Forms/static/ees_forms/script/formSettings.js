toggleSettings = (checkbox) => {
    const count = checkbox.dataset.count;
    const settingsCont = document.getElementById('settings' + String(count))
    if (checkbox.checked == true){
        settingsCont.style.display = 'block';
    } else {
        settingsCont.style.display = 'none';
    }
}

function displayAreaFields(elem, count){
    let areas = elem.value;
    console.log(areas)
    if (areas > 4){
        areas = 4;
        elem.value = areas;
    }
    console.log(areas)
    console.log(count)
    const htmlDIV = document.getElementById(String(count)+"-areaNames");
    console.log(htmlDIV)
    let buildHTML = "";
    for(i=0; i<areas; i++){
        buildHTML += `Name of area ${i+1}: <input name='${String(count)}-area${i+1}' type='text' required><br>`
        buildHTML += `How many options: <input name='${String(count)}-area${i+1}-optionsQty' type='number' oninput='createAreaChoices(this, ${count}, "area${i+1}")'required>`
        buildHTML += `<br><div id="${String(count)}-area${i+1}-choicesDiv" style="display:none;"></div>`
    } 
    htmlDIV.innerHTML = buildHTML;
    htmlDIV.style.display = 'block';
}

function createAreaChoices(elem, count, area){
    console.log('chicken')
    let choices = elem.value;
    let destinationDiv = document.getElementById(String(count)+ "-" + area + "-choicesDiv");
    let buildHTML = "";
    for(i=0; i<choices; i++){
        buildHTML += `Choice ${i+1}: <input name='${String(count)}-${area}-choice${i+1}' type='text' required><br>`
    } 
    destinationDiv.innerHTML = buildHTML;
    destinationDiv.style.display = 'block';
}