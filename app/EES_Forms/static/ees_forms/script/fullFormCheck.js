let x = document.getElementById('formID').querySelectorAll(
    'input, textarea, select');
for (let i = 0; i < x.length ;i++) {
    let theElem = x[i];
    console.log(theElem)
    theElem.addEventListener('input', checkFormFull)

}

function checkFormFull(){
    let x = document.getElementById('formID').querySelectorAll(
  'input, textarea, select');
    let allFilledInputs = true;
    for (let i = 0; i < x.length ;i++) {
        if (x[i].value == false){
            allFilledInputs=false;
            console.log(x[i].id)
        }
    }
    if (allFilledInputs){
        console.log('this one true')
        document.getElementById('submit').disabled = false;
    } else {
        console.log(' this onefalse')
        document.getElementById('submit').disabled = true;
    };
}
checkFormFull()