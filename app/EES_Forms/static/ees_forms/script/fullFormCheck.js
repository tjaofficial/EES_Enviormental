

let x = document.getElementById('formID');
let allFilledInputs = true;
var i;
for (i = 0; i < x.length ;i++) {
    if (x.elements[i].value == false){
        allFilledInputs=false;
    }
}
console.log(allFilledInputs)
if (allFilledInputs){
    console.log('this one true')
    document.getElementById('submitButton').disabled = false;
} else {
    console.log(' this onefalse')
    document.getElementById('submitButton').disabled = true;
};
