autoFillZeros = (divID) => {
    //console.log(divID)
    const inputValue = document.getElementById(divID).value;
    //console.log(inputValue)
    if (inputValue == 'fil'){
        let parseID = divID.slice(0,-1)
        //console.log(parseID)
        for (i=0;i<=11;i++){
            document.getElementById(parseID+String(i)).value = 0;
        }
    } 
}