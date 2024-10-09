toggleSettings = (checkbox) => {
    const count = checkbox.dataset.count;
    const settingsCont = document.getElementById('settings' + String(count))
    if (checkbox.checked == true){
        settingsCont.style.display = 'block';
    } else {
        settingsCont.style.display = 'none';
    }
}

