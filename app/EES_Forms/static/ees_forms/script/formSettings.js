document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.formCont input, .formCont select').forEach((item) =>{
        const formIDGrab = document.querySelector('#formID').dataset.formid;
        const settingsCont = document.getElementById('settings' + String(formIDGrab));
        if (!settingsCont.dataset.selector){
            item.disabled = true;
        }
    });
});

toggleSettings = (checkbox) => {
    const count = checkbox.dataset.count;
    //console.log(count)
    //console.log('settings' + String(count))
    const settingsCont = document.getElementById('settings' + String(count));
    const inputs = settingsCont.querySelectorAll('input, select');
    //console.log(settingsCont)
    if (checkbox.checked == true){
        settingsCont.style.display = 'block';
        inputs.forEach((input) => {
            input.required = true;
            input.disabled = false;
        });
    } else {
        settingsCont.style.display = 'none';
        inputs.forEach((input) => {
            input.required = false;
            input.disabled = true;
        });
    }
}

