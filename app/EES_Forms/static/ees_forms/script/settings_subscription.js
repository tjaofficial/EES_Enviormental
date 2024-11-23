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

registerActivate = (elem) => {
    const nameVariable = document.getElementsByClassName('registerName');
    const registerName = elem.dataset.name;
    const registerEnding = elem.dataset.ending;
    const registerID = elem.dataset.regid;
    const endingVariable = document.getElementById('registerEnding');
    const idVariable = document.getElementById('activateRegisterID');
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


function activateModal(elem){
    // Get the modal
    const modalOpen = document.getElementById(elem.dataset.secondid);
    console.log('clicked')
    modalOpen.style.display = "block";

// Get the <span> element that closes the modal
var modalClose = document.getElementById("closeActivate");

// When the user clicks on <span> (x), close the modal
modalClose.onclick = function() {
    modalOpen.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modalOpen) {
        modalOpen.style.display = "none";
    }
}
}
function checkActivateText(elem){
    let type = elem.parentNode.parentNode.parentNode.parentNode.id;
    if (type == "activateReg"){
        const submit = document.getElementById('submitActivate');
        const activate = document.getElementById('activateText').value;
        if(activate != "activate"){
            submit.disabled = true;
        } else {
            submit.disabled = false;
        }
    } else {
        console.log('nope');
    }
}