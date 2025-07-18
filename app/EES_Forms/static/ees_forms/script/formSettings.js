document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".formCheckBox").forEach(cb => {
        const id = cb.dataset.count;
        const settingsCont = document.getElementById('settings' + id);
        const inputs = settingsCont.querySelectorAll('input, select');
        if (cb.checked) {
            settingsCont.style.display = 'block';
            inputs.forEach((input) => {
                input.disabled = false;
                input.required = input.name.includes("custom_name")? false:true;
            });
        } else {
            settingsCont.style.display = 'none';
            inputs.forEach((input) => {
                input.disabled = true;
                input.required = false;
            });
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
            input.required = input.name.includes("custom_name")? false:true;
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

