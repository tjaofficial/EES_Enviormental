toggleSettings = (checkbox) => {
    const count = checkbox.dataset.count;
    //console.log(count)
    //console.log('settings' + String(count))
    const settingsCont = document.getElementById('settings' + String(count));
    //console.log(settingsCont)
    if (checkbox.checked == true){
        settingsCont.style.display = 'block';
    } else {
        settingsCont.style.display = 'none';
    }
}

