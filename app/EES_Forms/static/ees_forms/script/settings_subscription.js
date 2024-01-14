registerCancel = (elem) => {
    const nameVariable = document.getElementsByClassName('registerName');
    const registerName = elem.dataset.name;
    const registerEnding = elem.dataset.ending;
    const registerID = elem.dataset.regid;
    const endingVariable = document.getElementById('registerEnding');
    const idVariable = document.getElementById('registerID');
    for(let x=0;x<nameVariable.length;x++){
        let eachName = nameVariable[x];
        eachName.innerText = registerName;
    }
    endingVariable.innerText = registerEnding;
    idVariable.value = registerID;
}

function checkCancelText(elem){
    let type = elem.parentNode.parentNode.parentNode.parentNode.id;
    if (type == "cancelReg"){
        const submit = document.getElementById('submit');
        const cancel = document.getElementById('cancelText').value;
        if(cancel != "cancel"){
            submit.disabled = true;
        } else {
            submit.disabled = false;
        }
    } else {
        console.log('nope');
    }
}