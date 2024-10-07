let x = document.getElementById('formID');
for (let i = 0; i < x.length ;i++) {
    let theElem = x.elements[i];
    console.log(theElem)
    theElem.addEventListener('input', checkFormFull)

}

function checkFormFull(){
    let x = document.getElementById('formID');
    let allFilledInputs = true;
    for (let i = 0; i < x.length ;i++) {
        if (x.elements[i].value == false){
            allFilledInputs=false;
            console.log(x.elements[i].id)
        }
    }
    console.log(allFilledInputs)
    if (allFilledInputs){
        console.log('this one true')
        document.getElementById('submit').disabled = false;
    } else {
        console.log(' this onefalse')
        document.getElementById('submit').disabled = true;
    };
}
checkFormFull()