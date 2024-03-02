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
    const areas = elem.value;
    const htmlDIV = document.getElementById(String(count)+"areaNames");
    console.log(htmlDIV)
    let buildHTML = "";
    for(i=0; i<areas; i++){
        buildHTML += `Name of area ${i+1}: <input name='${String(count)}area${i+1}' type='text' required><br>`
    } 
    htmlDIV.innerHTML = buildHTML;
    htmlDIV.style.display = 'block';
}